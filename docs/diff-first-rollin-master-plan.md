# “DIFF → DONE” MASTER PLAN

Fully-merged, Rust-expert–approved roadmap for converting the current branch’s *git diff* into production-ready code, documentation and CI.

This file merges and de-duplicates the two previous planning artefacts that were circulating in parallel (the “UNIFIED DIFF-FIRST ROLL-IN PLAN” and the “Optimised Plan for Integrating the Diff Changes”).  It is now the single source of truth for the integration effort.

> **Everything in this document is traceable to a line or file that changed in** `git diff main...HEAD`.  Before starting any task, run the diff and confirm the file in question actually appears.

---

## High-Level Structure

Phase 0 Prerequisites & Tooling  (~½ day)  
Phase 1 Diff → Structured Inventory  (~1 h)  
Phase 2 Rapid Triage & Risk Heat-Map  (~½ day)  
Phase 3 Context & Stakeholder Alignment  (1–2 days)  
Phase 4 File-by-File Integration Tasks  (3–4 days)  
Phase 5 Validation Matrix & Shadow CI  (1 day)  
Phase 6 Roll-Out, QA & Monitoring  (3 days)  
Phase 7 Close-Out & Knowledge Capture  (~½ day)

Each phase produces a tangible artefact that becomes the explicit input for the next phase.

---

## PHASE 0 Prerequisites & Tooling

| ID | Action |
|----|--------|
| 0.1 | **Create feature branch**: `ci-integrate/theorem-pipelines` |
| 0.2 | **Run canonical diff** and park the result:  
`git diff main...HEAD > /tmp/full.diff` |
| 0.3 | **Install / verify helper scripts** (or stub them if missing):  
`scripts/diff_to_csv.py`, `scripts/select-tests.sh`, `scripts/lean_cache_stats.sh` |
| 0.4 | **Handy aliases** (append to your shell rc):  
`alias gdiff="git diff --name-status main...HEAD"`  
`alias gshadow="gh workflow run shadow-ci.yml -F dry_run=true"` |
| 0.5 | **Book 30-min alignment call** with Docs, CI, Security & Prover leads – meeting occurs at the start of Phase 3. |

> **Note** If `scripts/diff_to_csv.py` is missing, create a minimal version that consumes `STDIN` (the diff) and emits `status,path,cluster,owner,risk_level` so that the rest of the pipeline can proceed without re-planning.

---

## PHASE 1 Diff → Structured Inventory

1. **Generate inventory**  
   ```bash
   gdiff | ./scripts/diff_to_csv.py > docs/component_inventory.csv
   ```
   Columns: `status, path, cluster, owner, risk_level`

2. **Initial cluster mapping** (editable YAML inside the script):
   ```yaml
   .github/workflows/**:  CI
   core/**:               Core Workspace
   agents/hms-agent/**:   HMS Agent
   tools/**:              CLI Relocation
   provers/**, *.lean:    Provers
   docs/**, scripts/**:   Docs & Scripts
   "*":                  Misc
   ```

3. **Commit** `docs/component_inventory.csv` – this is the first artefact the whole team can see.

---

## PHASE 2 Rapid Triage & Risk Heat-Map

| Step | Description |
|------|-------------|
| 2.1 | Auto-count LoC added & removed per cluster; set `risk_level = high` if > 5 KLoC **or** the diff touches secrets / credentials.  Append the colour-coded results to `component_inventory.csv`. |
| 2.2 | **Shadow CI dry-run**:  
`gshadow`  
Runs the full workflow graph once with `if: inputs.dry_run`.  Collect missing secrets, cache misses, runtime errors (max 30 min). |
| 2.3 | **Log blockers** in `docs/risk_register.md` (examples: missing `HIPAA_REDACTOR_URL`, Lean tool-chain mismatch, Rust cache miss-rate > 80 %). |

---

## PHASE 3 Context & Stakeholder Alignment

1. **Background reading**  
   `docs/HMS_Master_Plan_v0.5.md`, `docs/UNIFIED_MASTER_PLAN.md`, `.codex/instructions.md` (fold-in content even if empty today).

2. **Live alignment call** (from 0.5) – agenda:
   • Concurrency groups & cache keys  
   • Lean 4 version pin  
   • HIPAA log-redaction rules  
   • CHANGELOG replacement  
   • CLI relocation impact

3. **Decisions → MoM** (minutes-of-meeting):
   • CHANGELOG → GitHub Releases **plus** `docs/release_notes/`  
   • `.codex/instructions.md` → merged into `docs/CODING_STANDARDS.md` with backlink from `docs/README.md`.

---

