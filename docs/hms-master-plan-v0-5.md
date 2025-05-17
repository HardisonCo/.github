# HMS Unified Master Plan v0.5 (draft)

**Purpose:** Provide a single, living blueprint for the Health Monitoring System (HMS) that harmonises dozens of satellite specs (HMS-SYS, HMS-A2A, HMS-DEV, etc.) into one actionable plan. It aligns with Codify's vision of verifiable, self-healing, multi-agent infrastructure for public-sector and enterprise workflows and serves as the coordination nexus for all future HMS extensions (e.g., the Economic Theorem-Proving MAS).

**Document Status:** Draft - Updated post-Sprint 1 implementation, outlining Sprints 2-4.

## 1 Strategic Goal & Objectives

**Primary goal:** Deliver a resilient, policy-compliant, and auditable Multi-Agent System (MAS) platform that continuously monitors, verifies, and optimises mission-critical services using formal methods and adaptive AI, while providing transparent human oversight and intervention capabilities.

**Key Performance Indicators (KPIs):**
*   **Resilience:** Achieve 99.9% uptime for the Supervisor and critical agents.
*   **Compliance:** 100% automated policy checks passed for agent actions.
*   **Scalability:** Support 1,000 concurrent agents with < 500ms task scheduling latency.
*   **Extensibility:** Reduce time to integrate a new agent skill by 50% (Baseline TBD).
*   **Verification Success Rate:** Achieve > 80% automated proof success for core Moneyball theorems (e.g., WAR/DRP/SPS bounds).
*   **Self-Healing Speed:** Detect and recover from simulated agent failures within 5 minutes.

## 2 Unified Architecture

(Diagram remains the same as v0.4 - Mermaid chart showing Supervisor, Agents, FFI, Verification, etc.)

### 2.1 Core Components

*   **HMS Supervisor (Rust):** Central orchestrator (Lifecycle, Task Assignment, Health Monitoring, GA Triggering).
    *   Maintains agent registry and task queue (in-memory V1, persistent V2).
    *   Exposes gRPC `SupervisorService` for agent spawning and task submission.
    *   Exposes gRPC `AgentService` for receiving heartbeats and status updates from agents.
*   **Agent Core (`agent_core`):** Basic agent logic (ID, State, `AgentService` client).
*   **Agent Skills (`agent_skills`):** Interface definitions for pluggable skills.
*   **Communication (`communication`):** Protobuf definitions and generated gRPC code.
*   **Verification (`verification`):** Formal proof backend interface (`ProofBackend`) and implementations (e.g., `DeepSeekBackend`).
*   **Self-Healing (`self_healing`):** Monitors agent health via heartbeats, triggers recovery actions (e.g., restart agent via Supervisor).
*   **Genetic Algorithm Engine (`genetic_engine`):** Optimises parameters (e.g., prover tactics/config) based on performance feedback.
*   **Policy Engine (`policy_engine`):** Enforces operational rules (stubbed V1).
*   **Data Store (`data_store`):** Central repository interface (stubbed V1).
*   **FFI Layer (`ffi`):** Python bindings (`hms_core` module) for Supervisor interaction via gRPC.
*   **Lean Libraries (`lean_libs`):** Formal specifications (e.g., `Moneyball.lean`).

## 3 Implementation Roadmap (Phased Sprints)

### Phase 1: Foundation (Sprints 0-1, Weeks 1-4)

*   **[DONE] Sprint 0: Scaffolding & Foundation**
    *   Setup Rust workspace (`hms`) with crates for core components.
    *   Define initial Protobuf messages (`AgentTask`, `ProofResult`, `SpawnAgentRequest`) & Supervisor service.
    *   Define workspace dependencies (`Cargo.toml`).
    *   Implement basic `ProofBackend` trait in `verification`.
    *   Setup basic CI (`ci.yml`) with build, format, clippy checks.
    *   Create FFI stub (`ffi/lib.rs`) with PyO3 basics.
    *   Generate `HMS_Master_Plan_v0.4.md`.
*   **[DONE] Sprint 1: Code Skeletons**
    *   Implement basic Supervisor gRPC server (`supervisor/main.rs`) with in-memory state.
    *   Implement basic `DeepSeekBackend` execution logic (`verification/deepseek.rs`) with temp file creation.
    *   Implement FFI Python functions (`ffi/lib.rs`) calling Supervisor gRPC.
    *   Add basic integration test placeholders in `ci.yml`.
    *   Generate `HMS_Master_Plan_v0.5.md` (this version).

