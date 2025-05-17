# HMS Master Plan v0.7

// The rest of the content is identical to v0.6 but with 'Next Phase (v0.7 Draft)' renamed to 'Next Phase (v0.7)' to indicate finalized status. 

## Repository Refactor & CLI Consolidation Plan (v0.7)

> **Problem Statement:** The project root currently hosts many top-level folders (status-system, lean_libs, hms-ffi-protos, HMS-DEV, hms-agent, hms, examples, economic-theorem-prover, doc-gen, codex-rs, codex-cli) that create cognitive overhead, redundant code paths, and brittle import logic. We need a deliberate strategy to inventory, classify, and re-home these components into a coherent monorepo layout.

### Guiding Principles
1. **Domain Coherence:** Group code by bounded context (Core HMS, FFI, Agents, Provers, Docs, Tooling).
2. **Single Source of Truth:** Shared crates/libs live once; consumers import via workspaces or package managers.
3. **CLI Gateway Pattern:** Expose one entry-point per domain via `cargo install`, `pip install`, or `npm exec`—avoid scattered ad-hoc scripts.
4. **Incremental Migration:** Preserve `git` history with `git mv`; maintain compatibility shims until downstream paths are updated.
5. **Automated Validation:** CI enforces new path conventions and detects stray root-level additions.

### Proposed Top-Level Layout (post-cleanup)
```
/
├── core/                # Rust workspace: supervisor, agent_core, policy_engine, self_healing…
│   └── Cargo.toml
├── ffi/                 # all PyO3 & gRPC proto generation
│   ├── proto/           # .proto defs shared across langs
│   ├── rust/            # ffi crate(s)
│   └── python/          # wheels & helper libs
├── provers/             # Lean libs + DeepSeek integration
│   ├── lean_libs/
│   └── rust_backend/
├── agents/              # hms-agent crate + examples
├── tools/               # repo-wide utility CLIs (codex-rs, codex-cli, doc-gen, status-system)
├── examples/            # polished end-to-end demos (cargo, python, bash)
├── docs/                # markdown + diagrams (incl. Moneyball plans)
└── scripts/             # dev-ops helpers (rename_md_files.sh …)
```

### Work Breakdown Structure
| Phase | Duration | Tasks | Output |
|-------|----------|-------|--------|
| **A** Inventory & Dependency Graph | 2d | • Run `cargo tree`, `pipdeptree`, `npm ls`<br>• Map CLI entry-points & shared libs | *inventory.json* | 
| **B** Proposed Mapping Review | 1d | • Align teams on new layout<br>• Document path translations | *layout-proposal.md* | 
| **C** Mechanical Moves (Git) | 3d | • `git mv` folders to new layout<br>• Update Cargo workspaces, `setup.py`, `package.json` paths | new directory structure | 
| **D** Build & CI Fixes | 2d | • Adjust GitHub Actions matrix<br>• Fix import paths & module names<br>• Add root-level path-lint job | green CI | 
| **E** Deprecation & Shims | 1d | • Create thin wrapper CLIs forwarding to new bins for 1 release cycle | compat scripts | 
| **F** Documentation Update | 1d | • Update READMEs, diagrams, architecture docs | refreshed docs | 

Total: **10 developer-days ~ 2 calendar weeks** (Sprint 5 overhead already planned).

### Migration Automation
- Use `justfile` recipes for `just move-crate <src> <dest>`.
- Add a `repo_layout.toml` manifest; a Python script validates folder placement pre-commit.

### Research Agenda
1. **Monorepo vs Polyrepo Tooling:** Evaluate `pants` or `nx` for cross-lang builds.
2. **Incremental Compilation Caching:** Test `sccache`/`bazel-remote` to keep CI time ≤ 15 min.
3. **CLI Telemetry:** Instrument unified CLIs to emit usage metrics for future pruning.

### Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Hidden path assumptions in notebooks/scripts | Build breaks | `ripgrep` sweep + automated refactor scripts |
| Large Git history rewrite | Contributor confusion | Use `git mv` (preserves history) & announce changes early |
| CI matrix explosion | Slower pipelines | Use composite actions & dependency caching |

### Approval Checklist
- [ ] Inventory report accepted
- [ ] Directory layout finalised
- [ ] CI green after mechanical moves
- [ ] Docs updated & wrapper shims published

> Upon approval, Phase A begins immediately with target completion by *Sprint 5, Day 3*. 