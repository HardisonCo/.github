# Chapter 3: Collaboration Interface (Agent Dial-Tone)

```markdown
_file: 03_collaboration_interface__agent_dial_tone__.md_

[← Back to Chapter 2: Human-in-the-Loop (HITL)](02_human_in_the_loop_hitl_decision_maker_engagement_.md)

---

> “Carol approved the OpenAI key, but the **LLM-Dispatcher** still can’t see it—  
> they’re speaking different JSON dialects!”  
> — NSF DevOps stand-up, day 4

The key is now safely stored (thanks, Chapter 2).  
Next obstacle in our **system-functionality** saga:  
*how do the dozens of HMS agents—dispatchers, vaults, auditors—talk to each other without
format fights, mismatched fields, or silent errors?*

Enter the **Collaboration Interface (CI)**, affectionately nick-named the **Agent Dial-Tone**.

Think of it as the federal phone standard for software agents:  
pick up, hear the dial-tone, dial an extension, and you’re guaranteed the same
language every time.

---

## 1. Why NSF Needs a Dial-Tone—Concrete Example

Target Use Case Flow (summarised):

1. Analyst presses **Generate Research Summary**.  
2. LLM-Dispatcher looks for `openai_primary` key.  
3. No key found → **creates a provisioning request**.  
4. `_ref` reviewers approve (Chapter 2).  
5. Key Vault writes the secret.  
6. **LLM-Dispatcher must now be notified** so it can retry the call.

Steps 3 → 5 → 6 involve **three different agents**.  
Without a common envelope:

* The Key Vault might send `{ "keyName": … }`  
* The Dispatcher expects `{ "name": … }`  
* Logs would explode with silent 400s, the analyst still sees  
  “Unable to generate content from LLM.”

A single 8-field envelope fixes all of that.

---

## 2. The Eight-Field Envelope (Beginner View)

| Field        | What it Does in Our Use Case                          |
|--------------|-------------------------------------------------------|
| `id`         | Trace the entire “where’s my key?” journey            |
| `source`     | Who’s calling (e.g., `key-vault`)                     |
| `target`     | Who should act (e.g., `llm-dispatcher`)               |
| `action`     | Verb, e.g., `key_ready`, `rotate_key`, `call_llm`     |
| `payload`    | The meat—key meta or LLM prompt                       |
| `cort`       | Optional link to **CoRT** thought chain               |
| `timestamp`  | ISO-8601 for audits                                   |
| `status`*    | (`success`, `error`, `conflict`) in **responses**     |

*Requests* carry the first seven fields, *responses* reuse `id` and add `status`.

---

## 3. How to Use the Dial-Tone  
*(Key-Ready Notification Example)*

Below is everything the **Key Vault agent** does once Carol hits “Approve”.

```python
# key_vault/notify.py   (≤ 18 lines)
from ci.call import call_agent   # helper from the CI library

def tell_dispatcher_key_is_ready(key_name):
    call_agent(
        target="llm-dispatcher",
        action="key_ready",
        payload={"key": key_name}  # no custom fields outside "payload"!
    )

# Carol approved "openai_primary"; notify immediately
tell_dispatcher_key_is_ready("openai_primary")
```

What goes in:

* `"llm-dispatcher"` — registered agent name  
* `"key_ready"`      — shared verb both sides understand  
* `{"key": "openai_primary"}` — tiny, self-describing payload

What comes out (inside the helper):

* A JSON file/HTTP message matching the 8-field spec.  
* Automatic schema validation—rejects anything off-spec before it is sent.

Result: the Dispatcher instantly knows the key is live and retries the analyst’s prompt … no more angry error banner.

---

## 4. Internal Mechanics for This Call

```mermaid
sequenceDiagram
    participant VAULT as Key Vault Agent
    participant CI as Collaboration Interface
    participant DIS as LLM-Dispatcher
    participant LOG as HMS-API Logs

    VAULT->>CI: build 8-field envelope (action=key_ready)
    CI->>DIS: deliver envelope
    DIS-->>CI: 200 OK {"status":"success"}
    CI->>LOG: append to audit log
```

1. **Envelope Build** – `ci.call` creates and validates JSON.  
2. **Delivery** – CI routes by `target`. Channel can be file, SQS, HTTP—shape identical.  
3. **Response** – Dispatcher replies with the same `id`, `status="success"`.  
4. **Logging** – HMS-API stores both request & response for IG audits.

---

## 5. Under-the-Hood Snippets

### 5.1 Envelope Builder (simplified, 11 lines)

```python
# ci/envelope.py
import uuid, time
def build(src, tgt, action, payload):
    return {
        "id": str(uuid.uuid4()),
        "source": src,
        "target": tgt,
        "action": action,
        "payload": payload,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
```

### 5.2 Universal Validator (7 lines)

```python
# ci/validate.py
import jsonschema, json
SCHEMA = json.load(open("ci/envelope_schema.json"))
def ok(msg):
    try: jsonschema.validate(msg, SCHEMA); return True
    except jsonschema.ValidationError: return False
```

Both helpers are < 20 lines yet guarantee every agent speaks the same language.

---

## 6. Where the Dial-Tone Touches the HMS Map

Component | Interaction Path in Our Use Case
----------|----------------------------------
[Three-Layer Architecture](01_three_layer_architecture_governance_management_interface_.md) | CI messages travel **between** Management (`llm-dispatcher`) and Interface (web UI) layers.
[HITL Cockpit](02_human_in_the_loop_hitl_decision_maker_engagement_.md) | `_ref` emits `key_approved` using the same envelope.
[Backend API (“Heart”)](05_backend_api_heart_communication_hub_.md) | Stores every envelope in its event log for audit & replay.
[Real-Time Sync](06_real_time_synchronization_event_broadcast_.md) | Uses the envelope as the *payload* on WebSockets/Kafka.
[Zero-Trust Security](12_zero_trust_security_model_.md) | CI signs each envelope, then ZT verifies the signature before routing.

---

## 7. Analogy Corner

Picture the **old red desk phone** in every NSF office:

1. Pick it up—*dial-tone* means the line is alive.  
2. Dial a 4-digit extension—routing.  
3. Speak English—shared language.  
4. Hang up—both sides know the call ended cleanly.

CI gives every HMS agent its own extension and guarantees the same “English” JSON dialect.

---

## 8. FAQ Quick Hits

**Q:** Is this overkill for just passing one key-ready event?  
**A:** Today it’s one event; tomorrow 50 agents will coordinate models,
budgets, ethics flags, and dataset lineage. Standardising now prevents chaos later.

**Q:** Can humans read these envelopes?  
**A:** Yes—flat JSON, 8 fields. Auditors love it.

**Q:** What about large payloads like PDFs?  
**A:** Stick to ≤ 256 KB. Send a signed S3/GCS URL in `payload` for anything bigger.

---

## 9. Key Takeaways

1. Without a common envelope, the approved key would *still* never reach the LLM-Dispatcher—system functionality remains broken.  
2. The **Collaboration Interface** supplies that missing dial-tone: same 8 fields, same verbs, same error semantics.  
3. Less than 20 lines of helper code lets any HMS agent call any other, audit-ready.

---

### Up Next → Chapter 4

Now that agents can call each other, let’s see how a **single AI Representative Agent** will talk to humans on behalf of the whole system—handling prompts, clarifications, and even small-talk.

[Continue to Chapter 4: AI Representative Agent](04_ai_representative_agent_.md)

---
```

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)