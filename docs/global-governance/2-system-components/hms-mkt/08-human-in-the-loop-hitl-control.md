# Chapter 8: Human-in-the-Loop (HITL) Control  
*A friendly sequel to [Agent Framework (HMS-AGT / HMS-AGX)](07_agent_framework__hms_agt___hms_agx__.md)*  

---

## 1. Why Do We Need HITL?

Picture the **Department of Veterans Affairs (VA)**.  
Last night *ClaimBot* (built in Chapter 7) auto-evaluated 400 disability claims. One record looks suspicious:

```
Veteran ID ........ 99123  
AI Recommendation . "Reject – insufficient medical evidence"  
Confidence ........ 58 %
```

Rejecting benefits on shaky grounds is unacceptable. A **human claim officer** must:

1. Open the AI proposal  
2. Read attached evidence  
3. Edit the decision if needed  
4. Sign off (or kick it back)

HITL is the **emergency brake** that guarantees this human checkpoint exists **before** any irreversible action (denial, payment, arrest, etc.) happens.

---

## 2. Key Ideas in Plain English

| HITL Term | Friendly Analogy | VA Example |
|-----------|------------------|-----------|
| Override  | Pulling the red train brake | Officer changes “Reject” ➜ “Approve (80 %)” |
| Edit      | Surgeon’s scalpel | Adjust benefit start-date from Jan 5 → Feb 1 |
| Endorse   | Thumbs-up emoji | “AI got it right, ship it.” |
| Audit Log | Security camera | Stores *who*, *what*, *when*, *why* |
| SLA Timer | Hourglass | Auto-escalate if no human acts in 48 h |

---

## 3. 3-Minute Tour – Overriding a Claim Decision

### 3.1 Agent Flags a Task for Review

```js
// agents/claimBot.js (excerpt)
if (confidence < 0.75){
  await tools.hitl.request({
    title: 'Disability Claim #99123',
    draft: aiRecommendation,        // JSON payload
    slaHours: 48
  })
}
```

Explanation  
* Within **19 lines** the bot asks HITL to spin up a review task.

---

### 3.2 Listing Pending Tasks (Reviewer UI)

```vue
<script setup>
import { ref, onMounted } from 'vue'
const tasks = ref([])
onMounted(async () => {
  tasks.value = await fetch('/api/hitl?status=pending').then(r=>r.json())
})
</script>

<template>
  <ul>
    <li v-for="t in tasks" :key="t.id">
      {{ t.title }}
      <button @click="open(t.id)">Review</button>
    </li>
  </ul>
</template>
```

Explanation  
* <20 lines fetch all **pending** tasks and shows a “Review” button.

---

### 3.3 Approve, Edit, or Reject

```js
// services/hitl.service.js
export async function decide(id, action, patch = {}){
  await fetch(`/api/hitl/${id}`, {
    method: 'POST',
    body: JSON.stringify({ action, patch }) // action = 'endorse' | 'edit' | 'reject'
  })
}
```

• `endorse` → AI decision stands  
• `edit`    → override fields with `patch`  
• `reject`  → send back for re-work  

---

## 4. What Happens Behind the Curtain?

```mermaid
sequenceDiagram
  participant AG as ClaimBot
  participant HITL as HITL Queue
  participant OFF as Human Officer
  participant ACT as HMS-ACT
  participant LOG as Audit Log

  AG->>HITL: createTask(draft)
  OFF->>HITL: fetchPending()
  OFF->>HITL: decide(task, action)
  HITL->>LOG: save decision
  HITL->>ACT: continue workflow
```

*Max 5 actors keeps the story clear.*

---

## 5. Inside HITL – Minimal Implementation

### 5.1 Task Schema (JSON)

```json
{
  "id": "task_5489",
  "title": "Disability Claim #99123",
  "draft": { "decision": "reject", "confidence": 0.58 },
  "status": "pending",
  "history": [],
  "slaHours": 48,
  "createdAt": "2024-05-01T10:00Z"
}
```

Only six required fields – easy to reason about.

---

### 5.2 Create a Task (Server Route)

```js
// routes/hitl.create.js
router.post('/hitl', async (req, res) => {
  const task = { ...req.body, status:'pending', history:[] }
  await db.tasks.insert(task)
  res.status(201).json(task)
})
```

≤ 10 lines: insert into DB and return `201 Created`.

---

### 5.3 Record a Decision

```js
// routes/hitl.decide.js
router.post('/hitl/:id', async (req,res)=>{
  const { action, patch } = req.body
  const t = await db.tasks.get(req.params.id)
  t.history.push({ by:req.user.id, action, patch, at:Date.now() })
  t.status = 'closed'
  await db.tasks.update(t.id, t)
  await act.resume(t.id, { action, patch })   // notify HMS-ACT
  res.sendStatus(204)
})
```

Explanation  
1. Append to `history`.  
2. Flip `status`.  
3. Hand control back to [Workflow Orchestrator](05_workflow_orchestrator__hms_act__.md).

---

## 6. Integrating HITL with Other Layers

• **From Agents** – use `tools.hitl.request` supplied by [HMS-AGT](07_agent_framework__hms_agt___hms_agx__.md).  
• **From Workflows** – add a `{"type":"hitl"}` step in the JSON plan; [HMS-ACT](05_workflow_orchestrator__hms_act__.md) pauses until a decision arrives.  
• **Governance Dashboard** – advanced users can browse audit logs in [HMS-GOV](01_governance_interface_layer__hms_gov__.md).  

---

## 7. Frequently Asked Questions

**Q: What if no human responds before the SLA timer?**  
HITL auto-escalates to the next reviewer group or a supervisor queue.

**Q: Can HITL tasks be delegated between agencies (e.g., VA ➜ DoD)?**  
Yes—tasks are routed over the message bus managed by [Inter-Agency Exchange](11_inter_agency_exchange__hms_a2a__.md).

**Q: Is the audit log tamper-proof?**  
Every decision hash is also written to the blockchain‐like ledger in [Observability & Operations](17_observability___operations__hms_ops__.md).

**Q: Does HITL slow down low-risk cases?**  
No—agents only create tasks when confidence < threshold *or* policy dictates mandatory review.

---

## 8. What You Learned

• **HITL** provides a safety valve: humans can **override, edit, or endorse** any AI proposal.  
• Creating a HITL task is a one-liner (`tools.hitl.request`).  
• Reviewers get a simple queue, make a decision, and every click is logged.  
• HITL plugs into workflows (ACT), audits (OPS), and dashboards (GOV) with minimal code.

Next we’ll see how all these pieces talk to each other efficiently inside the platform’s plumbing:  
[Core Service Mesh (HMS-SVC)](09_core_service_mesh__hms_svc__.md)

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)