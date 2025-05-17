# Chapter 12: Zero-Trust Security Model

```markdown
# Chapter 12: Zero-Trust Security Model  
_file: 12_zero_trust_security_model_.md_

[← Back to Chapter&nbsp;11: Stakeholder Access Model (Five Wristbands)](11_stakeholder_access_model_five_wristbands_.md)

---

> “The **Admin** wristband let me upload the OpenAI key last night,  
> but how do I know every micro-service that touches it is really *itself* and
> not a compromised pod?”  
> — NSF Security Engineer, launch-day checklist

The OpenAI key is now approved, stored, and visible to the right roles.  
Yet a single poisoned container—or an insider riding on a forgotten VPN—could
still call the key-storage API and exfiltrate credentials, dragging us *back* to

```
Unable to generate content from LLM.
Please provide API keys …
```

Zero-Trust Security Model (“never trust, always verify”) is `_ref`’s final
shield against exactly that disaster.  
Every HTTP call and inter-service hop—yes, even *inside* the NSF data center—is
forced to prove identity, privilege, encryption, and auditability.  
No proof → no key → no LLM call.  
Result: system functionality *and* federal compliance stay intact.

---

## 1. Motivation — Closing the Last Security Gap

Concrete NSF flow with the new key in place:

1. Analyst (`Verified`) presses **Generate Research Summary**.  
2. Browser calls `POST /ai/summary`.  
3. HMS-API must fetch `openai_primary` from the Vault.  
4. Vault must *re-verify* HMS-API’s identity *right now* (not just at pod
   start-up) before handing over the key.

Without Zero-Trust, step 4 might silently succeed for a hijacked container.
With Zero-Trust, the Vault challenges HMS-API on every request; any mismatch
kills the call, and the key stays safe.

---

## 2. Six Pillars in Plain English

| Pillar                 | One-line Explanation | Why NSF Cares for the LLM Key |
|------------------------|----------------------|--------------------------------|
| Strong Identity        | Mutual TLS + JWT on **every** hop | Stops impostor services grabbing the key |
| Least Privilege        | Scoped tokens (`ai:key:read`) | Even HMS-API can’t list *all* keys, only the one it needs |
| Micro-Segmentation     | Per-service network policies | Compromise of `stats-worker` can’t reach the Vault |
| Continuous Verification| Re-auth every request | Long-lived stolen JWTs become useless |
| End-to-End Encryption  | mTLS / TLS 1.3 | Keys & prompts unreadable in transit |
| Immutable Audit Logs   | Append-only, 7 yrs | GAO can replay *every* key access |

Keep these pillars handy; the code & diagrams below implement them.

---

## 3. How to Use It — The `secure_call()` Wrapper

The easiest way for beginners to tap Zero-Trust is a **one-liner**:

```python
from hms_security import secure_call   # < 20 lines in src

html = secure_call(                    # 🛡️ Zero-Trust in action
    target   = "hms-api/ai/summary",
    method   = "POST",
    payload  = {"prompt": "Summarize quantum networking grants."},
    scope    = "ai:invoke-summary"     # least-privilege scope
)
print(html)                            # 300-word draft
```

Input  
• `target`  – internal URL that will, behind the scenes, need the OpenAI key.  
• `scope`   – minimal permission string tied to the caller’s wristband.

Output  
• Sanitised HTML summary **or** a detailed `AccessDenied` error explaining
  which Zero-Trust pillar failed.

### Under the hood (condensed)

1. Builds a short-lived JWT with the requested `scope`.  
2. Opens an mTLS channel to the ZT Gateway.  
3. Gateway re-verifies the token *and* network policy.  
4. Call is forwarded to HMS-API only if all six pillars pass.

---

## 4. Internal Flow for the Target Use Case

```mermaid
sequenceDiagram
    actor Analyst
    participant UI   as Browser
    participant GW   as ZT Gateway
    participant AU   as Auth Service
    participant PO   as Policy Engine
    participant API  as HMS-API
    participant VAULT as Key Vault
    participant LLM  as OpenAI
    UI->>GW: mTLS + JWT (ai:invoke-summary)
    GW->>AU: validate token & cert
    AU-->>GW: ok
    GW->>PO: check scope policy
    PO-->>GW: allow
    GW->>API: forward request (mTLS)
    API->>VAULT: mTLS + JWT (ai:key:read openai_primary)
    VAULT->>AU: re-auth token
    AU-->>VAULT: ok
    VAULT-->>API: key
    API->>LLM: external HTTPS
    LLM-->>API: draft
    API-->>GW: html
    GW-->>UI: html
