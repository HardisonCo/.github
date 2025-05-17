# Chapter 13: Human-in-the-Loop (HITL) Override
*(“The red-pen moment before anything goes live”)*  

[← Back to Chapter&nbsp;12: Codified Democracy Engine (HMS-CDF)](12_codified_democracy_engine__hms_cdf__.md)

---

## 0. Why Do We Need a HITL Gate?

Imagine last night an agent inside the **International Trade Administration (ITA)** auto-drafted a rule to:

> “Double tariffs on imported widgets effective tomorrow.”

Before the news hits front pages **someone** in Commerce must:

1. See *exactly* what changed.  
2. Understand the projected economic impact.  
3. Click **Approve**, **Tweak**, or **Reject**—and own that decision.

That pause-and-sign step is the **Human-in-the-Loop (HITL) Override**.  
No AI proposal—policy, payment, data release, or code deployment—skips the human signature sheet.

---

## 1. Key Concepts (Plain English)

| Term                | Friendly Analogy                    | One-sentence meaning |
|---------------------|-------------------------------------|----------------------|
| Diff View           | Redline markup in Word              | Highlights everything the AI changed. |
| Impact Score        | Weather alert color                 | Quick risk grade (0–100) to focus human attention. |
| Decision Buttons    | Stamp pads                          | **Approve**, **Tweak**, **Reject** with one click. |
| Override Token      | Wet-ink signature                   | Cryptographic proof that a named official took the action. |
| Audit Trail         | Clerk’s ledger                      | Immutable record saved to [HMS-DTA](06_data___telemetry_hub__hms_dta__.md). |
| Escalation Ladder   | “Call my manager” list              | Who is next if no one signs before the SLA timer rings. |

---

## 2. Where Does HITL Fit in the Pipeline?

```mermaid
flowchart LR
    AGT[Agent (AI)] --> CDF[HMS-CDF<br/>draft policy]
    CDF --> HITL[HMS-HITL<br/>Override Gate]
    HITL -->|Approve| ENACT[Stage = ENACTED]
    HITL -->|Reject| FAILED[Stage = FAILED]
    HITL -->|Tweak|  BACK[CDF returns to DRAFT]
    HITL --> DTA[HMS-DTA<br/>Audit Trail]
```

*Nothing* reaches the “ENACTED” stage (or production, or treasury vault) until a human presses one of the three buttons.

---

## 3. A 3-Minute Tour of the HITL Screen

```
┌─────────────────────────────────────────────────────────┐
│  Proposal: Fair Back-Pay Act  (Trace ID CDF-682A…F9)   │
├─────────────────────────────────────────────────────────┤
│  DIFF                                                 ▲│
│  - max_backpay: 50000                                 │
│  + max_backpay: 75000   ← colored red/green            │
│                                                       │
│ Impact Score: 72  (High)  🔶                           │
├─────────────────────────────────────────────────────────┤
│   [ REJECT ]   [ TWEAK ]   [ APPROVE ]                │
└─────────────────────────────────────────────────────────┘
```

* Under the hood the diff is computed from the CDF version history.  
* **Impact Score** comes from a pluggable risk model (budget delta, citizen reach, legal conflicts).  
* Clicking a button stores the official’s **Override Token** and moves the playbook forward.

---

## 4. Using HITL in Your Workflow (9 Lines of Code)

### 4.1 Submitting a Proposal & Opening a HITL Gate

```js
import { submitBill } from '@hms/cdf-sdk'
import { hitl } from '@hms/hitl-sdk'

// 1) Draft bill (see Chapter 12)
const id = await submitBill(billYaml)

// 2) Pause pipeline until human review
await hitl.request({
  traceId: id,
  diffUrl:  `/cdf/diff/${id}`,
  impact:   72
})
```

Explanation  
1. After `submitBill`, we immediately **request** a HITL review.  
2. The SDK creates a record in HMS-HITL and notifies the assigned officials.

### 4.2 Handling the Decision Callback (≤10 Lines)

