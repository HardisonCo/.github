# Verification & Specification Plan

This document defines **how we will know the integration work is *really* done**.  At its core, completion is proven by a comprehensive suite of executable specifications (specs/tests) that cover every file touched in `git diff main...HEAD`.

The workflow is intentionally simple:

```
Understand change  →  Write/extend spec  →  Run full spec suite
                                    ↘︎       ↗︎
                                       Pass?  
                                 yes ────────┘       no ───→ fix code / spec
```

If **all** specs pass in every CI matrix dimension, the work is considered finished.  Any failure (or test flake) automatically re-opens the task board until green.

---

## 1. Spec Authoring Ground-Rules

1. **One spec per diffed unit**  
   • Rust → `core/**/tests/*.rs` & `cargo nextest`  
   • TypeScript → `__tests__/*.test.ts` & `pnpm test`  
   • Lean proofs → `*.lean` unit tests or `#eval` checks  
   • CI/GitHub Actions → use `act` or workflow-test action for lint-style tests.

2. **Behaviour over implementation** – assert externally-observable effects, not private details.

3. **90 % diff-coverage** – at least one assertion per public API path or CLI entry point changed/added.

4. **Use golden-file snapshots** only for deterministic output; random / stochastic flows must mock randomness.

5. **Flake-free** – specs that fail intermittently block merge.

---

## 2. Mapping Diff → Spec Suites

| Cluster | Changed Items (examples) | Spec Location | Primary Runner |
|---------|--------------------------|---------------|----------------|
| Core Rust | `core/**` crates | `core/**/tests/*.rs` | `cargo nextest` |
| HMS Agents | `agents/hms-agent/**` | `agents/hms-agent/tests/*.rs` or `.ts` | `cargo nextest` / `pnpm jest` |
| CLI Tools | `tools/codex-cli/**` | `tools/codex-cli/__tests__/*.test.ts` | `pnpm jest` |
| Provers | `provers/**/*`, `*.lean` | inline Lean test files | `lean --run tests` via `economic_theorem_ci.yml` |
| Workflows | `.github/workflows/*` | `.github/workflows/tests/*` (yaml-lint) | `act`, `actionlint` |
| Docs | `docs/**` | markdown-lint + doctest in Rust/TS examples | `markdownlint`, `cargo test --doc` |

> **Tip** Run `scripts/select-tests.sh --paths <changed files>` during local dev to run only the impacted suites.

---

## 3. CI Integration

Each Phase-4 task that modifies code **must** append or update a spec.  CI enforces this by:

1. Failing if `diff-coverage < 90 %` (via `cargo llvm-cov`, `jest --coverage`, Lean coverage script).
2. Re-running the full validation matrix (Phase 5).  All dimensions must be ✅.

CI artefacts:

• `coverage-summary.html` published per job.  
• `lean_cache_stats.txt` to track hit-rate.  
• Redacted logs for HIPAA compliance.

---

## 4. “Definition of Done” Checklist

☑ All specs pass on the **first try** in the full matrix.  
☑ Diff coverage ≥ 90 % (Rust, TS) / 100 % (new Lean proofs).  
☑ No TODO / FIXME markers remain in touched files.  
☑ Security lead signs off HIPAA redacted logs.  
☑ Docs updated with any new config/env vars introduced by the code.

---

## 5. Immediate Actions (Today)

1. **Generate initial spec gap report** – fails CI if gaps exist
   ```bash
   gdiff | python3 scripts/spec_gap_report.py
   ```
2. **Create empty spec stubs** for any file that shows “No tests”.
3. **Wire stubs into CI** – failing with `#[ignore]` so pipeline stays green until implemented.

These steps will bootstrap the verification effort while the integration tasks (Phase 4) proceed in parallel.
