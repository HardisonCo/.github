# Chapter 12: KPI & Metrics Dashboard

*[Link back to Chapter&nbsp;11: Observability & Audit Log](11_observability___audit_log_.md)*  

---

## 1. Why Do We Need a “Mission-Control” Screen?

Central use-case (2 sentences)  
• The **Federal Communications Commission (FCC)** launches a new AI-assisted license-renewal portal.  
• Commissioners want to watch—*in real time*—whether queue length, approval rate, and average turnaround are getting **better** (mission accomplished) or **worse** (roll it back!).

The **KPI & Metrics Dashboard** is that Houston-style Mission Control.  
It turns billions of audit events and ETL rows into **three things executives actually understand**: dials, graphs, and red/yellow/green lights.

---

## 2. Key Concepts (Plain-English Cheat-Sheet)

| Mission-Control Analogy | Term | 10-Second Newbie Take |
|-------------------------|------|-----------------------|
| Dial that shows “Fuel %” | KPI (Key Performance Indicator) | One number the boss cares about |
| Raw sensor reading | Metric | Building block feeding a KPI |
| Gauge, Line Graph | Widget | Visual element on the screen |
| Data pipe from rocket | Data Source | Where numbers come from (bus, DB, API) |
| “Every 5 sec” refresh | Interval | How often widget recomputes |
| Red flashing light | Threshold / Alert | Value outside safe range |

Keep this table open; the rest of the chapter is just these six ideas in action.

---

## 3. Hands-On: Build Your First Dashboard in < 10 Minutes

### 3.1 Declare the Dashboard (11 lines)

`dashboards/fcc_license.yaml`
```yaml
id: FCC_LICENSE_HEALTH
title: "FCC License Renewal – Mission Control"
refresh_every: 5s
widgets:
  - id: QUEUE_LEN
    type: gauge
    source: metric:license_queue_length
    green_under: 50
    red_over: 150
  - id: AVG_TAT
    type: line
    source: metric:avg_turnaround_sec
    window: 1h
  - id: APPROVAL_RATE
    type: spark
    source: metric:approval_percent
    window: 24h
```
Explanation  
• YAML is just **metadata**—no code here.  
• Each widget points to a **metric** (next section) and how to color it.

---

### 3.2 Emit Metrics (Aggregator in 18 lines)

`metrics/aggregator.py`
```python
from hms_bus import subscribe          # see Chapter 8
import time, collections

METRICS = collections.defaultdict(int)
WINDOW  = collections.defaultdict(list)   # time-series buckets

@subscribe("LicenseSubmitted")
def on_submit(_):
    METRICS["license_queue_length"] += 1

@subscribe("LicenseApproved")
def on_approve(evt):
    METRICS["license_queue_length"] -= 1
    dt = evt.payload["seconds_in_system"]
    WINDOW["turnaround"].append(dt)
    METRICS["approval_count"] += 1

def compute():
    METRICS["avg_turnaround_sec"] = (
        sum(WINDOW["turnaround"][-3600:]) / max(1, len(WINDOW["turnaround"][-3600:]))
    )
    METRICS["approval_percent"] = (
        METRICS["approval_count"] * 100 / max(1, METRICS["approval_count"] + METRICS["reject_count"])
    )

while True:
    compute()
    time.sleep(5)
```
What happens?  
1. **Subscribes** to live events (`LicenseSubmitted`, `LicenseApproved`).  
2. Keeps in-memory counters & simple arrays.  
3. Every 5 s computes fresh **metrics** that widgets will read.

---

### 3.3 Serve the Metrics (8 lines)

`metrics/api.py`
```python
from fastapi import FastAPI
from aggregator import METRICS

app = FastAPI()

@app.get("/metric/{name}")
def get_metric(name: str):
    return {"value": METRICS.get(name, 0)}
```
Now any widget can hit `/metric/avg_turnaround_sec` and get JSON.

---

### 3.4 Render the Dashboard (Frontend Stub – 18 lines)

`frontend/dash.js`
```javascript
// Very tiny widget runner (uses plain fetch)
const cfg = await (await fetch('/dash/fcc_license.yaml')).text();
const dash = YAML.parse(cfg);

setInterval(() => dash.widgets.forEach(async w => {
  const m = await fetch('/metric/' + w.source.split(':')[1]).then(r=>r.json());
  const v = m.value;
  document.getElementById(w.id).innerText = v;
  if (w.green_under && v < w.green_under) flash(w.id, 'green');
  else if (w.red_over && v > w.red_over)  flash(w.id, 'red');
}), dash.refresh_every_ms || 5000);

function flash(id,color){
  const el = document.getElementById(id);
  el.style.background = color; setTimeout(()=>el.style.background='',500);
}
```
Explanation  
• Fetches the YAML, then every 5 s fetches each metric API.  
• Simple DOM updates = instant dashboard, zero React or D3 required.

