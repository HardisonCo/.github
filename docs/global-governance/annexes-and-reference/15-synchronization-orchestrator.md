# Chapter 15: Synchronization Orchestrator  

*(Sequel to [External System Connector & Sync](14_external_system_connector___sync_.md))*  

---

## 1. Why Do We Need a “Train Dispatcher” Inside HMS-SME?

Meet **Elijah**, a benefits officer at the **Department of Labor (DOL)**.  
Yesterday Congress approved a **10 % increase** in unemployment-benefit payments.  
When Elijah presses **Publish** in the HMS-GOV portal three very different engines must leave the station – **in order** and **without crashing into each other**:

| Departure Order | Micro-service | What It Must Do |
|-----------------|---------------|-----------------|
| 🥇 1st          | `payment-svc` | Re-calculate 2 M weekly payments |
| 🥈 2nd          | `notice-svc`  | E-mail / SMS every claimant |
| 🥉 3rd          | `archive-svc` | Snapshot the old rule for auditors |

If any wagon derails—say, e-mails go out *before* the new amount is booked—citizens panic and hot-lines melt.  

**Synchronization Orchestrator (HMS-SYNCOR)** is the *train dispatcher* that:

1. Tracks **every change** as an immutable event.  
2. Starts each downstream workflow **in the correct order**.  
3. Rolls back safely if a step fails (using *compensation*).  

Result: Elijah sleeps, citizens smile, auditors applaud. 🙌  

---

## 2. Key Concepts in Plain English

| Term            | Beginner Analogy                | One-Sentence Meaning |
|-----------------|---------------------------------|----------------------|
| Event Store     | Station logbook                 | Append-only ledger of “policy.changed”, “payment.done”… |
| Saga            | Train schedule                  | A multi-step journey with forward + compensation steps |
| Step            | Individual wagon                | One call like `POST /payments/recalc` |
| Compensation    | Reverse gear                    | Action that undoes a step if something later fails |
| Orchestrator    | Train dispatcher                | Service that watches events, runs sagas, guarantees order |

> Think of a **saga** as “do X → then Y → then Z; if Y fails, undo X”.

---

## 3. 5-Minute Hands-On: Publish the Benefit Increase Safely  

### 3.1 Define the Saga (18 lines)

```yaml
# sagas/benefit-increase.yaml
id: dol.benefit.increase.v1
trigger:  policy.changed
filter:   data.policyId == "dol.unemployment.v3"
steps:
  - name: recalc_payments
    call:  payment-svc:/recalc
    compensate: payment-svc:/revert
  - name: send_notices
    call:  notice-svc:/broadcast
    compensate: notice-svc:/cancel
  - name: archive_rule
    call:  archive-svc:/snapshot
    compensate: archive-svc:/deleteSnapshot
retry:
  attempts: 3
  backoffMs: 2000
timeoutMs: 300000       # 5 min per step
```

Beginners’ view  
1. **trigger** – listen for `policy.changed` events.  
2. **filter** – only fire when the *unemployment* rule hits version 3.  
3. **steps** – normal HTTP calls; **compensate** paths are optional.  
4. **retry / timeout** – automatic resilience knobs.

### 3.2 Deploy & Start the Dispatcher

```bash
hms-orch deploy sagas/benefit-increase.yaml
hms-orch up           # http://localhost:7600 dashboard
```

### 3.3 Simulate the Policy Change

```bash
# pretend HMS-GOV already wrote the new rule
hms-bus publish policy.changed \
  --data '{"policyId":"dol.unemployment.v3"}'
```

Console:

```
▶ dol.benefit.increase.v1  START
✓ recalc_payments          117 956 payments updated
✓ send_notices             2 001 445 e-mails queued
✓ archive_rule             snapshot #834 saved
✔ dol.benefit.increase.v1  COMPLETED (3 m 14 s)
```

Zero manual scripts, zero race conditions. 🎉  

---

## 4. What Happens Under the Hood?

```mermaid
sequenceDiagram
    participant BUS  as Event Bus
    participant ORCH as Sync Orchestrator
    participant PAY  as payment-svc
    participant NOTE as notice-svc
    participant ARC  as archive-svc

    BUS->>ORCH: policy.changed
    ORCH->>PAY: /recalc
    PAY-->>ORCH: 200 OK
    ORCH->>NOTE: /broadcast
    NOTE-->>ORCH: 200 OK
    ORCH->>ARC: /snapshot
    ARC-->>ORCH: 200 OK
    ORCH-->>BUS: saga.completed
```

