# Chapter 13: Extension & Specialty Capabilities (HMS-AGX)

[← Back to Chapter 12: Marketplace Service](12_marketplace_service__hms_mkt__.md)

---

> “Downloadable super-powers for every agent—safely.”

---

## 1. Why Do We Need HMS-AGX?

Imagine the **Veterans Health Administration** wants an AI clerk to:

1. Read a **hand-written doctor’s note** (vision).  
2. Extract dosage instructions via **speech-to-text** from a follow-up voicemail (audio).  
3. Suggest nearest pharmacies on a **map** (geo).

None of those “extra senses” exist in the vanilla agent toolbox we built earlier.  
Buying three entirely new services would be over-kill.  
Instead, we install **HMS-AGX**—the “DLC pack” that plugs cutting-edge models into the platform **without breaking governance, policy, or budgets**.

---

## 2. Starter Use-Case – “Refill My Prescription”

Goal: an agent receives a *scanned* prescription form and:

1. Reads the image.  
2. Turns it into structured data.  
3. Finds the nearest 24-hour pharmacy.  

We’ll solve this in **under 20 lines of code** using AGX.

---

## 3. Key Concepts (Beginner Friendly)

| Term            | Everyday Analogy                   | One-Line Job |
|-----------------|------------------------------------|--------------|
| Capability Pack | App on your phone                  | Bundles a vision or audio model |
| Sandbox         | Play-pen                            | Runs the model with no internet or file access |
| Capability Gate | Bouncer at the door               | Checks policy & quotas before use |
| Credits         | Arcade tokens                     | Each call consumes prepaid credits |
| Plugin Manifest | Nutrition label                   | Lists models, sizes, and allowed scopes |
| Safe Interface  | Child-proof scissors               | Exposes only vetted functions (e.g., `ocr()` not raw GPU access) |

Remember these six items; AGX is just **“packs, gates, and credits.”**

---

## 4. Using HMS-AGX in Code (18 Lines)

```js
// refillAgent.js  – run with: node refillAgent.js
import axios from 'axios';

// 1. Request OCR capability
const env = {
  traceId: 'tx-'+Date.now(),
  capability: 'VISION_OCR_V1',
  inputUrl: 'https://files.gov/vet42_rx_scan.png'
};

const ocr = await axios.post('http://agx/vision/ocr', env, {
  headers:{ 'x-api-key':'AGT_PHARM' }   // checked by Capability Gate
});

const text = ocr.data.text;  // "Take Lisinopril 10mg once daily."

// 2. Ask geo capability for nearest 24-hour pharmacy
const geo = await axios.post('http://agx/geo/nearest', {
  traceId : env.traceId,
  text    : '24hour pharmacy',
  lat     : 38.899, long:-77.036
});

console.log('Nearest pharmacy ➜', geo.data.name);
```

**What happens?**

1. `OCR` pack runs in a **sandbox**; AGX returns pure text.  
2. A **geo pack** converts text into coordinates.  
3. Both calls are logged with the same `traceId` so auditors can replay them.

---

## 5. What Happens Under the Hood?

```mermaid
sequenceDiagram
    participant AGT as Agent
    participant GATE as Capability Gate
    participant BOX as Sandbox
    participant BIL as Credit Meter
    AGT->>GATE: POST /vision/ocr
    GATE->>BIL: check credits & policy
    GATE->>BOX: run model (if allowed)
    BOX-->>GATE: text result
    GATE-->>AGT: text result
```

1. **Gate** validates API key & [HMS-CDF](02_policy_codification_engine__hms_cdf__.md) rules.  
2. **Credit Meter** ensures the agency has tokens left this month.  
3. **Sandbox** loads the model weights, runs inference, and returns only permitted fields.  
4. Everything is stamped into the **Activity Log** for audits.

---

## 6. Inside HMS-AGX – A Gentle Peek

```
/hms-agx
 ├─ packs/
 │    ├─ vision_ocr_v1/
 │    │     ├─ model.onnx
 │    │     └─ manifest.json
 │    └─ geo_nearest_v1/
 ├─ gate/
 │    └─ index.js           # 60 lines
 ├─ sandbox/
 │    └─ runner.py          # loads ONNX safely
 └─ credits/
      └─ meter.js
```

### 6.1 Plugin Manifest (10 Lines)

```jsonc
// packs/vision_ocr_v1/manifest.json
{
  "id"       : "VISION_OCR_V1",
  "functions": ["ocr"],
  "modelFile": "model.onnx",
  "maxTokens": 2048,
  "piiSafe"  : true
}
```

Manifest tells the Gate:

* Which functions are exposed.  
* Resource limits (`maxTokens`).  
* Whether output is free of raw PII.

### 6.2 Capability Gate Core (16 Lines)

```js
// gate/index.js
import { hasCredits } from '../credits/meter.js';
import { allow }      from '../policy/check.js';

export async function handle(req, res){
  const { capability } = req.body;
  if(!await allow(req.headers['x-api-key'], capability))
      return res.status(403).send('policy block');

  if(!hasCredits(req.headers['x-api-key']))
      return res.status(402).send('out of credits');

  const result = await sandboxRun(capability, req.body);
  res.json(result);
}
```

Line-by-line:

1-3  Imports helpers.  
4-6  Policy check against **HMS-CDF** packs.  
8-9  Credit enforcement.  
11   Delegate to the **sandbox**; return JSON only.

### 6.3 Credit Meter (8 Lines)

```js
// credits/meter.js
const usage = {};  // apiKey → calls this month

export function hasCredits(key){
  return (usage[key]||0) < 10000;  // free 10k calls
}

export function record(key){
  usage[key] = (usage[key]||0) + 1;
}
```

A toy in-memory meter; swap with Redis later.

---

## 7. Installing a New Pack in 3 Steps

1. **Drop Files**

```
packs/
 └─ speech_stt_v1/
      ├─ model.onnx
      └─ manifest.json
```

2. **Register in Marketplace**

```bash
curl -X POST http://mkt/listings \
  -d '{"id":"SPEECH_STT_V1","type":"agx-pack"}'
```

3. **Grant Policy**

Add to your agency’s CDF file:

```yaml
allow_capability:
  - SPEECH_STT_V1
```

No code changes for existing agents—they can now call `http://agx/speech/stt`.

---

## 8. Frequently Asked Questions

**Q: How is AGX different from a normal Python library?**  
It enforces **policy gates, credits, and sandboxing**—so even a powerful vision model can’t leak PII or bankrupt the GPU budget.

**Q: GPU vs. CPU?**  
Sandbox chooses the best available device; admins set per-pack limits in the manifest.

**Q: Can I chain packs?**  
Yes. Each call returns plain JSON, perfect for piping into the next pack or agent step.

**Q: What if a pack is compromised?**  
Sandbox blocks network and file writes; worst case the inference fails—data and infrastructure stay safe.

---

## 9. Key Takeaways

• HMS-AGX gives agents **plug-and-play super-powers**—vision, speech, geo—without compromising governance.  
• Every call passes a **Capability Gate** that checks policy, credits, and signatures.  
• Packs live in simple folders with a **manifest.json**; installation is drop-in.  
• Auditors trace usage via shared `traceId`, making AGX fully compatible with [HMS-MCP](06_model_context_protocol__hms_mcp__.md) and the platform’s audit trail.

---

### Up Next

Sometimes we need to **train** agents (and AGX packs) in a risk-free playground before deploying them to real citizens.  
Meet the virtual sandbox in [Chapter 14: Simulation & Training Environment (HMS-ESR)](14_simulation___training_environment__hms_esr__.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)