### Phase 2: Specialisation (Sprints 2-4, Weeks 5-10)

*   **Sprint 2 (Weeks 5-6): Agent Core Lifecycle & A2A Foundation**
    *   **Protobuf:** Add `AgentService` (Heartbeat, UpdateTaskStatus) to `agent.proto`.
    *   **Supervisor:** Implement `AgentService` handlers; update state based on heartbeats/status.
    *   **Agent Core:** Implement basic agent (`hms-agent-core/src/main.rs` binary) that:
        *   Connects to Supervisor's `AgentService`.
        *   Sends periodic heartbeats.
        *   (Placeholder) Receives tasks (no execution yet).
    *   **FFI:** Add Python functions to query agent status via Supervisor.
    *   **CI:** Add test job to spawn Supervisor, spawn Agent Core binary, check heartbeat receipt.
*   **Sprint 3 (Weeks 7-8): Verification V1 & GA Engine V1**
    *   **Lean Library:** Create `hms/lean_libs/Moneyball.lean` defining core Moneyball concepts (WAR, DRP, SPS formulas/constraints) based on `moneyball_formal_specifications.json`.
    *   **Refine `DeepSeekBackend`:**
        *   Implement input formatting in `create_temp_lean_file` to generate valid Lean files importing `Moneyball` and stating the specific property/theorem from `AgentTask`.
        *   Investigate/implement relevant `deepseek-prover` CLI arguments for theory/context loading.
        *   Implement basic parsing of proof success/failure/term from prover output.
    *   **Implement `genetic_engine`:** Define `Genome` (e.g., prover tactics/config for Moneyball); implement basic mutation/crossover; simple fitness function stub (e.g., based on `ProofResult.status`).
    *   **Supervisor GA Trigger:** Implement logic to call `genetic_engine` on repeated proof failures for a specific theorem type (e.g., "WAR bounds check").
    *   **CI:** Add test job to submit a basic Moneyball proof task, check for prover execution, basic result parsing (success/fail).
*   **Sprint 4 (Weeks 9-10): Lean Library v0.2 & Verification Decision**
    *   **Phase 1 & 2 (Data Structures & Theorem Stubs)**
        *   Use `Finmap` for core inputs: `TradeAnalysisInput`, `DeficitAnalysisInput`, `SectorPrioritizationInput`.
        *   Implement precise `war_score`, `drp`, `sps` functions per JSON formulas.
        *   Add theorem stubs (`war_score_bounds`, `drp_conservative`, `sps_bounds`) with `admit` placeholders and JSON proof outlines.
        *   Add smoke-test `#eval` calls to confirm Lean file compiles and runs.
    *   **Phase 3 (Integrated Logic & Extended Domains)**
        *   Define `Integrated.economic_analysis_valid` and key invariants (`war_threshold`, etc.) as Props/axioms.
        *   Provide O3 Optimization placeholders (`O3.optimize_deals`, `monte_carlo_roadmap_simulation_optimized`).
        *   Provide HMS Dashboard stubs (`HMSDashboardInput`, `war_score_hms`, `project_deficit_impact_hms`).
        *   Add `#check` for these stubs in Lean to ensure registration.
    *   **Phase 4 (Verification vs Spec-Clarity Decision)**
        *   Document that v0.2 uses `Float` and proof stubs (`sorry`) for spec clarity.
        *   Outline v0.3: migrate to subtype-wrapped inputs (`{x // 0≤x≤...}`) for executable verification.
        *   Plan to fill `admit` proofs leveraging `Finmap`/`Finset` lemmas in v0.3.
    *   **CI Integration:**
        *   Add a CI job to compile the Lean file (`lake build` or `lean --make`).
        *   Smoke-test gRPC-based submission of one theorem proof task (even if it fails/admits).

### Phase 3: Integration & Optimization (Sprints 5-7, Weeks 11-16)

*   **Sprint 5 (Weeks 11-12): Data Store V1 & Agent Task Execution**
    *   Implement `data_store` V1 (e.g., PostgreSQL backend with `sqlx`).
    *   Supervisor persists agent/task state to DB.
    *   Agent Core: Implement basic task execution loop (receive task via gRPC stream or poll, call skill, update status).
    *   Define basic `AgentSkill` trait in `agent_skills`.
