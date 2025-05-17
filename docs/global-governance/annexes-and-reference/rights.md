# HMS-ACH Integration with 

# Integrating the HMS-ACH HMS Component with the RIGHTS Platform

This document outlines how the HMS-ACH (Hospital Management System – Admission/Discharge/Transfer) component can integrate with and enhance the RIGHTS platform (Regulatory & Interoperability Governance for Health Technology Services). We cover:

1. HMS-ACH capabilities aligned to RIGHTS mission  
2. Technical integration (APIs, data flows, auth)  
3. Benefits & metrics for RIGHTS stakeholders  
4. RIGHTS-specific implementation considerations  
5. Concrete use-case scenarios  

---

## 1. HMS-ACH Capabilities Addressing RIGHTS Mission Needs

- **Real-time ADT Event Stream**  
  ● Instantly captures patient admissions, discharges, transfers  
  ● Feeds RIGHTS with up-to-date census for rights/consent checks  

- **Master Patient Index (MPI) & Demographic Validation**  
  ● Ensures unique patient identifiers, reduces duplicate records  
  ● Harmonizes with RIGHTS’ governance of identity and consent profiles  

- **Consent Capture & Status Tracking**  
  ● Records patient consent for data sharing, research, or telehealth  
  ● Exposes consent status via API for RIGHTS’ policy engine  

- **Audit Trails & Reporting**  
  ● Immutable logs of who, when, and what ADT events occurred  
  ● Meets RIGHTS’ requirements for compliance reporting and forensics  

- **Role-Based Access Controls (RBAC)**  
  ● Defines user roles (clerk, nurse, registrar) and scopes of data access  
  ● Integrates with RIGHTS’ centralized policy decision point  

- **Standards Compliance (HL7v2, FHIR)**  
  ● Publishes ADT messages in HL7v2 or FHIR R4 formats  
  ● Aligns with RIGHTS’ interoperability framework  

---

## 2. Technical Integration

### 2.1 API & Message Interfaces

- **Inbound to RIGHTS**  
  • HL7v2 ADT^A01, A03, A08 messages over MLLP or TCP TLS  
  • FHIR REST (Subscription & Event Notification)  
- **Outbound from RIGHTS**  
  • FHIR `Consent` GET/POST for real-time checks  
  • REST webhook callbacks when new rights policies are issued  

### 2.2 Data Flow

1. **Admission**  
   - HMS-ACH emits an ADT A01 event to RIGHTS’ FHIR Subscription endpoint  
   - RIGHTS queries HMS-ACH (FHIR `Patient/{id}`) to enrich demographic details  
2. **Consent Verification**  
   - RIGHTS policy engine retrieves patient `Consent` resource  
   - Deny/admit decision routed back to HMS-ACH before care workflows proceed  
3. **Transfer/Discharge**  
   - ADT A02/A03 events update bed‐management in RIGHTS dashboard  
   - RIGHTS logs event, updates audit trail, triggers any needed external notifications  

### 2.3 Authentication & Security

- **OAuth 2.0 / OpenID Connect**  
  • JWT access tokens scoped to “adt:read”, “patient:consent:read”  
- **Mutual TLS**  
  • Ensures only trusted HMS-ACH instances connect  
- **Field-Level Encryption**  
  • Encrypt PII (SSN, DOB) at rest; TLS 1.2+ in transit  
- **API Gateway**  
  • Throttling, request validation, schema conformance  

---

## 3. Benefits & Measurable Improvements for RIGHTS Stakeholders

| Stakeholder                | Pain Point                               | HMS-ACH + RIGHTS Integration Impact               | Key Metric                              |
|----------------------------|------------------------------------------|---------------------------------------------------|-----------------------------------------|
| Compliance Officers        | Manual reconciliation of ADTs & consents | Automated ADT‐to‐Consent correlation                | 90% reduction in manual audits          |
| Clinical Registrars        | Duplicate/erroneous admissions           | Centralized MPI & real-time demographic checks     | 75% drop in duplicate MRNs              |
| IT Security Team           | Siloed logs & inconsistent policies      | Unified audit trail & centralized RBAC            | 100% of ADT events logged centrally     |
| Care Coordinators          | Delays in discharge paperwork            | Instant discharge notifications & rights closure   | 50% faster discharge processing times   |
| Privacy/Oversight Board    | Hard to demonstrate HIPAA/GDPR compliance| Detailed, immutable logs & consent snapshots       | 0 compliance findings in external audit |

---

## 4. Implementation Considerations Specific to RIGHTS

- **Regulatory Compliance**  
  • Map HMS-ACH data fields to RIGHTS’ privacy policy clauses (HIPAA, GDPR)  
  • Establish Data Processing Agreements (DPAs)  

- **Data Residency & Sovereignty**  
  • Ensure HMS-ACH storage aligns with RIGHTS’ regional data-residency rules  

- **Policy Versioning & Change Management**  
  • Rights policies evolve; coordinate version upgrades with HMS-ACH release cycles  

- **Schema Alignment & Transformation**  
  • Use FHIR profiles/extensions to capture RIGHTS-specific consent codes  
  • Validate HL7v2 zoned fields (e.g., OBX for consent metadata)  

- **Organizational Readiness & Training**  
  • Train staff on new workflows (e.g., consent checks at registration)  
  • Update SOPs to include automated ADT-Rights handshakes  

---

## 5. Use Cases

### Use Case 1: Admission with Consent Check  
1. Front-desk registrar enters patient into HMS-ACH  
2. HMS-ACH sends FHIR ADT A01 → RIGHTS  
3. RIGHTS queries existing `Consent` resource  
4. If “OK,” admission proceeds; otherwise triggers request for fresh consent  
5. Registry logs outcome; care staff notified via HMS-ACH UI  

### Use Case 2: Conditional Discharge Notification  
1. Physician discharges patient in HMS-ACH → ADT A03 event  
2. RIGHTS receives A03, verifies any outstanding data-sharing obligations (e.g., post-op follow-up)  
3. RIGHTS publishes action item to Care Coordination queue  
4. Patient exit summary is only released once all rights-related checks clear  

### Use Case 3: Telehealth Session Pre-Validation  
1. Telehealth module in HMS-ACH requested for Patient X  
2. HMS-ACH calls RIGHTS’ REST API to confirm telehealth consent  
3. If expired, HMS-ACH triggers digital consent capture workflow  
4. Rights resource updated; session initiated only after consent is recorded  

### Use Case 4: Research Data Extract (De-identified)  
1. Research team requests batch of ADT events for analytics  
2. RIGHTS applies de-identification rules to HMS-ACH data feed  
3. Filtered, anonymized dataset provided under a `Consent` authorization token  
4. Audit log retains linkage for future compliance reviews  

---

By leveraging HMS-ACH’s robust ADT management, consent capture, and auditing capabilities—and tightly integrating them with RIGHTS’ policy engine and governance workflows—organizations can achieve real-time compliance, reduce manual overhead, and enhance patient-centric care across the admission‐to‐discharge continuum.