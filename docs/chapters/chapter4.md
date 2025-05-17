# Chapter 4: AI Representative Agents

> “Great, the OpenAI key was approved and broadcast—but who actually **uses** it so my ‘Generate Research Summary’ button stops flashing red?”
>
> > AG: ask_llm(prompt, user_id)


    AG -> > CI: (needs_key)                 %% 1 request envelope


    CI -> > VAULT: fetch(openai_primary)


    VAULT --> > CI: key_encrypted


    CI --> > AG: key_decrypted


    AG -> > LLM: prompt + key


    LLM --> > AG: draft_text


    AG --> > UI: stream draft_html


    AG -> > LOG: write {tokens, cost, model}


```text


> ## 1. Introduction: The Challenge of AI Representative Agents






```text
## Chapter 4: AI Representative Agent  


[← Back to Chapter&nbsp;3: Collaboration Interface (Agent Dial-Tone)](03_collaboration_interface_agent_dial_tone_.md)

---

> “Great, the OpenAI key was approved and broadcast—but who actually **uses** it so my ‘Generate Research Summary’ button stops flashing red?”  
> — NSF program officer, day 6 of pilot



That final mile—from *key now available* to *draft text on screen*—is the exact slice of **system functionality** the **AI Representative Agent** covers.  
Think of it as a tireless junior analyst who:

1. Hears that a new credential is ready.  
2. Grabs the key securely.  
3. Calls the outside LLM.  
4. Hands the answer back to the analyst, fully logged and policy-compliant.

Without this agent, NSF would still be stuck at the dreaded:

```text


Unable to generate content from LLM.
Please provide API keys …



```text

---

## 2. Key Concepts: Understanding AI Representative Agents

### Representative Agents

The Representative Agents provides essential functionality in the HMS ecosystem.

## 3. Technical Implementation: Building AI Representative Agents

This section provides a detailed technical implementation guide for the AI Representative Agents component:

```markdown


## Chapter 4: AI Representative Agent  


[← Back to Chapter&nbsp;3: Collaboration Interface (Agent Dial-Tone)](03_collaboration_interface_agent_dial_tone_.md)

---

> “Great, the OpenAI key was approved and broadcast—but who actually **uses** it so my ‘Generate Research Summary’ button stops flashing red?”  
> — NSF program officer, day 6 of pilot



That final mile—from *key now available* to *draft text on screen*—is the exact slice of **system functionality** the **AI Representative Agent** covers.  
Think of it as a tireless junior analyst who:

1. Hears that a new credential is ready.  
2. Grabs the key securely.  
3. Calls the outside LLM.  
4. Hands the answer back to the analyst, fully logged and policy-compliant.

Without this agent, NSF would still be stuck at the dreaded:



```text

```text


---

## 1. Key Concepts (What the Agent Actually Does)

| Piece | Role in the NSF flow | 1-Sentence Analogy |
|-------|----------------------|--------------------|
| Event Listener | Subscribes to `KeyReady` messages on the HMS event bus. | Doorbell that only rings when a key is activated. |
| Credential Fetcher | Pulls the fresh key from the Vault, never writes it to disk. | Unlocks a safety-deposit box, copies nothing. |
| LLM Invoker | Sends the program officer’s prompt + key to GPT / Claude / Gemini. | Places a phone call to an outside expert. |
| Response Router | Streams the LLM answer back through WebSocket to the UI. | Slides the finished memo under the office door. |
| Token Logger | Records usage so Governance can cap budget. | Time-clock punch for auditors. |

---

## 2. How Do I Use It? – NSF One-Click Example

Once the key is approved (Chapter 2) and the dial-tone is live (Chapter 3), an NSF analyst needs only these few lines:



```text

```text


Input: a plain English prompt.  
Output: HTML draft—no key handling, no rate-limit headaches.

---

## 3. Internal Flow in the Target Use Case



```text

```text


What this diagram shows in plain words:

1. **Needs Key** – Agent asks via the dial-tone; Vault responds.  
2. **Single Use** – Key lives only in memory for one API call.  
3. **Answer Delivered** – Draft flows back to the browser; usage flows to logs for auditors.

---

## 4. Mini Code Walk-Through (< 20 Lines Total)



```text

