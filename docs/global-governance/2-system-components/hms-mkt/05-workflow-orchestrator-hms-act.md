# Chapter 5: Workflow Orchestrator (HMS-ACT)

*A friendly sequel to [Compliance & Legal Reasoning (HMS-ESQ)](04_compliance___legal_reasoning__hms_esq__.md)*  

---

## 1. Why Do We Need HMS-ACT?

Imagine you are a program manager at **FEMA** responding to a severe hurricane.  
Over the next 24 hours thousands of citizens will:

1. File damage claims  
2. Upload photos  
3. Request temporary housing  
4. Await payment approval

Behind the curtain we must:

* Verify identity (DHS data)  
* Geo-validate the address (US Postal Service API)  
* Run fraud checks (Treasury)  
* Trigger human review if damage > \$50 000  
* Finally disburse funds via ACH  

If each micro-task is an instrument in an orchestra, **HMS-ACT is the conductor**:  
it listens for the first note (a claim) and directs every player—AI agents, micro-services, or a human official—at exactly the right time so the music (public service) never misses a beat.

---

## 2. Key Ideas in Plain English

| Concept | Friendly Analogy | FEMA Example |
|---------|-----------------|--------------|
| Event Listener | Doorbell sensor | “New Claim #9321 arrived” |
| Task Queue | Wait-list at a DMV | Claims line up for processing |
| Routing Rules | Air-traffic control tower | Large claims → human lane |
| Agent Runner | A temp worker agency | Spins up AI bots or micro-services |
| Escalation | “Talk to a supervisor” | Damage > \$50 000 → senior reviewer |

---

## 3. A 3-Minute Walk-Through (End-to-End)

We will automate the **“New FEMA Claim”** workflow in four baby steps.

### 3.1 Describe the Workflow (just JSON)

```json
{
  "name": "fema_claim_v1",
  "steps": [
    { "id": "verify_id",   "type": "service", "svc": "DHS_ID_CHECK" },
    { "id": "geo_check",   "type": "service", "svc": "USPS_GEO" },
    { "id": "fraud_scan",  "type": "agent",   "agent": "AntiFraudBot" },
    { "id": "human_rev",   "type": "hitl",    "rule": "claim>50000" },
    { "id": "pay_out",     "type": "service", "svc": "TREASURY_ACH" }
  ],
  "links": [
    ["verify_id", "geo_check"],
    ["geo_check", "fraud_scan"],
    ["fraud_scan", "human_rev", "claim>50000"],
    ["fraud_scan", "pay_out",   "else"],
    ["human_rev",  "pay_out"]
  ]
}
```

Explanation  
• 5 steps → 5 different actors.  
• `links` define the flow; one branch routes big claims to a human.

### 3.2 Submit an Event to HMS-ACT

```js
// act.client.js  (≤ 15 lines)
export async function newClaim(claim){
  await fetch('/api/hms-act/events', {
    method: 'POST',
    body: JSON.stringify({
      type: 'NEW_CLAIM',
      data: claim
    })
  })
}
```

Call `newClaim()` when the citizen hits “Submit”.  
**No queues, no threads—HMS-ACT handles the rest.**

### 3.3 What Happens Next (Story Mode)

1. **Event received** – HMS-ACT stores it in a queue.  
2. **Step 1 – verify_id** – Calls DHS API; if failed → auto-reject.  
3. **Step 2 – geo_check** – Confirms address is inside disaster zone.  
4. **Step 3 – fraud_scan** – AI bot scores risk.  
5. **Branch** – Claim \$60 000 ⇒ route to **human_rev**.  
6. Senior reviewer clicks “Approve”.  
7. **Step 5 – pay_out** – Treasury ACH is invoked.  
8. HMS-ACT marks the workflow *complete* and logs a receipt.  

Nothing fell through the cracks—even if services were briefly down, the queue would retry.

---

## 4. Under the Hood

```mermaid
sequenceDiagram
  participant APP as Web App
  participant ACT as HMS-ACT
  participant DHS as DHS API
  participant BOT as AntiFraudBot
  participant OFF as Human Reviewer
  APP->>ACT: NEW_CLAIM event
  ACT->>DHS: verify_id
  DHS-->>ACT: ✅
  ACT->>BOT: fraud_scan(job)
  BOT-->>ACT: risk=low
  ACT->>OFF: (skip, risk low)
  ACT->>Treasury: pay_out
```

*The diagram shows a “happy path” where the claim is small—human step skipped.*

---

## 5. Peeking at HMS-ACT Code (Really Tiny!)

### 5.1 Minimal Express-Style Event Ingest

```js
// routes/act.events.js
router.post('/events', async (req, res) => {
  const evt = req.body                    // {type, data}
  await queue.add(evt.type, evt.data)     // push to Redis
  res.sendStatus(202)                     // Accepted
})
```

Only 4 lines: receive, enqueue, respond 202.

### 5.2 A Super-Slim Worker

```js
// workers/act.worker.js
import { getNextJob, complete } from './queue.js'
import { runStep } from './runners.js'

while (true){
  const job = await getNextJob()      // blocks until one is ready
  for (const step of plan(job)){
     await runStep(step, job)         // auto-retries on failure
  }
  await complete(job)
}
```

*plan()* maps the JSON workflow to an array of steps;  
*runStep()* picks the right “runner” (service call, agent, or human task).

### 5.3 Runners Map (Strategy Pattern)

```js
// runners.js  (≤ 20 lines)
export async function runStep(step, job){
  const fn = {
    service: callService,
    agent:   invokeAgent,
    hitl:    awaitHuman
  }[step.type]
  return await fn(step, job)
}
```

Three functions, one lookup—beginners can trace it in minutes.

---

## 6. Plugging HMS-ACT into Other Chapters

* From [Protocol Builder Page](03_protocol_builder_page_.md) you already save a diagram; that JSON is **the workflow plan** HMS-ACT runs.  
* Compliance screening via [HMS-ESQ](04_compliance___legal_reasoning__hms_esq__.md) adds a risk score **before** the plan reaches ACT.  
* If a human must sign off, HMS-ACT calls [Human-in-the-Loop Control](08_human_in_the_loop__hitl__control_.md).  
* External payouts use the [Financial Clearinghouse](13_financial_clearinghouse__hms_ach__.md).

---

## 7. Frequently Asked Questions

**Q: Does HMS-ACT guarantee tasks won’t be lost if a server crashes?**  
Yes—events and task states live in a durable queue (Redis, SQS, etc.). Workers can restart anytime.

**Q: Can I run multiple workflows in parallel?**  
Absolutely. Each event carries a `workflow` key; ACT can juggle thousands simultaneously.

**Q: What if a human never responds?**  
Set an SLA on `hitl` steps—ACT will auto-reassign or escalate after the timeout.

**Q: Is ACT limited to federal use?**  
No—state, city, or even university help-desk flows work the same way.

---

## 8. What You Learned

• **HMS-ACT** is the traffic-cop (or orchestra conductor) that schedules every task across services, agents, and humans.  
• A workflow is just a **JSON plan** plus **events**—easy to author, easy to read.  
• With <20 lines of code you can enqueue events and run workers.  
• ACT collaborates with many layers—legal (ESQ), human review (HITL), payments (ACH).

Ready to see how agents know *what context* they are operating in?  
Jump to [Model Context Protocol (HMS-MCP)](06_model_context_protocol__hms_mcp__.md).

---

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)