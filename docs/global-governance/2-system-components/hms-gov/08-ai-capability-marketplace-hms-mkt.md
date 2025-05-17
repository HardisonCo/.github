# Chapter 8: AI Capability Marketplace (HMS-MKT)

*(jumping in from [Model Context Protocol (HMS-MCP)](07_model_context_protocol__hms_mcp__.md))*  

---

> “Think **App Store**, but every download is a civil-service super-power.”  
> A town of 7 000 citizens can lease the same flood-prediction model NASA uses—no PhD required.

---

## 1. Why bother with a marketplace?

### Use-case: Cedar Falls needs flood alerts

1. The Public Works director types “flood prediction” into HMS-GOV.  
2. The **AI Capability Marketplace** shows a NASA-published “Climate Simulator”.  
3. One click → the capability installs; a lease fee is logged.  
4. The town’s existing **AI Representative Agent** (see [Chapter 6](06_ai_representative_agent__hms_agt___hms_agx__.md)) immediately gains a new skill:  
   `runClimateModel(lat,long)`  
5. The next morning citizens receive SMS alerts: “River expected to rise 1.2 ft on Friday.”

No procurement cycle, no custom code. That is the promise of **HMS-MKT**.

---

## 2. Key concepts (plain English)

| Term | Analogy | What it means |
|------|---------|---------------|
| Catalog | Shopping window | JSON list of all publishable capabilities. |
| Capability | App download | A bundle of skills, tool cards, & docs. |
| Manifest (`capability.json`) | Nutrition label | Declares skills, version, provider, license. |
| Lease Token | Rental receipt | Proof your agency may run the capability. |
| Sandbox | Play-pen | Each capability runs isolated (no data leaks). |

Keep these five words in mind—everything else is detail.

---

## 3. Browsing the catalog (client side)

```js
// ui/Marketplace.js   – 18 lines
export async function listCapabilities () {
  const res = await fetch('/api/mkt/catalog')
  return res.json()      // → [{ id:'climate.sim-basic', name:'Climate Simulator', ...}]
}

// inside a Vue tile
onMounted(async ()=> caps.value = await listCapabilities())
```

Beginner notes  
• One GET call returns an array; render it in a table or cards.  
• No log-in? The API still replies, but without price details.

---

## 4. Installing a capability

```js
// ui/Marketplace.js
export async function install(id) {
  const res = await fetch('/api/mkt/install', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ id })
  })
  return res.json()   // → { status:'installed', skills:['runClimateModel'] }
}
```

Explanation  
1. POST `/install` with chosen `id`.  
2. On success you receive the **new skills** now available to agents.

---

## 5. What does a capability look like?

```json
{
  "id": "climate.sim-basic",
  "name": "Climate Simulator (Basic)",
  "version": "1.0.2",
  "provider": "NASA",
  "skills": ["runClimateModel"],
  "tools": ["climate.run"],
  "license": "pay-as-you-go",
  "docs": "https://nasa.gov/hms/climate-sim/docs"
}
```

• Saved as `capability.json` at the root of the bundle (zip or npm pkg).  
• **Skills** and **tools** automatically register with **HMS-AGT** via the same Tool Card format you met in [MCP](07_model_context_protocol__hms_mcp__.md).

---

## 6. Under the hood – install flow

```mermaid
sequenceDiagram
    participant UI  as Clerk UI
    participant CAT as Catalog Svc
    participant DL  as Package Downloader
    participant VER as Signature Verifier
    participant REG as Skill Registry

    UI ->> CAT: POST /install {id}
    CAT ->> DL: fetch bundle URL
    DL -->> VER: hash & verify sig
    VER -->> REG: extract skills/tools
    UI <<-- CAT: {status:'installed'}
```

Only five moving parts—easy to audit and scale.

---

### 6.1 Minimal installer (server, 20 lines)

```js
// routes/mkt.js
router.post('/install', auth(), async (req,res)=>{
  const { id } = req.body
  const url = await catalog.bundleUrl(id)      // 1. find package
  const zip = await download(url)              // 2. fetch bytes
  if(!verify(zip))  return res.status(409).send('Bad signature')
  const skills = await unpack(zip,'skills/')   // 3. extract JS files
  registerSkills(skills)                       // 4. merge into AGT
  const token = await leases.issue(id, req.user.agency)
  res.json({ status:'installed', token, skills:Object.keys(skills) })
})
```

Line-by-line  
1–2  Look up and download the zip.  
3    Verify supplier signature.  
4    Unpack only the `skills/` folder.  
5    Register the new skills in runtime memory.  
6    Emit a **Lease Token** for billing & compliance.

---

## 7. Trying the new skill

```js
// Anywhere in a prompt to HMS-AGT
You may call runClimateModel(lat,long) if the user asks about flood risk.
```

Because **registerSkills()** injected the Tool Card into the agent registry, no further code changes are required.

---

## 8. Removing or suspending a capability

```js
await fetch('/api/mkt/uninstall/climate.sim-basic', { method:'DELETE' })
```

The Marketplace service:

1. Revokes the Lease Token.  
2. Deregisters its skills.  
3. Schedules a background job in **HMS-OMS** to archive related data.  

Safe, reversible, and audit-logged.

---

## 9. FAQ

| Question | Answer |
|----------|--------|
| Can a small agency publish its own capability? | Yes—upload a signed bundle to the Catalog service and mark visibility `private`. |
| What if a capability needs DB migrations? | The bundle can include `/migrations/*.sql`; the installer runs them inside a transaction. |
| Offline deployments? | Mirror the catalog to an on-prem S3 bucket; set `MKT_CATALOG_URL` env variable. |
| Pricing models? | `license` field may be `free`, `flat`, or `metered`; billing service sends monthly reports. |

---

## 10. Recap

You now know:

✓ Why HMS-MKT lets governments **borrow** world-class algorithms instead of reinventing them.  
✓ The five core ideas: Catalog, Capability, Manifest, Lease Token, Sandbox.  
✓ How to list, install, and uninstall a capability in just a few lines.  
✓ The behind-the-scenes flow that downloads, verifies, and registers new skills.

Next we’ll see how these shiny new capabilities plug into the rule-making pipeline:  
[Legislative Workflow Engine (HMS-CDF)](09_legislative_workflow_engine__hms_cdf__.md)

---

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)