*   **Sprint 6 (Weeks 13-14): Theorem Proving Skill & GA Integration**
    *   Create `TheoremProvingSkill` in `agent_skills` that uses `verification` crate.
    *   Agent Core loads and runs `TheoremProvingSkill` based on `SpawnAgentRequest`.
    *   Supervisor uses GA results to update agent config (e.g., prover args) on spawn.
    *   Refine GA fitness function based on proof duration, success.
*   **Sprint 7 (Weeks 15-16): FFI Enhancements & Monitoring**
    *   Deploy Prometheus/Grafana stack (via Docker Compose or k8s manifests).
    *   Supervisor/Agents expose basic metrics (e.g., task queue size, agent counts, proof times).
    *   FFI: Add functions for submitting complex tasks, monitoring metrics.
    *   CI: Test full lifecycle: FFI submits task -> Supervisor assigns -> Agent proves -> Status updated -> Metrics scraped.

(Phases 4 and 5 remain high-level as before)

### Phase 4: Advanced Features (Months 5-6)

*   **Distributed Coordination:** Implement agent-to-agent communication layer.
*   **Advanced GA/RL:** Hybrid approaches, swarm proving strategies.
*   **Complex Self-Healing:** Workflow-based recovery, resource reallocation.

### Phase 5: Production Hardening (Months 7-8)

*   **Scalability Tuning:** Optimize DB queries, gRPC communication, load balancing.
*   **Security Audit:** Code review, dependency scanning, vulnerability assessment.
*   **DevSecOps Integration:** CI/CD pipelines, automated security checks, infrastructure as code.
*   **Governance & UI:** Develop admin UI, refine policy engine, implement audit trails.

## 4 Testing & Verification Strategy

*   **Unit Tests:** Per-crate testing (`cargo test`).
*   **Integration Tests:** CI jobs testing interactions (Supervisor <-> Agent, FFI <-> Supervisor, Prover Execution).
*   **End-to-End Tests:** Full lifecycle tests simulating user requests.
*   **Chaos Testing:** Simulate agent/network failures to test self-healing (Phase 3/4).
*   **Formal Verification:** Validate Lean proofs generated for Moneyball specs.
*   **Performance Testing:** Measure latency, throughput, resource usage under load (Phase 5).

## 5 Risks & Mitigations

*   **Prover Integration Complexity:** (Mitigation: Start with basic execution/parsing in Sprint 3, iterate). **[Updated]**
*   **Lean Library Development:** Requires Lean expertise. (Mitigation: Start with stubs based on JSON spec, collaborate with Lean experts).
*   **Scalability Challenges:** gRPC, DB bottlenecks. (Mitigation: Phased rollout, monitoring, async processing, consider message queue).
*   **GA Convergence:** Finding optimal prover params. (Mitigation: Start simple, add complexity, monitor fitness).
*   **FFI Stability:** Cross-language complexity. (Mitigation: Robust error handling, type conversions, integration tests).

## 6 Appendix

### A.1 Communication Protocol (agent.proto Summary)

*   **Services:** `SupervisorService`, `AgentService`
*   **Key Messages:** `SpawnAgentRequest/Response`, `AgentTask`, `ProofResult`, `TaskStatusRequest/Response`, `HeartbeatRequest/Response`, `UpdateTaskStatusRequest/Response`

### A.2 FFI Contract (`hms_core` Python module)

*   `ping_supervisor()`
*   `spawn_agent(skills: list[str], config: dict) -> str`
*   `submit_proof_task(theorem_id: str, lean_expr: bytes, axioms: list[str]) -> str`
*   `query_task_status(task_id: str) -> dict`
*   `query_agent_status(agent_id: str) -> dict` (Added Sprint 2)
*   *Additional functions for policy, self-healing, complex tasks added in later sprints.*

### A.3 CI/CD Workflow (`ci.yml` Summary)

*   **Triggers:** Push/PR to `main`.
*   **Jobs:**
    *   `lint_format_check` (rustfmt, clippy)
    *   `build_workspace` (`cargo build --workspace`)
    *   `unit_tests` (`cargo test --workspace`)
    *   `integration_test_supervisor_agent` (Added Sprint 2)
    *   `integration_test_prover` (Added Sprint 3)
    *   `integration_test_self_healing` (Added Sprint 4)
    *   *Further integration/e2e tests added later*

