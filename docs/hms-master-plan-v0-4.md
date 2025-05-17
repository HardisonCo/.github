# HMS Unified Master Plan v0.4 (draft)

**Purpose:** Provide a single, living blueprint for the Health Monitoring System (HMS) that harmonises dozens of satellite specs (HMS-SYS, HMS-A2A, HMS-DEV, etc.) into one actionable plan. It aligns with Codify's vision of verifiable, self-healing, multi-agent infrastructure for public-sector and enterprise workflows and serves as the coordination nexus for all future HMS extensions (e.g., the Economic Theorem-Proving MAS).

**Document Status:** Draft - Updated based on Sprint 0 spec hardening.

## 1 Strategic Goal & Objectives

**Primary goal:** Deliver a resilient, policy-compliant, and auditable Multi-Agent System (MAS) platform that continuously monitors, verifies, and optimises mission-critical services using formal methods and adaptive AI, while providing transparent human oversight and intervention capabilities.

**Key Performance Indicators (KPIs):**

| Objective      | KPI                                           | Target      | Owner         | Measurement Method                     |
|----------------|-----------------------------------------------|-------------|---------------|----------------------------------------|
| **Resilience** | Mean Time To Recovery (MTTR) for P0 incidents | < 3 min     | Eng Lead      | Prometheus Alertmanager + Incident Logs |
|                | Auto-Recovery Rate (Self-Healing Success)     | > 95%       | Eng Lead      | Supervisor recovery logs               |
| **Compliance** | Automated Policy Checks Passing Pre-Merge     | 100%        | SecOps Lead   | CI Gate results (Policy Engine)        |
|                | FedRAMP/ISO Controls Mapped & Audited       | Continuous  | SecOps Lead   | Audit reports + Compliance Dashboard   |
| **Observability**| Agent Telemetry Coverage (Metrics, Logs)      | > 99%       | Eng Lead      | Prometheus scrape targets + Log counts |
|                | Core API Request Latency (p95)                | < 500 ms    | Eng Lead      | Grafana dashboards                     |
| **Scalability**| Max Concurrent Agents Supported (Linear Scale)| > 10k pods  | Eng Lead      | Load test results (k6)                 |
|                | Performance Regression Per Release            | < 10%       | Eng Lead      | Benchmark CI job                       |
| **Extensibility**| Time to Add & Deploy New Agent Skill (Basic)| < 1 day     | Product Owner | Developer survey + CI deploy times     |
|                | Zero-Downtime Rollout Success Rate          | > 99.9%     | Eng Lead      | Deployment logs & uptime               |

## 2 Unified Architecture (Conceptual)

```mermaid
graph TD
    subgraph Core [Core Services]
        Supervisor[«Core» Supervisor Service<br>(crates/supervisor)]
        Verification[«Core» Verification & Compliance<br>(crates/verification)]
        Policy[«Core» Policy Engine<br>(crates/policy_engine)]
        DataRepo[«Core» Data & State Store<br>(crates/data_store)]
        KB[«Core» Knowledge Base<br>(crates/data_store)]
    end

    subgraph AgentPlane [Agent Plane]
        AGT[«Agent» Identity & Lifecycle<br>(crates/agent_core)]
        AGX[«Agent» Skills / Tactics<br>(crates/agent_skills)]
        MAC[«Agent» Collaboration Bus<br>(crates/communication)]
    end

    subgraph Integration [Infrastructure & Integration]
        FFI[«Infra» FFI Layer<br>(crates/ffi)]
        A2A[«Infra» A2A Protocol<br>(crates/communication)]
        Marketplace[«Infra» OSS Marketplace<br>(crates/marketplace - Future)]
        SelfHeal[«Infra» Self-Healing Mesh<br>(crates/self_healing)]
    end

    subgraph Interface [Interface]
        UI[«UI» Web / CLI<br>(Future)]
        HITL[«UI» Human-in-the-Loop<br>(Future)]
    end

    User((User / Admin))

    %% Connections
    User --> UI
    UI --> FFI --> Supervisor
    Supervisor -->|tasks via A2A| AGT
    Supervisor --> Verification
    Verification --> Policy
    Supervisor --> SelfHeal
    Supervisor -->|metrics/status| DataRepo
    AGT -->|state/memory| DataRepo
    AGT -->|knowledge| KB
    AGT <--> AGX
    AGT <-->|via A2A| MAC
    MAC <--> A2A
    FFI -->|calls| Supervisor
    FFI -->|calls| Verification
    HITL -->|overrides/approvals| Supervisor
    HITL -->|policy exceptions| Policy
    SelfHeal -->|recovery actions| Supervisor

    classDef core fill:#f9f,stroke:#333,stroke-width:1px;
    classDef agent fill:#bbf,stroke:#333,stroke-width:1px;
    classDef infra fill:#bfb,stroke:#333,stroke-width:1px;
    classDef interface fill:#ffc,stroke:#333,stroke-width:1px;
    class Core,AgentPlane,Integration,Interface internal-link;
    class Supervisor,Verification,Policy,DataRepo,KB,AGT,AGX,MAC,FFI,A2A,Marketplace,SelfHeal,UI,HITL internal-link;
```

