# agents-md-lifecycle 技能持续改进实施跟踪与管理看板 (todo.md)

## 技能改进目标
本文件仅跟踪 `skills/agents-md-lifecycle/` 技能本身的持续改进落地。
依据 AI Agent 记忆机制（RFC/ADR/Rejected 指针）、magpie（错题本/Seen 3×/诚实验收）及 yoyo-gasp（硬门禁）事实分析结论，对 `agents-md-lifecycle` 的模板、契约及工作流进行增强。

---

## 任务执行状态

### 任务 1：轻量 ADR 决策体系与模板集成 (属于 agents-md-lifecycle 模板)
- [x] 1.1 在 `skills/agents-md-lifecycle/references/template-adr.md` 提供标准决策记录模板（含 Status: Accepted/Rejected/Superseded 及 Alternatives 分析）
- [x] 1.2 更新 `skills/agents-md-lifecycle/references/software-template.md`：注入决策库路由指针与防翻案约束
- [x] 1.3 更新 `skills/agents-md-lifecycle/references/non-software-template.md`：注入决策库路由指针与防翻案约束

### 任务 2：教训频次跟踪与 Seen 3× 晋升机制 (属于 agents-md-lifecycle 演进工作流)
- [x] 2.1 更新 `skills/agents-md-lifecycle/references/handoff-workflow.md`：升级目标项目的索引总账模板，新增 `Seen Count` 与 `Status` (观察中 / PROMOTED) 列
- [x] 2.2 更新 `skills/agents-md-lifecycle/references/evolution-prompts.md`：在 JSON 契约中注入 `seen_count`、`promotion_action` 与 `promotion_target` 判定

### 任务 3：工作流整合与质量门禁升级
- [x] 3.1 更新 `skills/agents-md-lifecycle/SKILL.md`：在阶段五与阶段六工作流中整合融合修改规则、决策治理及 Seen 3× 晋升流水线（154 行 <= 200 行上限）
- [x] 3.2 升级 `skills/agents-md-lifecycle/scripts/audit_agents_md.py`：扩展检查目标项目指针有效性与合规性
- [x] 3.3 保持与其他独立技能（`skills/handoff`, `skills/modern-userscript`）及仓库根目录的严格边界，不跨界污染
