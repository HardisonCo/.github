# Chapter 1: HMS-MFE Micro-Frontend Shell


Welcome! In this first chapter we’ll meet the “LEGO® base-plate” that every other screen in the **HMS-MKT** project snaps onto. By the end you will:

1. Understand what a *micro-frontend shell* is.  
2. See how it lets many government teams ship UI pieces without breaking each other’s work.  
3. Build and run your very first widget inside the shell.

---

## 1. Why Do We Need a Shell?

Imagine a citizen, Maria, visiting a single government portal to:

* Renew her health insurance card (Health Department).  
* Apply for a winter-energy rebate (Energy Department).  
* Check her retirement benefit status (Retirement Services).

Maria expects one smooth website. Behind the scenes, however, three separate agencies—and their developer teams—own those pages.  
Without a shared **shell**, they would:

* Fight over CSS (one button purple, the other green).  
* Duplicate login flows, causing security holes.  
* Ship updates at different speeds, breaking pages for each other.

The **HMS-MFE shell** fixes this by providing:

* A common HTML container & grid layout.  
* Shared CSS tokens and accessibility rules.  
* A plug-and-play slot system where each team drops its widget.

Think of it exactly like a government-issue LEGO base-plate. Every agency gets bricks (widgets) in its own box, but the studs on top line up perfectly so any brick fits.

---

## 2. Key Concepts (the “Studs” on the Plate)

| Concept | Plain-English Explanation |
|---------|---------------------------|
| Shell | The outer page that loads first, handles routing, theming, auth, and then invites widgets to render. |
| Slot | A predefined region inside the shell (e.g., `header`, `main`, `sidebar`). |
| Widget / Micro-Frontend | One self-contained UI module owned by a team (e.g., “Energy Rebate Form”). |
| Shared Services | Utilities exposed by the shell: design tokens, feature flags, auth checks, analytics. |
| Independent Deploy | Each widget ships on its own CI/CD pipeline and version, but the shell stitches them together at runtime. |

---

## 3. Quick Start: Hello Government Widget

We’ll create a tiny widget that greets users from the *Office of National Drug Control Policy (ONDCP)* and plug it into the shell.

### 3.1 Folder Layout

```
hms-portal/
└─ mfe-shell/            <-- the shell
   └─ src/
└─ widgets/
   └─ ondcp-hello/
       ├─ HelloONDCP.vue
       └─ manifest.json
```

### 3.2 Widget Code (HelloONDCP.vue)

```vue
<template>
  <div class="ondcp-card">
    <h2>Hello from ONDCP 👋</h2>
    <p>We advise the President on drug-control policy.</p>
  </div>
</template>

<script>
export default { name: 'HelloONDCP' }
</script>

<style scoped>
.ondcp-card { padding: 1rem; background: var(--surface-1); }
</style>
```

Explanation  
1. Plain Vue component—no special imports required.  
2. Uses `var(--surface-1)` so it automatically picks up the shell’s color palette.

### 3.3 Widget Manifest

```json
{
  "name": "hello-ondcp",
  "slot": "main",
  "module": "/widgets/ondcp-hello/HelloONDCP.vue"
}
```

The manifest tells the shell:

* Widget name: `hello-ondcp`.  
* Where to render: the `main` slot.  
* Which file exports the component.

### 3.4 Registering with the Shell

Open `mfe-shell/src/widgetRegistry.js`:

```js
import HelloONDCP from '../../widgets/ondcp-hello/HelloONDCP.vue'

export const registry = [
  { name: 'hello-ondcp', slot: 'main', component: HelloONDCP },

  // existing widgets stay untouched
]
```

Run `npm run dev` in `mfe-shell`, visit `localhost:3000`, and you’ll see the ONDCP greeting living happily next to any Health or Energy bricks already loaded.

---

## 4. What Happens Under the Hood?

Let’s peek behind the curtain.

### 4.1 Step-By-Step Flow (No Code)

1. Browser loads `index.html`.  
2. Shell JavaScript bootstraps: reads *widgetRegistry*.  
3. User’s route (`/citizen/dashboard`) maps to a *layout* with defined slots.  
4. Shell iterates the registry, mounts each widget into its slot.  
5. Widgets call shared services (e.g., `auth.getUser()`).

### 4.2 Minimal Sequence Diagram

```mermaid
sequenceDiagram
  participant B as Browser
  participant S as Shell
  participant A as AuthService
  participant E as EnergyWidget
  participant H as HealthWidget

  B->>S: Load shell bundle
  S->>A: Check login status
  A-->>S: user = Maria
  S->>E: mount()
  S->>H: mount()
  B<<--E: Render energy rebate form
  B<<--H: Render health card renewal
```

### 4.3 Core Mount Logic (simplified)

```js
// mfe-shell/src/mount.js
export function mountWidgets(registry, slots) {
  registry.forEach(w => {
    const el = document.querySelector(`[data-slot="${w.slot}"]`)
    if (el && w.component) {
      // Vue magic simplified:
      new Vue({ render: h => h(w.component) }).$mount(el)
    }
  })
}
```

Less than 10 lines! The shell simply finds the right DOM node and mounts each Vue component.

---

## 5. Styling & Accessibility for Free

Because widgets rely on CSS Variables from the shell (`--surface-1`, `--font-scale`), every button, card, and heading automatically:

* Meets WCAG AA color-contrast.  
* Scales text size according to user preferences.  
* Supports right-to-left layout if the shell toggles it.

No individual team must reinvent these accessibility wheels.

---

## 6. Independent Deployments

Each department can:

1. Update its widget repository.  
2. Run CI/CD to push a new `*.js` bundle to a CDN.  
3. Submit a tiny manifest PR to the shell (or use dynamic discovery).

The Health team’s delay won’t block the Denali Commission from shipping a fix for rural internet applications.

---

## 7. Linking Forward

You now have a working mental model—and a running demo—of the HMS-MFE shell.  
Next we’ll learn how routes and buttons can understand user *intent* instead of raw URLs, creating seamless journeys across widgets.

[Next Chapter: Intent-Driven Navigation & Guided Journeys](02_intent_driven_navigation___guided_journeys_.md)

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)