**Interaction Highlights:**

*   **Supervisor:** Delegates goals (e.g., `SubmitProofTask`) to agent clusters via A2A messages; collects results & telemetry.
*   **Verification:** Runs CI-style checks (Lean kernel, security scans) on artefacts produced by agents, triggered by the Supervisor.
*   **Self-Healing:** Watches Prometheus alerts (or agent heartbeats); when an agent/service drifts, triggers recovery actions (genome mutation via `genetic_engine`, pod restart, task replay) via the Supervisor.
*   **Policy:** Acts as a gatekeeper—any action not meeting policy contracts (e.g., disallowed Lean tactics, resource limits) is quarantined or rejected, potentially requiring HITL review.
*   **FFI:** Exposes core functionalities (task submission, status query) to external systems (Python scripts, UI).

## 3 Logical Component Reference

### 3.1 Agents (HMS-AGT / HMS-AGX)

*   **AGT (`crates/agent_core`):** Provides process-bound identity (UUID), state management (status, memory), and a basic RPC harness for receiving tasks and sending events via the A2A protocol.
*   **AGX (`crates/agent_skills`):** Defines traits and potentially a plugin system for agent capabilities (e.g., `ProofSkill`, `ETLSkill`). Specific complex skills (like a Lean Prover agent integrating DeepSeek) might reside here or in dedicated crates.
*   **Lifecycle API:** `/SpawnAgent`, `/StopAgent` (future), `/PauseAgent` (future), `/GetAgentStatus` (future) exposed by the Supervisor service.

### 3.2 Supervisor Service (`crates/supervisor`)

*   **Implementation:** Rust service using Tokio and Tonic, exposing gRPC & A2A endpoints. Source: `crates/supervisor`.
*   **Core Loop:** Runs scheduling logic → selects agent(s) based on skills/load → dispatches tasks via A2A → tracks status → publishes metrics (Prometheus).
*   **Goal Alignment (Future):** May embed guards (e.g., vector similarity against org OKRs) to flag potentially rogue agent behaviour.

**Supervisor Responsibility Matrix:**

| Responsibility                 | Primary Mechanism                          | Interaction Crates                                    |
|--------------------------------|--------------------------------------------|-------------------------------------------------------|
| Agent Lifecycle Management     | gRPC API (`SpawnAgent`, `StopAgent` etc.)  | `agent_core`, `communication`                         |
| Task Orchestration & Assignment| Internal Scheduler + A2A (`SubmitTask`)    | `communication`, `agent_core`                         |
| Health & Performance Monitoring| Heartbeats / Metrics endpoint scraping     | `agent_core`, `data_store` (Prometheus/Grafana)       |
| Self-Healing Coordination    | Receives triggers, initiates recovery plans| `self_healing`, `genetic_engine`, `agent_core`        |
| Verification Triggering        | Calls `Verification::verify()`             | `verification`, `policy_engine`                       |
| Policy Enforcement Gateway     | Checks with `PolicyEngine` before critical actions | `policy_engine`                                   |
| FFI Exposure                   | Provides API endpoints via gRPC            | `ffi` (client-side)                                   |
| HITL Interface Point         | Accepts overrides/approvals via API/UI   | `ffi`, (future UI crate)                              |

### 3.3 A2A Communication (`crates/communication`)

*   **Protocol v0.1:** Protobuf schema (`proto/agent.proto`) defining `AgentTask`, `AgentEvent`, `ProofResult`, `SupervisorService` etc. See **Appendix A** for details.
*   **Transport:** gRPC over HTTP/2 (Tonic) for primary request/response. NATS or Redis Streams may be considered for Pub/Sub event broadcasting later.

### 3.4 Verification Pipeline (`crates/verification`)

*   **Interface:** Defines a core `trait ProofBackend` allowing pluggable provers.
    ```rust
    #[async_trait]
    pub trait ProofBackend: Send + Sync + std::fmt::Debug {
        async fn prove(&self, task: &AgentTask) -> Result<ProofResult, VerificationError>;
        fn name(&self) -> String;
    }
    ```
*   **Implementations:**
    *   `DeepSeekBackend`: Executes the `deepseek-prover` binary via `tokio::process::Command`. Parses stdout/stderr for results. Handles timeouts. (Initial implementation)
    *   `LSPBackend` (Future): Interacts with Lean 4 via its Language Server Protocol for finer-grained control.
*   **Stages (Conceptual):** Static Analysis (linting) → Formal Verification (Lean Kernel check via `ProofBackend`) → Security Scan (Semgrep/Trivy - Future) → Policy Scan (`PolicyEngine`).
*   **Triggers:** Called by Supervisor upon task completion or specific events (e.g., Git commit).

### 3.5 Data & Knowledge Layer (`crates/data_store`)

*   **DataRepo:** Postgres for structured data (agent registry, task status, audit logs). S3/MinIO for large artefacts (proof files, logs).
*   **Vector Store:** Qdrant for embedding agent memory, past proofs, or CoT logs for retrieval.
*   **Knowledge Base:** Conceptual; realized via structured data and vector retrieval.

### 3.6 FFI Layer (`crates/ffi`)

