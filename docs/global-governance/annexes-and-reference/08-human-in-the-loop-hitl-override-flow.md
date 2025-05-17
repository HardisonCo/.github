# Chapter 8: Human-In-The-Loop (HITL) Override Flow
*(Coming from [Agent Action Orchestration (HMS-ACT)](07_agent_action_orchestration__hms_act__.md)? Great—now we’ll see **how a human can hit “pause” or “change course” while the orchestra is playing!)*  

---

## 1. Motivation – “Where’s the Big Red Stop Button?”

Imagine the **Office of Environmental Management** is automating hazardous-waste permit renewals.  
An AI agent proposes shortening the public-comment window from 30 days to 7 days to speed up clean-up projects.  
Good idea? Perhaps. **But federal law requires a public-interest officer to review and, if needed, halt or modify the change.**

The **HITL Override Flow** is that safety valve:

* Lets an authorized official **pause, modify, or cancel** an AI-driven change or an in-flight run.  
* Starts a short “Congressional-style” review clock (e.g., 3 business days).  
* Records **who**, **when**, and **why** for later credit—or blame.

> Analogy: Think of it as the **“emergency brake”** on a commuter train.  
> The train (HMS-ACT) runs by schedule, but any passenger with the proper badge can pull the brake, forcing a stop until a conductor approves resumption.

---

## 2. Key Concepts (Plain-English Glossary)

| Term | Friendly meaning |
|------|------------------|
| **Override Request** | A ticket saying “Stop or change X.” |
| **Review Window** | Countdown (e.g., 72 hrs) for officials to act. |
| **Decision** | Approve, modify, or reject the original AI change. |
| **Override Record** | Immutable log row storing who/when/why. |
| **Attribution** | Later analytics that show which official made which call. |

Keep these five in mind; everything else hangs off them.

---

## 3. A Walk-Through Example

### Scenario  
The AI recommends: “Set hazardous-waste comment window to 7 days.”  
A public-interest officer from the **Unified Combatant Commands** feels that’s too short and files an override.

### 3.1 Submit the Override (15-line cURL)

```bash
curl -X POST \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  https://api.hms.gov/hitl/overrides \
  -d '{
        "governance_task_id": 77,
        "action": "pause",
        "reason": "Need stakeholder outreach before shortening window."
      }'
```

**What happens?**

1. An **Override Record** is created (`override_id = 19`).  
2. HMS-ACT pauses the related run or recommendation.  
3. Review window (72 hrs) starts ticking.  
4. All subscribed officials receive an email + GOV portal alert.

### 3.2 Official Acts on the Override (React, 18 lines)

```jsx
// HitlDecisionCard.jsx
export default function HitlDecisionCard({ov, jwt}) {
  const decide = async (choice) => {
    await fetch(`/api/hitl/overrides/${ov.id}/decision`, {
      method: 'POST',
      headers:{'Content-Type':'application/json',
               'Authorization':`Bearer ${jwt}`},
      body: JSON.stringify({choice}) // approve / modify / reject
    });
  };
  return (
    <div className="card">
      <h4>Override #{ov.id}</h4>
      <p>{ov.reason}</p>
      <button onClick={()=>decide('approve')}>Approve Override</button>
      <button onClick={()=>decide('reject')}>Reject</button>
    </div>
  );
}
```

Explanation  
1–4. POSTs the chosen decision.  
5–10. Simple UI with two buttons; a **modify** option could open an extra input.

### 3.3 Outcomes

| Decision | Effect on the run / change |
|----------|---------------------------|
| **Approve** | AI suggestion is vetoed; run canceled. |
| **Modify** | Officer supplies new parameters (e.g., 14 days). HMS-ACT resumes with updated values. |
| **Reject** | Override dismissed; original AI suggestion proceeds. |

Every branch writes an **Override Record** entry like:

```json
{
  "override_id": 19,
  "decided_by": "maj.taylor@defense.gov",
  "decision": "modify",
  "new_value": 14,
  "decided_at": "2024-06-30T09:14:22Z"
}
```

---

## 4. What Happens Behind the Curtain?

