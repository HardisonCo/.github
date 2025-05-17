# Chapter 10: Metrics & Observability Pipeline
*(Filename: 10_metrics___observability_pipeline_.md)*  

[← Back to Chapter 9: Human-in-the-Loop (HITL) Oversight](09_human_in_the_loop__hitl__oversight_.md)

---

## 1. Why Should We “Count Every Click”?

On April 15th (Tax Day), millions of citizens hit the IRS e-file portal.  
If page loads creep from **300 ms** to **5 s**, complaints explode and the headline writes itself.

The **Metrics & Observability Pipeline** is our digital **Government Accountability Office (GAO)**:  
it sits in the balcony 24 × 7, counting UI clicks, API latencies, and AI success rates, then shouts *“Something’s off!”* before CNN does.

We will:

1. Attach a tiny counter to an endpoint (`/efile/submit`).  
2. Ship those numbers to a central **Collector**.  
3. Draw a live chart that a non-tech program officer can understand.  
4. Trigger an alert + auto-rollback if error rate spikes—closing the loop with the [AI Representative Agent](08_ai_representative_agent__hms_a2a__.md).

---

## 2. Key Ideas in Plain English

| Term                | Beginner Analogy                                    |
|---------------------|-----------------------------------------------------|
| Metric              | A single fact (“/efile/submit took 420 ms”).        |
| Log                 | A diary entry (“user 123 failed validation”).       |
| Trace               | Breadcrumb trail of one request through services.   |
| Dashboard           | Wall of TV screens in a NASA control room.          |
| SLO (Objective)     | “95 % of tax returns processed < 1 s.”              |
| Anomaly Detector    | Radar gun screaming “speed limit exceeded!”.        |
| Collector           | The mailroom—bundles incoming envelopes (metrics).  |

*Keep these six words in mind; nothing in this chapter is scarier than them.*

---

## 3. A 3-Minute “Hello Metrics”

### 3.1 Instrument a Single API Route (≤ 15 lines)

```js
// File: api/routes/efile.js
import { Counter, Histogram } from '@/telemetry.js'

const hits      = new Counter('efile_hits_total')
const durations = new Histogram('efile_latency_ms')

app.post('/efile/submit', async (req, res) => {
  const stop = durations.startTimer()     // ① start stopwatch
  hits.inc()                              // ② count the hit
  // ... existing business logic ...
  stop()                                  // ③ record ms
  res.sendStatus(202)
})
```

What happened?  
1. `startTimer()` remembers *now*.  
2. `inc()` bumps a plain integer.  
3. `stop()` calculates “duration” and stores it.

No external servers, no PhD—just three function calls.

---

### 3.2 Forwarding From the Front-End (≤ 10 lines)

```js
// File: widgets/EFileButton.vue (snippet)
import { recordMetric } from '@/services/metricsClient'
function clickHandler() {
  recordMetric('efile_click')   // async fire-and-forget
  emit('submit')
}
```

Now every citizen click is counted alongside back-end latencies.

---

## 4. How the Pieces Talk (Step-By-Step)

```mermaid
sequenceDiagram
    participant FE as Browser
    participant COL as Metrics Collector
    participant DB as Time-Series DB
    participant DAS as Dashboard
    participant AL as Alerting Bot

    FE->>COL: JSON {metric:"efile_latency_ms",value:420}
    COL->>DB: write point
    DB-->>DAS: streaming data
    AL<-DB: threshold breach? (yes) 
    AL-->>Ops: "Latency > 1 s – roll back!"
```

*Only five actors—promise kept.*

---

## 5. Peeking Under the Hood

### 5.1 The Tiny Collector (≤ 20 lines)

```js
// File: metrics/collector.js
import express from 'express'
const app = express()
app.use(express.json())

app.post('/metrics', (req, res) => {
  bus.emit('metric', req.body)     // global EventEmitter
  res.sendStatus(204)
})

app.listen(7070)   // one port, done
```

