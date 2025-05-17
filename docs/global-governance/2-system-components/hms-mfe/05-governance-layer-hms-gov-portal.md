# Chapter 5: Governance Layer (HMS-GOV Portal)
[← Back to Chapter 4: Human-in-the-Loop (HITL) Review Console](04_human_in_the_loop__hitl__review_console_.md)

---

> “Think Situation Room meets Google Docs change-tracking.”  
> The **HMS-GOV Portal** is where senior officials, auditors, and agency leads decide **which policy code is allowed into production**—and under which conditions.

---

## 1. Why another portal? — A fax-machine nightmare

Picture the **Judicial Panel on Multidistrict Litigation (JPML)**.  
Every month, an AI agent drafts dozens of routing rules for new civil cases (e.g., “send all opioid lawsuits to Ohio”).  

Without a governance layer, each rule would be:

1. emailed as a PDF,  
2. printed, initialed, scanned, and  
3. manually copied into five different court systems.

Errors creep in, accountability vanishes, and weeks pass.

**HMS-GOV fixes the problem**:

* One web dashboard shows **every proposed rule** and its projected impact.  
* Officials can **Accept**, **Edit**, **Request Clarification**, or **Reject** with a single click.  
* Every click is timestamped and stored in an immutable audit ledger.

---

## 2. Key Concepts (parliament analogies)

| Portal Term | Parliamentary Analogy | What it means |
|-------------|-----------------------|---------------|
| Proposal Queue | Agenda | List of AI-drafted or staff-submitted changes waiting for review. |
| Vote Panel | Committee vote | Buttons: Accept, Amend, Reject. |
| Impact Sheet | Fiscal note | Auto-calculated KPIs (cost, wait-time, risk). |
| Oversight Log | Public record | Append-only timeline of who did what. |
| Guardrail Policy | Standing order | Auto-rules that accept/deny low-risk proposals. |

---

## 3. Quick Tour – Reviewing a proposal in 8 clicks

Below is the **entire flow** for a manager at the Bureau of Engraving and Printing reviewing an AI suggestion to shorten currency-print turnaround.

```vue
<!-- ProposalCard.vue -->
<template>
  <article>
    <h2>{{ p.title }}</h2>                <!-- “Reduce turnaround to 3 days” -->
    <p>Impact: {{ p.impact.score }}</p>  <!-- “-12 % cost, +2 % risk” -->
    <button @click="vote('accept')">👍 Accept</button>
    <button @click="vote('amend')">✏️ Edit</button>
    <button @click="vote('reject')">👎 Reject</button>
  </article>
</template>

<script setup>
const props = defineProps({ p: Object })
async function vote(choice){
  await fetch(`/gov/proposals/${props.p.id}/${choice}`, {method:'POST'})
}
</script>
```

What happens on **Accept**?

1. The portal posts `POST /accept`.  
2. Backend tags the proposal `approved`, signs it, and forwards it to the [Policy/Process Engine](09_policy_process_engine_.md).  
3. An entry like `"BEP_mgr_42 accepted proposal P-882 at 14:03 UTC"` is written to the audit ledger.

---

## 4. Life of a Proposal — 5-step Walkthrough

```mermaid
sequenceDiagram
  participant A2A as AI Agent
  participant GOV as Governance Portal
  participant Off as Official
  participant PPE as Policy Engine
  participant Audit
  A2A->>GOV: createProposal()
  Off->>GOV: GET /queue
  Off->>GOV: POST /proposals/P-882/accept
  GOV->>PPE: applyPatch(P-882)
  GOV-->>Audit: log(accept, Off)
```

Only five actors, end-to-end visibility.

---

## 5. Guardrails – “Auto-approve if safe”

Low-risk tweaks shouldn’t block traffic.  
Create a **Guardrail Policy** in YAML (under 20 lines):

```yaml
# gov/guardrails/low_risk.yaml
if:
  cost_delta_percent: [-2, 5]   # saves money or costs <5 %
  risk_score:        < 3         # negligible risk
then: auto_accept
else: require_human_vote
```

Governance service reads these files at startup; anything matching `if` is auto-accepted and still logged.

---

## 6. Under the Hood – Tiny code peeks

### 6.1 Proposal schema  
File: `gov/models/proposal.ts`

```ts
export interface Proposal {
  id:        string
  title:     string
  patch:     string   // YAML or JS snippet
  impact:    {score:number, details:string}
  status:    'queued'|'approved'|'rejected'
  history:   Array<{by:string, action:string, ts:number}>
}
```

Simple, JSON-serialisable, perfect for DynamoDB or Postgres.

### 6.2 Accept endpoint  
File: `gov/routes/accept.ts`

```ts
import { applyPatch } from '../services/ppe.js'
import { log } from '../services/audit.js'

export async function accept(req, res){
  const { id } = req.params
  const user = req.user.id
  await db.proposals.update(id,{status:'approved'})
  await applyPatch(id)                  // hand off to Policy Engine
  log({proposal:id, by:user, action:'accept'})
  res.status(204).end()
}
```

Under 18 lines including imports!

### 6.3 Guardrail check (simplified)

```ts
export function passesGuardrail(p){
  return p.impact.score < 3 && p.impact.costDelta < 5
}
```

If true, the **Queue Service** calls `accept()` automatically.

---

## 7. Integrating with Other HMS Layers

* **AI Representative Agent** creates proposals → [Chapter 3](03_ai_representative_agent__hms_a2a__.md).  
* **HITL Console** can pause an already-accepted change → [Chapter 4](04_human_in_the_loop__hitl__review_console_.md).  
* **Compliance & Audit Trail** persists the Oversight Log → [Chapter 13](13_compliance___audit_trail_.md).  
* API traffic flows through the **Backend API Gateway** we will meet next → [Chapter 6](06_backend_api_gateway__hms_api___hms_mkt__.md).

---

## 8. Hands-On Exercise (5 min)

1. Run `npm run dev:gov` to start the Governance Portal.  
2. In another terminal, simulate a new AI proposal:

```bash
curl -X POST localhost:4000/a2a/mock-proposal \
  -d '{"title":"Auto-close low-value FOIA requests","impact":{"score":2,"costDelta":-1}}'
```

3. Refresh the portal – the card appears.  
4. Click “Accept”.  
5. Check the audit log:

```bash
tail -n1 logs/audit.log
# => 2024-05-12T14:03Z  User:alice  Action:accept  Proposal:P-901
```

6. Verify the policy is now live by querying the Policy Engine endpoint `/policy/status`.

---

## 9. Common Questions

**Q: Can multiple agencies share one portal?**  
Yes. Each proposal has an `agency` field; RBAC from [IAM](07_identity___access_management__iam__.md) shows only relevant items.

**Q: What if two officials edit at the same time?**  
The portal uses optimistic locking; you’ll be prompted to merge or override.

**Q: How is data tamper-proof?**  
All logs are hashed and appended to a blockchain-style ledger in the **Compliance & Audit Trail** layer.

---

## 10. Summary & What’s Next

Today you learned to:

✓ View, evaluate, and approve AI or staff-generated policy changes.  
✓ Set automatic guardrails for low-risk proposals.  
✓ Understand the end-to-end flow from draft to audit trail.

Next we’ll see **how those approved patches reach microservices securely**:  
[Chapter 6: Backend API Gateway (HMS-API / HMS-MKT)](06_backend_api_gateway__hms_api___hms_mkt__.md)

---

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)