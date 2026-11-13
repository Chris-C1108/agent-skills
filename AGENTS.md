# AGENTS.md

## WORKSPACE PURPOSE & ARCHITECTURE
- Primary Mission: Dedicated Personal Studio for Authoring, Quality Gatekeeping, and Deploying AI Agent Skills.
- Core Assets (`skills/`): Incubating 3 independent, isolated skills (`modern-userscript`, `handoff2docs`, `agents-md-lifecycle`).
- Tooling & Support: `scripts/` (scaffold, lint, sync), `docs/` (standards, studio handoff), `user-ref/` (external references).
- Boundary Invariant: Each skill in `skills/<name>/` is completely autonomous. FORBIDDEN: Cross-skill coupling or polluting repo root with single-skill logic.
- Target Runtimes: `~/.agents/skills` (Claude Code / OpenCode / Windsurf), `~/.codex/skills` (Codex CLI / App).

## CRITICAL COMMANDS
- Scaffold Skill: `npm run new-skill <skill-name> -- --desc "<brief>"`
- Lint Skills: `npm run lint`
- Sync All Skills: `npm run install:all`
- Sync Single Skill: `node scripts/install.js --skill <skill-name>`
- List Ready Skills: `npm run list`
- Audit Root Spec: `npm run audit:agents-md`
- Harness Eval: `dsh eval --suite default` (if DeepSeek Harness active)

## WORKFLOW CONSTRAINTS (SPARTAN RULES)
- NO polite conversational fluff. Skip preamble.
- Always run `npm run lint` before declaring any skill development or edit task complete.
- Keep each `SKILL.md` <= 200 lines and root `AGENTS.md` <= 150 lines.
- FORBIDDEN: Direct guesswork when confidence < 90% -> USE: Clarifying questions.
- FORBIDDEN: Submitting untested skills -> USE: Local sync test via `npm run install:all`.
- FORBIDDEN: Cross-skill boundary pollution -> USE: Keep each skill in `skills/<name>/` strictly isolated and self-contained.
- FORBIDDEN: Polluting workspace root or other skills with single-skill artifacts -> USE: Confine skill-specific tasks and configs inside `skills/<name>/`.
- Review `docs/handoff/handoff-readme.md` before major refactors, complex bug fixes, or session start.
- FORBIDDEN: Repeating documented past mistakes -> USE: Consult `docs/handoff/*-lesson.md`.
- Keep rules paired: state prohibited action and required replacement.

## PROGRESSIVE DISCLOSURE POINTERS
- Skill development standards: -> `docs/rules/skill-authoring.md`
- Studio handoff & lessons ledger: -> `docs/handoff/handoff-readme.md`
- ADHD Spartan style guide: -> `skills/agents-md-lifecycle/references/adhd-style-guide.md`
- DeepSeek Harness guide: -> `skills/agents-md-lifecycle/references/deepseek-harness-guide.md`