```

One failed check (red arrow) returns
`403 AccessDenied: pillar <name> failed`, never leaking the key.

---

## 5. Minimal Code Peeks (All ≤ 20 Lines)

### 5.1 secure_call() Helper

```python
# hms_security/secure_call.py
import jwt, httpx, ssl, time, os
def secure_call(target, method, payload, scope):
    token = jwt.encode({
        "sub":  os.getenv("USER_ID"),
        "role": os.getenv("ROLE"),
        "scope": scope,
        "exp": time.time() + 60    # 1-min TTL
    }, os.getenv("JWT_KEY"), algorithm="HS256")

    ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    ctx.load_cert_chain("client.crt","client.key")  # mTLS

    with httpx.Client(verify=ctx) as c:
        r = c.request(method, f"https://{target}",
                      headers={"Authorization": f"Bearer {token}"},
                      json=payload, timeout=25)
        r.raise_for_status()
        return r.text
```

### 5.2 Gateway Guard (excerpt)

```python
# gateway/guard.py
def guard(req):
    cert = req.client_cert
    token = auth.parse_jwt(req.headers["Authorization"])
    if not auth.valid(cert, token):
        raise AccessDenied("identity")
    if not policy.allowed(token["scope"], req.path):
        raise AccessDenied("least-privilege")
    return forward(req)   # only after both green
```

---

## 6. Where Zero-Trust Touches Other HMS Components

Component | Interaction for the “OpenAI key” Flow
----------|---------------------------------------
[Stakeholder Access Model](11_stakeholder_access_model_five_wristbands_.md) | Wristband role becomes the `role` claim inside the short-lived JWT.
[Backend API (“Heart”)](05_backend_api_heart_communication_hub_.md) | Reads keys *only* when the ZT Gateway has stamped the request.
[Real-Time Sync](06_real_time_synchronization_event_broadcast_.md) | Bus drops any envelope whose mTLS session or JWT fails ZT checks.
[AI Governance Framework](09_ai_governance_framework_.md) | Governance rules feed the Policy Engine (`budget ≤ $50/day`, etc.).
[Component Agent](10_component_agent_.md) | Sidecar containers inherit the same `secure_call()` wrapper to fetch policies & keys.

---

## 7. Analogy Corner 🔐

Imagine NSF’s HQ as a **museum with laser tripwires**:

1. Every door badge proves *who you are* (identity).  
2. Each room unlocks only for curators who need it (least privilege).  
3. Lasers segment each gallery; crossing the wrong one triggers alarms
   (micro-segmentation).  
4. Guards scan badges *again* inside sensitive rooms (continuous verification).  
5. Thick walls muffle all conversations (encryption).  
6. Cameras film every step (audit logs).

Zero-Trust gives HMS those lasers—no skeleton keys, no dark corridors.

---

## 8. Quick FAQ

| Q | A |
|---|---|
| “Can I turn off mTLS in dev?” | Yes: set `ZT_OFF=true`, but CI & prod always force it. |
| “Does this slow down LLM calls?” | Median overhead ≈ 30 ms; far smaller than model latency itself. |
| “Where are audit logs stored?” | Append-only `zt_audit` table in HMS-API (7-year retention). |

---

## 9. Summary & Transition

Zero-Trust finishes the security puzzle:

1. Every hop—browser to Vault—re-authenticates and encrypts.  
2. Only the **exact** services allowed to see `openai_primary` ever touch it.  
3. NSF can now flip the “Generate Research Summary” button **on** with high
   confidence that neither insider mistakes nor external attackers will leak
   the key or the data.

With the perimeter locked, Chapter 13 shows how the same Zero-Trust rails power
the **Data Access API (Clean-Data Vending Machine)** so analysts can safely pull
datasets that fuel their new LLM workflows.

[Continue to Chapter&nbsp;13: Data Access API (Clean-Data Vending Machine)](13_data_access_api_clean_data_vending_machine_.md)
```

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)