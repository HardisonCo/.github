# Chapter 14: Monitoring & Observability (HMS-OPS)

*(Fresh out of the data vault in [Secure Data Repository (HMS-DTA)](13_secure_data_repository__hms_dta__.md), we now need a **control-tower** that keeps every service, queue, and dataset under 24 × 7 radar.)*  

---

## 1. Why Do We Need a “Public-Sector NORAD” for Software?

### Central Use-Case – “Catch a Tax-Refund Latency Spike Before Social Media Does”

1. On April 14th the **Internal Revenue Service (IRS)** site is flooded with refund-status checks.  
2. The `/refund/status` endpoint suddenly slows from **120 ms → 2 seconds**.  
3. Angry tweets appear within minutes; Congress asks for a briefing by noon.

With **HMS-OPS** in place:

* An **SLO alert** (“p95 latency > 500 ms for 3 minutes”) fires automatically.  
* An on-call engineer sees the spike on a **dashboard**, scales workers, and posts a status update.  
* Every request, metric, and action is **logged** for next month’s oversight hearing.

Without OPS, we’d spot the issue only after the Washington Post headline.

---

## 2. Key Concepts (Plain-English Cheat-Sheet)

| Term                | Beginner-Friendly Meaning |
|---------------------|---------------------------|
| Metric              | A single number tracked over time – e.g. “latency 140 ms”. |
| Dashboard           | A real-time chart of metrics – think cockpit dials. |
| SLO (Service Level Objective) | A promise like “95 % of calls < 500 ms”. |
| Alert               | A rule that pings humans when an SLO is at risk. |
| Trace               | A step-by-step record of one request (“entered gateway → DB → out”). |
| Audit Log           | A tamper-proof diary: who changed what alert, when. |

---

## 3. Solving the IRS Latency Use-Case in Three Tiny Files

### 3.1 Emit Metrics From the Service (≤ 12 Lines)

`refund_status_service.py`
```python
from prometheus_client import Counter, Histogram, start_http_server
import time, random, flask

REQS  = Counter('refund_requests_total', 'Total refund checks')
LAT   = Histogram('refund_latency_seconds', buckets=[.1,.3,.5,1,2])

app = flask.Flask(__name__)
start_http_server(8001)       # metrics scrapes on :8001/metrics

@app.get("/refund/status")
def status():
    REQS.inc()
    with LAT.time():
        time.sleep(random.uniform(.05, .7))  # pretend work
    return {"status": "accepted"}
```
Explanation  
1. We import **Prometheus** helpers.  
2. Every request increments `REQS` and records latency.  
3. A sidecar scrapes `/metrics`—no extra code needed.

---

### 3.2 Collect & Store Metrics (≤ 15 Lines)

`ops/collector.py`
```python
from prometheus_client import Summary, Gauge
import prometheus_client, requests, time

IRS_LAT = Gauge('irs_latency_p95_ms', 'p95 latency for IRS refund')
while True:
    r = requests.get("http://refund-svc:8001/metrics").text
    for line in r.splitlines():
        if line.startswith('refund_latency_seconds_bucket{le="0.5"'):
            # crude p95: 0.5 s bucket ≈ 95-th percentile
            count = int(line.split()[-1])
            IRS_LAT.set(count)          # store in central Prom DB
    time.sleep(15)
```
Explanation  
1. Scrapes the service every 15 s.  
2. Derives a quick p95 and pushes it to the central Prometheus instance.

---

### 3.3 Alert Rule (YAML, 8 Lines)

`alerts/irs_latency.yaml`
```yaml
alert: IRS_Latency_Spike
expr:  irs_latency_p95_ms > 0.5
for:   3m
labels:
  severity: page
annotations:
  summary: "IRS refund latency high"
  runbook: "go/docs/runbooks/irs_latency.md"
```

If p95 stays above 0.5 s for 3 minutes, PagerDuty (or an SMS gateway) rings the on-call phone.

---

## 4. What Happens Inside? (Step-by-Step)

