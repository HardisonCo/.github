# HMS-ACH Integration with 

# Integration of HMS-ACH with FACILITIES

This document outlines how the HMS-ACH component of the Hospital Management System (HMS) can integrate with and benefit the FACILITIES (Facilities Management) organization by addressing mission-critical needs, detailing the technical integration, quantifying stakeholder benefits, and highlighting implementation considerations and real-world use cases.

---

## 1. HMS-ACH Capabilities Addressing FACILITIES’ Mission Needs

1. **Centralized Access Control & Visitor Management**  
   - Role-based credentials synchronized with HR and security directories  
   - Biometric (fingerprint/face) and RFID card reader integration  
   - Temporary QR- or PIN-based passes for contractors and visitors  

2. **Real-Time Monitoring & Event Handling**  
   - Live door/gate lock status and battery/health metrics  
   - Automated alarms on forced-entry, door-held-open, or tamper events  
   - Event stream export via webhooks or messaging bus  

3. **Automated Scheduling & Overrides**  
   - Time-based lock/unlock schedules (e.g., after-hours, weekends)  
   - Emergency “all-unlock” or lockdown commands on demand  
   - Conditional rules (e.g., unlock exterior doors if fire alarm triggers)

4. **Reporting, Analytics & Compliance**  
   - Dashboard views of occupancy, peak-throughput, and access trends  
   - Automated incident reports and audit-ready logs (e.g., for JCAHO, ISO)  
   - Predictive maintenance alerts for door controllers and readers  

---

## 2. Technical Integration

### 2.1 APIs & Data Flows  
```http
# 1. Authentication (OAuth2 Client Credentials)
POST /api/v1/auth/token
Content-Type: application/json
{
  "client_id": "...",
  "client_secret": "...",
  "grant_type": "client_credentials"
}

# 2. Query Door Status
GET /api/v1/doors/{doorId}/status
Authorization: Bearer <token>

# 3. Control Door (lock/unlock)
POST /api/v1/doors/{doorId}/control
Authorization: Bearer <token>
Content-Type: application/json
{
  "action": "unlock",
  "reason": "scheduled maintenance"
}

# 4. Event Webhook (push to FACILITIES endpoint)
POST https://facilities.company.local/hms-ach/events
Content-Type: application/json
{
  "eventId": "E12345",
  "doorId": "D6789",
  "type": "FORCED_ENTRY",
  "timestamp": "2024-07-01T14:22:05Z"
}
```

- **Synchronous calls** for status checks & control commands  
- **Asynchronous webhooks** or **Kafka/RabbitMQ** streams for event notifications  
- **JSON over HTTPS** for structured payloads; optional MQTT/TLS for IoT sensors  

### 2.2 Authentication & Authorization  
- **OAuth2** with Client Credentials grant for machine-to-machine  
- **JWT tokens** embedding scopes (e.g., `doors.read`, `doors.control`)  
- **mTLS** on API gateways where extra assurance is required  
- **SCIM** integration for user provisioning (syncing FACILITIES directory → HMS-ACH)

---

## 3. Benefits & Measurable Improvements

Stakeholder | Current Baseline | Post-Integration Improvement  
---|---|---  
Key Issuance Time (avg) | 30 min/manual lookup | 6 min/automated (↓ 80%)  
Unauthorized Access Incidents | 20 events/month | 2 events/month (↓ 90%)  
Audit Compliance Coverage | 40% events auto-logged | 100% events auto-logged  
Lock Maintenance Downtime | 4 hrs/month | 2 hrs/month (↓ 50%)  
Visitor Throughput—Peak | 50 visitors/hr | 150 visitors/hr (↑ 200%)  

- **Security Team**: Immediate alerts on policy violations, faster incident response  
- **Facilities Managers**: Centralized dashboard for real-time overview, lower manual churn  
- **Compliance Officers**: Auto-generated reports for audits, reduced non-compliance risk  
- **Contractors/Visitors**: Self-service badge issuance reduces bottlenecks  

---

## 4. Implementation Considerations for FACILITIES

- **Network Architecture**  
  - Place lock controllers on a secure VLAN; APIs in DMZ  
  - Leverage VPN or private link between FACILITIES data center and HMS cloud  

- **Legacy Hardware Integration**  
  - Deploy IoT Edge Gateways to translate Wiegand/RS-485 reader data into IP  
  - Use protocol adapters for older door controllers  

- **Scalability & High Availability**  
  - Containerize API services (Kubernetes auto-scaling)  
  - Multi-zone deployment for geo-redundancy  

- **Data Retention & Privacy**  
  - Align log retention with FACILITIES policy (e.g., 7+ years for audits)  
  - Encrypt PII at rest and in transit (FIPS-compliant crypto modules)  

- **Security & Compliance**  
  - Regular pen tests and vulnerability scans  
  - IDS/IPS monitoring on API endpoints  
  - Role-based access reviews every quarter  

---

## 5. Use Cases

### Use Case A: After-Hours Security Lockdown  
1. FACILITIES schedules a “lockdown” at 7 PM via HMS-ACH API.  
2. At 7 PM exactly, all perimeter doors receive `lock` commands.  
3. Security dashboard displays locked status; any forced-entry triggers webhook → SMS/email to guard.  
4. Post-shift, on successful all-clear, operator issues `unlock` batch command.

### Use Case B: Contractor Maintenance Visit  
1. Maintenance request submitted in FACILITIES portal → SCIM sync to HMS-ACH.  
2. HMS-ACH auto-generates a time-bound QR pass (valid 8 AM–5 PM next day).  
3. Crew scans QR at loading dock reader → HMS-ACH validates token, unlocks gate & logs event.  
4. After window expires, pass auto-revokes; any reuse attempt raises alert.

### Use Case C: Emergency Evacuation Drill  
1. FACILITIES triggers “Evacuation Drill” mode via API.  
2. HMS-ACH issues immediate `unlock` to all internal doors.  
3. BMS overlays live door-open status on evacuation map.  
4. Post-drill, analytics report traffic flow, identifies chokepoints for future optimization.

---

By leveraging HMS-ACH’s centralized access control, real-time event monitoring, and robust API framework, FACILITIES can dramatically enhance security posture, streamline operations, and ensure compliance—all while reducing manual workload and response times.