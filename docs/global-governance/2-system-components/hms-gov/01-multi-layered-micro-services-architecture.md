# Chapter 1: Multi-Layered Micro-services Architecture


*Welcome to HMS-GOV!  
Before we dive into writing code, let’s look at the “city plan” that holds everything together.*

---

## 1. Why do we need it? – A Passport-Renewal Story

Imagine Alex, a U.S. citizen, wants to renew her passport online:

1. She visits the public **Passport Portal**.
2. Her browser talks to HMS-GOV’s **API Gateway**.
3. The gateway routes her request to a **Passport Service**.
4. That service checks eligibility, stores data, and triggers a **Payment Service**.
5. Finally, Alex sees **“Application Received”** on the screen—without ever noticing the dozens of tiny services that cooperated behind the scenes.

Without a solid architecture, one slow database or a single buggy feature page could freeze the entire system.  
Our answer is a *multi-layered micro-service mesh* that keeps each concern separate, replaceable, and scalable.

---

## 2. The Three Vertical Layers

```
mermaid
graph TD
    subgraph Storefront Layer
        A[Citizen Portals] -->|UI calls| B(API Gateway)
    end
    subgraph Service Layer
        B --> C[Passport Service]
        B --> D[Payment Service]
    end
    subgraph Infrastructure Layer
        C -.->|reads/writes| E[(Database)]
        D -.-> E
        C -.-> F[(Message Bus)]
        D -.-> F
    end
```

Think of a modern city:

| City Analogy                | HMS-GOV Layer               | Typical Components                                   |
|-----------------------------|-----------------------------|------------------------------------------------------|
| Roads & Power Lines         | **Infrastructure**          | Databases, queues, networking, monitoring            |
| Schools, Hospitals, Banks   | **Service**                 | Passport, Payment, Audit, Notification micro-services|
| Public Offices & Kiosks     | **Storefront**              | Web apps, mobile apps, admin dashboards              |

### 2.1 Infrastructure Layer (“Power & Roads”)
Handles raw compute, storage, and observability:
* Kubernetes clusters  
* Postgres or DynamoDB  
* Prometheus, Grafana  

### 2.2 Service Layer (“The Buildings”)
Small, single-purpose services:
* `passport-svc` – passport logic  
* `payment-svc` – card processing  
* `audit-svc` – compliance logs  

### 2.3 Storefront Layer (“Front Desks”)
Visual touchpoints for humans:
* Citizen portals (React)  
* Admin dashboards (Angular/Vue)  
* Mobile apps  

---

## 3. Key Micro-service Ideas (in Plain English)

| Term              | What it really means for beginners                    |
|-------------------|-------------------------------------------------------|
| **Micro-service** | A tiny program that does *one job* well.              |
| **Service Mesh**  | A smart traffic cop ensuring services find each other.|
| **Stateless**     | Service forgets everything once it replies (storage lives elsewhere).|
| **Scaling Out**   | Run 10 copies of the same service when the queue gets long.|

---

## 4. Let’s Build One Tiny Service

Below is an ultra-small **Passport Service** written in Node.js/Express.

```javascript
// passport-svc/index.js
const express = require("express");
const app = express();
app.use(express.json());

// POST /apply
app.post("/apply", (req, res) => {
  // TODO: validate passport data
  console.log("Received passport application:", req.body);
  // pretend we saved to database
  res.status(202).send({ status: "Application Received" });
});

app.listen(3000, () => console.log("passport-svc up on 3000"));
```

Explanation (for absolute beginners):

1. We import Express – a tiny web-server library.  
2. `app.post("/apply")` reacts to HTTP POST requests.  
3. We log the data and immediately answer with **202 Accepted**.  
4. That’s it! In production, you’d validate, store, and maybe queue a background job.

---

## 5. How Does the Request Travel?

Below is a *sequence diagram* showing the happy-path for Alex’s request:

```
mermaid
sequenceDiagram
    participant Browser
    participant GW as API Gateway
    participant PS as Passport Service
    participant DB as Database
    Browser->>GW: POST /apply
    GW->>PS: /apply JSON
    PS-->>DB: INSERT application
    DB-->>PS: ok
    PS-->>GW: 202 Accepted
    GW-->>Browser: 202 Accepted
```

*Notice:* Each arrow is an isolated hop. If the Passport Service crashes, only that box is restarted—storefronts and other services keep running.

---

## 6. Peeking Under the Hood

When the gateway forwards a request, several invisible helpers jump in:

1. **Service Discovery** – finds a healthy Passport Service pod.  
2. **Circuit Breaker** – if calls start failing, it temporarily blocks them to avoid a cascade.  
3. **Tracing** – tags the request so we can later ask *“Why was Alex’s renewal slow?”*.  

Many teams implement these cross-cutting helpers with a *sidecar* proxy (e.g., Envoy) injected automatically by the platform.

---

## 7. Coding the Glue (simplified)

A bare-bones Kubernetes `Deployment` manifest for our service:

```yaml
# k8s/passport-svc.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: passport-svc
spec:
  replicas: 2               # <— scales horizontally
  selector:
    matchLabels: app: passport-svc
  template:
    metadata:
      labels:
        app: passport-svc
    spec:
      containers:
        - name: passport
          image: hms/passport-svc:latest
          ports:
            - containerPort: 3000
```

Explanation:

• `replicas: 2` means “run two copies.”  
• If traffic spikes, we can bump this to 10 without code changes.  
• Kubernetes (Infrastructure Layer) watches health, restarts on failure, and rolls out updates one pod at a time (zero downtime).

---

## 8. Common Questions Beginners Ask

**Q: Can services talk directly to each other?**  
A: They *can*, but we usually keep them behind the API Gateway to simplify auditing and policy enforcement.

**Q: Where do shared functions like logging live?**  
A: In sidecars or the [Shared Utilities Library](20_shared_utilities_library__hms_utl__.md).

**Q: What if a new agency, e.g., the Nuclear Waste Technical Review Board, needs a specialized calculator?**  
A: Add a new micro-service (`nwtrb-calc-svc`) in the Service Layer. Storefronts call it the same way—no core rewrite required.

---

## 9. What You Learned

• HMS-GOV is organized into Infrastructure, Service, and Storefront layers.  
• Each feature is a micro-service that can scale or fail independently.  
• A service mesh, gateway, and Kubernetes provide traffic control, resilience, and deployments.  
• Even complex government journeys (passport renewals, benefit claims, legislative workflows) are just orchestrations of many tiny services.

Next, we’ll zoom into the heart of that traffic control: the API Gateway.

➡️ Continue to [Backend API Gateway (HMS-SVC / HMS-API)](02_backend_api_gateway__hms_svc___hms_api__.md)

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)