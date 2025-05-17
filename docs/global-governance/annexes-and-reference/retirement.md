# HMS-ACH Integration with 

# Integration of HMS-ACH with the RETIREMENT Mission

This document outlines how the Health Management System’s Automated Clearing House component (HMS-ACH) can integrate with and enhance the RETIREMENT mission. It covers specific capabilities, technical integration details, stakeholder benefits, implementation considerations, and illustrative use cases.

---

## 1. HMS-ACH Capabilities Addressing RETIREMENT’s Mission Needs

1. **Automated Benefit Disbursement**  
   - Batch and real-time ACH credit for pension, annuity, and insurance reimbursements  
   - NACHA-compliant file generation, pre-validation, and transmission  

2. **Claims and Premium Refund Processing**  
   - Automatic adjudication of health-care premium refunds for retirees  
   - Automated exception routing for incomplete claims  

3. **Reconciliation & Reporting**  
   - Daily reconciliation reports against bank acknowledgements  
   - Dashboards for payment status, exceptions, and audit trails  

4. **Error Handling & Exception Workflows**  
   - Automated identification of NOC/R06 returns  
   - Workflow-driven resolution (re-submit, notify stakeholder, escalate)  

5. **Security & Compliance**  
   - End-to-end encryption (TLS 1.2+) and tokenization of account data  
   - Role-based access control and audit logging (FISMA, FedRAMP, NACHA)  

---

## 2. Technical Integration Overview

### 2.1 APIs & Data Flows

1. **RESTful Payment Instruction API**  
   - Endpoint: `POST /api/v1/ach/payments`  
   - Payload: retiree identifier, bank routing/account, amount, payment type  
   - Response: payment `jobId`, initial validation status  

2. **Webhooks for Status Updates**  
   - HMS-ACH pushes to RETIREMENT’s webhook endpoint on:  
     - `payment.acknowledged`  
     - `payment.completed`  
     - `payment.exception`  

3. **File-Based Exchange (Optional)**  
   - Secure SFTP drop for NACHA formatted files  
   - HSMS-ACH polls `/incoming` directory, processes, and writes `/outgoing/ack`  

### 2.2 Authentication & Authorization

- **OAuth 2.0 Client Credentials**  
  - Scopes: `ach:create`, `ach:query`, `ach:reports`  
- **Mutual TLS (mTLS)** for file-based channels  
- **JWT Tokens** signed by RETIREMENT’s Identity Provider (IdP)  

### 2.3 Data Mapping & Schema

| RETIREMENT Field     | HMS-ACH JSON Field   | Notes                         |
|----------------------|----------------------|-------------------------------|
| retiree_id          | customerReference    | Unique 10-digit ID            |
| bank_routing_number | routingNumber        | 9-digit numeric               |
| bank_account_number | accountNumber        | Up to 17 alphanumeric         |
| payment_amount      | amount.value         | Decimal, USD                  |
| payment_type        | standardEntryClass   | “PPD” for person-to-person    |
| scheduled_date      | settlementDate       | YYYY-MM-DD                    |

---

## 3. Benefits & Measurable Improvements

| Stakeholder          | Benefit                             | Key Metric                       |
|----------------------|-------------------------------------|----------------------------------|
| Retirees             | Faster, reliable payments           | ⬇ Processing time: 2 days → 2 hours |
| Finance/Accounting   | Reduced manual reconciliation       | ⬇ Exceptions by 90%               |
| IT & Ops             | Simplified exception workflows      | ⬇ Mean Time to Resolution (MTTR) by 70% |
| Compliance/Audit     | Improved traceability & audit logs  | 100% NACHA compliance             |
| Leadership           | Cost savings                        | ⬇ FTE hours: 200 → 50/month       |

---

## 4. RETIREMENT-Specific Implementation Considerations

1. **Data Privacy & PII Handling**  
   - Ensure HIPAA-aligned encryption at rest/in transit  
   - Mask account numbers in UI and logs  

2. **Cut-over & Roll-out Strategy**  
   - Parallel-run with legacy payments for 2 pay cycles  
   - Incremental onboard: first health-premium refunds, then pensions  

3. **Exception Management Integration**  
   - Hook into existing RETIREMENT case-management platform  
   - Define SLA—for example, auto-resolve simple returns in 4 hours  

4. **Regulatory & Audit Requirements**  
   - Pre-go-live NACHA file certifications  
   - Integration with RETIREMENT’s GRC (Governance, Risk, Compliance) tools  

5. **User Training & Change Management**  
   - Workshops for pay-and-processing teams  
   - Update SOPs to reflect new automated workflows  

---

## 5. Use Cases

### 5.1 Monthly Pension Disbursement
1. RETIREMENT generates a monthly payment batch.  
2. Sends JSON payload to `/ach/payments` with all retiree records.  
3. HMS-ACH validates, schedules settlement, and returns `jobId`.  
4. Webhook notifies RETIREMENT when ACH file is accepted by the bank.  
5. On settlement date, HMS-ACH issues credits; final webhook signals completion.

### 5.2 Health Premium Refund
1. Retiree submits overpayment claim via RETIREMENT portal.  
2. Upon claim approval, RETIREMENT system calls the single-payment API.  
3. HMS-ACH processes and returns a transaction reference.  
4. If bank return occurs, HMS-ACH triggers `payment.exception` webhook.  
5. RETIREMENT case system auto-opens a ticket and notifies retiree.

### 5.3 Ad Hoc Lump-Sum Disbursement
1. HR triggers a one-time severance payment after retirement date.  
2. Through a secure SFTP drop, RETIREMENT places a NACHA file in `/incoming`.  
3. HMS-ACH picks up, processes, and delivers a confirmation file to `/outgoing`.  
4. IT Ops reviews acknowledgment and schedules cut-over.

---

By leveraging HMS-ACH, the RETIREMENT mission will realize faster, more accurate benefit disbursements, tighter compliance, and reduced operational burden—ultimately elevating service quality for retirees and internal stakeholders alike.