# Chapter 3: Data Privacy & Compliance Engine  
*(“The Shredder, Stamp, and Filing Cabinet of HMS-MCP”)*  

[← Back to Chapter 2: Governance Layer (HMS-GOV)](02_governance_layer__hms_gov__.md)

---

## 1. Motivation — The “FOIA Packet” Story

The **Social Security Administration (SSA)** just received a *Freedom of Information Act* (FOIA) request from a journalist.  
SSA must email 1,200 pages of benefit determinations **tomorrow morning**, but:

1. Every page contains citizens’ Social Security Numbers (SSNs).  
2. HIPAA rules forbid leaking any medical detail.  
3. An inspector may audit the whole process next month.

How do we:

* Black-out SSNs automatically?  
* Keep medical info out of the packet?  
* Prove—*without extra work*—that we followed HIPAA and FOIA rules?

Answer: **Data Privacy & Compliance Engine** (DPCE).  

Think of DPCE as a super-powered office clerk who can:  
• **Detect** sensitive data,  
• **Redact** or encrypt it,  
• **Delete** it when the law says “time’s up,” and  
• **Stamp** the paperwork that proves we did everything by the book.

---

## 2. Key Building Blocks (Beginner Edition)

| Nickname | What It Does | Real-World Analogy |
|----------|--------------|--------------------|
| PII Radar | Finds Social Security #s, addresses, health codes, etc. | Highlighter pen that marks secrets |
| Redaction Roller | Scrubs or masks what the radar finds | Black marker that blacks out text |
| Retention Timer | Counts days until data must be deleted | Sticky note saying “Shred on 2029-07-01” |
| Evidence Printer | Creates PDFs/CSVs for auditors | Clerk stamping *“COMPLIANT”* and filing |

All four pieces live inside DPCE and work together.

---

## 3. Using DPCE in 3 Easy Steps

We will redact an SSA PDF, delete it after 30 days, and generate an audit receipt.

### 3.1 Prepare a Privacy Policy File (YAML)

`ssa_foia_policy.yml`

```yaml
agency: SSA
targets:
  - "*.pdf"
pii_types: [ "SSN", "HIPAA_MEDICAL_TERM" ]
redact_mode: MASK          # options: MASK, REMOVE, ENCRYPT
retention_days: 30
compliance_labels: [ "FOIA", "HIPAA" ]
```

**Explanation**  
• `targets` – match all PDFs.  
• `pii_types` – what to look for.  
• `redact_mode` – here we replace SSNs with ***-**-****.  
• `retention_days` – DPCE will auto-delete the file after 30 days.  
• `compliance_labels` – tags that appear in the evidence report.

### 3.2 Call the DPCE API

```python
import requests, yaml, pathlib

policy = yaml.safe_load(open("ssa_foia_policy.yml"))
file_to_send = pathlib.Path("benefits_batch.pdf").read_bytes()

resp = requests.post(
    "https://dpce.gov/api/redact",
    files={"document": file_to_send},
    json=policy,
    timeout=20
)

open("redacted.pdf", "wb").write(resp.content)
print("✅ Redacted file saved!")
```

What happened?  
1. We uploaded the PDF + policy.  
2. DPCE returned a **clean** PDF with SSNs masked.  
3. Behind the scenes DPCE also queued a “delete on +30 days” job and logged everything.

### 3.3 Fetch the Compliance Receipt

```python
ticket = resp.headers["X-DPCE-Ticket"]      # e.g. "TCK-9123"
pdf = requests.get(f"https://dpce.gov/api/receipt/{ticket}").content
open("compliance_receipt.pdf", "wb").write(pdf)
print("📄  Receipt downloaded!")
```

The receipt is a human-readable PDF:

```
Data Privacy & Compliance Receipt
Ticket: TCK-9123
Agency: SSA
Actions:
  • Masked 214 SSNs
  • Removed 12 HIPAA terms
  • Scheduled deletion 2024-11-05
Status: COMPLIANT
Signatures: DPCE, HMS-GOV
```

Auditors love this.

---

## 4. How It Works Under the Hood (5-Step Tour)

