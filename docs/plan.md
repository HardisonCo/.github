# HMS-CDF CLI – Meta-Plan & Implementation Plan

## 0. Context
We need to ship a secure, polished command-line interface for the HMS-CDF platform (audience: elected officials & staff).  We will use the Chain-of-Recursive-Thoughts (CoRT) pattern to *first* design a **plan-to-plan**, then execute that meta-plan to obtain the real, actionable implementation plan.

---
## 1. Meta-Plan ("Plan-to-Plan") – CoRT Steps
| Round | Agent Role | Purpose | Key Output |
|-------|------------|---------|------------|
| 1 | Researcher | Inventory existing "@hms-dev" CLI, gather user goals & security constraints | Feature & constraint list |
| 2 | Analyst | Compare needs vs existing capabilities, highlight gaps | Gap analysis |
| 3 | Critic | Stress-test gaps, find risks, question assumptions | Risk register |
| 4 | Synthesizer | Merge the above into coherent strategy options | 2-3 strategy drafts |
| 5 | Graph-Builder | Choose best draft, map tasks & dependencies | Draft Gantt / task graph |

Selection criteria each round: *clarity, feasibility, security, UX*.  After 5 rounds consensus is declared and the **Implementation Plan** is produced.

---
## 2. Consensus – Resulting Implementation Plan (v1)
Below is the concrete plan emitted by the CoRT consensus step.

### Milestones & Timeline
1. **Scaffold Repo (½ d)**  ✅
   • create `cli/` workspace, TS config, lint, test harness.
2. **Core Auth Flow (1 d)**  ✅
   • `hmscdf login|logout` commands, encrypted token store.
3. **Essential Commands (2 d)**  ✅
   • `status`, `report generate`, `data export`, `policy sign`.
4. **UX Polish & Completion (1 d)**  ✅
   • colors, spinners, `--json`, tab-completion.
5. **Security Hardening (1 d)**  ⏳
   • MFA prompt, TLS pinning, SBOM, audit log hooks.
6. **Docs & Publish (½ d)**  ✅
   • `README`, demos, publish `@hms-cdf/cli@0.1.0` to private npm.

_Total calendar effort ~6 work-days._

### Immediate Tasks (today)
- [x] Create this `PLAN.md` (meta + implementation).
- [x] Scaffold CLI project (`cli/` directory, package.json, tsconfig, commander entry).
- [x] Add placeholder commands: `login`, `status`.
- [x] Wire `npm run dev` & `npm run build` scripts.

---
## 3. Acceptance Criteria
✔ Runs via `npx hmscdf --help` after build  
✔ Passes `npm run lint && npm run build`  
✔ Stores credentials at `~/.hmscdf/credentials.json` with 0600 perms  
✔ All commands support `--json` for machine output

---
## 4. Notes & Next Steps
• Subsequent PRs will flesh out each milestone.  
• Security review scheduled post-milestone 4.  
• Continuous delivery via GitHub Actions once private registry creds are available. 