*   **Strategy:** Expose core Rust functionality primarily via Python bindings using PyO3. Provide a stable C ABI using `#[no_mangle]` and `cbindgen` for other language integrations or direct linking.
*   **Python Bindings (`hms_core` module):** Exposes functions like `spawn_agent_py`, `submit_proof_py`, `query_task_status_py`. Uses a shared Tokio runtime (`RUNTIME`) to bridge async Rust with synchronous Python calls.
*   **C Bindings:** Exports functions like `hms_ffi_ping_supervisor_c`, `hms_ffi_spawn_agent_c`, etc., with clear memory management (`hms_ffi_free_string`).
*   **FFI Contract:** A generated document `target/ffi_contract.md` (produced by build/CI step) lists all exported symbols (Python & C), their signatures, and stability guarantees (Experimental, Stable).
    ```mermaid
    graph LR
        A[Rust Function<br>`supervisor::spawn_agent()`] --> B(Rust FFI Wrapper<br>`ffi::spawn_agent_py()`<br>`#[pyfunction]`);
        A --> C(Rust C FFI Wrapper<br>`ffi::hms_ffi_spawn_agent_c()`<br>`#[no_mangle] extern "C"`);
        B --> D{Python Wheel<br>`hms_core.whl`}; 
        C --> E{C Header<br>`hms.h`};
        D --> F((Python Client));
        E --> G((C/C++/Go Client));
    ```

### 3.7 Self-Healing Mesh (`crates/self_healing`)

*   **Logic:** Implemented as dedicated diagnostic agents or a module within the Supervisor.
*   **Loop:** Detect (Prometheus alerts, missing heartbeats) → Diagnose (Analyze logs/metrics) → Plan (Select recovery playbook) → Act (Trigger Supervisor actions: restart pod, mutate genome via `genetic_engine`, reassign task).
*   **Playbooks:** Declarative recovery strategies (e.g., YAML files) defining conditions and actions.

### 3.8 Governance / HITL (Future `crates/ui`)

*   **Portal:** Web application (e.g., Next.js) providing dashboards, task views, agent topology, log access, and intervention controls.
*   **Roles:** Role-based access control (RBAC) for operators, admins, auditors.
*   **Escalation:** On policy violations or critical failures exceeding auto-recovery limits, Supervisor raises Incidents → HITL must approve/reject corrective actions (e.g., genome mutation, manual rollback).

## 4 Plan Ingestion & Consolidation Workflow
(Unchanged from v0.3, process remains valid)

1.  **Scan & Tag:** `hms lint --scan` auto-tags docs.
2.  **Backlog:** Prioritised reading queue synced with GitHub Projects board.
3.  **Extract:** YAML front-matter for goals, scope, timeline.
4.  **Diff:** Structural comparison with current master spec (e.g., JSON/YAML representation).
5.  **Workshop:** Weekly guild review for flagged diffs.
6.  **Integration PR:** Bot opens PR with updated plan + Mermaid diff; requires CI checks (doc lint, link validation).
7.  **Traceability:** Back-links via `[source:filename.md#Section]` tokens.

## 5 Implementation Roadmap (Sprint-Based)

*Dependencies Note:* A2A Protocol (Sprint 0) is needed before Supervisor-Agent communication (Sprint 2). Verification Interface (Sprint 1) is needed before Policy Engine integration (Sprint 4).

| Phase             | Sprints (Weeks) | Focus                                       | Key Deliverables (Cumulative)                                                                 |
|-------------------|-----------------|---------------------------------------------|-----------------------------------------------------------------------------------------------|
| **1: Bootstrapping** | **0-1 (1-4)**   | Workspace, IaC, A2A Schema, Supervisor MVP | Cargo workspace, Nix Flake dev env, `agent.proto` v0.1, Supervisor gRPC Ping/Spawn stub, CI base |
|                   |                 | Lean Env & Basic Proof Backend              | `ProofBackend` trait, `DeepSeekBackend` stub, FFI Python stubs (`hms_core` wheel), Basic Lean Econ Lib |
| **2: Specialisation**| **2-4 (5-10)**  | Core Agent Logic, A2A Transport           | `agent_core` identity/heartbeat, gRPC/NATS client+server, Supervisor ↔ Agent ping test        |
|                   |                 | GA Engine v1, Specialized Agents          | `genetic_engine` `Genome`/fitness, Decomposition/Strategy/Verification Agent *stubs*          |
|                   |                 | Monitoring Integration                      | Prometheus/Grafana dashboards for Supervisor/Agent metrics                                    |
| **3: Self-Healing** | **5-7 (11-16)** | Diagnostic Agents, Recovery Playbooks     | `self_healing` crate, failure detection, auto-restart playbook, Genome mutation trigger         |
|                   |                 | Distributed Proving                         | Supervisor assigns subgoals, Lean remote tactic setup (basic)                               |
|                   |                 | Chaos Testing                               | CI job injecting agent failures, validating recovery                                          |
| **4: Meta-Learning** | **8-10 (17-22)**| RL-GA Hybrid Loop                         | PPO/GA integration PoC, reward based on fitness, Agent memory via `data_store` (Vector)       |
|                   |                 | Policy Engine Integration                   | `policy_engine` crate, basic rule execution (e.g., tactic allowlist), Supervisor policy checks|
|                   |                 | Knowledge Store                             | `data_store` (Postgres) for task history, proof artefacts                                   |
| **5: Productionisation**| **11-13 (23-28)**| DevSecOps, Scalability, UI              | Docker containers, Helm charts, in-toto/SBOM PoC, Basic Web UI (task view), HITL approval flow|
|                   |                 | Public API/SDK, Community                 | Stable v1.0 API, Python SDK, Documentation site, Proof-a-thon event plan                    |
| *Contingency*     | *14- (29-)*     | Buffer / Advanced Features / Bug Fixing     |                                                                                               |

## 6 Testing Matrix

| Level       | Tools                   | Success Gate                     | CI Job / Test ID Traceability        |
|-------------|-------------------------|----------------------------------|--------------------------------------|
| Unit        | Rust `cargo test`, PyTest | ≥ 90% Code Coverage              | `test-unit-*` (e.g., TX-U01..U99)    |
| Integration | `docker-compose up test`| All services 2× green runs       | `test-integration-*` (e.g., TX-I01..I20) |
| E2E         | GitHub Actions Matrix   | Key User Journeys Pass           | `test-e2e-*` (e.g., TX-E01..E10)     |
|             | (Python scripts + k6)   | Pass Lean proofs scenario        | `test-e2e-lean-proof` (TX-E05)       |
|             |                         | Pass self-heal chaos test        | `test-e2e-chaos` (TX-E06)            |
| Load        | k6                      | p95 < 500 ms @ target RPS        | `test-load-*` (TX-L01)               |
| Security    | Trivy, Semgrep          | Zero Critical/High CVEs/Findings | `scan-security-*` (TX-S01)           |
| Compliance  | Policy Engine Tests     | 100% Policy Suite Pass           | `test-compliance-*` (TX-C01)         |
| FFI         | `maturin develop` tests | Python & C bindings functional   | `test-ffi-*` (TX-F01)                |

## 7 Top Risks & Mitigations

| Risk                     | Likelihood | Impact | Mitigation                                                                     |
|--------------------------|------------|--------|--------------------------------------------------------------------------------|
| Spec Drift               | Med        | Med    | Weekly doc ingestion workflow (Sec 4), single authoritative plan (this doc)    |
| Compute Cost (GPU/CPU)   | Med        | High   | Auto-scale nodes (Kubernetes HPA), spot instances, prover efficiency tuning    |
| Byzantine Agents         | Low        | High   | Policy engine gates, external verifier quarantine, resource quotas, goal guards |
| Data Leakage             | Low        | High   | Field-level encryption, differential privacy wrappers (future), RBAC           |
| Human Bottleneck (HITL)  | Med        | Med    | Escalate only high-risk/unrecoverable incidents; rest auto-approved/logged     |
| Proto Schema Churn       | High       | Med    | Mark v0.x as experimental, versioning rules (Appendix A), compatibility tests |
| DeepSeek Binary Mismatch | Med        | High   | Pin container image digest in CI/dev env (Nix Flake), version negotiation      |
| PyO3/FFI Build Complexity| Med        | Med    | Use `maturin`, cross-compilation CI matrix, well-defined C ABI               |
| Lean Versioning          | Med        | Med    | Pin Lean/Mathlib versions in Nix Flake, CI matrix for Lean versions            |

## 8 Appendix A: A2A Protocol v0.1 (Protobuf)

**Versioning:** v0.1 is considered **Experimental**. Breaking changes are allowed until v1.0. Schema defined in `crates/communication/proto/agent.proto`.

**Transport:** Primarily gRPC (Tonic). Pub/Sub (NATS/Redis) may be added later for events.

**Key Messages:**

*   `AgentTask`: Represents a task assigned to an agent (includes `task_id`, `theorem_id`, `lean_expr`, `axiom_deps`, `metadata`).
*   `AgentEvent`: Wrapper for events published on the bus (includes `event_id`, `timestamp`, `payload` which can be `TaskSubmitted`, `TaskStatusUpdate`, `ProofResult`, etc.).
*   `ProofResult`: Outcome of a proof attempt (includes `task_id`, `status` enum, `lean_proof_term`, `stdout`, `stderr`, `chain_of_thought`, `duration_sec`).
*   `SpawnAgentRequest`/`Response`: For supervisor to request agent creation.
*   `TaskStatusRequest`/`Response`: To query or report the status of a task.

**(Snippet from `agent.proto`)**
```protobuf
syntax = "proto3";
package agent;
import "google/protobuf/timestamp.proto";

service SupervisorService {
    rpc Ping (PingRequest) returns (PingResponse);
    rpc SpawnAgent (SpawnAgentRequest) returns (SpawnAgentResponse);
    rpc SubmitProofTask (AgentTask) returns (TaskStatusResponse);
    rpc QueryTaskStatus (TaskStatusRequest) returns (TaskStatusResponse);
}

message AgentTask {
    string task_id = 1;
    string theorem_id = 2;
    bytes lean_expr = 3;
    repeated string axiom_deps = 4;
    string assigned_agent_id = 5;
    map<string, string> metadata = 6;
}

message ProofResult {
    // ... fields defined earlier ...
    enum Status {
        UNKNOWN = 0;
        SUCCESS = 1;
        FAILURE = 2;
        TIMEOUT = 3;
        CANCELLED = 4;
    }
    Status status = 3;
    // ... other fields ...
}
// ... other messages ...
```

---
**Changelog:**
*   v0.4: Filled goal/KPIs, unified Supervisor spec, added Protocol Appendix, defined ProofBackend/FFI interfaces, updated roadmap to Sprints, added CI traceability. Aligned with Sprint 0/1 deliverables.
*   v0.3: Initial draft consolidating multiple sources. 