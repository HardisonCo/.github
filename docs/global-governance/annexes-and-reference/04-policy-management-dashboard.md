# Chapter 4: Policy Management Dashboard <a name="chapter-4"></a>

*(Follow-up to [Front-end Micro-Frontend Framework (HMS-MFE)](03_front_end_micro_frontend_framework__hms_mfe__.md))*  

---

## 1. Why Do We Need a “Control Tower”?

Picture Maria, an analyst at the **Office of Fossil Energy**.  
Congress just approved a **Clean-Coal Rebate** regulation. Today Maria must:

1. Upload the legal text.  
2. Watch it move from *Draft* ➜ *Under Review* ➜ *Nation-wide Roll-out*.  
3. Verify early KPIs (e.g., “rebates processed / day”).  
4. Roll back instantly if numbers look fishy.  

Doing that with e-mails and spreadsheets is like **air-traffic control with walkie-talkies**.  
Instead, HMS-GOV offers a single web page—the **Policy Management Dashboard**—that shows *every policy’s flight path* in real time and gives one-click actions (Publish, Clone, Rollback).

---

## 2. The Big Picture

```
mermaid
graph TD
    subgraph Storefront Layer
        PD[Policy Management Dashboard] 
    end
    subgraph Service Layer
        API[HMS-API Gateway]
        PLSVC[policy-svc]
    end
    PD -->|REST| API
    API --> PLSVC
```

• The Dashboard is a **micro-frontend** (Chapter 3) rendered inside `<PolicyDashboard />`.  
• All data still flows through the [Backend API Gateway](02_backend_api_gateway__hms_svc___hms_api__.md) for security and logging.  

---

## 3. Key Concepts in Plain English

| Term                      | Beginner Explanation                                                |
|---------------------------|---------------------------------------------------------------------|
| **Flight Path**           | The life-cycle status of a policy (Draft → Pilot → Roll-out).      |
| **Queued Proposal**       | A policy waiting for approval—think “planes on runway.”            |
| **Active Roll-out**       | A policy now live in one or more states.                           |
| **KPI Panel**             | Little gauges (widgets) that stream metrics (e.g., error rate).    |
| **Audit Trail**           | An uneditable log of who clicked what, when—like a flight recorder.|
| **Action Buttons**        | UI hooks that call backend endpoints (`/publish`, `/rollback`).    |

Keep these six ideas in mind; the Dashboard is just a **pretty wrapper** around them.

---

## 4. A 60-Second Tour for New Admins

```
┌──────────────────────────────────────────────────────────┐
│ Clean-Coal Rebate (P-2024-017)         ⏳ Queued         │  <-- Flight Path Card
├──────────────────────────────────────────────────────────┤
│ • Drafted by: Maria Gonzales (DOE)                       │
│ • Go-Live ETA: 2024-07-01                                │
│ • KPI Snapshot: Errors 0.1%, Avg Process Time 1.3 s      │
│                                                          │
│   [Preview]   [Publish]   [Clone]   [Rollback]           │  <-- Action Buttons
└──────────────────────────────────────────────────────────┘
```

New policies show up automatically; you just push the buttons.  
Charts, tables, and KPIs are **micro-frontend widgets** plugged into slots you will see next.

---

## 5. Scaffolding the Component

The file already exists: `components/PolicyDashboard.vue`.  
Below is the default skeleton (10 lines):

```vue
<!-- components/PolicyDashboard.vue -->
<template>
  <div class="policy-dashboard">
    <h1>Policy Management Dashboard</h1>
    <!-- widgets will mount here -->
    <div id="slot-flight-table"></div>
    <div id="slot-kpi-panel"></div>
  </div>
</template>

<script>
export default { name: 'PolicyDashboard' }
</script>
```

Explanation  
• Two empty `<div>`s (`slot-flight-table`, `slot-kpi-panel`) are *docking ports* for future widgets.  
• Designers can drop React/Svelte/Vue bricks in these slots exactly as described in Chapter 3.  

---

## 6. Loading Your First Widget

Let’s mount a **Flight Table** brick that lists queued proposals.

```html
<!-- views/AdminHome.vue (snippet) -->
<template>
  <PolicyDashboard />
</template>

<script setup>
// 1) import the shell
import PolicyDashboard from '@/components/PolicyDashboard.vue'

// 2) load widget bundle at runtime
import { onMounted } from 'vue'
onMounted(async () => {
  await loadBrick('https://cdn.hms.gov/mfe/flight-table@1.0.0.js')
  window.renderFlightTable(
     document.getElementById('slot-flight-table'),
     { apiRoot: '/policies' }      // props sent to widget
  )
})

// tiny helper
function loadBrick(url){
  return new Promise(res => {
     const s=document.createElement('script'); s.src=url; s.onload=res
     document.head.appendChild(s)
  })
}
</script>
```