---

## 4. What Happens Under the Hood?

```mermaid
sequenceDiagram
  participant BUS as Event&nbsp;Bus
  participant Agg as Metric&nbsp;Aggregator
  participant API as Metric&nbsp;API
  participant FG as Front-End
  participant Exec as Commissioner

  BUS-->>Agg: License events
  Agg->>API: Updates in-memory metrics
  FG->>API: GET /metric/…
  API-->>FG: {"value":123}
  FG-->>Exec: Render widgets
```
Only **5 participants**—easy to troubleshoot.

---

## 5. Tiny Peek at the Internal Wiring

### 5.1 Dashboard Registry (≤ 16 lines)

`kpi/registry.py`
```python
import yaml, glob

DASHES = {}
for y in glob.glob("dashboards/*.yaml"):
    spec = yaml.safe_load(open(y))
    DASHES[spec["id"]] = spec

def list_dashboards():
    return [{"id": d["id"], "title": d["title"]} for d in DASHES.values()]

def get_widgets(dash_id):
    return DASHES[dash_id]["widgets"]
```
• **Registry** is just a dict loaded at startup.  
• No DB necessary for a starter project.

### 5.2 Permissions (rides on Chapter 5)

Add to `rules.yaml` in [Access & Identity](05_access___identity_management_.md):

```yaml
  FCC_COMMISSIONER:
    can:
      - ["GET", "/dash/*"]
```
So only commissioners see the dashboard.

---

## 6. Safety Rails You Already Know

| Prior Layer | How It Helps the Dashboard |
|-------------|----------------------------|
| [Governance](01_governance_layer__hms_gov__.md) | YAML dashboards require change tickets. |
| [Policy Engine](02_policy___process_engine_.md) | Checks widget thresholds match policy (e.g., queue must stay < 200). |
| [Versioning](03_versioning___rollback_mechanism_.md) | Bad widget layout? Point `current` back to prior YAML in seconds. |
| [Security Seals](04_security___compliance_framework_.md) | Aggregator & frontend images carry Seal IDs. |
| [IAM](05_access___identity_management_.md) | Only roles like `FCC_COMMISSIONER` fetch metrics. |
| [Audit Log](11_observability___audit_log_.md) | Every widget fetch auto-emits `DASH_VIEWED` for traceability. |

---

## 7. Common Pitfalls & Quick Fixes

| Oops! | Why It Happens | Fast Fix |
|-------|----------------|----------|
| Graph jumps every refresh | Aggregator emits NaN on divide-by-zero | Use `max(1, denominator)` like in sample code. |
| Red light stays on after fix | Browser caching old metric | Append `?ts=` + Date.now() to the fetch URL. |
| Widget flickers | Duplicate IDs in YAML | Linter warns during Governance review—rename the widget. |

---

## 8. Mini-Lab: Add an Alert E-mail in 3 Steps

1. Append to widget YAML:  
   ```yaml
   alerts:
     when: red_over
     notify: "kpi-alerts@fcc.gov"
   ```
2. Add a 6-line cron job:

```python
# alert_daemon.py
import requests, smtplib, time
while True:
    w = requests.get('/metric/license_queue_length').json()['value']
    if w > 150:
        smtplib.SMTP('mail').sendmail('bot','kpi-alerts@fcc.gov',f'Queue={w}')
    time.sleep(60)
```
3. Trigger a load test; watch the e-mail arrive.  
You just built *lights + sirens* in under 20 lines!

---

## 9. What You Learned

✓ Difference between **metrics** and **KPIs**, and how widgets display them.  
✓ Authored a dashboard in 11-line YAML, built a metric aggregator & micro-API (< 20 lines each).  
✓ Understood the data flow from event bus ➜ aggregator ➜ API ➜ browser.  
✓ Saw how Governance, IAM, Security, and Audit automatically wrap the dashboard.  
✓ Added an alert with just a few extra lines.

Ready to see how **AI bots** will use these live KPIs to self-tune policies (or ask a human for help)?  
Jump to [AI Representative Agent (HMS-A2A)](13_ai_representative_agent__hms_a2a__.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)