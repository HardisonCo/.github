# Chapter 3: Backend API Layer (HMS-API / HMS-MKT)

In [Chapter 2: Micro-Frontend Architecture (HMS-MFE)](02_micro_frontend_architecture__hms_mfe__.md) we built tiny UI fragments that talk to a server. Now it’s time to explore the **Backend API Layer**, the house rules and machine-to-machine “forms” that power every feature in HMS.

## Why the Backend API Layer?

Imagine an online e-filing portal at the Department of the Interior. Citizens, admin UIs, AI agents, and automated schedulers all need to:

- Submit applications  
- Update workflows  
- Query policy data  

Our **Backend API Layer** (HMS-API / HMS-MKT) exposes clean, versioned HTTP endpoints to make these tasks possible. It’s like official government forms, but for code.

### Central Use Case: Permit Application Workflow

Alice’s User Portal (from [Chapter 1](01_interface_layer__user___admin_uis__.md)) calls our API to:

1. POST a new permit application  
2. Poll or subscribe for status updates  
3. PUT a status change when an agent or scheduler approves it  

Behind the scenes, HMS-API routes each request to internal services, validates permissions, stores data, and notifies interested parties in real time.

## Key Concepts

1. **Endpoints & Methods**  
   Defined URLs (e.g. `/api/applications`) with HTTP verbs (GET, POST, PUT).  
2. **Authentication & Trust**  
   Only authenticated UIs, AI Agents, or schedulers can call certain routes.  
3. **Versioning**  
   Prefix URLs with `/v1/` or `/v2/` to allow safe API evolution.  
4. **Data Models**  
   JSON schemas for applications, policies, workflows—similar to paper forms.  
5. **Clients**  
   - **User Portal** (browser)  
   - **Admin Dashboard**  
   - **AI Agent** (HMS-A2A)  
   - **External Schedulers**  

## Using HMS-API in Your Code

Here’s how a Node.js client might submit a new application and read the response:

```js
// submit.js
fetch('https://hms.gov/api/v1/applications', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    agency: 'Bureau of Ocean Energy Management',
    applicantName: 'Alice',
    type: 'Energy Lease Permit'
  })
})
  .then(res => res.json())
  .then(payload => {
    console.log('Application ID:', payload.id);
    console.log('Current Status:', payload.status);
  });
```
Above, you POST form data and get back `{ id: 123, status: "Pending" }`.

To update that status (e.g. by an AI Agent):
```js
// approve.js
fetch('https://hms.gov/api/v1/applications/123/status', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ status: 'Approved' })
});
```
This triggers notifications so that Alice’s UI sees “Approved” in real time.

## What Happens Under the Hood?

Let’s walk through a simple sequence when an application is created and then approved:

```mermaid
sequenceDiagram
  participant Portal as User Portal
  participant API as HMS-API
  participant DB as Database
  participant Notif as NotificationSvc

  Portal->>API: POST /v1/applications {…}
  API->>DB: INSERT new application
  DB-->>API: { id:123, status:"Pending" }
  API->>Notif: publish event (app:123 created)
  API-->>Portal: { id:123, status:"Pending" }
  Note over Portal,Notif: Portal subscribes via WebSocket/SSE
  Portal<--Notif: {"id":123,"status":"Approved"}
```

1. The UI calls **HMS-API**.  
2. HMS-API stores data in the **Database**.  
3. HMS-API publishes an event to **NotificationSvc**.  
4. NotificationSvc pushes updates back to UIs or other clients.

## Inside HMS-API: Simple Express Example

Below is a minimal skeleton showing how routes are organized.

```js
// src/api/index.js
const express = require('express');
const app = express();
app.use(express.json());

// Mount versioned routes
app.use('/v1/applications', require('./routes/applications'));
app.listen(3000, () => console.log('HMS-API running on port 3000'));
```

```js
// src/api/routes/applications.js
const router = require('express').Router();

// POST /v1/applications
router.post('/', (req, res) => {
  // validate req.body, save to DB, publish event...
  const newApp = { id: 123, status: 'Pending' }; 
  res.status(201).json(newApp);
});

// PUT /v1/applications/:id/status
router.put('/:id/status', (req, res) => {
  // update DB, publish event...
  res.sendStatus(204);
});

module.exports = router;
```
Each route:
1. Validates and parses JSON.  
2. Talks to a data store (or service).  
3. Sends back a JSON response or status code.  
4. Emits events for real-time updates.

## Summary

In this chapter you learned how the **Backend API Layer (HMS-API / HMS-MKT)** exposes machine-friendly “forms” to manage applications, policies, and workflows. You saw:

- Why we need clean, versioned endpoints  
- How to call them from code  
- A step-by-step sequence of data insertion and notifications  
- Minimal Express.js examples illustrating route setup  

Next up, we’ll see how these APIs get wired together into higher-level processes and orchestrations in the [Management Layer (Service Orchestration)](04_management_layer__service_orchestration__.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)