```js
hitl.onDecision(id, async (decision, note) => {
  if (decision === 'approve')
    await cdf.continue(id)        // move to ENACT
  else if (decision === 'tweak')
    await cdf.returnToDraft(id, note)
  else
    await cdf.fail(id, note)      // rejected
})
```

The callback is fired once, carrying the signer’s name and cryptographic token.

---

## 5. What Happens Behind the Curtain?

```mermaid
sequenceDiagram
    participant CDF as HMS-CDF
    participant HITL as HMS-HITL
    participant OFF as Reviewing Official
    participant DTA as HMS-DTA
    CDF->>HITL: openGate(traceId,diff,impact)
    HITL->>OFF: Email + UI link
    OFF-->>HITL: Click APPROVE (token=abc)
    HITL->>CDF: decision(approve, token)
    HITL->>DTA: store audit {traceId,decision,actor}
```

Steps:

1. CDF pauses at “HITL_PENDING”.  
2. HITL emails/SMS/pings the first reviewer on the ladder.  
3. When someone clicks, HITL verifies their PIV card, seals an **Override Token**, and forwards the decision.  
4. Both the request and the decision are logged in an immutable audit trail.

---

## 6. Internal Files (Tiny & Friendly)

### 6.1 `gate.ts` – Create or Resume a Gate (18 lines)

```ts
// core/gate.ts
import { store } from './db'
import { notify } from './notify'

export async function openGate(g: Gate) {
  await store('gates', g.traceId, { ...g, status:'PENDING' })
  notify(g)                        // email & Slack
}

export async function decide(id: string, d: Decision) {
  const gate = await store('gates', id)
  if (gate.status !== 'PENDING') throw 'Already decided'

  await store('gates', id, { ...gate, status:'CLOSED', ...d })
  return d                         // bubbled back to caller
}
```

Beginners’ notes  
* `store` is a wrapper over HMS-DTA.  
* `notify` sends templated messages to the first human in the escalation ladder.

### 6.2 `impact.ts` – Super-Simple Impact Calculator (14 lines)

```ts
// core/impact.ts
export function score(diff: Record<string, any>) {
  let pts = 0
  if (diff.amountChange)  pts += Math.min(diff.amountChange / 1000, 40)
  if (diff.citizensImpacted > 50000) pts += 30
  if (diff.legalConflicts.length)    pts += 30
  return Math.min(pts, 100)          // always 0-100
}
```

*Real systems use ML; this keeps the example beginner friendly.*

---

## 7. Common “Uh-oh” Moments & Quick Fixes

| Symptom | Possible Cause | Fix |
|---------|----------------|-----|
| UI shows *“No reviewer available”* | Escalation ladder empty | Add officials in `hitl.yaml`. |
| Decision callback never fires | Firewall blocks WebSocket | Fallback to HTTPS long-poll in SDK (`hitl.init({ transport:'poll' })`). |
| Duplicate review emails | openGate called twice | Check you aren’t submitting multiple HITL requests for same `traceId`. |
| Impact Score always 0 | diff object missing | Ensure you pass a parsed diff, not a string path, to `score()`. |

---

## 8. Where HITL Sits in the Bigger Picture

```
AI Agents / Pipelines
       ↓
   HMS-HITL  ← (you are here)
       ↓              ↘
    Human Decision     HMS-OPS (metrics)
       ↓
  Next Stage (CDF, ACH, etc.)
       ↓
  HMS-DTA (audit log)
```

HITL is the **pressure valve**: humans steer, AI assists.

---

## 9. Recap & Next Stop

You learned:

* Why every AI action pauses at a **Human-in-the-Loop** checkpoint.  
* The core pieces—Diff View, Impact Score, Decision Buttons, Override Token.  
* How to request a gate, listen for a decision, and see what happens under the hood.  
* Where to debug common hiccups.

Once humans approve, many proposals need specialized AI models or commercial APIs.  
Those live in a curated bazaar you can plug into next:  
[Chapter 14: AI Marketplace (HMS-MKT)](14_ai_marketplace__hms_mkt__.md)

---

*End of Chapter 13*

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)