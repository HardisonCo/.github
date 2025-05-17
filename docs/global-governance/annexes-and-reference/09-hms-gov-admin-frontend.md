# Chapter 9: HMS-GOV (Admin Frontend)

In [Chapter 8: Modules Directory (Business Logic)](08_modules_directory__business_logic__.md) we organized our “bureaus” of functionality into modules. Now we’ll build **HMS-GOV**, the Vue.js admin dashboard where policy-makers and administrators log in, browse existing regulations, draft or amend policies, and push changes to the backend.

---

## 1. Motivation & Central Use Case

Imagine you’re an administrator in the California Housing Department. You need to:

1. See all current housing subsidy policies.  
2. Drill into a specific policy to update eligibility thresholds.  
3. Upload a revised draft (PDF or Markdown).  
4. Monitor which regulations are pending enactment.

**HMS-GOV** is your “legislative chamber dashboard”:

- A **table view** of policies and status badges.  
- A **hierarchy navigator** to switch between divisions (e.g., “Housing → Urban Housing → Subsidies”).  
- A **form editor** with sliders, file uploads, and rich text.  
- A **push button** that calls HMS-API to save or submit for enactment.

---

## 2. Key Concepts

1. **DomainNavigator**  
   Lets you browse government domains and sub-departments.  
2. **PolicyDashboard**  
   Table of policies with status (Draft, Under Review, Enacted).  
3. **PolicyEditor**  
   Form with components like `slider-base`, `v-filepond-props`, and styled cards.  
4. **EnactmentMonitor**  
   Real-time list of enactment requests and their outcomes.

---

## 3. Building the Dashboard

### 3.1 Project Setup

```bash
vue create hms-gov
cd hms-gov
npm install axios slider-base card-colors v-filepond-props
```
This creates a Vue project and adds UI components for government-style forms.

### 3.2 main.js (Bootstrapping)

```js
// src/main.js
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './assets/card-colors.css'   // styling for cards

Vue.config.productionTip = false
new Vue({ router, render: h => h(App) }).$mount('#app')
```
We import `router` and our card styles before mounting the app.

---

## 4. Routing & Layout

### 4.1 router/index.js

```js
import Vue from 'vue'
import Router from 'vue-router'
import Dashboard from '../components/PolicyDashboard.vue'
import Editor    from '../components/PolicyEditor.vue'

Vue.use(Router)
export default new Router({
  routes: [
    { path: '/',         component: Dashboard },
    { path: '/edit/:id', component: Editor, props: true }
  ]
})
```
Two routes: a dashboard at `/` and an editor for `/edit/:id`.

### 4.2 App.vue

```html
<template>
  <div id="app">
    <h1>HMS-GOV Admin</h1>
    <router-view/>
  </div>
</template>
```
A simple wrapper showing our page title and the routed component.

---

## 5. PolicyDashboard Component

File: `src/components/PolicyDashboard.vue`

```html
<template>
  <div>
    <domain-navigator @change="loadPolicies"/>
    <table>
      <tr><th>Policy</th><th>Status</th><th>Actions</th></tr>
      <tr v-for="p in policies" :key="p.id">
        <td>{{ p.title }}</td>
        <td><span :class="p.status">{{ p.status }}</span></td>
        <td><router-link :to="`/edit/${p.id}`">Edit</router-link></td>
      </tr>
    </table>
  </div>
</template>

<script>
import DomainNavigator from './DomainNavigator.vue'
import api from '../services/api'

export default {
  components: { DomainNavigator },
  data: () => ({ policies: [] }),
  methods: {
    async loadPolicies(domain) {
      this.policies = await api.fetchPolicies(domain)
    }
  },
  created() { this.loadPolicies('all') }
}
</script>
```

- **domain-navigator** emits the selected domain.  
- We call `api.fetchPolicies(domain)` to load a filtered list.

---

## 6. PolicyEditor Component

File: `src/components/PolicyEditor.vue`

```html
<template>
  <div>
    <h2>Edit Policy: {{ policy.title }}</h2>
    <slider-base v-model="policy.priority" :min="1" :max="10"/>
    <v-filepond-props v-model="attachments"/>
    <button @click="save">Save & Submit</button>
  </div>
</template>

<script>
import sliderBase from 'slider-base'
import filepond    from 'v-filepond-props'
import api         from '../services/api'

export default {
  components: { sliderBase, filepond },
  props: ['id'],
  data: () => ({ policy: {}, attachments: [] }),
  async created() {
    this.policy = await api.fetchPolicy(this.id)
  },
  methods: {
    async save() {
      await api.updatePolicy(this.id, { ...this.policy, attachments: this.attachments })
      this.$router.push('/')
    }
  }
}
</script>
```

- **slider-base** sets a numeric priority.  
- **v-filepond-props** handles file uploads.  
- On save, we update via `api.updatePolicy` and return to dashboard.

---

## 7. API Service Layer

File: `src/services/api.js`

```js
import axios from 'axios'
const client = axios.create({ baseURL: 'http://localhost:3000/api' })

export default {
  fetchPolicies(domain) {
    return client.get(`/policies?domain=${domain}`)
                 .then(r => r.data)
  },
  fetchPolicy(id) {
    return client.get(`/policies/${id}`).then(r => r.data)
  },
  updatePolicy(id, payload) {
    return client.put(`/policies/${id}`, payload)
  }
}
```
A minimal wrapper around HMS-API endpoints.

---

## 8. Under the Hood: User Flow

```mermaid
sequenceDiagram
  participant Admin
  participant GOV as HMS-GOV
  participant API as HMS-API
  participant DB

  Admin->>GOV: click “Edit” on policy 123
  GOV->>API: GET /policies/123
  API->>DB: SELECT * FROM policies WHERE id=123
  DB-->>API: { id:123, title:…, status:Draft }
  API-->>GOV: JSON policy
  Admin->>GOV: adjust slider & upload file
  GOV->>API: PUT /policies/123
  API->>DB: UPDATE policies …; INSERT attachments …
  API-->>GOV: success
  GOV-->>Admin: redirect to dashboard
```

1. **Admin** selects a policy to edit.  
2. **GOV** fetches data from **API**.  
3. **Admin** makes changes and saves.  
4. **GOV** pushes updates back to **API** and reloads.

---

## 9. Internal File Structure

```
src/
├─ assets/
│  └─ card-colors.css
├─ components/
│  ├─ DomainNavigator.vue
│  ├─ PolicyDashboard.vue
│  └─ PolicyEditor.vue
├─ router/
│  └─ index.js
├─ services/
│  └─ api.js
├─ App.vue
└─ main.js
```

- **components/**: Vue views and widgets  
- **services/api.js**: HTTP calls  
- **router/index.js**: routes  

---

## 10. Conclusion & Next Steps

In this chapter you learned how **HMS-GOV**:

- Provides a Vue.js interface for policy-makers.  
- Uses intuitive tables, domain navigation, and form components (`slider-base`, `v-filepond-props`).  
- Calls **HMS-API** to fetch, update, and monitor policy enactment.

Next up is the public-facing marketplace in [Chapter 10: HMS-MKT (Public Marketplace Frontend)](10_hms_mkt__public_marketplace_frontend__.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)