```mermaid
sequenceDiagram
participant User as SSA App
participant DPCE as Data Privacy&nbsp;Engine
participant GOV as HMS-GOV
participant STORE as Secure Storage
participant AUD as Audit&nbsp;Log

User->>DPCE: Upload PDF + policy
DPCE->>GOV: Validate policy
GOV-->>DPCE: ✅ OK
DPCE->>DPCE: Detect & redact PII
DPCE->>STORE: Save clean file
DPCE->>AUD: Write immutable log
DPCE-->>User: Return redacted PDF + Ticket
```

Key points:  
• HMS-GOV (from [Chapter 2](02_governance_layer__hms_gov__.md)) confirms the policy is legal.  
• DPCE owns the heavy lifting (detection, redaction, timers).  
• Audit logs are append-only for inspectors.

---

## 5. A Peek at Each Component’s Code (Ultra-Simple)

> NOTE: Real code spans many files. We show only the core ideas—each under 20 lines.

### 5.1 PII Detector (`pii.py`)

```python
import re

SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

def find_pii(text):
    for m in SSN.finditer(text):
        yield ("SSN", m.start(), m.end())
```

Scans text and yields positions of SSNs.

### 5.2 Redaction Roller (`redact.py`)

```python
from pii import find_pii

def mask(text):
    out = list(text)
    for _, s, e in find_pii(text):
        out[s:e] = "***-**-****"
    return "".join(out)
```

Replaces each SSN with masked version.

### 5.3 Retention Scheduler (`retention.py`)

```python
import datetime, sqlite3

def schedule_deletion(ticket_id, days):
    delete_on = datetime.date.today() + datetime.timedelta(days=days)
    with sqlite3.connect("retention.db") as db:
        db.execute("INSERT INTO jobs VALUES (?, ?)", (ticket_id, delete_on))
```

Stores a simple record; a cron job later performs the deletion.

### 5.4 Evidence Generator (`evidence.py`)

```python
from fpdf import FPDF

def make_receipt(ticket, actions, delete_on):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in actions:
        pdf.multi_cell(0, 10, line)
    pdf.multi_cell(0, 10, f"Retain until: {delete_on}")
    pdf.output(f"{ticket}.pdf")
```

Creates the PDF receipt.

Even with these toy snippets you can see the **flow**: detect → redact → schedule → print receipt.

---

## 6. Folder Map (Partial)

```
hms-dpce/
 ├─ api/               # FastAPI or Flask endpoints
 ├─ pii.py             # detectors
 ├─ redact.py          # masking logic
 ├─ retention.py       # timers
 ├─ evidence.py        # PDF builder
 ├─ policies/          # uploaded YAML files
 └─ audits/            # append-only logs
```

Each micro-file is tiny but together they guarantee privacy.

---

## 7. DPCE & The Rest of HMS-MCP

• Rules arrive from [Governance Layer (HMS-GOV)](02_governance_layer__hms_gov__.md).  
• User permissions are checked via [Role-Based Access Control & Multi-Tenant Security](04_role_based_access_control__rbac____multi_tenant_security_.md) (next chapter!).  
• Metrics flow into the [Monitoring & Metrics Dashboard](16_monitoring___metrics_dashboard_.md).  

Everything is discoverable thanks to the [Microservice Mesh & Service Discovery](06_microservice_mesh___service_discovery_.md).

---

## 8. Recap

You learned how DPCE:

1. Detects and redacts sensitive data (PII Radar + Redaction Roller).  
2. Enforces legal retention windows (Retention Timer).  
3. Autogenerates auditor-friendly evidence (Evidence Printer).  
4. Cooperates with HMS-GOV and upcoming RBAC for end-to-end compliance.

With just a YAML file and a simple API call, federal agencies can protect citizens’ data **and** keep inspectors happy.

---

Ready to see how user roles determine **who** can view or edit those redacted PDFs?  
Jump to [Chapter 4: Role-Based Access Control (RBAC) & Multi-Tenant Security](04_role_based_access_control__rbac____multi_tenant_security_.md).

---

Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge)