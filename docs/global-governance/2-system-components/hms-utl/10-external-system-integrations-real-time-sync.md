# Chapter 10: External System Integrations & Real-Time Sync
*(a.k.a. “Helping Old Mainframes Speak Millennial JSON”)*  

[← Back to Chapter&nbsp;9: Inter-Agency Communication Bus (HMS-A2A)](09_inter_agency_communication_bus__hms_a2a__.md)

---

## 1. Why Do We Need This Layer?

Picture the **Federal Student Aid (FSA)** office.  
When a loan is approved, three things must happen **outside** HMS within seconds:

1. A 1980s **COBOL mainframe** must mark “Loan Disbursed.”  
2. A commercial **bank’s API** must receive ACH instructions.  
3. The student’s **mobile app** must light up “Funds on the way!”  

If any of these systems get out of sync—duplication, delays, or missing records—the government may over-pay, under-pay, or face angry calls.

**External System Integrations & Real-Time Sync** ensures that:

* Legacy or vendor systems can connect with **tiny adapters** (no forklift upgrades).  
* Every insert/update/delete becomes a **change feed event** that the whole HMS ecosystem sees in near-real-time.  

Think of it as a **universal translator + live news ticker** for any outside database, API, or flat-file server.

---

## 2. Six Key Concepts (Sticker-Note Simple)

| Concept            | Plain-English Analogy                     | One-Line Meaning |
|--------------------|-------------------------------------------|------------------|
| Adapter            | Phone-charger plug adapter                | Small program that converts *that* system’s dialect to HMS JSON. |
| Connector          | Outlet strip                              | Library that knows how to talk to a source type (JDBC, SFTP, REST). |
| Change Feed        | News ticker                               | Ordered stream of “insert / update / delete” events. |
| Sync Cursor        | Dog-ear in a book                         | “I’ve processed up to event #987.” |
| Mapping Table      | Rosetta Stone                             | Column-to-field mapping between the legacy schema and HMS schema. |
| Retry Queue        | Parcel locker                             | Temporarily stores failed events for automatic re-delivery. |

Keep these six in mind—the rest is plumbing.

---

## 3. Walk-Through Use Case: Disbursing a Student Loan

### 3.1 Goal

When the **COBOL mainframe** inserts a new row:

```
LOAN_ID | AMT | STATUS
12345   | 5000| DISBURSED
```

…HMS should, **within 2 seconds**:

1. Emit `loan.disbursed` for dashboards.  
2. Call the **bank’s SaaS API** to push ACH details.  

### 3.2 Writing a COBOL Adapter (18 lines)

```python
# file: adapters/cobol_loan_adapter.py
from hms_sync import Connector, publish   # tiny helper lib

cobol = Connector.jdbc(
    dsn="jdbc:odbc:mainframe_ds",
    table="LOANS",
    key_col="LOAN_ID",
    cursor_file=".cursor"      # stores last seen row-id
)

MAPPING = {                    # Rosetta Stone
    "LOAN_ID": "loan_id",
    "AMT": "amount",
    "STATUS": "status"
}

for row in cobol.stream_changes(poll=1):   # 1-sec poll
    msg = { MAPPING[k]: v for k, v in row.items() }
    publish("loan.change", msg)            # goes to Change Feed
```

Explanation (beginner-friendly):
1. `Connector.jdbc` knows how to poll a mainframe table.  
2. `.stream_changes()` returns only **new or updated** rows.  
3. We rename columns via `MAPPING` to match modern JSON keys.  
4. `publish()` hands the event to the **Change Feed** bus.

### 3.3 Subscribing Downstream (15 lines)

```python
# file: listeners/bank_payout.py
from hms_sync import subscribe
from bank_sdk import send_ach

@subscribe("loan.change")
def handle(event):
    if event["status"] != "DISBURSED":
        return            # ignore other updates
    ach = {
        "loanId": event["loan_id"],
        "amount": event["amount"],
        "routing": "021000021",   # sample
    }
    ok = send_ach(ach)
    if not ok:
        raise RuntimeError("bank error")  # lands in Retry Queue
```

