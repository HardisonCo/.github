# Chapter 8: Policy & Process Management API
[← Back to Chapter 7: Human-in-the-Loop (HITL) Oversight](07_human_in_the_loop__hitl__oversight_.md)

---

## 0. Why Do We Need a “Legislative Clerk” Inside the Codebase?

Imagine Congress passes a bill lowering the **federal withholding tax rate** from **22 % → 20 %** effective next Monday.  
If every agency hard-codes rates in their own service, we would have:

* 50+ pull-requests  
* 50+ emergency deploys  
* 50 chances to mistype “0.20” as “0.02” 😱

Instead, HMS gives us **one** microservice—the **Policy & Process Management API** (PPM-API).  
Treasury sends **one** JSON payload, the API:

1. Validates it (is the scope really “withholding_rate”?)  
2. Writes an immutable record  
3. Notifies payroll, benefits, and analytics services in real time  
4. Keeps the old 22 % version so we can roll back if disaster strikes

Citizens keep getting paid, developers keep their Friday night. 🎉

---

## 1. Key Concepts in Plain English

| Concept | Think of It Like… | Why It Matters |
|---------|------------------|----------------|
| Policy | A law or rule (“withholding_rate = 0.20”) | Source of truth for all services |
| Version | Page number in the statute book | Lets us see history & roll back |
| Scope | Which part of government it touches | Stops Arts from editing IRS tables |
| Notification | Certified letter to every clerk | Down-stream services re-calculate instantly |
| Immutable Record | A museum copy under glass | Auditors can prove what rule was active |
| Rollback | “Repeal” stamp | Undo bad policies in seconds |

Keep this table open while you code; it’s 90 % of the API.

---

## 2. Quick-Start: Changing a Tax Rate in 3 Calls

We’ll use `curl` so you can follow along without writing code.  
Replace the token with your own.

### 2.1 Create a New Policy Version (POST)
```bash
curl -X POST https://api.hms.gov/ppm/policies \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "key": "withholding_rate",
        "value": 0.20,
        "effective_date": "2024-07-01"
      }'
```
Response (201):
```json
{ "version": 42, "status": "PENDING", "id": "pol_1ff2..." }
```
What happened?  
* The policy is stored **but not yet active** (needs HITL approval per [Human-in-the-Loop](07_human_in_the_loop__hitl__oversight_.md)).  
* `version: 42` tells us this is the 42ᵗʰ change since 1993.

### 2.2 Approve the Policy (PATCH)  
(Usually done in HMS-GOV UI; here’s the raw call.)

```bash
curl -X PATCH https://api.hms.gov/ppm/policies/pol_1ff2/approve \
  -H "Authorization: Bearer $SUPERVISOR_TOKEN"
```
Response (200): `{ "status": "ACTIVE", "activated_at": "2024-07-01T00:00:00Z" }`

All subscribed services receive a **WebSocket** event:
```json
{ "topic":"policy.update",
  "key":"withholding_rate",
  "new_value":0.20,
  "version":42 }
```

### 2.3 Oops! Roll Back (POST)

```bash
curl -X POST https://api.hms.gov/ppm/policies/withholding_rate/rollback \
  -H "Authorization: Bearer $TREASURY_TOKEN" \
  -d '{ "to_version": 41 }'
```
Response (200): `{ "status":"ACTIVE", "version":41 }`  
Payroll instantly returns to 22 %.

---

## 3. How Does It Work Behind the Scenes?

```mermaid
sequenceDiagram
    participant Caller as Treasury Staff / AI Agent
    participant PPM as PPM-API
    participant Store as Immutable Policy Store
    participant Bus as Event Bus
    participant SVC as Payroll Service

    Caller->>PPM: POST new policy JSON
    PPM->>Store: append version 42
    PPM-->>Caller: 201 PENDING
    PPM-->>Bus: event "policy.pending"
    HITL approves (see Chapter 7)
    PPM->>Bus: event "policy.active"
    Bus-->>SVC: withholding_rate=0.20
```

Five participants, zero room for “he said, she said.”

---

## 4. Under-the-Hood Code Walk-Through

### 4.1 API Route (Express – 19 lines)
```ts
// routes/policies.ts
import express from 'express';
import { store } from '../util/policyStore';
import { bus } from '../util/eventBus';

const router = express.Router();

router.post('/', async (req, res) => {
  const { key, value, effective_date } = req.body;
  if (!key || value == null) return res.status(400).send('Bad payload');

  const version = await store.nextVersion(key);
  const record = { key, value, version, status: 'PENDING', created_by: req.user.id };

  await store.append(record);         // immutable write
  bus.publish('policy.pending', record);

  res.status(201).json(record);
});

export default router;
```
What you just did:

1. Grabbed the next version number.  
2. Wrote an **append-only** record.  
3. Fired a non-blocking event so other services stay decoupled.

### 4.2 Immutable Store Helper (10 lines)
```ts
// util/policyStore.ts
import db from './knex';

export const store = {
  append: r => db('policy_log').insert(r),
  nextVersion: async key => {
    const { max } = await db('policy_log').where({ key }).max('version as max').first();
    return (max || 0) + 1;
  },
  getActive: key => db('policy_log').where({ key, status:'ACTIVE' }).first()
};
```
One table, three helper functions—beginners can grok this in minutes.

---

## 5. Typical Folder Layout

```
hms-ppm/
 ├─ routes/
 │   └─ policies.ts
 ├─ util/
 │   ├─ policyStore.ts
 │   └─ eventBus.ts
 └─ migrations/
     └─ 001_create_policy_log.sql
```
Nothing fancy; senior devs can swap PostgreSQL for DynamoDB without touching route code.

---

## 6. Working With Other HMS Components

* **AI Agents** from [Specialized AI Agents (HMS-A2A)](05_specialized_ai_agents__hms_a2a__.md) call PPM-API to propose rule tweaks.  
* All create/update calls are pre-checked by the **AI Governance Model** ([Chapter 6](06_ai_governance_model_.md)).  
* Approvals & rollbacks write signatures into the **Accountability Ledger** ([Chapter 9](09_role_based_access_control___accountability_ledger_.md)).  
* Real-time policy change counts appear on dashboards in [Real-Time Metrics & Monitoring](10_real_time_metrics___monitoring_.md).

---

## 7. Mini-FAQ

**Q: Can two agencies edit the same key?**  
Yes—if their **scope** overlaps. Use namespacing like `treasury.withholding_rate` vs `arts.grant_deadline` to avoid collisions.

**Q: Is JSON the only format?**  
Today yes; YAML support is planned. Binary protobufs are overkill for <2 kB payloads.

**Q: What if a service is offline during a policy update?**  
On startup every service calls `GET /ppm/policies/active` and re-hydrates the latest rules.

---

## 8. Recap & Next Steps

You learned:

1. Why a single **Policy & Process Management API** prevents chaos.  
2. Six core concepts: policy, version, scope, notification, immutable record, rollback.  
3. How to create, approve, and roll back a rule in three tiny HTTP calls.  
4. The 19-line Express route that makes it all possible.  
5. How PPM-API ties into governance, HITL, monitoring, and the accountability ledger.

Ready to see **who** is allowed to change these rules and how every click is recorded forever?  
Jump to [Chapter 9: Role-Based Access Control & Accountability Ledger](09_role_based_access_control___accountability_ledger_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)