```text


Follow the emoji comments:

1️⃣ Secure key retrieval → 2️⃣ LLM call → 3️⃣ Usage log.  
Notice: no local file writes, no long-lived tokens—fully compliant with NSF security rules.

---

## 5. Where It Touches Other HMS Components

Component | Interaction in this Chapter
----------|----------------------------
[Three-Layer Architecture](01_three_layer_architecture_governance_management_interface_.md) | Agent sits in the **Management** layer, translating Governance rules into real calls.
[HITL Cockpit](02_human_in_the_loop_hitl_decision_maker_engagement_.md) | Only fires after reviewers approve or rotate keys.
[Collaboration Interface](03_collaboration_interface_agent_dial_tone_.md) | Provides the envelopes (`needs_key`, `llm_response`) the agent sends/receives.
[Backend API (“Heart” / Communication Hub)](05_backend_api_heart_communication_hub_.md) | Stores token logs and exposes them for audits.
[Real-Time Synchronization](06_real_time_synchronization_event_broadcast_.md) | Streams draft_html back to the analyst in milliseconds.
[Zero-Trust Security Model](12_zero_trust_security_model_.md) | Ensures the decrypted key never leaves a trusted enclave.

---

## 6. Analogy Corner 📨

Picture a **courier in a secure government building**:

1. Security desk (Vault) hands the courier a sealed envelope (API key).  
2. Courier exits, makes a single phone call (LLM request).  
3. Immediately shreds the envelope, writes a note in the logbook (token usage), and hands the message to the requester (draft summary).  

Fast, logged, and nothing sensitive lingers.

---

## 7. Summary & Transition

The **AI Representative Agent** closes the loop that started with “missing API key,” transforming an approved credential into the actual research summary NSF staff asked for—thus restoring full **system functionality**.

Ready to see where all these messages live and how they stay queryable months later?  
Head to [Chapter 5: Backend API (“Heart” / Communication Hub)](05_backend_api_heart_communication_hub_.md).

---



```text

## 4. Hands-On Example: Using AI Representative Agents

Once the key is approved (Chapter 2) and the dial-tone is live (Chapter 3), an NSF analyst needs only these few lines:

```python


## analyst_portal_call.py   (≤ 16 lines)
from hms_agents.llm_client import ask_llm   # wrapper around the AI Rep Agent

def make_summary(question, user):
    return ask_llm(
        prompt = f"Generate a 300-word research summary:\n\n{question}",
        user_id = user.id           # used for quota & logging
    )

draft_html = make_summary("quantum networking grants, 2022-2024")
print(draft_html)                  # → formatted summary ready to paste


```text

Input: a plain English prompt.  
Output: HTML draft—no key handling, no rate-limit headaches.

---

```mermaid




```text
```text

mermaid
sequenceDiagram
    participant UI   as Analyst UI (HMS-GOV)
    participant AG   as AI Representative Agent
    participant CI   as Collaboration Interface
    participant VAULT as Secure Vault
    participant LLM  as External LLM (OpenAI / Claude / Gemini)
    participant LOG  as HMS-API Logs


```text
```text




    UI -> > AG: ask_llm(prompt, user_id)


    AG -> > CI: (needs_key)                 %% 1 request envelope


    CI -> > VAULT: fetch(openai_primary)


    VAULT --> > CI: key_encrypted


    CI --> > AG: key_decrypted


    AG -> > LLM: prompt + key


    LLM --> > AG: draft_text


    AG --> > UI: stream draft_html


    AG -> > LOG: write {tokens, cost, model}



## 5. Connection to Other Components

Component | Interaction in this Chapter
----------|----------------------------
[Three-Layer Architecture](01_three_layer_architecture_governance_management_interface_.md) | Agent sits in the **Management** layer, translating Governance rules into real calls.
[HITL Cockpit](02_human_in_the_loop_hitl_decision_maker_engagement_.md) | Only fires after reviewers approve or rotate keys.
[Collaboration Interface](03_collaboration_interface_agent_dial_tone_.md) | Provides the envelopes (`needs_key`, `llm_response`) the agent sends/receives.
[Backend API (“Heart” / Communication Hub)](05_backend_api_heart_communication_hub_.md) | Stores token logs and exposes them for audits.
[Real-Time Synchronization](06_real_time_synchronization_event_broadcast_.md) | Streams draft_html back to the analyst in milliseconds.
[Zero-Trust Security Model](12_zero_trust_security_model_.md) | Ensures the decrypted key never leaves a trusted enclave.

---

## 6. Summary and Next Steps

### 7. Summary & Transition

The **AI Representative Agent** closes the loop that started with “missing API key,” transforming an approved credential into the actual research summary NSF staff asked for—thus restoring full **system functionality**.

Ready to see where all these messages live and how they stay queryable months later?  
Head to [Chapter 5: Backend API (“Heart” / Communication Hub)](05_backend_api_heart_communication_hub_.md).

---


```text

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)

### What's Next?

In the next chapter, we'll explore Backend API: The Heart of Communication, examining how it:

- API Design
- Communication Hub
- Service Architecture

## 7. Exercises for the Reader

1. **Design Exercise:** Sketch a implementation of AI Representative Agents for a specific healthcare scenario.

2. **Implementation Exercise:** Create a simple prototype that demonstrates the key principles of AI Representative Agents.

3. **Analysis Exercise:** Review an existing system and identify how it could benefit from implementing AI Representative Agents.

4. **Integration Exercise:** Design how this component would connect with other HMS components in a real-world application.

5. **Challenge Exercise:** How would you extend this component to address a complex healthcare challenge like pandemic response or chronic disease management?

---

In Chapter 5, we'll dive into Backend API: The Heart of Communication and see how it a detailed look at the hms backend api architecture that serves as the central communication hub for all system components..
```text




```text
```text

