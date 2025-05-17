# Chapter 17: Intent-Driven Navigation & AI-Guided Journeys
*Coming from the previous chapter: [Simulation & Training Environment (HMS-ESR)](16_simulation___training_environment__hms_esr__.md)*  

---

## 1. Why Do Citizens Need a “GPS for Government”?

Imagine Rosa, a new café owner in **Austin, TX**:

> “I just want to open my coffee shop.  
>  What licenses, inspections, and taxes do I need?”

Today she must:

1. Google vague terms (“Texas food permit”).
2. Skim 15 agency web pages—each with different jargon.
3. Re-enter her name, address, and CAFÉ ¡OLÉ! logo five times.
4. Hope she didn’t miss a hidden fire-safety form.

**Intent-Driven Navigation (IDN)** turns that maze into a **GPS-like chat**:

```
Rosa: I need to open a café in Austin.
System: Great! 7 steps detected across 3 agencies. 
        Step 1 – Register business name with the state. Ready?
```

She answers *yes/no* questions; the system **drives** her, step-by-step, across city, state, and federal lanes—never worrying about *which* agency owns *which* form.

---

## 2. Key Concepts (Plain-English Cheatsheet)

| Concept            | Everyday Analogy                 | What It Means in IDN |
|--------------------|----------------------------------|----------------------|
| **Intent**         | “I want pizza” to a delivery app | A plain-language goal (“open a café”). |
| **Journey Map**    | GPS route                        | Ordered list of tasks & forms. |
| **Waypoint**       | Road intersection                | One concrete step (e.g., “file LLC paperwork”). |
| **Navigator**      | GPS voice                        | Chat/voice/GUI that keeps the user on track. |
| **Context Wallet** | Travel passport holder           | Stores user answers so they auto-fill every form. |
| **Re-planner**     | Reroute after a missed turn      | Updates the map if rules or answers change. |

Keep these six ideas in mind; they fuel everything that follows.

---

## 3. Five Minutes to Build Rosa’s Journey

Below is a **single 19-line script** using an imaginary `hms_nav` SDK.

```python
# File: cafe_journey.py
from hms_nav import Navigator

# 1️⃣  Start a navigator session for Rosa
nav = Navigator.start(
    user = "rosa@example.com",
    locale = "en-US"
)

# 2️⃣  Capture the intent in plain English
journey = nav.plan("I want to open a café in Austin, Texas")

# 3️⃣  Show the first waypoint
print(journey.current())          # -> "Register LLC with TX Secretary of State"

# 4️⃣  Mark the waypoint done (auto-submits form via HMS-SVC)
journey.complete_current(
    data = {"businessName": "Cafe Ole", "address": "123 6th St"},
)

# 5️⃣  Continue until journey is finished
while not journey.done():
    print("Next:", journey.next_title())
    input("Press Enter when done…")
    journey.complete_current()

print("🎉 All steps finished!  Good luck, Rosa!")
```

**What just happened?**

1. `Navigator.plan()` called the **Intent Engine** to interpret Rosa’s goal.  
2. A **Journey Map** with ~7 waypoints was created.  
3. Each `complete_current()` auto-filled forms through [Core Backend Services (HMS-SVC)](10_core_backend_services__hms_svc__.md).  
4. Rosa never visited 7 different portals; the navigator handled it all.

---

## 4. Under the Hood (Step-By-Step Walkthrough)

1. **Intent Parse** – A language model converts “open a café” to tags like `business_license`, `food_service`, `location=TX`.  
2. **Journey Planner** queries policy rules from [Legislative & Policy Engine (HMS-CDF)](02_legislative___policy_engine__hms_cdf__.md) and compliance checks via [HMS-ESQ](03_compliance___legal_reasoning__hms_esq__.md).  
3. **Planner** outputs an ordered list of **Waypoints**—each tied to a real API endpoint or form in [HMS-SVC](10_core_backend_services__hms_svc__.md).  
4. **Navigator** sends waypoint tasks to [Agent Orchestration (HMS-ACT)](07_agent_orchestration___workflow__hms_act__.md), which calls agents/tools through the [Model Context Protocol (HMS-MCP)](05_model_context_protocol__hms_mcp__.md).  
5. If Rosa misses a step or policy changes mid-journey, the **Re-planner** adjusts remaining waypoints—just like a GPS after a wrong turn.

