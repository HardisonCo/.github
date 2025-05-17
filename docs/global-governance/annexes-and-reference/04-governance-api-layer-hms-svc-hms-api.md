# Chapter 4: Governance API Layer (HMS-SVC / HMS-API)

*(just hopped over from [Micro-Frontend Framework (HMS-MFE)](03_micro_frontend_framework__hms_mfe__.md))*  

---

> “The public counter is closed—send the robot clerk.”  
> When software, not staff, files city paperwork it goes through the Governance API Layer.

---

## 1. Why do we need a “robot clerk”?

Picture the **Indoor Air Quality Division** (EPA).  
They publish a new **mold-inspection form** every spring. In HMS-GOV that looks like:

1. An AI agent finishes drafting `mold-inspection-2024.pdf`.  
2. The agent says “Publish this.”  
3. No human waits in a queue; instead it calls `POST /api/forms`.  
4. Two seconds later the form is stamped ✔ `v1`, audit-logged, and searchable.

The **Governance API Layer** is the pneumatic-tube system that makes this instant filing possible.  
Without it you would:

* Upload manually via FTP.  
* Email three supervisors.  
* Back-date the document when you realize you forgot version control.

---

## 2. What exactly lives in this layer?

HMS-GOV splits the server side in two thin pieces:

| Piece | Nickname | What it does | Who can talk to it |
|-------|----------|--------------|--------------------|
| HMS-API | “Front door” | Rate-limiting, CORS, public docs | Browsers, outside world |
| HMS-SVC | “Back office” | Business rules, DB access, audit | HMS-API, internal services |

The split lets us scale, lock, or even **air-gap** the back office without touching public endpoints.

---

## 3. Five key concepts (plain English)

1. **Endpoint** – a single mailbox (`/api/forms`) where you drop requests.  
2. **Auth Token** – your city badge; no token, no entry.  
3. **Version Tag** – every change bumps `v1 → v2 → v3`, never overwrite.  
4. **Audit Trail** – a running receipt: *who*, *when*, *what changed*.  
5. **Rollback** – press one button, system re-publishes the previous version.

---

## 4. A 60-second “publish form” example

### 4.1 Client call (from any micro-frontend or agent)

```js
// in FormPublisher.js  (12 lines)
async function publish(file, meta) {
  const body = new FormData()
  body.append('file', file)
  body.append('meta', JSON.stringify(meta))

  const res = await fetch('/api/forms', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + userToken },
    body
  })
  return res.json()          // → { id:42, version:'v1', status:'published' }
}
```

What happens:  
1. We attach the PDF (`file`) and description (`meta`).  
2. Add an **Auth Token** so the API knows *who* we are.  
3. Await a tiny JSON confirming version and status.

### 4.2 How the server handles it

```js
// routes/forms.js  (Node/Express, 18 lines)
router.post('/forms', auth(), async (req, res) => {
  const { file, meta } = req.body                 // 1. unpack
  const id  = await db.forms.insert({             // 2. store file+meta
    filePath: await saveFile(file),
    meta     : JSON.parse(meta),
    version  : 'v1'
  })
  await audit.log(req.user.id, 'CREATE_FORM', id) // 3. audit
  res.status(201).json({ id, version:'v1', status:'published' })
})
```

• `auth()` middleware verifies the token.  
• `audit.log()` writes a one-line receipt.  
• Business logic (HMS-SVC) stays <10 lines; helpers do the heavy lifting.

---

## 5. A peek inside: step-by-step journey

```mermaid
sequenceDiagram
    participant UI  as Client (Agent/UI)
    participant API as HMS-API
    participant SVC as HMS-SVC
    participant DB  as Database

    UI ->> API: POST /forms + token
    API ->> API: Validate token & quota
    API ->> SVC: Forward clean request
    SVC ->> DB : Save file & meta (v1)
    SVC -->> API: success JSON
    UI <<-- API: 201 Created
```

Only four actors: easy to debug, easy to scale.

---

## 6. Guards at the gate: authentication & roles

Very small middleware (`middleware/auth.js`, 17 lines):

```js
export function auth(requiredRole = 'editor') {
  return (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1]
    const user  = verify(token)       // JWT or session lookup
    if (!user || !user.roles.includes(requiredRole))
      return res.status(403).send('Forbidden')
    req.user = user                   // attach for later use
    next()
  }
}
```

Explanation:  
*Extract token → decode → check role → proceed.*  
Swap `verify()` for whatever auth provider your agency uses (Okta, Login.gov).

---

## 7. How versioning & rollback work

1. Every record has `version` + `parentId`.  
2. Updating a form **never** edits the row—HMS-SVC inserts a **new** row with `parentId = originalId`.  
3. Rolling back simply marks the older row as “current”.

Tiny update route (15 lines):

```js
router.put('/forms/:id', auth(), async (req, res) => {
  const prev = await db.forms.find(req.params.id)
  const ver  = 'v' + (parseInt(prev.version.slice(1)) + 1)
  const id   = await db.forms.insert({ ...prev, ...req.body, version: ver, parentId: prev.parentId || prev.id })
  await audit.log(req.user.id, 'UPDATE_FORM', id)
  res.json({ id, version: ver })
})
```

Rollback = same call but cloning the **older** version.

---

## 8. Where does this layer sit in the bigger picture?

```
Browser ──▶ HMS-API ──▶ HMS-SVC ──▶ DB / Task Queues ▶ Other Services
          ▲            ▲
          │            └── Detailed rules, audit, versioning
          └──── rate-limits, CORS, public docs
```

Later you’ll see HMS-SVC hand off long-running jobs (PDF conversion, OCR, etc.) to **task queues** covered in the next chapter.

---

## 9. Quick FAQ

• **Can agencies create custom endpoints?**  
  Yes—mount a new router file under `services/agency/{name}.js`. HMS-API auto-discovers it.

• **Does every request get audit-logged?**  
  Anything that mutates data (`POST`, `PUT`, `DELETE`) is logged by a one-line **Audit Middleware** you can copy-paste:

```js
// middleware/audit.js  (9 lines)
export function audited(req, res, next) {
  res.on('finish', () => {
    if (['POST','PUT','DELETE'].includes(req.method))
      audit.log(req.user.id, req.method + ' ' + req.path, res.statusCode)
  })
  next()
}
```

• **How big can a file be?**  
  Default limit is 25 MB; override with `MAX_UPLOAD_MB` env variable.

---

## 10. Recap & next steps

You learned:

✓ Why the Governance API Layer is the “pneumatic tube” for automated paperwork.  
✓ The split between HMS-API (front door) and HMS-SVC (back office).  
✓ Core concepts: Endpoint, Auth Token, Version Tag, Audit Trail, Rollback.  
✓ How to publish a form in <20 lines of client and server code.  
✓ How authentication, versioning, and auditing are enforced.

Time to see what happens when a request needs heavy lifting (e.g., generating 100 PDFs). That’s the job of queues and orchestration—jump to  
[Service Orchestration & Task Queues (HMS-OMS)](05_service_orchestration___task_queues__hms_oms__.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)