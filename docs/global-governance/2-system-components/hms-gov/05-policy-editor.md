# Chapter 5: Policy Editor

*(Follow-up to [Chapter 4: Policy Management Dashboard](04_policy_management_dashboard_.md))*  

---

## 1. Why Do We Need a “Word-Processor-Plus-Compiler”?

Meet **Sam**, an analyst at the **Department of Education**.  
Congress just changed the **FAFSA income-threshold rule** and Sam must:

1. Rewrite the legal text.  
2. Check that no student application will be rejected by mistake.  
3. Show managers the *diff* between “old” and “new.”  
4. Publish only after everything passes automated legal linting.

E-mails and copy-pasted Word docs won’t cut it.  
Sam opens the **Policy Editor**—an in-browser workshop where text, code, simulation, and version control live side-by-side.

---

## 2. Big Picture

```
mermaid
graph LR
    subgraph Storefront
        PE[Policy Editor<br/>pages/PolicyEditor.vue]
    end
    subgraph Service
        PCS(policy-compile-svc)
    end
    PE -- POST /compile --> PCS
    PCS -- Result (OK/Errors) --> PE
```

• Sam sees a rich textarea.  
• Experts can toggle “Source View” to edit JSON directives.  
• “✅ Compile” calls `policy-compile-svc`; errors come back in seconds.

---

## 3. Key Concepts (Simple Definitions)

| Concept             | Beginner-friendly Meaning                                            |
|---------------------|-----------------------------------------------------------------------|
| **Draft Pane**      | Rich-text box—type like in Google Docs.                              |
| **Source View**     | Raw JSON behind the draft; pros tweak IDs & dates here.              |
| **Version Control** | Every save creates a new commit; you can always “rewind.”            |
| **Diff Viewer**     | Two-pane view that highlights additions in green, deletions in red.  |
| **Legal Linter**    | Robot proof-reads for missing citations (§, †, etc.).                |
| **Simulation**      | Runs fake citizen data to see if the rule behaves as intended.       |

Remember: **Policy Editor = Word + Git + Test Runner—all in one tab.**

---

## 4. A 20-Second Tour

```
┌─────────────────────────────────────────────────────────┐
│ FAFSA Income Threshold (Draft v12)            [Compile] │
├─────────────────────────────────────────────────────────┤
│ Rich-Text Pane (left)  |  Source JSON (right)           │
│---------------------------------------------------------│
│ Simulation Results     |  Diff vs. Production           │
└─────────────────────────────────────────────────────────┘
```

Buttons: **Save**, **Compile**, **Preview**, **Submit for Review**.

---

## 5. Scaffolding `PolicyEditor.vue`

`pages/PolicyEditor.vue` already exists; we’ll extend it.

```vue
<template>
  <div class="policy-editor">
    <h1>{{ title }}</h1>

    <!-- 1. Draft Pane -->
    <textarea v-model="draft" rows="12"></textarea>

    <!-- 2. Compile & Errors -->
    <button @click="compile">✅ Compile</button>
    <pre v-if="errors.length">{{ errors }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const title  = 'Policy Editor'
const draft  = ref('// type here')
const errors = ref([])

async function compile(){
  const res = await fetch('/api/policy/compile', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ text: draft.value })
  })
  errors.value = await res.json()   // ["line 3: missing citation"]
}
</script>
```

Explanation (line-by-line):  
1. `textarea` lets Sam type.  
2. Clicking **Compile** sends the text to the backend (`/api/policy/compile`).  
3. Any errors show inside `<pre>`.

Under 20 lines, yet fully functional!

---

## 6. Example Input & Output

Input (Sam’s draft snippet):

```text
§ 2 Income Threshold  
Students with AGI below **$75,000** qualify for maximum aid.
```

Backend returns:

```json
["Warning: $ value missing currency code (USD)"]
```

Sam fixes the text, clicks **Compile** again, and sees an empty error list—green light to move on.

---

## 7. What Happens Behind the Screen?

```
mermaid
sequenceDiagram
    participant SamBrowser as Browser
    participant PE as PolicyEditor
    participant GW as HMS-API
    participant PC as policy-compile-svc
    SamBrowser->>PE: click Compile
    PE->>GW: POST /policy/compile
    GW->>PC: forward text
    PC-->>GW: JSON errors
    GW-->>PE: relay
```

Only four hops; latency is usually < 200 ms.

---

## 8. Inside `policy-compile-svc` (Server Pseudocode)

```python
# compile.py  (simplified)
from fastapi import FastAPI
app = FastAPI()

@app.post("/compile")
def compile(req: dict):
    text = req["text"]
    errs = []

    # 1. Legal linting
    if "$" in text and "USD" not in text:
        errs.append("Warning: $ value missing currency code (USD)")

    # 2. JSON transform for machines
    machine_json = {"sections":[{"id":"2","body":text}]}

    # 3. Return result
    return errs
```

Explain:  
• Step 1—cheap pattern check.  
• Step 2—convert to canonical JSON (so downstream systems share one source of truth).  
• Step 3—send back error list (empty if all good).

---

## 9. Saving a New Version

```javascript
async function saveDraft(){
  await fetch('/api/policy/save', {
    method:'POST',
    body: JSON.stringify({ text: draft.value })
  })
  alert('Saved as v' + new Date().toISOString())
}
```

Every save becomes a **commit**. The diff viewer later reads:

```
GET /api/policy/diff?from=v11&to=v12
```

and highlights changes—no Git skills needed.

---

## 10. Running a Quick Simulation

```javascript
async function simulate(){
  const res = await fetch('/api/policy/simulate', {
    method:'POST',
    body: JSON.stringify({
      text: draft.value,
      sampleCitizen: { agi: 68000 }
    })
  })
  console.log(await res.json())  // { qualifies: true }
}
```

Sam can try edge cases (AGI=$80k, $120k…) until results look right.

---

## 11. Swapping to “Source View”

Add a checkbox:

```vue
<label><input type="checkbox" v-model="raw"> Source View</label>
<div v-if="raw">
  <pre>{{ JSON.stringify(toJson(draft), null, 2) }}</pre>
</div>
```

`toJson` is a helper that converts rich text into machine-readable JSON; experts love it, beginners ignore it.

---

## 12. Pulling it All Together

1. **Dashboard** (Chapter 4) lists all policies.  
2. Clicking a policy opens this **Policy Editor**.  
3. Sam types, compiles, simulates, and saves versions.  
4. When ready, Sam clicks “Submit for Review.”  
   *That moves the policy back to the Dashboard’s “Queued” column.*

---

## 13. Beginner Q & A

**Q: Do I need to know Git?**  
A: No. The backend wraps Git commands for you; buttons are enough.

**Q: Can two analysts edit at the same time?**  
A: Yes—optimistic locking merges non-overlapping lines; otherwise you’ll see a friendly “Resolve conflict” screen.

**Q: Where is the JSON schema stored?**  
A: In `policy-compile-svc/schemas/`. Compile loads the matching file based on the policy type.

**Q: How do I add a new linter rule?**  
A: Add a Python function in `lint_rules.py`, register it, deploy; the Editor automatically surfaces new warnings.

---

## 14. What You Learned

• The **Policy Editor** marries human-friendly typing with machine-friendly checks.  
• A single **Compile** button calls `policy-compile-svc` to lint and transform text.  
• Version control, diffing, and simulation run transparently.  
• All heavy logic lives in services; the Vue page is < 100 lines.

Ready to see how these freshly minted policies travel to other federal systems? Jump to [Chapter 6: HMS-GOV – Government Integration Gateway](06_hms_gov____government_integration_gateway_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)