### Minimal Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Citizen (Rosa)
    participant NAV as Navigator
    participant PLAN as Journey Planner
    participant ACT as HMS-ACT
    participant SVC as HMS-SVC
    
    C->>NAV: "open a café"
    NAV->>PLAN: parse & plan
    PLAN-->>NAV: journey map
    NAV->>C: "Step 1: Register LLC"
    C->>NAV: complete step
    NAV->>ACT: run waypoint
    ACT->>SVC: POST /llc_application
    SVC-->>NAV: success
    loop remaining steps
```

Only five participants—easy to follow!

---

## 5. Peeking Inside the Codebase (≤ 20 Lines Each)

### 5.1  Intent Parser  
*File: `hms_nav/intent.py`*

```python
import re

def parse(text):
    tags = []
    if re.search(r"\bcafé|restaurant|food\b", text, re.I):
        tags.append("food_service")
    if "open" in text and "business" in text or "café" in text:
        tags.append("business_license")
    # Extract state
    m = re.search(r"in (\w{2}),? ?(usa|us)?", text, re.I)
    if m:
        tags.append(f"state={m.group(1).upper()}")
    return tags
```

*Take-away:* A real build would use ML, but beginners can grok this regex starter.

### 5.2  Journey Planner  
*File: `hms_nav/planner.py`*

```python
RULES = {
    ("business_license", "food_service", "state=TX"): [
        "tx_llc_registration",
        "city_health_permit",
        "fire_safety_inspection"
    ]
}

def plan(tags):
    for key, steps in RULES.items():
        if all(k in tags for k in key):
            return steps
    return ["manual_review"]
```

Fewer than 15 lines to map tag combos → waypoints.

### 5.3  Context Wallet  
*File: `hms_nav/context.py`*

```python
class Wallet(dict):
    def autofill(self, form_fields):
        return {f: self.get(f) for f in form_fields if f in self}
```

Keeps Rosa’s name/address once, re-uses everywhere—no repeated typing.

---

## 6. Putting It All Together in the Portal UI

In the next chapter we’ll build a **single-page interface** where:

```
┌── chat box ──┐   Rosa types: "I need a café license"
└──────────────┘   ↓
[Micro-Frontend shows Step 1 wizard]
```

That UI will simply subscribe to `navigator.events.*` on the [Inter-Agency Bus (HMS-A2A)](08_inter_agency_communication_bus__hms_a2a__.md) and render each waypoint as it arrives—zero hard-coded screens.

---

## 7. Common Questions

| Question | Quick Answer |
|----------|--------------|
| “Can I support voice or SMS?” | Yes—`Navigator.start(mode="sms")` plugs in other channels. |
| “What if two waypoints need **Human-in-the-Loop** approval?” | Those steps pause in [HITL Oversight](06_human_in_the_loop__hitl__oversight_.md) until a clerk approves, then the Navigator auto-resumes. |
| “Does the journey survive browser crashes?” | Yes—state lives server-side; re-open with `Navigator.resume(session_id)`. |
| “Can agencies add custom steps?” | Add rules in `planner.py` or via [Governance Layer (HMS-GOV)](01_governance_layer__hms_gov__.md) UI; changes go live instantly. |

---

## 8. Mini Exercise

1. Clone `examples/nav_quickstart.ipynb`.  
2. `Navigator.plan("I want to drive Uber in Chicago")`.  
3. Inspect `journey.map`—note city, state, and background-check steps.  
4. Simulate failing the background check; watch `Re-planner` add an appeal-form waypoint.  

---

## 9. What You Learned

* **Intent-Driven Navigation** translates plain-language goals into a sequenced, cross-agency **Journey Map**.  
* A tiny SDK call (`Navigator.plan()`) spares citizens from hunting down forms.  
* Waypoints plug into existing HMS layers—no duplication of logic or policy.  

Ready to display these journeys in a polished, reusable web component library?  
Head to the next chapter: [Micro-Frontend Interface Library (HMS-MFE)](18_micro_frontend_interface_library__hms_mfe__.md)

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)