Every service—front-end or back-end—`POST`s to `http://collector:7070/metrics`.

### 5.2 Writing to a Time-Series DB (Stub ≤ 15 lines)

```js
// File: metrics/writer.js
import bus from './eventBus.js'
import { insert } from './tinyTsDb.js'   // fake DB for demo

bus.on('metric', (point) => {
  insert(point.metric, point.value, Date.now())
})
```

You can swap `tinyTsDb.js` for InfluxDB or Prometheus later—API stays the same.

---

### 5.3 A One-Rule Anomaly Detector (≤ 20 lines)

```js
// File: metrics/detector.js
import { queryLastN } from './tinyTsDb.js'
import bus from './eventBus.js'

setInterval(() => {
  const vals = queryLastN('efile_latency_ms', 50)   // last 50 samples
  const avg  = vals.reduce((a,b)=>a+b,0) / vals.length
  if (avg > 1000) {                // > 1 s
     bus.emit('alert', {metric:'efile_latency_ms', avg})
  }
}, 30_000)   // run every 30 s
```

When latency crosses 1 s, we broadcast an `alert` event.  
The [AI Representative Agent](08_ai_representative_agent__hms_a2a__.md) or on-call engineer can subscribe.

---

### 5.4 A 10-Line Dashboard Widget

```vue
<!-- File: widgets/LatencyChart.vue -->
<template><LineChart :data="series" /></template>

<script setup>
import { ref, onMounted } from 'vue'
const series = ref([])
onMounted(async ()=>{
  const res = await fetch('/api/metrics?m=efile_latency_ms')
  series.value = await res.json()   // [{t:..., v:420}, …]
})
</script>
```

This simple chart appears on the **Operations Dashboard** page—visible to both engineers and policy officers.

---

## 6. Feeding Data Back to Policy & AI

1. The anomaly detector fires `alert`.  
2. [HMS-A2A](08_ai_representative_agent__hms_a2a__.md) listens, pauses the risky deployment, and files a **digital motion** to roll back.  
3. [HITL Oversight](09_human_in_the_loop__hitl__oversight_.md) sees a pre-filled “Rollback” proposal—one click to approve.  
4. Metrics instantly confirm latency drops back to normal, closing the loop.

---

## 7. Real-World Government Examples

| Agency                                | Metric Example                               |
|---------------------------------------|----------------------------------------------|
| Secret Service                        | Fraud-detection model false-positive rate.   |
| Office of Multifamily Housing (HUD)   | Average loan-approval days per region.       |
| Bureau of Land Management (BLM)       | GIS map-tile render time during wildfire season. |

All follow the same pattern: **collect → store → visualize → alert → improve.**

---

## 8. Frequently Asked Questions

**Q: Does every micro-service need its own collector?**  
A: No. One side-car **Collector** pod per Kubernetes node is plenty; services write to `localhost:7070`.

**Q: Won’t extra API calls slow the app?**  
A: Each metric POST is non-blocking (<1 KB). For high-traffic paths, batch metrics every 5 seconds.

**Q: Can we keep sensitive data out of metrics?**  
A: Yes. A sanitizer in `telemetry.js` strips PII fields before sending—required by [Governance](06_governance_layer__hms_gov__.md).

**Q: How do I set an SLO?**  
A: Add a JSON file:  
```json
{ "metric":"efile_latency_ms", "target":800, "window":"5m" }
```  
The detector reads it instead of hard-coding `1000 ms`.

---

## 9. Recap

You now know how to:

• Drop 3-line snippets that count hits & durations.  
• Ship data to one lightweight collector and DB.  
• Draw a chart and trigger an alert with < 40 lines of code.  
• Let the AI agent and human reviewers react—closing the feedback loop.

Ready to see how HMS-MKT syncs *external* systems (e.g., Treasury, DMV) in real time?  
Continue to [Chapter 11: External System Sync Adapter](11_external_system_sync_adapter_.md) →

---

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)