# Chapter 16: Activity Orchestration Service (HMS-ACT)

*(Follow-up to [Legislative Workflow Engine (HMS-CDF)](15_legislative_workflow_engine__hms_cdf__.md))*  

---

## 1. Why Do We Need an **Air-Traffic Controller**?

A real morning at the **Employee Benefits Security Administration (EBSA)**:

1. A factory fails its **work-safety inspection**.  
2. The inspector says:  
   *“Please reschedule a follow-up visit for next Tuesday.”*  
3. Behind the scenes, six things must happen **in the right order**:

   ① find an open time slot in the scheduling system  
   ② e-mail the factory owner  
   ③ reserve a government car  
   ④ notify the field supervisor  
   ⑤ update the public compliance dashboard  
   ⑥ escalate to a human if any step stalls > 2 h  

Without coordination, each micro-service (calendar, mailer, fleet, dashboard) would be guessing who goes first—like planes landing without a tower.

**HMS-ACT** is that tower.  
It converts one plain-English *intent* (“reschedule inspection”) into an **ordered set of jobs**, watches deadlines, and calls the [Human-in-the-Loop system](14_human_in_the_loop__hitl__oversight_mechanism_.md) if anything gets stuck.

---

## 2. Key Concepts (in Plain English)

| Word            | What It Really Means |
|-----------------|----------------------|
| **Intent**      | Short sentence from a user or agent (“reschedule inspection”). |
| **Workflow**    | Ordered list of **Tasks** needed to fulfil the intent. |
| **Task**        | One atomic action (HTTP call, SQL insert, or human todo). |
| **SLA**         | Time-limit for a task (“finish within 2 h”). |
| **Escalation**  | Automatic creation of a HITL ticket when an SLA fails. |
| **Gantt Board** | Timeline view that shows every task like bars on a calendar. |
| **Worker**      | Service or human that *claims* a task via pub/sub. |

Keep that seven-item cheat-sheet handy—everything else is just glue.

---

## 3. Quick Start: From English to Executable Jobs

### 3.1 One POST Does the Trick

```bash
curl -X POST /api/act/intent \
  -H "Content-Type: application/json" \
  -d '{"intent":"Reschedule field inspection 123 for next Tuesday"}'
```

**HMS-ACT replies**

```json
{
  "workflowId": "WF-785",
  "tasks": [
    {"id":"T1","type":"calendar.reschedule","args":{"id":123,"date":"2025-04-22"}},
    {"id":"T2","type":"email.notify","deps":["T1"]},
    {"id":"T3","type":"fleet.reserve","deps":["T1"]},
    {"id":"T4","type":"dashboard.update","deps":["T2","T3"]}
  ],
  "slaMinutes": 120
}
```

What happened?

1. **Parser** spotted keywords *reschedule*, *inspection*, *date*.  
2. **Planner** produced four tasks with dependencies (`deps`).  
3. **Monitor** attached a 120-minute SLA to the whole workflow.  

That’s it—you now have an executable workflow ID `WF-785`.

---

### 3.2 Workers Claim & Complete Tasks

```javascript
// calendar-svc/worker.js  (≤18 lines)
import { subscribe, complete } from 'hms-act-sdk'

subscribe('calendar.reschedule', async task => {
  await calendarApi.move(task.args.id, task.args.date)
  await complete(task.id)             // tell HMS-ACT we're done
})
```

Explanation  
• **subscribe** puts this service on the task’s pub/sub channel.  
• After finishing, it calls `complete()`; HMS-ACT moves to the next tasks.

---

## 4. Step-by-Step Under the Hood

```mermaid
sequenceDiagram
    participant UI as EBSA Portal
    participant ACT as HMS-ACT
    participant CAL as calendar-svc
    participant MAIL as mailer-svc
    participant HITL as HITL
    UI->>ACT: Intent JSON
    ACT->>CAL: publish T1
    CAL-->>ACT: complete T1
    ACT->>MAIL: publish T2
    ... loop ...
    ACT-->>UI: workflow finished ✅
    note over ACT,HITL: If any task > SLA ➜ create HITL ticket
```

