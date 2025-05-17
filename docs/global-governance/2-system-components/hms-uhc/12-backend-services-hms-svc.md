# Chapter 12: Backend Services (HMS-SVC)

Welcome back! In [Chapter 11: Modular Microservices Structure](11_modular_microservices_structure_.md) we split our platform into independent “neighborhoods”—each running its own code and data. Now we’ll go inside those neighborhoods and build the **Backend Services (HMS-SVC)**, the “administrative offices” of our system that process core business logic and data.

---

## 1. Why Backend Services?

Imagine the **University Health Sciences Center** needs to:

- Check if a student is eligible for clinical rotations  
- Schedule lab usage slots and prevent conflicts  
- Run month-end reports on equipment utilization  

Rather than dumping all this logic into a single app or the frontend, we create dedicated backend services. Each one:

- Encapsulates a single business domain (eligibility, scheduling, analytics)  
- Manages its own data store and processing logic  
- Exposes a clear, minimal API that other layers ([Interface Layer](01_interface_layer_.md), [API Gateway](13_backend_api_layer__hms_api___hms_mkt__.md)) can call  

This separation keeps our code organized, teams independent, and services easier to test and scale.

---

## 2. Key Concepts

1. **Business Logic Layer**  
   A service that runs domain rules (e.g., “only seniors can enter the research lab”).

2. **Data Processing**  
   Batch or real-time computations (e.g., calculating monthly billing totals).

3. **API Contract**  
   A simple HTTP interface: requests in, JSON out.

4. **State Management**  
   Each service owns its own database (no cross-service database joins).

5. **Service Isolation**  
   Failures or updates in one service don’t crash the others.

---

## 3. Using Backend Services: A Lab-Booking Example

Let’s build three tiny services under HMS-SVC:

1. **Eligibility Service**  
2. **Scheduling Service**  
3. **Analytics Service**  

### 3.1. Eligibility Check

Request:

```http
POST /eligibility
Content-Type: application/json

{ "studentId": 42, "labId": "BIO101" }
```

Response:

```json
{ "eligible": true, "reason": "Completed safety training" }
```

Explanation:  
- The frontend sends student+lab info.  
- Eligibility Service looks up training records in its database.  
- It returns a boolean and a short explanation.

### 3.2. Scheduling Slot

Request:

```http
POST /labs/schedule
Content-Type: application/json

{ "studentId": 42, "labId": "BIO101", "slot": "2024-07-15T10:00Z" }
```

Response:

```json
{ "scheduled": true, "confirmationId": 123 }
```

Explanation:  
- Checks for conflicts, writes to its own `slots` table, and returns a confirmation ID.

### 3.3. Monthly Utilization Report

Request:

```http
GET /reports/utilization?month=2024-06
```

Response:

```json
{ "labId":"BIO101", "hoursUsed": 320, "peakUsageDay":"2024-06-12" }
```

Explanation:  
- Runs an aggregation over scheduled sessions, returns key metrics.

---

## 4. Under the Hood: Step-by-Step Flow

```mermaid
sequenceDiagram
  participant Frontend
  participant APIGW as API Gateway
  participant SVC as HMS-SVC
  participant DB
  participant Analytics

  Frontend->>APIGW: POST /eligibility {studentId, labId}
  APIGW->>SVC: forward to /eligibility
  SVC->>DB: query training_records
  DB-->>SVC: {studentId:42, trainings:["safety"]}
  SVC-->>APIGW: {eligible:true,...}
  APIGW-->>Frontend: {eligible:true,...}

  Frontend->>APIGW: POST /labs/schedule {...}
  APIGW->>SVC: forward to /labs/schedule
  SVC->>DB: write new slot
  DB-->>SVC: success
  SVC-->>APIGW: {scheduled:true,...}

  // Analytics might run as a scheduled job calling SVC
  Analytics->>SVC: GET /reports/utilization?month=2024-06
```

1. The **API Gateway** routes requests to the right HMS-SVC endpoint.  
2. The service queries or updates its **own database**.  
3. Responses flow back through the gateway to the frontend.  
4. The Analytics job polls the service for monthly reports.

---

## 5. Inside HMS-SVC: Minimal Code

Below is a super-simple Express.js service combining our three endpoints.

```js
// File: hms-svc/server.js
const express = require('express');
const app = express();
app.use(express.json());

// In-memory stores for demo
const trainings = { "42":["safety"] };
const slots     = {};
const usageData = { "2024-06": { "BIO101": {hours:320, peak:"2024-06-12"} } };

// 1. Eligibility
app.post('/eligibility', (req, res) => {
  const {studentId, labId} = req.body;
  const eligible = trainings[studentId]?.includes('safety');
  res.json({ eligible, reason: eligible ? 'Completed safety training' : 'Missing training' });
});

// 2. Scheduling
app.post('/labs/schedule', (req, res) => {
  const key = `${req.body.labId}@${req.body.slot}`;
  if (slots[key]) return res.json({ scheduled: false, error: 'Conflict' });
  slots[key] = req.body.studentId;
  res.json({ scheduled: true, confirmationId: Object.keys(slots).length });
});

// 3. Analytics
app.get('/reports/utilization', (req, res) => {
  const report = usageData[req.query.month] || {};
  res.json(report);
});

app.listen(7000, () => console.log('HMS-SVC running on port 7000'));
```

Explanation:  
- We use three simple in-memory objects instead of real databases.  
- Each route handles its own domain logic, reads or writes its own store, and returns a minimal JSON response.  
- In production you’d swap these stores for real databases or analytics engines.

---

## 6. Summary & Next Steps

In this chapter, you learned how **Backend Services (HMS-SVC)**:

- Encapsulate core business logic and data processing  
- Own their own data stores and API contracts  
- Are called by higher layers ([API Gateway](13_backend_api_layer__hms_api___hms_mkt__.md), [Interface Layer](01_interface_layer_.md))  
- Can scale and evolve independently  

Up next, we’ll explore how to expose these services securely to other teams and portals in [Chapter 13: Backend API Layer (HMS-API / HMS-MKT)](13_backend_api_layer__hms_api___hms_mkt__.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)