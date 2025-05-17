# Chapter 14: Data Stewardship & Privacy Layer (HMS-DTA)

*(just came from [Secure Inter-Agency Messaging (HMS-A2A)](13_secure_inter_agency_messaging__hms_a2a__.md))*  

---

> “Think of every record as a **book in a giant library**.  
> HMS-DTA is the librarian who sticks a color-badge on the cover,  
> checks your library card, and, when the due-date arrives, shreds the book.”

---

## 1. Why does HMS-GOV need a librarian?

### Use-case:  
The **Defense Nuclear Facilities Safety Board (DNFSB)** runs an inspection lab.  
Yesterday a technician uploaded a soil-radiation CSV.  
Tomorrow a journalist files a **FOIA** request.  
We must instantly know:

1. Is the dataset public (green), internal (yellow), or restricted (red)?  
2. Did the citizen in row 191 sign a release form?  
3. Must we purge the file after 365 days?

If we guess wrong, we break **GDPR-style privacy rules** or slow down public transparency.  
**HMS-DTA** automates those decisions so staff (and AI agents) never have to think about them.

---

## 2. Five key concepts (plain English)

| Concept          | Library Analogy                        | One-line meaning |
|------------------|----------------------------------------|------------------|
| **Badge**        | Green / Yellow / Red sticker           | Classification level (`public`, `internal`, `restricted`) |
| **Consent Tag**  | Signed checkout card inside the book   | Proof a subject agreed to share their data |
| **Retention Clock** | Date stamped on cover               | Auto-delete schedule (`T+365 d`, `forever`, etc.) |
| **Checkpoint**   | Librarian’s desk                       | API that decides “allow” or “deny” every data access |
| **Shredder Job** | End-of-year book disposal              | Nightly task that wipes expired data |

*Remember: Badge + Consent + Clock → Checkpoint → (maybe) Shredder.*

---

## 3. Submitting a new dataset (client side)

```js
// dtaClient.js (≤18 lines)
export async function uploadDataset(file, meta) {
  const body = new FormData()
  body.append('file', file)
  body.append('meta', JSON.stringify(meta)) // {title,badge,retentionDays}

  const r = await fetch('/api/dta/datasets', {
    method : 'POST',
    headers: { Authorization:'Bearer '+userToken },
    body
  })
  return r.json()           // → { id:'DS-77', badge:'yellow', expires:'2026-05-01' }
}

// usage example
await uploadDataset(csvFile, { title:'Soil Radar', badge:'yellow', retentionDays:365 })
```

**What happens?**  
The file lands in HMS-DTA with a **yellow badge** and a **retention clock** (1 year).

---

## 4. Requesting data (AI agent or UI)

```js
// getFile.js  (≤15 lines)
export async function fetchDataset(id) {
  const r = await fetch(`/api/dta/datasets/${id}`, {
    headers:{ Authorization:'Bearer '+userToken }
  })
  if (r.status === 403) throw new Error('Access denied')
  return r.blob()           // 🔓 or 🔒
}

// inside an AI skill
try { const blob = await fetchDataset('DS-77') }
catch { /* agent backs off or requests HITL review */ }
```

HMS-DTA checks the caller’s **role**, the dataset’s **badge**, and any **consent tags** before streaming bytes.

---

## 5. What happens under the hood?

```mermaid
sequenceDiagram
    participant UI as Caller
    participant API as HMS-API
    participant DTA as Privacy Layer
    participant DB as Meta-Store
    participant S3 as File Store

    UI->>API: GET /datasets/DS-77
    API->>DTA: Is access allowed?
    DTA->>DB: read badge, consent, clock
    DTA-->>API: Allow / Deny
    API->>S3: (if allowed) Signed URL
    UI<<--API: 200 + URL or 403
```

Just **four** internal hops—easy to debug.

---

## 6. Inside HMS-DTA: minimal code tour

### 6.1 Access checkpoint (12 lines)

```js
// dta/checkpoint.js
export async function canAccess(user, record) {
  if (record.badge === 'public')      return true
  if (record.badge === 'internal')    return user.roles.includes('staff')
  if (record.badge === 'restricted')  return user.roles.includes('court_order')
  return false
}
```

*Beginner notes:*  
Green → everyone, Yellow → staff only, Red → court order.

### 6.2 Retention scheduler (18 lines)

```js
// jobs/shredder.js
import { Queue } from 'bullmq'
const shredQ = new Queue('shred')

setInterval(async ()=>{
  const expired = await db.datasets.find({ expires:{ $lt: Date.now() } })
  for (const ds of expired)
    await shredQ.add('delete', { id:ds.id, path:ds.path })
}, 60*60*1000)  // every hour
```

Files land in the **shred** queue.  
Workers erase S3 objects and mark the DB row `status:'deleted'`.

### 6.3 Consent checker (14 lines)

```js
// helpers/consent.js
export function hasConsent(record, userId) {
  if (!record.consent) return false
  return record.consent.includes(userId)
}
```

HMS-DTA calls this when **badge === 'restricted' AND record is about a specific person**.

---

## 7. Tagging rows inside a dataset (row-level privacy)

Sometimes only *some* rows are restricted (e.g., minors).  
Store tags in a sidecar JSON:

```json
{
  "DS-77": {
    "rowTags": {
      "191": ["minor","no_consent"],
      "192": []
    }
  }
}
```

Checkpoints combine **dataset badge** + **rowTags** before releasing slices to an AI model.

---

## 8. Linking to other HMS-GOV layers

* **Uploads** arrive via [Governance API Layer](04_governance_api_layer__hms_svc___hms_api__.md).  
* **Long shred jobs** run in [HMS-OMS](05_service_orchestration___task_queues__hms_oms__.md).  
* **AI agents** call `dta.fetch` as a **Tool Card** discovered through [Model Context Protocol](07_model_context_protocol__hms_mcp__.md).  
* **Connectors** borrow secrets (`ctx.secrets`) from HMS-DTA (see [Connectors](12_external_system_synchronization__hms_gov_connectors__.md)).  
* **Red Card** from [HMS-ESQ](10_compliance___legal_reasoning_engine__hms_esq__.md) may block public release if privacy law violated.

---

## 9. Quick FAQ

| Question | Answer |
|----------|--------|
| Can an agency define more than 3 badges? | Yes—add rows to `badges` table (`blue = PII`, etc.). |
| How big can a dataset be? | HMS-DTA streams; tested with 5 GB files. |
| Encryption at rest? | Always AES-256; keys rotate every 30 days. |
| Overriding retention? | Submit `PUT /datasets/:id/retention` → triggers [HITL Override](11_human_in_the_loop__hitl__override_.md). |

---

## 10. Recap & what’s next

You now know:

✓ Why HMS-DTA is the librarian that guards classification, consent, and retention.  
✓ Five building blocks: Badge, Consent Tag, Retention Clock, Checkpoint, Shredder Job.  
✓ How to upload, fetch, and auto-purge datasets with tiny API calls.  
✓ How HMS-DTA plugs into queues, agents, and legal checks across HMS-GOV.

Data is now **safe & compliant**—so how do we prove the whole platform is working?  
Next up: outcome dashboards and performance alerts in  
[Outcome Metrics & Monitoring (HMS-OPS / HMS-ACT)](15_outcome_metrics___monitoring__hms_ops___hms_act__.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)