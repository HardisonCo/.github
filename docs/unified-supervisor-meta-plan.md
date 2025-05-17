# HMS Unified Supervisor-Driven Meta-Planning Framework

> **Purpose**  Provide a three-layer roadmap:
> 1. **Analysis Plan** – How we will digest ~100+ design docs & specs using automated supervisors and the existing `hms-agent` toolkit.
> 2. **Improvement Plan** – How insights from the analysis loop feed concrete refactors/enhancements.
> 3. **Master Unification Plan** – A consolidated, supervisor-centric architecture & delivery timeline that stitches GA-MAS, FFI, self-healing, economic-prover, CLI, visualization, and governance streams into one living organism.

---

## A. Analysis Plan (Weeks 0-2)
| Step | Objective | Tools/Supervisors | Deliverables |
|------|-----------|------------------|--------------|
| **A1** | **Document Inventory & Tagging**<br>Scan `docs/`, `HMS-DEV/`, `SYSTEM-COMPONENTS/` trees; build manifest (path, size, hash, topic). | `github_issue_supervisor.py` (bulk-scan mode), `hms-agent` [`FileCrawler`] | `manifest.json`, auto-generated tags |
| **A2** | **Semantic Clustering**<br>Cluster docs by domain (Self-Healing, GA, FFI, MAS, Econ-Prover, CLI, Viz, Gov, Ops). | `cort_supervisor_enhanced.py` (CoRT-based clustering) | `cluster-map.csv`, dendrogram PNG |
| **A3** | **Executive Summaries**<br>LLM summarization (chunked w/ DeepSeek-LLM) ⇒ 1-page summary per doc. | `summarization_supervisor` (new) | `summaries/*.md` |
| **A4** | **Gap & Duplication Detection**<br>Natural-language diff across clusters to find overlaps/conflicts. | `analysis/gap_detector`, `analysis/repository_analyzer` | `gap-report.md`, `duplication-map.md` |
| **A5** | **Dependency Graph Extraction**<br>Parse specs for interfaces, APIs, protobufs → produce Neo4j graph. | `analysis/dependency_extractor` (Rust), Neo4j container | `hms-deps.graphml`, query scripts |
| **A6** | **Risk & Complexity Scoring**<br>Heuristics: size, coupling, missing tests, unclear ownership. | `analysis/quality_metrics` | `risk-matrix.xlsx` |
| **A7** | **Stakeholder Review**<br>Publish dashboards, hold 2-hr review with steering committee. | Notion board, Mermaid live diagrams | Sign-off to move to Plan B |

*Automation Note*: Supervisors orchestrate analysis tasks via A2A bus; results stored in `/analysis/reports/20YY-MM-DD-snapshot/`.

---

## B. Improvement Plan (Weeks 2-4)
Stage B transforms findings into actionable refactors/enhancements.

1. **B1 – Prioritisation Matrix**
   • Map gaps vs. business impact & dev effort ⇒ **P1/P2/P3** labels.
2. **B2 – RFC Sprint** (Rust + TS)
   • For top-10 gaps produce lightweight RFCs (template auto-filled from A-reports).
3. **B3 – Unified Terminology & Schemas**
   • Consolidate defs: "Agent", "Genome", "FFI Function", etc.
   • Update protobufs in `hms-ffi-protos/` + TypeScript types.
4. **B4 – Modular Repo Re-org**
   • Propose dir moves / crate splits to align with clusters.
5. **B5 – Test Debt Burn-down**
   • Autogen missing tests (Rust `cargo-insta`, TS `vitest`) for high-risk modules.
6. **B6 – CI Pipeline Extension**
   • Add lenses: doc-lint, schema-diff alert, GA fitness regression.
7. **B7 – Supervisor Playbook Update**
   • Encode recurring improvements as `SupervisorTask` YAMLs so future analyses run continuously (nightly cron).

Milestone: **v0.9 "Consolidated Core" tag** – All agreed improvements merged, CI green.

---

## C. Master Unification Plan (Weeks 4-12 & Ongoing)

### C1. Supervisor-Centric Architecture
```
┌───────────────┐            gRPC / A2A           ┌───────────────┐
│  GA-MAS Core  │◀──────── Supervises ───────────▶│  Domain Agents│
└──────┬────────┘                                   (Healer, FFI, …)
       │             event-bus / Redis              └───────────────┘
       ▼
┌──────────────────┐   FFI  ┌──────────────────┐   HTTP/gRPC  ┌────────────┐
│ CLI Supervisor   │◀──────▶│  Rust Services   │◀────────────▶│  Dashboards│
└──────────────────┘        └──────────────────┘              └────────────┘
```
Key roles:
• **Meta-Supervisor** (`codex-cli hms supervisor`): orchestrates other supervisors, hot-loads new playbooks.
• **Analysis Supervisor**: runs Plan A nightly.
• **Improvement Supervisor**: queues refactor tasks, opens PRs.
• **Runtime Supervisor**: live self-healing (existing HMS); ties into GA-MAS.

### C2. Cross-Stream Integration Tracks
| Stream | Lead Supervisor | Week 4-6 | Week 7-9 | Week 10-12 |
|--------|-----------------|----------|----------|------------|
| Self-Healing Core | Runtime | Circuit-Breaker v2 | Distributed Coordinator clustering | Chaos test hardening |
| GA-MAS Engine | GA-Supervisor | Fitness fn refactor | Distributed genomes | RL hybrid |
| FFI | FFI-Supervisor | Bindgen 1.0 | Econ-Prover hooks | Versioned schema registry |
| Econ-Prover | Prover-Supervisor | Lean axioms import | Rust orchestrator → CLI | Proof metrics in GA |
| CLI & Boot UX | CLI-Supervisor | Boot Viz POC | Interactive dashboards | Plug-in SDK |
| Governance & Docs | Gov-Supervisor | Doc sync bot | Policy enforcement hooks | External audits |

### C3. Milestones & KPIs
1. **M0 (Week 4)** – All supervisors alive; nightly analysis green.
2. **M1 (Week 6)** – Unified dependency graph published; ≤5 critical gaps open.
3. **M2 (Week 9)** – GA-MAS running distributed across 3 nodes; 90% chaos tests pass.
4. **M3 (Week 12)** – Economic-Prover proves 10 baseline theorems; FFI schema registry v1.0.
5. **Continuous** – MTTR < 5 s; Proof success rate ≥ 80%; Docs coverage ≥ 95% lines.

### C4. AI-Executable Task Matrix (excerpt)
| ID | Supervisor | Success Criterion |
|----|------------|-------------------|
| `DocManifest` | Analysis | `manifest.json` exists & ≥100 files hashed |
| `GapScan` | Analysis | `gap-report.md` lists ≥20 issues with severity |
| `RFCGen` | Improvement | 10 RFC PRs opened & all pass CI |
| `BindgenTS` | FFI | `dist/ts/index.d.ts` generated, type-check passes |
| `GACluster` | GA | GA population spread across 3 Redis shards |
| `Proof10` | Prover | 10/10 target theorems proved automatically |

---

## Next Actions (for Steering Committee)
1. Approve Analysis Plan tooling budget (≈2 developer-weeks).
2. Green-light creation of *Meta-Supervisor* crate & initial YAML playbooks.
3. Schedule Week-2 checkpoint to review A-reports and lock Improvement backlog.

*Document ID*: **UNIFIED-SUPERVISOR-META-PLAN v0.1**  — Generated `{{DATE}}` 