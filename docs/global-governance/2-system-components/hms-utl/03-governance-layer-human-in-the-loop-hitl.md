# Chapter 3: Governance Layer & Human-in-the-Loop (HITL)  
*(a.k.a. “The City Council Above Every Bot”)*  

[← Back to Chapter 2: Policy Lifecycle Engine (HMS-CDF)](02_policy_lifecycle_engine__hms_cdf__.md)

---

## 1. Why Do We Need a Governance Layer?

Imagine the **Farm Service Agency (FSA)** builds a chatbot that automatically approves small seed-loan requests.  
Everything hums along until the bot approves a *duplicate* loan for the same farmer, violating a federal cap. 💸

What went wrong?  
We let an algorithm make a binding decision with **no stop-gap** for:

* Ethical or legal red flags  
* Conflicting data from another agency  
* Simple human common sense (“wait, didn’t we already pay this farm?”)

The Governance Layer gives us that stop-gap.

> Think of it as a digital *city council*:  
> Bots *propose* actions, humans *review* or *veto*, and every step is written into the minutes.

---

## 2. Core Concepts (Only Four!)

| Term | One-Line Analogy | What It Does |
|------|-----------------|--------------|
| Proposal Log | A clerk’s notebook | Records every automated suggestion (“approve loan #123”). |
| Review Queue | Inbox for officials | Items that need a human eye before execution. |
| Decision Console | City-council chamber | UI where staff can approve, reject, or edit the proposal. |
| Audit Ledger | The public archive | Immutable history for OIG, FOIA, or internal audits. |

All four together = **Governance Layer**.

---

## 3. Walk-Through Use Case: Approving a Seed-Loan

1. Chatbot evaluates Farmer Jane’s application.  
2. It *proposes* → “Approve $5 000.”  
3. Proposal hits the **Review Queue**.  
4. Officer Maria opens the **Decision Console**, sees Jane already got $2 000 yesterday.  
5. Maria *edits* amount to $3 000, clicks **Approve**.  
6. Final action is written to **Audit Ledger** and sent downstream for payout.

Simple, but life-saving for compliance teams!

---

## 4. Trying It Out in Code (9 + 9 lines)

### 4.1 Bot Side – Create a Proposal

```python
# /agt/loan_bot.py  (HMS-AGT agent)
from hms_utl import governance as gov

def propose_loan(app):
    proposal = {
        "action": "approve_loan",
        "payload": {"app_id": app.id, "amount": 5000},
        "reason": "meets credit score"
    }
    gov.submit(proposal)   # ← hands off to Governance Layer
```

Explanation: The agent never touches the bank account.  
It simply logs a **proposal**.

---

### 4.2 Human Side – Review & Decide

```javascript
// /mfe/DecisionConsole.jsx  (HMS-MFE)
function ReviewCard({ proposal }) {
  const [amount, setAmount] = useState(proposal.payload.amount);

  return (
    <Card>
      <h3>Loan Request #{proposal.payload.app_id}</h3>
      <input value={amount} onChange={e => setAmount(e.target.value)} />
      <button onClick={() => gov.approve(proposal.id, { amount })}>Approve</button>
      <button onClick={() => gov.reject(proposal.id, "Duplicate loan")}>Reject</button>
    </Card>
  );
}
```

Explanation:  
Users *edit or override* before committing.  
Clicks translate to `POST /gov/api/v1/decision`.

---

### 4.3 Result – Automated Payout Trigger

```bash
curl /gov/api/v1/decisions/42
```

Returns:

```json
{
  "status": "approved",
  "final_payload": { "amount": 3000 },
  "decided_by": "maria.fsa",
  "timestamp": "2025-01-15T14:06Z"
}
```

Downstream payout system (HMS-ACH) only acts on **approved** entries.

---

## 5. What Happens Under the Hood?

```mermaid
sequenceDiagram
    participant AGT as Loan Bot
    participant GOV as Governance API
    participant OFF as Officer Console
    participant ACH as Payout Service
    AGT->>GOV: submit(proposal)
    GOV->>OFF: push to Review Queue
    OFF->>GOV: POST /decision (approve/reject)
    GOV->>ACH: webhook "approved_loan"
```

*The bot literally cannot pay the money.*  
Only after a human’s decision does HMS-ACH move funds.

---

## 6. Sneak Peek at Implementation Files

### 6.1 Event Schema (`hms-gov/models.py`, 15 lines)

```python
class Proposal(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    action: str             # e.g., "approve_loan"
    payload: dict           # arbitrary JSON
    reason: str
    status: str = "pending" # pending|approved|rejected
    created_at: datetime = Field(default_factory=datetime.utcnow)
    decided_by: str | None = None
    decided_at: datetime | None = None
```

Key idea: **append-only**; status changes create new records, original stays intact.

---

### 6.2 Tiny Approval Endpoint (`hms-gov/api.py`, 12 lines)

```python
@app.post("/decision/{id}")
def decide(id: UUID, body: DecisionIn, user = Depends(auth)):
    prop = db.get(id)
    if prop.status != "pending":
        raise HTTPError(409, "Already decided")
    prop.status = body.status      # approved|rejected
    prop.payload |= body.patch or {}
    prop.decided_by = user.email
    prop.decided_at = utcnow()
    db.save(prop)                  # new ledger entry
    if prop.status == "approved":
        emit_webhook(prop)
    return prop
```

Notice the guard-rail: only **pending** items can be changed.

---

## 7. Running Locally in < 2 Minutes

```bash
git clone hms-utl
cd hms-gov
docker compose up -d     # starts Postgres + FastAPI
pnpm --filter hms-mfe dev   # Decision Console UI
```

1. Visit `http://localhost:5173/queue`.  
2. In another shell run:  

   ```bash
   python examples/demo_propose.py      # emits 3 sample proposals
   ```  

3. Approve one, reject another, leave one pending.  
4. Check `logs/audit.jsonl`—every state change is there.

---

## 8. How It Fits in the 3-Floor Architecture

| Floor | What Lives Here | Files |
|-------|-----------------|-------|
| Basement (HMS-SYS) | Audit Ledger DB, message queue | `docker/postgres`, `hms-gov/db.py` |
| Middle (HMS-SVC)   | Governance REST API | `hms-gov/api.py` |
| Top (HMS-MFE)      | Decision Console UI | `mfe/DecisionConsole.jsx` |

No service may **skip** the middle floor to write directly to the ledger or payout—enforcing accountability.

---

## 9. Takeaways

✔ You learned why even the smartest bots need supervisors.  
✔ The Governance Layer = Proposal Log + Review Queue + Decision Console + Audit Ledger.  
✔ Bots *suggest*, humans *decide*, and auditors can **replay every click**.  
✔ All actions remain interoperable with other layers like the [Policy Lifecycle Engine (HMS-CDF)](02_policy_lifecycle_engine__hms_cdf__.md) and future enforcement by HMS-ACH.

Next, we’ll see how legally complex questions (e.g., “Is this loan within federal subsidy limits?”) are answered automatically using rules and statutes in the [Compliance & Legal Reasoning Engine (HMS-ESQ)](04_compliance___legal_reasoning_engine__hms_esq__.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)