# AGENTS.md

## CONTEXT & STACK
- Environment: {RUNTIME_VERSION} (e.g., Node 22 / Python 3.12 / Go 1.23)
- Framework: {FRAMEWORK} (e.g., Next.js App Router / FastAPI / Spring Boot)
- Package Manager: {PKG_MGR} (e.g., pnpm / uv / cargo)
- Harness / Runtime: {HARNESS_RUNTIME} (e.g., DeepSeek Harness / Cordis / Standalone)

## CRITICAL COMMANDS
- Build: `{BUILD_CMD}`
- Test Single: `{TEST_SINGLE_CMD}`
- Test All: `{TEST_ALL_CMD}`
- Lint & Fix: `{LINT_CMD}`
- Type Check: `{TYPECHECK_CMD}`
- Harness Eval: `{HARNESS_EVAL_CMD}` (if DeepSeek Harness enabled, e.g. `dsh eval`)

## WORKFLOW CONSTRAINTS (SPARTAN RULES)
- NO polite preamble. Output diffs or direct answers immediately.
- Run typecheck and single test before declaring any task complete.
- Review `docs/handoff/handoff-readme.md` before major refactors or when investigating recurring bugs.
- FORBIDDEN: Repeating documented past mistakes -> USE: Consult `docs/handoff/*-lesson.md` or run `handoff2docs`.
- Before ending session or switching agent: Run `handoff2docs` to persist context and lessons.
- FORBIDDEN: Reversing deliberate decisions or proposing rejected options -> USE: Check docs/decisions/ first.
- FORBIDDEN: Direct mutations to `{CRITICAL_SCHEMA_FILE}` -> USE: Migration scripts.
- Code style: `{CODE_STYLE_RULE}`.
- Git flow: Branch prefix `{BRANCH_PREFIX}`. Atomic commits with conventional commit syntax.

## PROGRESSIVE DISCLOSURE POINTERS
- Handoff & lessons ledger: -> `docs/handoff/handoff-readme.md`
- Architecture decisions & rejected archive: -> docs/decisions/
- Backend architecture & API schema: -> `docs/rules/backend.md`
- Frontend state & component specs: -> `docs/rules/frontend.md`
- Database & migration protocols: -> `docs/rules/database.md`
- Deployment & CI pipelines: -> `docs/rules/ci.md`