```mermaid
sequenceDiagram
    participant API as HMS-API
    participant ACT as Orchestrator
    participant OFF as Officer
    participant GOV as GOV Portal
    participant LOG as Audit DB

    OFF->>API: POST /hitl/overrides  (pause run 77)
    API->>ACT: create_override()
    ACT->>LOG: log override #19 status=pending
    GOV-->>OFF: portal alert "Override pending"
    OFF->>API: POST /override/19/decision modify 14
    API->>ACT: apply_decision()
    ACT->>LOG: update status=completed, decision=modify
```

Only five actors—easy to audit!

---

## 5. Internal Implementation (File Peek)

```
app/
└─ Models/
   └─ HITL/
      └─ Override.php          # ActiveRecord
└─ Controllers/
   └─ HITL/
      ├─ OverrideController.php     # create()
      └─ DecisionController.php     # decide()
└─ Jobs/
   └─ PauseRun.php
```

### 5.1 Model (8 lines)

```php
class Override extends Model {
  protected $table = 'overrides';
  protected $casts = ['meta'=>'array']; // for extra fields
  // relationships
  public function governanceTask(){return $this->belongsTo(GovTask::class);}
}
```

### 5.2 Create Controller (≤ 20 lines)

```php
class OverrideController {
  public function store(Request $r) {
    $ov = Override::create([
       'governance_task_id'=>$r->gov_task_id,
       'action'=>$r->action,      // pause / modify
       'reason'=>$r->reason,
       'created_by'=>$r->user()->id
    ]);
    // Pause the run immediately
    PauseRun::dispatch($ov->governance_task_id);
    return response(['override_id'=>$ov->id], 201);
  }
}
```

### 5.3 Decision Controller (≤ 15 lines)

```php
class DecisionController{
  public function __invoke($id, Request $r){
    $ov = Override::findOrFail($id);
    $ov->decision = $r->choice;          // approve / modify / reject
    $ov->meta['new_value'] = $r->new_value ?? null;
    $ov->decided_by = $r->user()->id;
    $ov->save();
    HitlApplyService::run($ov);          // resume or cancel
    return response()->noContent();
  }
}
```

---

## 6. Data Model at a Glance

| Column | Example Value |
|--------|---------------|
| id | 19 |
| governance_task_id | 77 |
| action | pause |
| reason | Need stakeholder outreach… |
| decision | modify |
| meta | `{ "new_value":14 }` |
| created_by / decided_by | user IDs |
| timestamps | auto |

All override rows are **append-only**; updates always create a new version row, fulfilling audit requirements.

---

## 7. Best Practices & Safety Nets

1. **Default to Pause** – If the review timer expires with no decision, HMS-ACT stays paused.  
2. **Multi-Signer Support** – Require 2-of-3 signatures for high-impact Programs (toggle in Program settings).  
3. **Public Comment Sync** – When the override reason mentions “public comment,” HMS-ACT can automatically open a 7-day comment window using the [Micro-Frontend Experience Layer](05_micro_frontend_experience_layer__hms_mfe__.md).  
4. **Metrics** – Override counts feed into [Metrics & Monitoring](12_metrics___monitoring__hms_ops__.md) for trend graphs (“How many AI proposals were vetoed last quarter?”).

---

## 8. Common API Cheat-Sheet

| Path | Purpose |
|------|---------|
| `POST /hitl/overrides` | File a new override request. |
| `GET /hitl/overrides?status=pending` | List open overrides (for reviewers). |
| `POST /hitl/overrides/{id}/decision` | Approve / modify / reject. |
| `GET /hitl/overrides/{id}` | Full history & audit log. |

All routes use the usual JWT + audit middleware from [Backend API Gateway](03_backend_api_gateway__hms_api___hms_svc__.md).

---

## 9. Recap

You can now:

1. Explain **why** a Human-In-The-Loop override exists—democratic oversight & safety.  
2. File, review, and resolve an override in ≤ 20 lines of code.  
3. Trace the end-to-end flow (API → Orchestrator → Audit).  
4. Understand the simple Laravel/PHP files that power the safety valve.  

Next we’ll look at the legal brain that enforces statutes **before** and **after** overrides:  
[Compliance & Legal Reasoning Engine (HMS-ESQ)](09_compliance___legal_reasoning_engine__hms_esq__.md)  

Stay tuned—the lawyers are entering the chat!

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)