If the bank API is down, the adapter raises → event is re-queued and retried.

### 3.4 Live Dashboard Listener (9 lines)

```javascript
// file: mfe/Dashboard.jsx
import { useFeed } from "hms-sync-react";

export default function LoanTicker() {
  const events = useFeed("loan.change");
  return <ul>{
    events.slice(0,5).map(e =>
      <li key={e.id}>Loan {e.loan_id} → {e.status}</li>)
  }</ul>;
}
```

Zero server calls—the React hook tails the same Change Feed.

---

## 4. What Happens Under the Hood?

```mermaid
sequenceDiagram
    participant MF as COBOL Mainframe
    participant AD as Adapter
    participant BUS as Change Feed
    participant BK as Bank API
    MF->>AD: new row LOAN_ID=12345
    AD->>BUS: publish loan.change
    BK<<-BUS: subscription event
    BK->>BUS: ack / retry if fail
```

Only **4 actors** keep it digestible.

---

## 5. Peek Inside the Engine Room

### 5.1 Change-Feed Table (6 lines)

```sql
CREATE TABLE feed (
  id        BIGSERIAL PRIMARY KEY,
  channel   TEXT,
  payload   JSONB,
  ts        TIMESTAMP DEFAULT now()
);
```

Every `publish()` is a single `INSERT`.  
Subscribers use `SELECT * FROM feed WHERE id > $cursor`.

### 5.2 Minimal Publish Helper (10 lines)

```python
def publish(channel, payload):
    cur.execute(
      "INSERT INTO feed (channel,payload) VALUES (%s,%s)",
      (channel, json.dumps(payload))
    )
```

Dead simple so adapters can be written in <15 mins.

### 5.3 Retry Queue Worker (12 lines)

```python
def drain_retry():
    for evt in db.pop("retry", limit=100):
        try:
            deliver(evt)
        except Exception:
            db.push_back("retry", evt)   # exponential back-off
```

No human wakes up at 3 a.m.; retries keep rolling until success or max-age.

---

## 6. Tying Into Other HMS Layers

| Layer | Why It Cares | Example |
|-------|--------------|---------|
| [HMS-OMS / HMS-ACT](07_workflow_orchestration___task_queues__hms_oms___hms_act__.md) | A workflow step can wait for a `loan.disbursed` event instead of polling. |
| [HMS-A2A](09_inter_agency_communication_bus__hms_a2a__.md) | Change events destined for **another agency** are re-wrapped into A2A envelopes. |
| [HMS-DTA](05_data___privacy_management_hub__hms_dta__.md) | Adapters must attach **Data Tickets** when emitting sensitive payloads. |

Everything still respects the 3-floor rule from [Chapter&nbsp;1](01_multi_layered_system_architecture_.md):  
adapters live on the **middle floor**, never writing straight into basement DBs.

---

## 7. Hands-On Lab (90 Seconds)

```bash
git clone hms-utl
cd hms-utl/demo
docker compose up sync_bus bank_api   # starts Postgres + tiny bank mock

# 1. Start the COBOL adapter (simulated CSV)
python adapters/cobol_loan_adapter.py &

# 2. Insert a fake row into the "mainframe"
psql cobol -c "INSERT INTO LOANS VALUES (12345, 5000, 'DISBURSED');"

# 3. Watch the bank mock log
tail -f logs/bank_api.log
# → ACH sent for loan 12345
```

No refresh buttons—events propagate automatically.

---

## 8. Recap & What’s Next

You now know:

✔ How **Adapters + Connectors** bridge any legacy or SaaS system into HMS.  
✔ What a **Change Feed** is and why it beats nightly batch files.  
✔ How **Sync Cursors** & **Retry Queues** guarantee *at-least-once* delivery.  
✔ How other HMS layers subscribe to the same live stream.  

Ready to move **real money** once those events fire?  
Head over to [Financial Transaction & Clearinghouse (HMS-ACH)](11_financial_transaction___clearinghouse__hms_ach__.md).

---

*End of Chapter 10*

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)