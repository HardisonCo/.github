# Chapter 8: Monitoring, Telemetry, and KPIs
*Coming from [Data Pipeline & Real-Time Analytics](07_data_pipeline___real_time_analytics_.md).*

---

## 1. Why Bother? – A 90-Second Story  

It’s April 14th.  The **Internal Revenue Service (IRS)** web-portal is receiving *millions* of last-minute tax filings per hour.  
If page latency silently doubles, frustrated citizens flood Twitter and congressional phone lines **before** engineers even notice.

A thin safety net—**Monitoring, Telemetry, and KPIs (Key Performance Indicators)**—lets us:

1. See CPU, memory, and error-rates in real time.  
2. Convert raw numbers into easy “traffic-light” dashboards.  
3. Page the on-call engineer *or* policy lead **before** Twitter does.

Think of it as placing traffic cameras, water meters, and satisfaction surveys all over our micro-service “city.”

---

## 2. Key Concepts (Plain-English Cheat-Sheet)

| Analogy | Real Term | 1-Sentence Beginner Explanation |
|---------|-----------|---------------------------------|
| Speedometer | **Telemetry** | Raw numbers a service emits every few seconds (CPU %, req/sec). |
| Weather Reporter | **Monitoring Service** | Collects telemetry from *all* cars and displays trends. |
| School Report Card | **KPI** | A *business-level* score (“99% e-filings under 2 s”). |
| Fire Alarm | **Alert** | Automatic page/email when any KPI crosses a bad line. |
| Control Room Screen | **Dashboard** | Web UI that shows green/yellow/red dials at a glance. |

---

## 3. Government Use Case: IRS “1040 E-File” Service  

Goal:  
• Track **HTTP error-rate** and **average response time** per minute.  
• Alert if error-rate > 3 % for 3 consecutive minutes.  
• Display a simple dashboard for managers.

We’ll build everything in ~60 lines of code.

---

## 4. Step 1 – Emit Telemetry from Each Microservice  

Add a `/metrics` endpoint to the existing FastAPI microservice you met in earlier chapters.

```python
# metrics_middleware.py  (≤18 lines)
import time, prometheus_client as prom
REQ_TIME = prom.Summary('req_ms', 'Request duration in ms')
ERRORS   = prom.Counter('http_errors', '500 responses')

def add_metrics(app):
    @app.middleware("http")
    async def _mw(request, call_next):
        start = time.time()
        resp = await call_next(request)
        REQ_TIME.observe((time.time()-start)*1000)
        if resp.status_code >= 500: ERRORS.inc()
        return resp

    @app.get("/metrics")
    def expose(): return prom.generate_latest()
```

Explanation:  
• `REQ_TIME` collects latency.  
• `ERRORS` increases on failures.  
• `/metrics` returns plain-text numbers Prometheus can scrape.

---

## 5. Step 2 – Collect & Store (Tiny “Prometheus” Clone)  

```python
# collector.py  (19 lines)
import requests, time
SERVICES = ["http://svc-a:8000/metrics",
            "http://svc-b:8000/metrics"]
STORE = {"lat": [], "err": []}

while True:
    for url in SERVICES:
        text = requests.get(url, timeout=1).text
        lat = float(_grep(text, "req_ms_sum"))
        cnt = float(_grep(text, "http_errors_total"))
        STORE["lat"].append(lat)
        STORE["err"].append(cnt)
    time.sleep(60)             # every minute

def _grep(txt, key):
    for line in txt.splitlines():
        if key in line: return line.split()[-1]
```

Explanation:  
• Polls each `/metrics` endpoint every minute.  
• Saves latest totals in `STORE` for quick math (e.g., deltas to compute rate).

---

## 6. Step 3 – Compute KPIs & Expose a Dashboard  

```python
# dashboard.py  (Flask, 17 lines)
from flask import Flask
import collector, statistics, time
app = Flask(__name__)

THRESH_ERR = 0.03      # 3 %

@app.route("/")
def home():
    lat = _avg_delta("lat")
    err = _err_rate()
    color = "green" if err < THRESH_ERR else "red"
    return (f"<h1>IRS 1040 E-File</h1>"
            f"<p>Avg latency (ms): {lat:.1f}</p>"
            f"<p style='color:{color}'>Error-rate: {err:.2%}</p>")

def _avg_delta(k):
    vals = collector.STORE[k][-10:]     # last 10 mins
    return statistics.mean(vals) if vals else 0

def _err_rate():
    e = collector.STORE["err"][-2:]     # last 2 records
    req = len(collector.STORE["lat"][-2:]) or 1
    return (e[-1]-e[0]) / req
```

Open the flask URL and watch the numbers update live.

---

## 7. Step 4 – Auto-Alert the On-Call  

```python
# alerter.py  (≤15 lines)
import smtplib, time, dashboard

while True:
    err = dashboard._err_rate()
    if err > dashboard.THRESH_ERR:
        msg = f"Subject: IRS E-File Alert\n\nError-rate {err:.1%}"
        smtplib.SMTP("mail.gov").sendmail("noreply@irs.gov",
                                          "oncall@irs.gov", msg)
        time.sleep(180)   # prevent alert-storm
    time.sleep(60)
```

Explanation:  
Fires an email when the KPI threshold exceeds 3 %.

---

## 8. What Happens Under the Hood?

```mermaid
sequenceDiagram
    participant SVC as IRS Microservice
    participant COL as Collector
    participant DASH as Dashboard
    participant ALT as Alerter

    SVC-->>COL: /metrics scrape
    COL-->>DASH: push computed KPI
    DASH-->>ALT: read KPI
    ALT-->>ALT: if >3 % → send email
```

Four actors, easy to trace.

---

## 9. Where Does This Plug into HMS-SCM?

```mermaid
flowchart TD
    subgraph Runtime
        SVC1[All\nMicroservices] --> COL
    end
    COL --> DASH
    COL -->|raw| [Data Pipeline](07_data_pipeline___real_time_analytics_.md)
    DASH --> [Management Layer](05_management_layer__hms_svc___hms_sys__.md)
    ALT --> OnCall[Engineer / Policy Lead]
```

*Telemetry* is produced by every service, stored by the **Collector**, visualized by **Dashboard**, and acted on by **Alerter**.  
Management rules (auto-scaling, budget caps) can *read the same KPIs* to adjust replicas—see [Management Layer](05_management_layer__hms_svc___hms_sys__.md).

---

## 10. Quick Tips & Best Practices  

1. **One Exporter Everywhere** – Drop `metrics_middleware.py` into *every* FastAPI service.  
2. **Tag Metrics** – Add labels like `agency="IRS", env="prod"` for slice-and-dice dashboards.  
3. **Keep KPIs Few & Clear** – Everyone understands “< 3 % errors” better than 40 obscure graphs.  
4. **Pair Alerts with Runbooks** – Email should link to “how to fix” docs.  
5. **Governance Integration** – Thresholds themselves are *policies*; store them in [HMS-GOV](02_governance_layer__hms_gov__.md) so they can be reviewed and versioned.

---

## 11. Recap  

• **Telemetry** = raw numbers; **Monitoring** collects them; **KPIs** turn them into human-readable health scores.  
• With < 60 lines you built exporters, a collector, a live dashboard, and auto-alerting.  
• These signals feed Management for auto-scaling and feed AI Agents for smart recommendations.

Next we’ll secure all this data and ensure it meets federal regulations in  
[Security & Compliance Framework](09_security___compliance_framework_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)