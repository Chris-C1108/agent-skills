---
name: handoff2docs
description: Compact the current conversation into structured handoff and lessons-learned documents inside docs/handoff/ to prevent repeating past mistakes and enable seamless multi-agent transitions.
triggers:
  - handoff2docs
  - /handoff2docs
  - handoff
  - /handoff
  - 交接
  - 会话交接
  - 归档经验教训
  - 记录踩坑与总结
---

# Handoff2Docs: Session Knowledge & Lessons Archiver

将当前会话提炼为结构化交接文档与避坑经验教训，实现长周期会话知识沉淀与防重复犯错机制。
基于 Matt Pocock skills 生态规范 (https://github.com/mattpocock/skills) 演进，升级为项目内持久化知识总账。

---

## 执行流水线 (Execution Pipeline)

当接收到交接指令时，依次执行以下确定性步骤：

### 步骤一：时间戳与目录准备
1. 获取当前系统时间，格式化为 `YYYY-MM-DD-HHmmss`（如 `2026-09-29-153000`）。
2. 检查项目根目录下是否存在 `docs/handoff/` 目录；若无，立即创建。

### 步骤二：生成交接文档 (Handoff Artifact)
- 目标路径：`docs/handoff/YYYY-MM-DD-HHmmss-handoff.md`
- 结构规范：遵循 [template-handoff.md](references/template-handoff.md)。
- 核心要素：
  - 会话目标与触发原由。
  - 已完成事项清单与验证结果。
  - 当前 Git 分支、状态与核心变更文件列表。
  - 未决议题、待办事项（Next Steps）与明确的交接指引。
  - 推荐下一个 Agent 调用的 Skills（Suggested Skills）。

### 步骤三：生成经验教训文档 (Lesson Artifact)
- 目标路径：`docs/handoff/YYYY-MM-DD-HHmmss-lesson.md`
- 结构规范：遵循 [template-lesson.md](references/template-lesson.md)。
- 核心要素（杜绝再次犯错）：
  - 会话中遇到的核心故障、报错或逻辑死锁。
  - 根本原因分析（环境、配置、API 破坏性变更等）。
  - 验证有效的解决方案与具体改动。
  - 避坑禁令与反模式（必须采用成对语法：`FORBIDDEN: X -> USE: Y`）。
  - 提炼 1 条原子级规则，准备回填至项目 `AGENTS.md`。

### 步骤四：维护全局索引总账 (Update Ledger)
- 目标路径：`docs/handoff/handoff-readme.md`
- 若文件不存在，初始化表格头：
  ```markdown
  # Handoff & Lessons Ledger (会话交接与经验总账)

  | 日期时间 (Timestamp) | 规则提炼 / 主题 (Lesson / Topic) | 频次 (Seen Count) | 状态 (Status) | 交接 (Handoff) | 教训 (Lesson) | 核心标签 (Tags) |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  ```
- 将当前会话生成的条目插入表格首行（倒序排列），状态默认为 `观察中`，频次初始标记为 `Seen 1× ({YYYY-MM-DD})`。

### 步骤五：脱敏与规范审查
- 过滤所有 API Key、密码、Token、个人隐私等敏感数据。
- 检查项目根目录 `AGENTS.md` 是否已声明查阅与交接约束：
  `Review docs/handoff/handoff-readme.md before major refactors, complex bug fixes, or session start.`
  `FORBIDDEN: Repeating documented past mistakes -> USE: Consult docs/handoff/*-lesson.md or run handoff2docs.`

---

## 引用模板清单
- [交接文档模板](references/template-handoff.md)
- [经验教训模板](references/template-lesson.md)