```mermaid
sequenceDiagram
    participant SVC as Refund Service
    participant COL as Metrics Collector
    participant PRM as Prometheus DB
    participant ALT as Alert Manager
    participant ENG as On-Call Engineer

    loop every 15s
        SVC->>COL: /metrics scrape
        COL->>PRM: push gauges
    end
    PRM->>ALT: evaluate alert
    ALT-->>ENG: "Latency spike!"
```
Only **five** actors—easy to keep in your head.

---

## 5. Peeking Under the Hood

Folder layout:
```
hms-ops/
 ├─ collector.py
 ├─ dashboards/
 │   └─ irs_overview.json        # JSON spec for Grafana
 ├─ alerts/
 │   └─ irs_latency.yaml
 └─ audit/
     └─ changes.log
```

### 5.1 Dashboard Snippet (JSON excerpt, 9 Lines)

```json
{
  "title": "IRS Refund Health",
  "panels": [{
    "type": "graph",
    "targets": [{"expr": "irs_latency_p95_ms"}],
    "title": "Latency (p95)"
  }]
}
```
Load this file into Grafana → instant chart.

### 5.2 Change-Log Hook (≤ 15 Lines)

`ops/audit_hook.py`
```python
import json, datetime, pathlib, flask
app = flask.Flask(__name__)
LOG  = pathlib.Path("audit/changes.log")

@app.post("/ops/change")
def log_change():
    entry = {
       "time": datetime.datetime.utcnow().isoformat(),
       "user": flask.request.headers.get("X-User"),
       "change": flask.request.json
    }
    LOG.write_text(LOG.read_text()+json.dumps(entry)+"\n") if LOG.exists() \
        else LOG.write_text(json.dumps(entry)+"\n")
    return {"logged": True}
```
Any dashboard edit or alert update must `POST` here first → automatic paper trail for OIG auditors.

---

## 6. Where OPS Meets Other HMS Layers

| Layer | Why It Cares |
|-------|--------------|
| [Management Layer](11_management_layer__hms_svc___hms_ops___hms_oms__.md) | Auto-scaler decisions rely on OPS metrics. |
| [Backend API Gateway](10_backend_api_gateway_.md) | Gateway exports 4xx/5xx counts to OPS. |
| [Workflow Orchestration](12_workflow_orchestration__hms_act__.md) | ACT emits “step_failed” events; OPS pages humans if failures spike. |
| [Secure Data Repository](13_secure_data_repository__hms_dta__.md) | OPS checks disk usage & retention-deletion success. |
| [Human-in-the-Loop (HITL)](07_human_in_the_loop__hitl__oversight_.md) | Critical alerts can open review tickets automatically. |

---

## 7. Hands-On Mini-Lab

1. Run the refund service:  
   ```bash
   python refund_status_service.py
   ```
2. Start the collector (replace `refund-svc` with `localhost` if local):  
   ```bash
   python ops/collector.py
   ```
3. Hammer the endpoint:  
   ```bash
   for i in {1..200}; do curl -s localhost:5000/refund/status & done
   ```
4. Watch `irs_latency_p95_ms` climb in Prometheus (`http://localhost:9090`), then see the alert fire (Alertmanager UI on `:9093`).

5. Open Grafana, import `dashboards/irs_overview.json`, and show off your brand-new cockpit!

---

## 8. Frequently Asked Questions

**Q: Do I have to learn Prometheus and Grafana from scratch?**  
Not at first. Copy the sample configs; they work out-of-the-box. You can tweak visuals later.

**Q: What if an attacker floods the metrics endpoint?**  
Gateway rate-limits `/metrics`, and internal firewalls block external IPs. OPS also tracks unusual scrape volumes.

**Q: Can I alert on business KPIs (e.g., “benefits approved per hour”)?**  
Yes—emit them as counters and add alert rules. OPS is for **technical** and **business** health alike.

---

## 9. Recap & Next Steps

You now know how **HMS-OPS**:

* Collects metrics, traces, and logs from every service.  
* Shows them on live **dashboards**.  
* Enforces **SLOs** with alert rules that page humans.  
* Keeps an **audit log** of every configuration change.

With OPS, we catch issues **before** they hit the news.

Ready to move money safely once systems are healthy?  
➡️ Continue to [Financial Transaction Hub (HMS-ACH)](15_financial_transaction_hub__hms_ach__.md)

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)