What just happened?  
1. The host page (`AdminHome`) imports `<PolicyDashboard/>`.  
2. `loadBrick` fetches the widget’s JS from the CDN.  
3. The widget renders itself into `slot-flight-table`, fetching data via `/policies` (next section).  

---

## 7. Talking to the Backend (Minimal API Call)

Every widget—and the Dashboard shell when needed—talks to our services through HMS-API.

```javascript
// services/policyApi.js
export async function listQueued() {
  const res = await fetch('/api/policies?status=queued')
  return res.json()         // [{ id: 'P-2024-017', title: 'Clean-Coal', ... }]
}
```

• `/api` is auto-routed by the **Gateway** (Chapter 2) to `policy-svc`.  
• No CORS pain, no hard-coding IPs.

---

## 8. What Happens Under the Hood?

```
mermaid
sequenceDiagram
    participant Browser
    participant PD as PolicyDashboard
    participant API as HMS-API
    participant PSVC as policy-svc
    Browser->>PD: load widget bundle
    PD->>API: GET /policies?status=queued
    API->>PSVC: /policies ...
    PSVC-->>API: JSON list
    API-->>PD: JSON list
    PD-->>Browser: render table rows
```

If anything fails (e.g., `policy-svc` times out), the Gateway returns an error the widget can show as *“temporarily unavailable.”*

---

## 9. Wiring the Action Buttons

A **Publish** click should flip the policy’s status.

```javascript
// services/policyApi.js  (add)
export async function publish(id){
  const res = await fetch(`/api/policies/${id}/publish`, { method: 'POST'})
  if(!res.ok) throw new Error('Could not publish')
}
```

Inside the widget:

```javascript
// flight-table/ButtonBar.js
import { publish } from '../services/policyApi.js'

async function handlePublish(id){
   try { await publish(id); alert('Published!') }
   catch{ alert('Something went wrong; check Audit Trail.') }
}
```

This keeps UI code tiny; all heavy logic (permission checks, versioning, rollback) live in `policy-svc`.

---

## 10. Glimpse Inside `policy-svc` (Server Side)

```python
# policy_svc/routes.py  (pseudo-code, 17 lines)
from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.post("/policies/{pid}/publish")
def publish_policy(pid: str, user=Depends(get_user)):
    if not user.can('publish_policy'):
        raise HTTPException(403)
    # 1) mark policy as ACTIVE
    db.update('policies', pid, status='active')
    # 2) log audit trail
    audit.log(user.id, pid, action='publish')
    # 3) push event to KPI stream
    kpi.push('policy_published', pid)
    return {"status": "ok"}
```

Even beginners can read this:  
• Validate user ➜ update database ➜ write audit ➜ emit KPI.  
Zero extra magic.

---

## 11. Adding Live KPIs

Remember the empty `slot-kpi-panel`? Let’s drop a **Gauge** widget coming from **U.S. Space Command** to track policy latency across satellites (just for fun!):

```javascript
await loadBrick('https://cdn.hms.gov/mfe/kpi-gauge@0.3.0.js')
window.renderKpiGauge(
     document.getElementById('slot-kpi-panel'),
     { metric: 'policy_latency_ms' }
)
```

Widgets are agnostic—whether numbers come from satellites or servers, the API supplies JSON such as:

```json
{ "metric": "policy_latency_ms", "value": 134 }
```

---

## 12. FAQ for First-Time Dashboard Builders

**Q: Do I need Vue to create a widget?**  
A: Nope. Any framework works; you only expose a `render*` function (see Chapter 3).

**Q: How are audit logs shown?**  
A: Another widget reads `/api/policies/{id}/audit` and renders a timeline. Nothing is hard-coded in the Dashboard component.

**Q: Can I customize which columns show?**  
A: Yes. Pass extra props (`columns` array) to the widget; if missing, it falls back to defaults.

**Q: What if I break production by publishing a bad policy?**  
A: Click **Rollback**. The button calls `/policies/{id}/rollback`, which reverts the DB row and triggers compensating events—no manual SQL needed.

---

## 13. What You Learned

• The **Policy Management Dashboard** is a *host shell* plus plug-in widgets.  
• Widgets fetch data via HMS-API and speak to `policy-svc` for actions.  
• Slots (`slot-flight-table`, `slot-kpi-panel`, etc.) keep design flexible.  
• All heavy lifting—permissions, versioning, audit—lives in backend services.  

Next we will zoom into authoring an individual policy’s text, rules, and tests inside the [Policy Editor](05_policy_editor_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)