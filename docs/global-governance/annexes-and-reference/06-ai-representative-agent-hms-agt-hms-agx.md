# Chapter 6: AI Representative Agent (HMS-AGT / HMS-AGX)

*(coming from [Service Orchestration & Task Queues (HMS-OMS)](05_service_orchestration___task_queues__hms_oms__.md))*  

---

> “Imagine a 24/7 super-staffer who instantly reads every statute, ticket, and public comment—then drafts the fix before coffee cools.”  
> That is the **AI Representative Agent**.

---

## 1. Why add an AI staffer to HMS-GOV?

Use-case:  
Mayor Lee types one sentence into the city dashboard:

```
☑  Please shorten the residential building-permit wait-time.
```

Within minutes the agent:

1. Pulls the full permit queue from **HMS-API**.  
2. Finds bottlenecks (missing fire-inspection slots).  
3. Drafts a 3-step process change.  
4. Opens a pull-request in the **Policy Management UI** with the proposal pre-filled.  

No extra staff, no three-week committee meeting—just progress.

---

## 2. Key Concepts (plain English)

| Term | Think of it as… | Max 1-line explanation |
|------|-----------------|------------------------|
| HMS-AGT | The “brain” | Core agent that can read, plan, and act. |
| Skill | A verb | e.g., “summarize”, “schedule-inspection”. |
| HMS-AGX | Add-on toolkit | Domain packs: healthcare, finance, postal, etc. |
| Context | The agent’s notebook | Relevant docs + state for the current task. |
| Action | A single API call | What the agent is allowed to do. |
| Guardrail | The safety rails | Rules & reviewers to keep output lawful. |

---

## 3. Hello-World: asking the agent a question

### 3.1 One-liner client call

```js
// ui/AskAgent.js   (17 lines)
export async function askAgent(question) {
  const res = await fetch('/api/agent/message', {
    method : 'POST',
    headers: { 'Content-Type': 'application/json' },
    body   : JSON.stringify({ question })
  })
  return res.json()          // → { answer:'...', sources:[...] }
}

// In any micro-frontend
askAgent('How long is the permit backlog?')
  .then(r => console.log(r.answer))
```

What happens:  
• We send natural language → receive a structured answer with links to raw data.

---

## 4. Under the hood (step-by-step)

```mermaid
sequenceDiagram
    participant UI  as Client
    participant API as HMS-API
    participant AGT as HMS-AGT
    participant OMS as Task Queue
    participant SVC as HMS-SVC

    UI ->> API: POST /agent/message
    API ->> OMS: enqueue "chat" job
    OMS ->> AGT: deliver job
    AGT ->> SVC: GET /permits?status=pending
    AGT -->> OMS: result text + sources
    UI  <<-- API: JSON answer
```

Only five actors; the queue keeps the web request snappy.

---

## 5. Building a tiny agent loop

> File: `agents/coreAgent.js` (Node, 20 lines)

```js
import { Worker, Queue } from 'bullmq'
import { chat } from './llm.js'          // wraps OpenAI, Azure, etc.
import { guard } from './guardrails.js'  // safety checks
import { permits } from '../svc/client.js'

const replyQ = new Queue('agent-replies')

// 1 worker handles every "chat" task
new Worker('agent-chat', async job => {
  const q = job.data.question

  // Step A: gather context
  const backlog = await permits.list({ status: 'pending' })

  // Step B: let the LLM think
  const draft = await chat([
    { role:'system', content:'You are a city clerk.' },
    { role:'user', content:q },
    { role:'assistant', content:`Current backlog: ${backlog.length}` }
  ])

  // Step C: safety check + enqueue reply
  if (guard(draft)) await replyQ.add('send', { answer:draft, to:job.data.user })
})
```

Explanation (line-by-line):  
1-3  Import helpers.  
6  Create a queue for outgoing messages.  
9  Start a worker listening to **agent-chat** tasks.  
12 Gather context (permit list).  
15-19 Call the LLM with a short prompt.  
22-23 Run the guardrail; if safe, queue the reply.

---

## 6. Adding a new “Skill”

Need the agent to book inspection slots? Add one function.

```js
// skills/scheduleInspection.js  (11 lines)
import { inspections } from '../svc/client.js'
export async function scheduleInspection(appId) {
  const slot = await inspections.findNext()
  await inspections.book(appId, slot.id)
  return `Inspection booked for ${slot.date}`
}
```

Register the skill:

```js
// agents/registry.js
export const skills = { scheduleInspection }
```

The LLM now sees `"scheduleInspection"` as an available action through the [Model Context Protocol](07_model_context_protocol__hms_mcp__.md) you’ll meet next.

---

## 7. What is HMS-AGX?

HMS-AGX bundles skill-packs:

* **HMS-AGX-UHC** – healthcare compliance (“ICD-10-verify”).  
* **HMS-AGX-ACH** – finance math (“reconcile ledger”).  
* **HMS-AGX-MPSA** – postal logistics for the Military Postal Service Agency.

Installing a pack is one line:

```bash
npm i @hms-gov/agx-uhc
```

Then merge its skills into the registry:

```js
import { uhcSkills } from '@hms-gov/agx-uhc'
Object.assign(skills, uhcSkills)
```

---

## 8. Safety first: guardrails & HITL

Even super-staffers need supervision.

```js
// guardrails.js   (12 lines)
export function guard(text) {
  const banned = ['social security number', 'wire money']
  return !banned.some(w => text.toLowerCase().includes(w))
}
```

For high-risk actions (e.g., budget transfers) the guard enqueues a  
**Human-in-the-Loop** review covered later in  
[Human-in-the-Loop (HITL) Override](11_human_in_the_loop__hitl__override_.md).

---

## 9. Quick FAQ

1. **Q:** Where is the agent’s memory stored?  
   **A:** In Redis keys `agent:memory:{userId}`—keep it under 10 KB to avoid context overflow.

2. **Q:** Can multiple agents run?  
   **A:** Yes; spin up “budget-agent”, “health-agent”… each with its own queue.

3. **Q:** What LLM provider can I use?  
   **A:** Any—swap `llm.js`; HMS-AGT only needs a `chat(messages)` promise.

---

## 10. Recap & what’s next

You now know:

✓ Why HMS-AGT puts an always-awake staffer inside HMS-GOV.  
✓ Core ideas: Skills, Extensions, Context, Actions, Guardrails.  
✓ How a 20-line worker turns a citizen question into an informed answer.  
✓ How to bolt on new domain packs (**HMS-AGX**).

The next chapter explains the handshake that lets the agent see only the right data and actions:  
[Model Context Protocol (HMS-MCP)](07_model_context_protocol__hms_mcp__.md)  

---

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)