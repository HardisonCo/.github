# Chapter 5: Access & Identity Management
*[Link back to Chapter&nbsp;4: Security & Compliance Framework](04_security___compliance_framework_.md)*  

---

## 1. Why Do We Need Yet *Another* Layer?

Central use-case (2 sentences)  
• A **county clerk** in Wyoming wants to *view* a citizen’s marriage license.  
• A **federal Inspector General (IG)** wants to *export* every license issued in the last 10 years.  
Both people have valid government IDs, but **only one** may see bulk historical data.  
Access & Identity Management (AIM) makes sure the clerk stays in her lane while the IG gets the data he’s cleared for—no more, no less.

---

## 2. Key Concepts (Plain-English Cheat-Sheet)

| Concept | “Government Office” Analogy | TL;DR |
|---------|-----------------------------|-------|
| Identity Provider (IdP) | GSA’s **Login.gov** booth | Authenticates who you are |
| SSO (Single Sign-On) | One badge opens all doors | Re-use one login across HMS |
| MFA (Multi-Factor Auth) | Badge **+** PIN | Stops stolen passwords |
| RBAC (Role-Based Access) | GS-13 vs GS-5 pay grades | Access tied to job title |
| ABAC (Attribute-Based) | “*Top-Secret*” clearance | Access tied to data labels & user tags |
| PDP / PEP | Judge & Bailiff | PDP decides, PEP enforces |

> Keep this table handy—95 % of AIM is just these six ideas!

---

## 3. 3-Minute Walk-Through

### Scenario: Updating a SNAP Case

1. **Social Worker (GS-9, State of MD)** logs in through Login.gov (SSO + MFA).  
2. She tries to **PATCH** `/snap/case/123` via the HMS API.  
3. The HMS **Policy Enforcement Point (PEP)** forwards her JWT to the **Policy Decision Point (PDP)**.  
4. PDP checks:  
   - Role = `STATE_SNAP_WORKER` (RBAC) ✅  
   - User’s `county` attribute = `Baltimore` **matches** case file county ✅  
5. PDP returns `PERMIT`; the API call proceeds.  
6. A contractor with the same role **but** `clearance=Contractor-Limited` gets `DENY`.

Outcome: correct, fine-grained access in under 100 ms.

---

## 4. Hands-On: Your First “Permit or Deny”

We’ll fake an IdP so you can try this on localhost.

### 4.1 Get a JWT (≤ 10 lines)

```bash
# pretend "hms-idp" is our Identity Provider
TOKEN=$(curl -sX POST https://hms-idp.local/token \
  -d 'user=alice&role=STATE_SNAP_WORKER&county=Baltimore' )

echo $TOKEN   # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4.2 Call the Protected API (≤ 15 lines)

```bash
curl -s https://hms-api.local/snap/case/123 \
  -H "Authorization: Bearer $TOKEN" \
  | jq .
```

Expected output:

```json
{
  "status": "PERMIT",
  "message": "Case updated",
  "by": "alice"
}
```

Change `county=Montgomery` in step 4.1 and run again—you should see:

```json
{
  "status": "DENY",
  "reason": "County mismatch"
}
```

That’s AIM in action!

---

## 5. Under the Hood (Step-By-Step)

```mermaid
sequenceDiagram
  participant User
  participant IdP as Identity<br>Provider
  participant API as Backend<br>PEP
  participant PDP
  participant DB as Data&nbsp;API

  User->>IdP: username + MFA
  IdP-->>User: JWT
  User->>API: PATCH /snap (JWT)
  API->>PDP: evaluate(JWT, resource, action)
  PDP-->>API: PERMIT / DENY
  API-->>DB: do work (if PERMIT)
```

Only **5 hops**, all stateless = scalable.

---

## 6. A Peek at the Code (All ≤ 20 Lines!)

### 6.1 PEP Middleware — `pep.py`

```python
# super-tiny FastAPI middleware
from fastapi import Request, HTTPException
import requests, os, jwt

PDP_URL = os.getenv("PDP_URL", "http://pdp:8080/eval")

