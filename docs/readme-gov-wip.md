<h1 align="center">Codex-GOV: Government-Focused AI Agent Framework</h1>
<p align="center"><img src="https://img.shields.io/badge/Government-Approved-blue" alt="Government Approved Badge" /></p>
<p align="center">An opinionated, MAS-aligned AI platform combining A2A protocol, CoRT reasoning and verification-first pipelines for federal, state, and local agencies</p>

<p align="center"><code>npm i -g @openai/codex</code></p>

![Codex demo GIF using: codex "explain this codebase to me"](./.github/demo.gif)

---

<details>
<summary><strong>Table of Contents</strong></summary>

<!-- Begin ToC -->

- [Experimental technology disclaimer](#experimental-technology-disclaimer)
- [Executive Overview](#executive-overview)
- [Quickstart](#quickstart)
- [Architecture at a Glance](#architecture-at-a-glance)
- [Key Capabilities](#key-capabilities)
- [Further Architecture](#further-architecture)
- [Security & Compliance](#security--compliance)
- [Demo Mode Walk-throughs](#demo-mode-walk-throughs)
- [Roadmap & Success Criteria](#roadmap--success-criteria)
- [Contributing & Community](#contributing--community)
- [License](#license)

<!-- End ToC -->

</details>

---

## Experimental technology disclaimer

Codex CLI is an experimental project under active development. It is not yet stable, may contain bugs, incomplete features, or undergo breaking changes. We're building it in the open with the community and welcome:

- Bug reports
- Feature requests
- Pull requests
- Good vibes

Help us improve by filing issues or submitting PRs (see the section below for how to contribute)!

## Executive Overview

Codex-GOV is a purpose-built AI agent framework designed for government agencies, integrating secure agent communication, advanced recursive reasoning, and compliance-first pipelines.

- Standardized A2A protocol supporting secure, authenticated inter-agent messaging across HMS.
- Chain of Recursive Thoughts (CoRT) engine enabling recursive, multi-round collaborative reasoning.
- Verification-first pipelines enforcing government-grade security & compliance (FedRAMP, FISMA, HIPAA).
- Modular, hierarchical agent ecosystem spanning all HMS components with specialized sub-agents.
- Phased roadmap: deep analysis, architecture design, core integration, security & compliance, verification-first gates, demos, and continuous improvement.

## Quickstart

Install globally:

```shell
npm install -g @openai/codex-gov
```

Set your OpenAI API key:

```shell
export OPENAI_API_KEY="your-api-key-here"
```

> **Note:** This command sets the key only for your current terminal session. You can add the `export` line to your shell's configuration file (e.g., `~/.zshrc`) but we recommend setting for the session. **Tip:** You can also place your API key into a `.env` file at the root of your project:
>
> ```env
> OPENAI_API_KEY=your-api-key-here
> ```
>
> The CLI will automatically load variables from `.env` (via `dotenv/config`).

### Government Extensions

Use the `codex-gov` CLI with flags to target government contexts:

```shell
codex-gov --agency <agency> --level <level> --cort --compliance <standards> "<your prompt here>"
```

For example:

```shell
codex-gov --agency HHS --level federal --cort --compliance FedRAMP "generate security compliance report"
```

Interactively launch Codex-GOV:

```shell
codex-gov
```

---

## Architecture at a Glance

<!-- TODO: Replace placeholder with canonical architecture Mermaid diagram -->
```mermaid
flowchart LR
  A[Supervisor Agent (HMS-DEV)] --> B[HMS-SYS Operations Agent]
  B --> C[Pipeline Orchestrator (Argo CD)]
  C --> D[Env Controller (Crossplane)]
  D --> E[Cloud Providers]
  B --> F[Ephemeral Preview Environments]
  B --> G[Chaos Sub-Agent]
  B --> H[Security & Compliance Engine]
  subgraph StateStore
    I[Central Environment & State Store]
  end
  B --> I
  G --> I
```

<!-- Architecture Legend -->
**Legend:**
- **A**: Supervisor Agent (HMS-DEV)
- **B**: HMS-SYS Operations Domain Agent
- **C**: Pipeline Orchestrator (Argo CD)
- **D**: Environment Controller (Crossplane)
- **E**: Cloud Providers (AWS/Azure/GCP)
- **F**: Ephemeral Preview Environments (per-PR sandboxes)
- **G**: Chaos Engineering Sub-Agent (Litmus/Gremlin)
- **H**: Security & Compliance Engine (SAST/DAST/Trivy)
- **I**: Central Environment & State Store (Prometheus/DB)

Arrows (--> / --) indicate primary control and data flows.

## Key Capabilities

- **Ephemeral Preview Environments:** Automatic per-PR sandboxed namespaces with full infra/app stack via Codefresh and Argo CD ApplicationSets.
- **Chaos Engineering Integration:** Scheduled Litmus/Gremlin experiments for pod/network resilience with results logged in the state store.
- **SecOps Scanning:** Embedded SAST/DAST/Trivy scans in verification-first pipelines, enforcing OPA policies.
- **Service Mesh Traffic Shaping:** Blue-green and canary control via Argo Rollouts (Istio/Linkerd) with progressive traffic shifting and SLO-based rollbacks.
- **A2A Protocol:** Secure, authenticated inter-agent messaging with CoRT context propagation.
- **CoRT Reasoning Engine:** Recursive multi-round decision-making with reasoning traces.
- **Governance & Compliance:** FedRAMP/HIPAA/FISMA enforcement via policy engines and compliance dashboards.
- **Demo Mode Orchestrator:** Two specialized demo flows: GitHub Issue Resolution and Deal Monitoring.
- **Phased Roadmap & Metrics:** Quarter-level rollout plan with success metrics (coverage, pass rates, compliance scores).

## Further Architecture
For detailed ASCII diagrams and alternate architecture views, see:
- [HMS Agent Architecture & Component Structure (ASCII)](docs/diagrams/hms-agent-architecture-ascii.md)
- [CoRT Framework Integration (ASCII)](docs/diagrams/cort-framework.md)

[See full Feature & Capability Matrix](docs/feature_matrix.md)

---

## Security & Compliance

Codex-GOV merges the HMS Security & Compliance Framework to deliver layered defense and continuous verification:

- **Identity & Access Management:** Authentication, RBAC, and agent identity lifecycle.
- **Data Protection:** Encryption, anonymization, classification, and tokenization.
- **Communications Security:** Secure A2A messaging with digital signatures and transport encryption.
- **Operational Security:** Audit logging, monitoring, and incident response.
- **Compliance Management:** Automated FISMA, FedRAMP, HIPAA, and NIST checks via OPA policy engines.

### Government-grade Security

- **FedRAMP (High):** Strict control implementation and ongoing assessment.
- **FISMA:** Comprehensive risk management and reporting.
- **HIPAA:** Protected data handling and privacy safeguards.

## Demo Mode Walk-throughs

### GitHub Issue Resolution Demo

Showcase a full GitHub issue resolution across HMS components using the Demo Orchestrator:

```shell
python demo_orchestrator.py --type github_issue --issue-id ISSUE_ID
```

This runs the scenario, applies CoRT reasoning, coordinates component agents, and generates a visualization at `./visualizations/github_issue_demo_<session>.html`.

### Deal Monitoring Demo

Demonstrate an end-to-end deal monitoring flow:

```shell
python demo_orchestrator.py --type deal_monitoring --config configs/deal_demo.yaml
```

Output visualizations will be saved at `./visualizations/deal_monitoring_demo_<session>.html`.

## Roadmap & Success Criteria

Below is the quarter-level rollout plan with key milestones:

| Quarter | Timeline (Months) | Key Phases                                  |
|---------|-------------------|---------------------------------------------|
| Q1      | 1–2               | Foundation & Planning                       |
| Q2      | 3–5               | Core Infrastructure & First Component       |
| Q3      | 6–9               | Knowledge Acquisition & CoRT Framework      |
| Q4      | 10–14             | Integration & External Components           |
| Q5      | 15–19             | Expansion & Advanced Capabilities           |
| Q6      | 20–24             | System-Wide Integration & Optimization      |

**Success Metrics:**
- **Preview Envs Lifecycle:** Provision and teardown success for 100+ PR-driven sandboxes.
- **Chaos Experiment Pass Rate:** ≥95% pass on scheduled resilience tests.
- **Verification Pipeline Pass Rate:** ≥98% for SAST/DAST/Trivy scans.
- **Compliance Scanning Pass Rate:** ≥99% for FedRAMP, FISMA, HIPAA checks.
- **Traffic Shaping Rollback Rate:** <5% of deployments requiring rollback.
- **A2A Messaging Success:** ≥99.5% successful secure inter-agent exchanges.

---

## Contributing & Community

We welcome contributions from government and open-source communities. To contribute:

1. Fork the `openai/codex-gov` repository and create a feature branch:
   ```shell
   git checkout -b feature/my-enhancement
   ```
2. Implement your changes and add relevant tests.
3. Ensure code follows the project style and passes linters/CI checks.
4. Commit with a clear message and push your branch:
   ```shell
   git push origin feature/my-enhancement
   ```
5. Open a Pull Request against `main`, describing your changes and referencing relevant issues.

Please adhere to our [Code of Conduct](./CODE_OF_CONDUCT.md) and sign the [Contributor License Agreement](./CLA.md) if prompted.

Join discussions in GitHub Issues or Discussions for feature requests, questions, and community engagement.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.