## PHASE 4 File-by-File Integration Tasks

Canonical task board (import into Jira / Trello):

| ID | File(s) | Task | Owner |
|----|---------|------|-------|
| **CI-1** | `.github/workflows/bug-triage.yml` | Align cron `0 */6 * * *`, reuse shared labeler, add `concurrency` key | Ops |
| **CI-2** | `economic_theorem_ci.yml`, `lean_theorem_integration.yml` | Pin Lean 4, use `leanprover/lean-action@v1`, `rust-cache@v2`, matrix `{os,rust}` | Prover |
| **CI-3** | `pr-environments.yml`, `prover.yml` | Name envs `hms-pr-${{ github.event.number }}-env`, auto-delete on PR close | Ops |
| **CI-4** | `.github/workflows/ci.yml` | Insert **theorem-verify** job, drop duplicate doc checks | CI Lead |
| **CORE-1** | `core/**` | Update `[workspace]` members, run `cargo fix --workspace --edition 2021` | Core |
| **AGENT-1** | `agents/hms-agent/**` | Register agent in `core/crates/supervisor/agents.rs`; stub FFI facade | Core / Agent |
| **CLI-1** | `tools/codex-cli/**`, `tools/codex-rs/**` | Update package.json workspaces, Jest paths, docs URLs | Front-end |
| **PROVER-1** | `provers/**/*`, `*.lean` | Add mathlib & economic paths to `Lakefile`, cache `.lake/build` | Prover |
| **DOC-1** | `CHANGELOG.md` (deleted) | Migrate entries → `docs/release_notes/2024-Q2.md` | Docs |
| **HOOK-1** | `.husky/pre-commit` | `nx affected:lint`, `cargo fmt -- --check`, `leanpkg build` gated by path filters | DevEx |
| **IGN-1** | `.gitignore` | Remove obsolete CLI patterns; add `*.lake`, `*.lease` | DevEx |

> **Mapping removed → new locations**  
> • Old `codex-cli` / `codex-rs` now live under `tools/…` – update CI, docs and import paths accordingly.  
> • `CHANGELOG.md` is superseded by release-note files per quarter in `docs/release_notes/`.

---

## PHASE 5 Validation Matrix & Shadow Runs

| Dimension | Values |
|-----------|--------|
| OS | `ubuntu-latest`, `macos-latest` |
| Rust | `stable`, `nightly` |
| Lean | `4.1.0`, `4.2.0` |
| Node | `20.x LTS` |
| Dry-run | `true` / `false` |

**Pass gates**
• All jobs succeed ≤ 15 min  
• Lean lake tests ≤ 90 s, cache hit-rate ≥ 70 %  
• Logs automatically redact PHI (`***`)  
• `cargo nextest` & `pnpm test` green

Iterate until the matrix is all green.

---

## PHASE 6 Roll-Out, QA & Monitoring

1. **Test PR** – push the integration branch; run live CI (non-dry-run).  
2. **Lightweight QA** – ensure `bug-triage` labels once/6 h; Lean jobs trigger only on `**/*.lean` changes.  
3. **Refinement** – tune schedules, concurrency groups, secret scopes.  
4. **Final review** – green board + Confluence update.  
5. **Merge & monitor** – merge to `main`, tag `v0.4.0`, 48-hour Grafana watch (workflow times, Lean cache hits, redactor stats).

---

## PHASE 7 Close-Out & Knowledge Capture

| Step | Output |
|------|--------|
| 7.1 | 30-min retro – document wins & pain points |
| 7.2 | Update SOP: *How to add a workflow / Lean proof* |
| 7.3 | Archive feature-branch SHA in `docs/release_notes/2024-Q2.md` |

---

## Acceptance Checklist (all must be ☑ before merge)

☑ `docs/component_inventory.csv` committed  
☑ CI passes full matrix ≤ 15 min  
☑ Lean proofs green; lake cache ≥ 70 % hits  
☑ `cargo nextest` & `pnpm test` green  
☑ Single consolidated coding-standards doc  
☑ HIPAA redaction validated by Security lead

---

## Immediate Next Steps (--> Today)

1. Run `git diff main...HEAD` and commit `component_inventory.csv`.  
2. Kick off the first shadow-CI dry-run with `gshadow`.  
3. Schedule the stakeholder call for tomorrow 10 AM local.  
4. Triage any missing helper scripts (see Phase 0).

> Follow this plan end-to-end and you’ll integrate **100 % of the diff**—Rust crates, Lean proofs, CLI relocation, new CI—cleanly, quickly and compliantly, exactly as prescribed by senior Rust engineers and advanced AI-driven tooling.
