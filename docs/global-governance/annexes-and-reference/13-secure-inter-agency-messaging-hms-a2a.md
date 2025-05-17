# Chapter 13: Secure Inter-Agency Messaging (HMS-A2A)

*(arriving from [External System Synchronization (HMS-GOV Connectors)](12_external_system_synchronization__hms_gov_connectors__.md))*  

---

> “When one agency whispers a secret to another, **HMS-A2A** is the sound-proof tunnel.”

---

## 1. Why do we need an encrypted tunnel between agencies?

Concrete story – “Census-to-Energy Data Pull”  

1. The **National Renewable Energy Laboratory (NREL)** needs the latest *county-level population* numbers to model solar demand.  
2. Raw data lives inside the **Census Bureau** silo and is restricted by Title 13 privacy rules.  
3. Email attachments are out (too risky), and the APIs speak different dialects.  
4. NREL clicks **“Request Dataset”**.  
5. **HMS-A2A** negotiates encryption keys, maps the two payload formats, and streams the files—no one sees plain text.

Without HMS-A2A, engineers would juggle SFTP credentials, VPNs, and legal nightmares.

---

## 2. Five key concepts (in plain English)

| Word            | Everyday Analogy                | Meaning in HMS-A2A                                |
|-----------------|---------------------------------|---------------------------------------------------|
| Tunnel          | Armored courier bag             | End-to-end TLS + mutual authentication channel    |
| Envelope        | Sealed inner letter             | JSON wrapper that carries the actual payload      |
| Adapter         | Pocket translator               | Code that converts “Census CSV” ↔ “Energy JSON”   |
| Key Exchange    | Secret handshake                | One-time asymmetric key swap per session          |
| Audit Pin       | Tamper-proof wax seal           | SHA-256 hash stored in the ledger for later proof |

Keep these five nouns in mind—everything else is piping.

---

## 3. Quick tour – pulling Census data in **2 minutes**

```mermaid
sequenceDiagram
    participant NREL as NREL App
    participant G1  as A2A Gateway (NREL)
    participant Wire as Encrypted Tunnel
    participant G2  as A2A Gateway (Census)
    participant CEN as Census API

    NREL->>G1: request "county_pop_2024"
    G1->>G2: Envelope + Key₁
    G2->>CEN: fetch & adapt
    CEN-->>G2: CSV rows
    G2-->>G1: Envelope (JSON) + Audit Pin
    NREL<<--G1: clean JSON data
```

Five actors—easy to trace and test.

---

## 4. Using HMS-A2A from your service (only 15 lines)

```js
// nrelClient.js
import { send } from '@hms-gov/a2a'

export async function getPopulation() {
  const env = await send({
    to      : 'census.gateway',          // remote gateway id
    purpose : 'county_pop_2024',
    payload : {}                         // no args needed
  })
  return env.payload                     // ← JSON array
}

// anywhere in code
const pop = await getPopulation()
console.log(pop[0]) // { county:"Jefferson CO", pop: 582112 }
```

Explanation  
1. `send()` wraps your request in an **Envelope**.  
2. The SDK handles key exchange & TLS automatically.  
3. You receive a *ready-to-use JSON* list—no CSV wrangling.

---

## 5. What’s inside an Envelope?

```json
{
  "id": "env-7cfa",
  "from": "nrel.gateway",
  "to": "census.gateway",
  "purpose": "county_pop_2024",
  "payload": { /* encrypted body, Base64 */ },
  "auditPin": "sha256:9e7bf…",
  "timestamp": "2025-05-01T14:22:01Z"
}
```

• Only `from`, `to`, `purpose`, and `auditPin` are visible; `payload` is AES-GCM encrypted with the session key.

---

## 6. Writing a tiny **Adapter** (≤18 lines)

Census sends CSV; NREL wants JSON.

```python
# adapters/csv_to_json.py
import csv, io, json

def adapt(raw_bytes):
    text = raw_bytes.decode('utf-8')
    rows = list(csv.DictReader(io.StringIO(text)))
    return json.dumps(rows)     # ready for NREL
```

Drop the file in the Census gateway’s `adapters/` folder.  
Gateways auto-discover adapters by filename: `purpose → adapter`.

---

## 7. Inside the Gateway – 20-line handler

```js
// gateway/handler.js
import { decrypt, encrypt } from './crypto.js'
import { adapt } from './adapters/csv_to_json.js'
import { ledger } from './audit.js'

export async function handle(env) {
  const req = JSON.parse(decrypt(env.payload))
  const csv = await censusApi.download(req.purpose)

  const json = adapt(csv)
  const outEnv = { ...flip(env), payload: encrypt(json) }

  outEnv.auditPin = sha256(json)
  await ledger.record(outEnv)   // immutably store id + pin
  return outEnv
}

function flip(e){ return { from:e.to, to:e.from, purpose:e.purpose } }
```

Line-by-line  
1–2  Import helpers.  
5   Decrypt incoming args (none in this case).  
6   Call internal Census API.  
8   Run adapter to JSON.  
9-11 Create return Envelope, encrypt payload, add Audit Pin.  
12   Store a tamper-proof line in the audit DB.  
14   Send it back through the tunnel.

---

## 8. How key exchange works (code-light)

1. Sender looks up the **public key** of the receiver in the **Government PKI Directory**.  
2. Generates a random session key `K`.  
3. Encrypts `K` with receiver’s public key → `E(K)`.  
4. Places `E(K)` in the TLS header; only the receiver can decrypt.  
5. All envelope payloads in that session are AES-GCM with `K`.

No code required for beginners—the SDK (`@hms-gov/a2a`) hides it.

---

## 9. Health & monitoring

* Every gateway emits **heartbeat** events to [Outcome Metrics & Monitoring](15_outcome_metrics___monitoring__hms_ops___hms_act__.md).  
* Missing 3 heartbeats → raises `TunnelDown` alert → routed to [HITL Override](11_human_in_the_loop__hitl__override_.md).  
* Audit Pins allow investigators to verify any envelope’s integrity years later.

---

## 10. FAQ

| Question | Answer |
|----------|--------|
| “Can I send big files?” | Yes—payloads > 10 MB are auto-uploaded to S3, and the envelope carries a presigned URL. |
| “What if formats already match?” | Provide `adapters/identity.js` that just returns the bytes. |
| “Multiple tunnels?” | The SDK multiplexes many logical tunnels over one HTTPS/2 connection. |
| “Is this FedRAMP compliant?” | HMS-A2A uses FIPS-140-2 validated crypto; you still need an ATO per agency. |

---

## 11. Recap & what’s next

You learned:  

✓ Why HMS-A2A is the armored courier for sensitive, cross-agency data.  
✓ Five core ideas: Tunnel, Envelope, Adapter, Key Exchange, Audit Pin.  
✓ How to request data with a **one-line** `send()` call.  
✓ How adapters translate formats in ≤ 18 lines of code.  
✓ How gateways log tamper-proof Audit Pins for compliance.

Data is flowing safely—now we must guarantee it is kept, shared, or deleted **according to law**.  
Time to meet the watchdog of privacy:  
[Data Stewardship & Privacy Layer (HMS-DTA)](14_data_stewardship___privacy_layer__hms_dta__.md)

---

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)