Only **ACT** knows the whole plan; each worker just does its slice.

---

## 5. The Dashboard: “Gantt-Board” at a Glance

```
WF-785  Reschedule Inspection           (age: 34 min)

/ T1 calendar.reschedule     ██████████░░  90 %  
| T2 email.notify            ░░░░░░░░░░░░   0 % (queued)
| T3 fleet.reserve           ░░░░░░░░░░░░   0 % (queued)
\ T4 dashboard.update        ░░░░░░░░░░░░   0 %
```

• Green bars move as tasks finish.  
• Red bar flashes if any reaches its SLA.

---

## 6. Inside the Codebase (Bird’s-Eye)

```
hms-act/
 ├─ api/               # REST entry (POST /intent, GET /workflow)
 ├─ planner/           # English → task list
 ├─ scheduler/         # dependency resolver → pub/sub
 ├─ monitor/           # SLA timers + HITL escalations
 ├─ dashboard/         # Gantt UI (micro-frontend)
 └─ sdk/               # tiny client for workers
```

### 6.1 Ultra-Small Planner (12 lines)

```python
# planner/core.py
def plan(intent: str):
    if "reschedule" in intent and "inspection" in intent:
        return [
          {"type":"calendar.reschedule"},
          {"type":"email.notify","deps":["T1"]},
          {"type":"fleet.reserve","deps":["T1"]},
          {"type":"dashboard.update","deps":["T2","T3"]}
        ]
    raise ValueError("Unknown intent")
```

*Beginners:* start with `if` rules; advanced installs use GPT-4.

### 6.2 Scheduler Loop (16 lines)

```javascript
// scheduler/loop.js
setInterval(async ()=>{
  const tasks = await db.find({ state:'READY' })
  for(const t of tasks){
    publish(t.type, t)                 // push to pub/sub
    await db.update(t.id,{ state:'SENT'})
  }
}, 1000)
```

• Every second, publish any task whose dependencies are done.  
• Workers listen on channels like `calendar.reschedule`.

### 6.3 SLA Monitor (13 lines)

```javascript
// monitor/sla.js
setInterval(async ()=>{
  const late = await db.find({ due:{ $lt: Date.now() }, state:{ $ne:'DONE' }})
  for(const task of late){
      hitl.createTicket(task, "SLA missed")  // Chapter 14
      await db.update(task.id,{ state:'ESCALATED'})
  }
}, 60000)
```

If a task is late, HITL opens a ticket; no silent failures.

---

## 7. Adding a **New Task Type** in 4 Steps

1. **Define** it in `tasks.yaml`  

   ```yaml
   - type: census.lookup
     description: "Fetch latest Census block data"
   ```

2. **Write a worker** (≤15 lines) in `census-svc/worker.js`.  
3. **Teach the planner** a rule that uses `census.lookup`.  
4. **Deploy**—HMS-ACT auto-discovers via service registry.

Average time for beginners: **~30 minutes**.

---

## 8. Beginner Q & A

| Question | Quick Answer |
|----------|--------------|
| *What if two tasks can run in parallel?* | Just omit `deps`; scheduler publishes them at once. |
| *Can a human claim a task?* | Yes—the Gantt UI has a “Pick Up” button that marks the task `IN_PROGRESS` with your user ID. |
| *How do I cancel a workflow?* | `DELETE /api/act/workflow/WF-785`; running tasks finish, remaining ones are skipped. |
| *Does ACT store secrets?* | No; tasks carry only IDs. Workers fetch real data from their own vaults. |

---

## 9. What You Learned

• HMS-ACT turns one **plain sentence** into a fully monitored, SLA-aware workflow.  
• Tasks flow through **pub/sub**, workers mark **complete**, and the **Gantt board** shows progress.  
• If anything stalls, HITL tickets keep humans in the loop.  
• Adding new task types or planner rules is fast and beginner-friendly.

Next we’ll see how all this activity data is **governed and protected** by the [Data Governance & Privacy Framework (HMS-DTA + HMS-ESQ)](17_data_governance___privacy_framework__hms_dta___hms_esq__.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)