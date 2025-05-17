# Chapter 2: Intent-Driven Navigation
*(How HMS-CUR turns “I need to renew my license” into the exact screen you need—no menu digging required)*  

[← Back to Chapter 1: Micro-Frontend Interface](01_micro_frontend_interface__hms_mfe__.md)

---

## 1. Motivation — “GPS for Government Tasks”

Picture Maya, a citizen on her phone at a bus stop.  
She opens the national **MyGov** portal and simply types:

> renew my driver’s license

Instead of hunting through 4 levels of menus (“Transportation → DMV → Services → Renewal”), she is immediately shown the first renewal step.  

If Maya’s state supports online vision checks, the path is different than if it requires an in-person photo. If the payment API is down, she is re-routed to an alternative kiosk nearby—exactly like a GPS avoids traffic.

That experience is powered by **Intent-Driven Navigation (IDN)**.

---

## 2. Key Concepts (Road-Trip Analogies)

| IDN Piece | Road-Trip Equivalent | Plain-English Role |
|-----------|---------------------|--------------------|
| Intent | “I want to reach the Grand Canyon.” | A goal expressed by the user. |
| Context | Traffic, weather, road closures | User profile, permissions, agency schedules. |
| Planner | GPS algorithm | Chooses fastest compliant set of steps. |
| Waypoint | Highway exit | One concrete action (fill form, pay fee). |
| Rerouter | “Recalculating…” | Swaps a step if an API fails or user lacks a doc. |

---

## 3. A 3-Minute Hands-On Tour

We’ll build a **toy router** that:

1. Reads a user’s plain-text goal.
2. Matches it to an intent.
3. Loads the right micro-frontend pane from [Chapter 1](01_micro_frontend_interface__hms_mfe__.md).

### 3.1 Capture the User’s Goal

```html
<!-- intent-box.html -->
<input id="goal" placeholder="What do you need?" />
<button id="go">Go</button>
<script src="intent-capture.js"></script>
```

```js
// intent-capture.js
import { handleGoal } from './intent-router.js';

document.getElementById('go')
        .onclick = () => handleGoal(
            document.getElementById('goal').value);
```

Explanation  
A single text box + button delegates the heavy lifting to `handleGoal`.

---

### 3.2 Register Intents (super-simple)

```js
// intent-registry.js
export const intents = [
  { pattern: /renew.*license/i, pane: 'dmv-renewal' },
  { pattern: /apply.*coins/i,   pane: 'us-mint-coins' },
];
```

Explanation  
Each intent is just a regex that maps to a **pane ID**.  
(Real life will use NLP, synonyms, etc.)

---

### 3.3 Route to the Right Pane

```js
// intent-router.js
import { intents }     from './intent-registry.js';
import { mountPane }   from 'hms-mfe';

export function handleGoal(text){
  const hit = intents.find(i => i.pattern.test(text));
  if(!hit) return alert('Sorry, try rephrasing.');

  mountPane({
    slot : 'main-slot',                // slot from Chapter 1 host
    url  : `/panes/${hit.pane}.js`     // path to micro-frontend bundle
  });
}
```

Explanation  
• Finds the first regex that matches the user’s text.  
• Mounts its bundle in the central `<div id="main-slot">`.

---

## 4. What Happens Under the Hood?

### 4.1 Plain-English Flow

1. User enters “renew license”.  
2. `handleGoal` finds the “DMV renewal” intent.  
3. HMS-MFE downloads `dmv-renewal.js` and mounts it.  
4. The pane’s UI guides the user through steps (upload vision test, pay fee, etc.).  
5. If an API fails, the planner can issue a **reroute event** to load an alternative pane.

### 4.2 Minimal Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Box as Intent Box
    participant Router
    participant Host as MFE Host
    participant DMV as DMV Pane

    User->>Box: type "renew license"
    Box->>Router: handleGoal(text)
    Router->>Host: mountPane('dmv-renewal')
    Host->>DMV: mount(slot)
    DMV-->>User: Step-by-step renewal UI
```

---

## 5. Peeking Inside the Planner (Optional Deep Dive)

Imagine an **in-memory state machine** that chooses the next waypoint.

```js
// tiny-planner.js
export function nextStep(intent, context){
  if(intent === 'license' && !context.visionOK)
       return 'vision-check-pane';
  if(intent === 'license' && !context.paid)
       return 'payment-pane';
  return 'done';
}
```

Explanation  
1. Reads **context** (permissions, previous form states).  
2. Returns the key of the next pane to mount.  
3. Called after every waypoint completes to see if rerouting is needed.

---

## 6. Internal Files at a Glance

* `/ui/intent-box.html` – simple capture widget  
* `/ui/intent-capture.js` – hooks button to router  
* `/core/intent-registry.js` – list of patterns → panes  
* `/core/intent-router.js` – glue between user text and HMS-MFE  
* `/core/tiny-planner.js` – (optional) smarter waypoint chooser  

*(Real HMS-CUR adds logging, ML parsing, and risk checks from the  
[Security & Compliance Engine](10_security___compliance_engine__hms_esq___hms_ops__.md).)*

---

## 7. Frequently Asked Questions

1. **How is context gathered?**  
   The router queries profile APIs and reads JWT scopes to know state residency, age, etc.

2. **What if two intents match?**  
   Use a confidence score and ask the user to confirm:  
   “Did you mean renew your *driver’s* license or *business* license?”

3. **Can a user jump back to a previous step?**  
   Yes—the planner keeps a breadcrumb history; `mountPane` can be called with any earlier pane.

4. **Does IDN replace URLs?**  
   No. Each waypoint still has a deep link. IDN just chooses it for you.

---

## 8. Summary & What’s Next

You learned how **Intent-Driven Navigation** turns a free-form request into the right micro-frontend, gathers context, and reroutes when paths change—like a GPS for citizen services.

Next, we’ll see how agencies *publish* new panes so the planner can discover them in the first place:  
[Marketplace & Discoverability (HMS-MKT)](03_marketplace___discoverability__hms_mkt__.md)

Happy routing!

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)