async def pep(request: Request, call_next):
    token = request.headers.get("authorization", "").split()[-1]
    payload = jwt.decode(token, options={"verify_signature": False})
    query = {"sub": payload, "res": str(request.url), "act": request.method}
    verdict = requests.post(PDP_URL, json=query, timeout=0.05).json()
    if verdict["decision"] != "PERMIT":
        raise HTTPException(403, verdict["reason"])
    return await call_next(request)
```

**Explanation**  
1. Grab JWT from header.  
2. Ask PDP if the action is ok.  
3. Block request on `DENY`.

### 6.2 PDP Rule Engine — `rules.yaml`

```yaml
# RBAC mapping
roles:
  STATE_SNAP_WORKER:
    can:
      - ["PATCH", "/snap/case/*"]
# ABAC condition (Python-ish)
conditions:
  county_match: "sub.county == res.metadata.county"
policies:
  - when: "role == STATE_SNAP_WORKER and county_match"
    effect: PERMIT
  - effect: DENY
```

Lightweight, human-readable—perfect for auditors.

### 6.3 PDP Evaluator — `pdp.py` (≤ 18 lines)

```python
import yaml, jwt, ast

RULES = yaml.safe_load(open("rules.yaml"))

def eval_req(sub, res, act):
    role = sub["role"]
    ctx = {"sub": sub, "res": res, "role": role}  # exec context
    for rule in RULES["policies"]:
        if "when" in rule and not eval(rule["when"], {}, ctx):
            continue
        if act in RULES["roles"].get(role, {}).get("can", []):
            return {"decision": rule["effect"]}
    return {"decision": "DENY", "reason": "No matching rule"}
```

**Explanation**  
1. Load `rules.yaml` once at startup.  
2. For each request, test conditions with `eval` (yes, keep it sandboxed in real life!).  
3. Return first `PERMIT`; otherwise `DENY`.

---

## 7. How AIM Talks to Other Layers

• **Upstream**:  
  – Policies must be approved in [Governance Layer](01_governance_layer__hms_gov__.md).  
  – Security seals from [Security & Compliance Framework](04_security___compliance_framework_.md) attach to IdP & PDP code.  

• **Sidecar**:  
  – PPE rules (see [Policy & Process Engine](02_policy___process_engine_.md)) can reference roles like `FAA_DISPATCHER`.  

• **Downstream**:  
  – Every call inside [Backend Service Mesh (HMS-API)](07_backend_service_mesh__hms_api__.md) passes through PEP middleware.  
  – Audit events feed into [Observability & Audit Log](11_observability___audit_log_.md).

---

## 8. Common Pitfalls & Quick Fixes

| Oops! | Why it Happens | Quick Fix |
|-------|---------------|-----------|
| “Everything is **DENY**!” | Clock skew; token expired | Use NTP or increase `exp` leeway by ±2 min. |
| Role creep | Old roles never removed | Automate a 90-day role audit job. |
| OTP fatigue | Users hate MFA | Offer FIDO2 keys—fast tap instead of SMS. |

---

## 9. Mini-Lab: Add a New Clearance Level

1. Append to `rules.yaml`:

```yaml
  CONTRACTOR_LIMITED:
    can: []
```

2. Issue a JWT:

```bash
TOKEN=$(curl -sX POST https://hms-idp.local/token \
  -d 'user=bob&role=CONTRACTOR_LIMITED' )
```

3. Call the API—observe `DENY`.  
4. Add a narrow permission:

```yaml
  CONTRACTOR_LIMITED:
    can:
      - ["GET", "/snap/case/*"]
```

5. Reload PDP, retry → now `GET` passes, `PATCH` still fails.  
You just created your first least-privilege role!

---

## 10. What You Learned

✓ The difference between **identity** (who you are) and **access** (what you may do).  
✓ Core tools: SSO, MFA, RBAC, ABAC, PDP/PEP.  
✓ How to grab a JWT, call a protected API, and read a `PERMIT/DENY` verdict.  
✓ Under-the-hood flow & minimal source code.  
✓ How AIM plugs into the larger HMS architecture.

Ready to see how this fits within a **Multi-Layered Microservice Architecture**?  
Jump to [Chapter 6: Multi-Layered Microservice Architecture](06_multi_layered_microservice_architecture_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)