If **ANY** step returns error, ORCH runs *compensation* for all finished steps in **reverse order**, then emits `saga.failed`.

---

## 5. Using the Orchestrator in Your Service (Tiny SDK)

### 5.1 Emit Business Events (≤ 10 lines)

```ts
import { emit } from '@hms-sme/bus';

export async function publishRule(rule){
  await db.save(rule);
  await emit('policy.changed', {policyId: rule.id});
}
```

No orchestration code inside your service—just “fire the event.”

### 5.2 Listen for Rollback (≤ 12 lines)

```ts
import { on } from '@hms-sme/bus';

on('saga.compensate', async ev =>{
  if(ev.step.name === 'recalc_payments')
     await db.restoreBackup(ev.step.context.backupId);
});
```

Your service **implements** the compensate endpoint once; ORCH calls it if needed.

---

## 6. Internal Implementation Peeks

### 6.1 Light-Weight Event Store (Go ≤ 15 lines)

```go
func Append(event Event){
   file, _ := os.OpenFile("store.log", O_APPEND|O_CREATE|O_WRONLY, 0644)
   json.NewEncoder(file).Encode(event)
}
```

An append-only log; easy to replay for disaster recovery.

### 6.2 Saga Runner (TypeScript ≤ 18 lines)

```ts
async function runSaga(def, payload){
  const ctx = {sagaId: uuid(), data: payload};
  for (const step of def.steps){
     try{
        await call(step.call, ctx);
        log('DONE', step.name);
     }catch(e){
        await compensate(def, ctx, step);
        emit('saga.failed', {sagaId: ctx.sagaId, reason: e});
        return;
     }
  }
  emit('saga.completed', {sagaId: ctx.sagaId});
}
```

### 6.3 Compensation Helper (≤ 12 lines)

```ts
async function compensate(def, ctx, failedStep){
  const done = def.steps.slice(0, def.steps.indexOf(failedStep));
  for (const step of done.reverse()){
     if(step.compensate) await call(step.compensate, ctx);
  }
}
```

All snippets ignore retries/metrics for clarity.

---

## 7. Safety Nets & Integrations

| Concern                 | How SYNCOR Handles It                      | Related Chapter |
|-------------------------|--------------------------------------------|-----------------|
| Lost message            | Stores *all* events in the Event Store     | [Data Governance & Audit Trail](11_data_governance___audit_trail_.md) |
| Concurrent sagas        | Uses **sagaId locks** to avoid collisions  | — |
| Authorization           | Every step call carries a short-lived JWT  | [Role & Identity Management (HMS-SYS Auth)](10_role___identity_management__hms_sys_auth__.md) |
| Monitoring              | `saga_duration_ms`, `saga_fail_total`      | [Metrics & Monitoring Pipeline](12_metrics___monitoring_pipeline_.md) |
| Human intervention      | Auto-enqueue to HITL on 3 consecutive fails| [Human-in-the-Loop Oversight](05_human_in_the_loop_oversight__hitl__.md) |

---

## 8. Frequently Asked (Beginner) Questions

**Q: Do I have to write code for compensation?**  
Only if the action is **destructive** or **expensive**. Read-only steps often skip it.

**Q: What if two sagas touch the same data?**  
SYNCOR grants a *per-object lock* so the second saga waits or aborts.

**Q: Can steps run in parallel?**  
Yes – add `parallel: true` under any sub-array of steps.

**Q: Is this Kafka Streams?**  
Under the hood SYNCOR can use Kafka, NATS, or Postgres-listen/notify; the *concept* stays the same.

---

## 9. Recap

You learned:

• Why multi-step changes (like benefit increases) need a **train dispatcher**.  
• How to write a saga in under 20 lines of YAML.  
• What happens when the dispatcher runs, including rollbacks.  
• Where SYNCOR plugs into Auth, Metrics, Audit, and HITL.

HMS-SME now has a **reliable heartbeat** from the first rule edit all the way to external systems.  
You’ve reached the final core layer—time to orchestrate your own projects with confidence! 🚀  

Thank you for travelling through all 15 chapters of HMS-SME.  
Happy shipping, and may your trains always run on time! 🛤️

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)