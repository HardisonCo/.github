# HMS-ACH Integration with 

# Integration of HMS-ACH Component with ARCHIVES

This document outlines how the HMS-ACH system component can be integrated into ARCHIVES, addressing its mission needs, technical integration points, stakeholder benefits, implementation considerations, and illustrative use cases.

---

## 1. Specific Capabilities of HMS-ACH That Address ARCHIVES’ Mission Needs

1. **Automated Ingestion & Normalization**  
   - Bulk ingestion of heterogeneous formats (PDF, TIFF, XML, audio/video)  
   - On-the-fly format conversion (OCR, audio transcription)  
   - Validation against archival standards (METS, PREMIS, BagIt)

2. **Metadata Enrichment & Classification**  
   - AI/ML-driven entity extraction (people, places, events)  
   - Controlled-vocabulary mapping (Dublin Core, EAD, thesauri)  
   - Auto-tagging and subject‐heading recommendation

3. **Preservation Packaging & Storage Management**  
   - Generation of preservation packages (BagIt + checksums)  
   - Tiered storage orchestration (disk, tape, cloud archive)  
   - Automated integrity checks & bit-level audits

4. **Access Control & Audit Trails**  
   - Role-based access management (staff, researchers, public)  
   - Fine-grained permissions at collection, file, and record levels  
   - Immutable audit logs for chain-of-custody and compliance

5. **Search & Discovery API**  
   - Full-text and faceted search across collections  
   - Semantic search leveraging knowledge graphs  
   - API endpoints for integration with public portals and research tools

---

## 2. Technical Integration

### 2.1 Architecture & Data Flows
- **Event-Driven Ingestion**  
  • HMS-ACH publishes “new-item” events to a message bus (e.g., Kafka)  
  • ARCHIVES subscribes, pulls payload via secure API  
- **Batch Synchronization**  
  • Nightly or on-demand SFTP/HTTPS transfers of SIP packages  
  • HMS-ACH provides manifest (JSON/XML) for reconciliation

### 2.2 APIs & Protocols
- **RESTful APIs** (JSON, XML) for CRUD on records, collections, access policies  
- **Webhooks** to notify ARCHIVES of status changes (ingested, processed, error)  
- **OAI-PMH** endpoint for metadata harvesting  
- **FTP/SCP** fallback for legacy bulk deposits

### 2.3 Authentication & Security
- **OAuth 2.0 / OpenID Connect** for token-based service-to-service calls  
- **Mutual TLS** for batch endpoints  
- **SAML-based SSO** for staff portal integration  
- **Field-level encryption** for restricted records (PII, classified)

---

## 3. Benefits & Measurable Improvements for Stakeholders

| Stakeholder     | Benefit                                         | Metric / KPI                                  |
|-----------------|-------------------------------------------------|-----------------------------------------------|
| Archivists      | Reduced manual curation                          | 60% faster record ingest per month            |
| IT Operations   | Streamlined storage management                   | 30% reduction in redundant copies             |
| Researchers     | Enhanced discoverability                          | 40% improvement in search retrieval accuracy  |
| Compliance Team | Better auditability & chain-of-custody reporting  | 100% traceability on high-value records       |
| Leadership      | Cost predictability & service scalability         | 25% lower TCO over 5 years                    |

- **Throughput Gains**: From 500 to 2,000 records/day  
- **Metadata Quality**: From 70% to 95% adherence to controlled vocabularies  
- **User Satisfaction**: Survey scores rise from 3.2 to 4.5/5

---

## 4. Implementation Considerations Specific to ARCHIVES

1. **Standards Alignment**  
   - Map HMS-ACH metadata schema to ARCHIVES’ existing EAD/METS profiles  
   - Compliance with NARA/ISO 16363 audit requirements

2. **Data Migration & Cleanup**  
   - Pilot migration of a representative collection  
   - Parallel run for 2–3 months before cutover

3. **Network & Infrastructure**  
   - Firewall rules for API gateway and message bus  
   - High-availability clusters for HMS-ACH and ARCHIVES portal

4. **Governance & Workflow**  
   - Define joint Operating Level Agreement (OLA) and SLAs  
   - Update SOPs to include HMS-ACH automated triage steps

5. **Training & Change Management**  
   - Hands-on workshops on new ingestion dashboards  
   - Role-based training for metadata enrichment tools

---

## 5. Use Cases

### 5.1 Born-Digital Records Ingestion
- **Scenario**: An agency delivers daily e-mail archives in XML.  
- **Flow**:  
  1. HMS-ACH picks up XML files via SFTP → converts to preservation TIFF + PDF/A.  
  2. Metadata auto-extracted (sender, date, subject) → enriches with named-entity tags.  
  3. ARCHIVES API ingests SIP → automates accessioning and audit logging.  
- **Outcome**: Ingestion time shrinks from days to hours; metadata completeness up to 98%.

### 5.2 Bulk Digitization of Photographs
- **Scenario**: 10,000 analog photographs digitized and scannable.  
- **Flow**:  
  1. Batch upload of high-res TIFFs to HMS-ACH via REST.  
  2. Automated facial-recognition and geo-tagging.  
  3. ARCHIVES harvests enriched metadata nightly via OAI-PMH.  
- **Outcome**: Researchers locate images by person or place, boosting usage by 300%.

### 5.3 Researcher-Driven Discovery
- **Scenario**: Public researcher queries ARCHIVES portal for “mid-Century urban planning.”  
- **Flow**:  
  1. Query hits ARCHIVES search API → delegates semantic expansion to HMS-ACH.  
  2. HMS-ACH returns related topics (e.g., “Robert Moses,” “Garden City Movement”).  
  3. ARCHIVES UI displays “Suggested Collections” and “Did you mean?” prompts.  
- **Outcome**: Session duration increases 50%, bounce rate drops 20%.

---

By integrating the HMS-ACH component into ARCHIVES’ ecosystem, the organization can dramatically accelerate ingestion workflows, enhance metadata quality, and provide richer, more discoverable archival content—all while maintaining rigorous preservation and compliance standards.