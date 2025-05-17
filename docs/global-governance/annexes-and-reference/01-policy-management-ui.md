# Chapter 1: Policy Management UI


> “Every policy is a flight-plan.  
>  The Policy Management UI is the control tower.”

---

## 1. Why does HMS-GOV need a cockpit?

Imagine you are a city clerk in **Springfield**.  
Citizens keep asking for better recycling rules.  
You open a browser, log in, and see every ordinance—drafts, amendments, final versions—in one place.  
With two clicks you:

1. Open the draft called “2024 Recycling Update.”  
2. Add a sentence about glass pickup.  
3. Click **Publish** so council members can vote.

That single page is the **Policy Management UI**.  
Without it you would email Word files, lose track of comments, and spend days reconciling versions.  
With it, you work in minutes and the public sees results faster.

---

## 2. A first flight: Approving a Recycling Ordinance

We will walk through this very small journey:

1. Clerk opens the **Dashboard**.  
2. Clerk clicks a policy → **Editor** opens.  
3. Clerk edits and presses **Save**.  
4. UI sends a request to the backend (`HMS-API`).  
5. Dashboard refreshes and shows the new status “Ready for Council”.

You already have the two Vue tiles that make this possible.

---

## 3. Meet the two starter tiles

### 3.1 Dashboard Tile (`components/PolicyDashboard.vue`)

```vue
<template>
  <div class="policy-dashboard">
    <h1>Policy Management Dashboard</h1>
    <!-- Later: list of policies will go here -->
  </div>
</template>

<script>
export default { name: 'PolicyDashboard' }
</script>
```

**What it does now**  
Shows a big heading. That is fine: we are just wiring things up.

**What it will do soon**  
Call the backend, list policies, and let the user click one.

---

### 3.2 Editor Tile (`pages/PolicyEditor.vue`)

```vue
<template>
  <div class="policy-editor">
    <h1>Policy Editor</h1>
    <!-- Later: form fields & publish button -->
  </div>
</template>
```

**What it does now**  
Another heading. You will soon add a rich-text editor, change-tracking, and a “Publish” switch.

---

## 4. Quick start: wiring the tiles together

Below is a **tiny** `router.js` example (keep it under 20 lines):

```js
// router.js
import { createRouter, createWebHistory } from 'vue-router'
import PolicyDashboard from '@/components/PolicyDashboard.vue'
import PolicyEditor from '@/pages/PolicyEditor.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',       component: PolicyDashboard },
    { path: '/edit/:id', component: PolicyEditor, props: true }
  ]
})
```

Explanation:

1. When the URL is `/`, the dashboard loads.  
2. When the URL is `/edit/42`, the editor tile opens and receives `id=42`.  
3. Later we will add “intent-driven” links (see [Intent-Driven Navigation](02_intent_driven_navigation_.md)).

Run the app:

```bash
npm install
npm run dev
```

Open `http://localhost:5173` and you should see both headings by clicking around.

---

## 5. What happens under the hood?

Let’s look at the high-level sequence when the clerk hits **Save**.

```mermaid
sequenceDiagram
    participant UI as Policy Editor
    participant API as HMS-API
    participant SVC as HMS-SVC
    participant WF as Workflow Engine
    participant DB as Policy DB

    UI->>API: PUT /policies/42 (new text)
    API->>SVC: validate & sanitize
    SVC->>DB: update record
    SVC-->>WF: trigger "PolicyUpdated" event
    UI<<--API: 200 OK (status=ReadyToVote)
```

Only five participants—simple enough for a beginner!

---

## 6. Inside the code: saving a policy

Step 1: add a **Save** button (8 lines).

```vue
<!-- inside PolicyEditor.vue -->
<button @click="save()">Save</button>

<script setup>
import { ref } from 'vue'
const text = ref('')      // soon bound to a textarea

function save() {
  fetch(`/api/policies/42`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: text.value })
  })
  .then(() => alert('Saved!'))
}
</script>
```

Explanation:

• `fetch` calls `/api/policies/42`.  
• On success we show a simple alert.  
Later we will replace alerts with toast notifications.

Step 2: the backend route (Node/Express pseudo-code, 18 lines).

```js
// routes/policies.js
router.put('/policies/:id', async (req, res) => {
  const id   = req.params.id
  const text = req.body.text

  // 1. Very basic validation
  if (!text || text.length > 10000) return res.status(400).send('Bad text')

  // 2. Save to DB (pseudo)
  await db.policies.update(id, { text, status: 'ReadyToVote' })

  // 3. Emit event for other services
  await eventBus.publish('PolicyUpdated', { id })

  res.send({ status: 'ReadyToVote' })
})
```

This tiny route does three things the diagram already showed.  
Real code will live in **HMS-SVC** and will be covered in  
[Governance API Layer (HMS-SVC / HMS-API)](04_governance_api_layer__hms_svc___hms_api__.md).

---

## 7. Where does the cockpit fit in the avionics?

• The **UI** lives in the browser and is built as a set of **micro-frontends** (covered in [Micro-Frontend Framework (HMS-MFE)](03_micro_frontend_framework__hms_mfe__.md)).  
• Navigation between tiles is driven by user **intent** (next chapter).  
• Data comes from the **Governance API Layer** (chapter 4).  
• Workflows—like routing the ordinance to council—are handled by the **Legislative Workflow Engine** (chapter 9).

Keep this mental map; we will zoom into each part later.

---

## 8. Recap

You now know:

✓ Why the Policy Management UI matters (single cockpit).  
✓ How to display the starter dashboard and editor tiles.  
✓ How a Save operation travels from your click to the database.  
✓ How this UI connects to the wider HMS-GOV system.

In the next chapter you will learn how users move between tiles using “intent” links instead of fragile URLs. Ready? Fly over to  
[Intent-Driven Navigation](02_intent_driven_navigation_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)