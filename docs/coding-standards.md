# HMS Coding Standards

This document consolidates all repository-wide coding-guideline material – it now supersedes the legacy `.codex/instructions.md` file (removed in the same pull-request).

## 1. General Principles

1. **Diff-First** – Every change must reference a concrete line in `git diff main...HEAD`.
2. **Spec-Driven** – New or modified code **requires** an executable specification (see `docs/VERIFICATION_PLAN.md`).
3. **Fail-Fast CI** – Linting and formatting run before compilation; compilation runs before integration tests; Lean proofs block merge.
4. **HIPAA Compliance** – Logs (console, CI, artefacts) must redact PHI (`***`) at source.

## 2. Language-Specific Conventions

### Rust

• Edition 2021.
• `cargo fmt --all` with default rustfmt config.  
• One module per file; public re-exports live in `mod.rs` only.  
• Prefer `thiserror` for error handling; avoid `Box<dyn Error>` in public APIs.

### TypeScript / Node

• Node 20 LTS target, `tsconfig.json` uses `es2022` libs.  
• Use `pnpm` for dependency management.  
• Tests: `jest` with ESM + `ts-jest`.  
• Absolute imports via `@/*` alias.

### Lean 4

• Pin to the tool-chain version agreed in Phase 3.  
• Keep each theorem ≤ 100 LOC where practical; use `import` not `open` for namespaces.  
• Proof files live next to the Lean module they verify.

## 3. Directory Layout

```
core/            # Rust workspace crates
agents/          # HMS Agent crates / bindings
provers/         # Lean + Rust back-ends
tools/           # CLI utilities (codex-cli, codex-rs…)
docs/            # Everything you’re reading now
scripts/         # Automation helpers – bash/python only
```

## 4. Commit Hygiene

• One logical change per commit; message starts with subsystem tag (e.g. `core:`).  
• No generated files, IDE settings or `.DS_Store`.

## 5. Reference Material

• The full Diff-to-Done process: `docs/DIFF_FIRST_ROLLIN_MASTER_PLAN.md`.  
• Spec/verification rules: `docs/VERIFICATION_PLAN.md`.
