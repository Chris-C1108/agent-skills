# Handoff2Docs & Hooks Integration Specification

## 核心设计目标 (Design Goals)
在 Agent 长周期项目协作中，避免上下文遗忘与重复犯错（Prevent Mistake Recurrence）。
当 `agents-md-lifecycle` 优化项目时，将 `handoff2docs` 植入项目的 `AGENTS.md` 与工程 hooks，强制生成双工文档对（Dual-Document Pair）并更新全局索引。

---

## Hooks 植入标准 (Hooks Integration Canon)

在目标项目中配置以下自动检测与触发机制：

### 1. Claude Code / OpenCode 会话结束提示
在项目规则或 `.claude/settings.json` 中配置会话完成时的检查点：
```text
HOOK: Before declaring a complex session complete or handing off, invoke `handoff2docs` to persist deliverables and lessons.
```

### 2. Git 门禁 Hooks (.husky / .git/hooks)
在 `pre-push` 或 `pre-commit` hook 中添加轻量检测，提醒归档重大重构：
```bash
# .husky/pre-push
# 检查是否存在未记录重大变更或提醒运行 handoff2docs
if [ -d "docs/handoff" ]; then
  echo "✔ handoff2docs ledger present."
fi
```

---

## 目录与文件命名规范 (Path & Naming Canon)

所有交付文件归档于当前项目根目录下的 docs/handoff/：

1. **交接文档 (Handoff Artifact)**：
   - 路径：`docs/handoff/YYYY-MM-DD-HHmmss-handoff.md`
   - 职责：记录会话上下文、已完成改动、当前工作区状态、待办事项、推荐使用的 Skills。
2. **经验教训文档 (Lesson Artifact)**：
   - 路径：`docs/handoff/YYYY-MM-DD-HHmmss-lesson.md`
   - 职责：复盘会话中遇到的阻碍、踩坑记录、根本原因剖析、有效解决方案、反模式（Anti-patterns）。
3. **全局索引总账 (Ledger Index)**：
   - 路径：`docs/handoff/handoff-readme.md`
   - 职责：以倒序表格维护所有 handoff 与 lesson 文档的索引、主题、关键词及跳转链接。

---

## 模板 1：交接文档 (YYYY-MM-DD-HHmmss-handoff.md)

```markdown
# Session Handoff: {SESSION_TITLE}
- Timestamp: {YYYY-MM-DD HH:mm:ss}
- Trigger: {USER_INTENT_OR_REASON}
- Working Directory: {CWD}

## 1. COMPLETED WORK (已完成成果)
- [x] {Item 1: 具体文件变更与功能落地}
- [x] {Item 2: 测试与验证结果}

## 2. CURRENT REPOSITORY STATE (当前工作区状态)
- Branch / Commit: {GIT_BRANCH_OR_STATUS}
- Active / Modified Files:
  - `path/to/file1.ext`: {brief change summary}
  - `path/to/file2.ext`: {brief change summary}

## 3. PENDING & NEXT STEPS (未决事项与后续规划)
- [ ] {Immediate Priority 1}
- [ ] {Immediate Priority 2}

## 4. SUGGESTED SKILLS & TOOLS (推荐后续调用的能力)
- `{skill-name}`: {why it should be called}
```

---

## 模板 2：经验教训文档 (YYYY-MM-DD-HHmmss-lesson.md)

```markdown
# Session Lesson & Anti-Patterns: {LESSON_TITLE}
- Timestamp: {YYYY-MM-DD HH:mm:ss}
- Focus Area: {DOMAIN / MODULE / COMPONENT}

## 1. PROBLEMS ENCOUNTERED (遇到的核心问题与故障)
- 现象描述：{具体的错误日志、崩溃表现或行为不一致}
- 复现路径：{触发该问题的最小操作步骤}

## 2. ROOT CAUSE ANALYSIS (根本原因剖析)
- {为什么会出现该问题？环境差异、API 误用、时序竞争还是架构缺陷？}

## 3. PROVEN SOLUTION (验证有效的解决方案)
- {经过实践检验有效的修复方案或代码片段}
- Done right: {做对的范例或规范示例}

## 4. PITFALLS & ANTI-PATTERNS (避坑指南与反模式禁令)
- FORBIDDEN (反模式)：{严禁再次出现的做法或错误假设}
- USE (正规做法)：{必须采用的标准模式或规范}
- Seen: Seen 1× ({YYYY-MM-DD})

## 5. AGENTS.MD PROPOSAL (建议升格为全局规则的内容)
- 若该教训具有普遍意义，应提炼为 1 行成对规则写入 AGENTS.md：
  - `RULE: Action (FORBIDDEN: Bad -> USE: Good)`
```

---

## 模板 3：全局索引总账 (docs/handoff/handoff-readme.md)

```markdown
# Handoff & Lessons Ledger (会话交接与经验总账)

本目录记录项目全生命周期中的 Agent 会话交接与经验教训。
新会话开始、重大架构变更或排查复杂故障时，必须优先检索本目录避免重复踩坑。

| 日期时间 (Timestamp) | 规则提炼 / 主题 (Lesson / Topic) | 频次 (Seen Count) | 状态 (Status) | 交接 (Handoff) | 教训 (Lesson) | 核心标签 (Tags) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| {YYYY-MM-DD-HHmmss} | {规则提炼与主题描述} | Seen 1× ({YYYY-MM-DD}) | 观察中 | [{filename}-handoff.md]({filename}-handoff.md) | [{filename}-lesson.md]({filename}-lesson.md) | `{tag1}`, `{tag2}` |
```

### 状态生命周期与 Seen 3× 晋升机制 (Status Lifecycle & Promotion)
- **状态生命周期 (Status Lifecycle)**：
  - `观察中 (Observing)`：问题初次或偶发捕获，处于观察期，记录在案以防复发，但不直接写入全局硬规则。
  - `PROMOTED (已晋升至 docs/rules/ 或 AGENTS.md)`：教训已升格为硬性系统规范，标明晋升去向（如 `PROMOTED (AGENTS.md)` 或 `PROMOTED (docs/rules/<name>.md)`）。
- **Seen 3× 晋升门槛 (Promotion Threshold)**：
  - 当同一类问题在 3 个不同会话日期累计捕获达到 `Seen 3×`（跨 3 次独立会话捕获）时，必须强制晋升为硬规则，写入 `docs/rules/` 或根目录 `AGENTS.md`，状态更新为 `PROMOTED`。
  - 单次偶发教训禁止直接写入根规范，防止规则库膨胀与噪声积累。

---

## AGENTS.md 规则集成标准 (Integration Rule)

在目标项目的 AGENTS.md 中，注入以下标准规则行：
```markdown
## WORKFLOW CONSTRAINTS (SPARTAN RULES)
- Review docs/handoff/handoff-readme.md before major refactors, complex bug fixes, or session start.
- FORBIDDEN: Repeating documented past mistakes -> USE: Consult docs/handoff/*-lesson.md or run handoff2docs.
- Before ending session or switching agent: Run `handoff2docs` to persist context and lessons.

## PROGRESSIVE DISCLOSURE POINTERS
- Handoff & lesson ledger: -> docs/handoff/handoff-readme.md
```
