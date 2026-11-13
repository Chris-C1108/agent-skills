# `ddd-modeling-suite` (v2.0) 领域建模方法论套件：架构与风控规范

> **定位**：面向复杂软件系统与遗留代码现代化的端到端领域驱动设计（DDD）知识榨取、确定性蒸馏与运行时架构守卫套件。

---

## 一、 核心设计升级（V1 -> V2 重构对照）

针对多学科专家评审暴露的 6 大结构性缺陷，V2 完成了从“单向理想化逼问流水线”到**“认知友好访谈 + 溯源图谱蒸馏 + 确定性图校验”**的全面升级：

| 维度 | V1 缺陷与隐性假设 | V2 重构机制与落地实现 |
| :--- | :--- | :--- |
| **认知心理学 & 人类访谈** | 把内部 Schema (`T-P-I-P-O-S-E`) 直接当提问模板抛给用户，违反波兰尼默会知识悖论与工作记忆极限，易引发受访者防御或虚构规则。 | **双层解耦机制**：对外采用 **CIT 关键事件法（案例先行）+ 选项化收敛（A/B/C + 暂存待定区）+ 影子流程探针**，单轮严禁超过 3 问；对内映射为 7 步 `T-P-I-P-O-S-E` + `CRUDA` + `0/1/N` 结构化契约。 |
| **哲学 & 制度认识论** | 滥用波普尔证伪法（移除不崩溃即降级），误杀合规/审计/契约等制度性事实（忽视 Chesterton's Fence）。 | **四级证据认识论分层**：将领域规则划分为 `Tier 1 (hard_invariant)`、`Tier 2 (compliance_gate)`、`Tier 3 (configurable_policy)` 与 `Tier 4 (ui_convention)`，在 DMML 中分别路由至 `invariants` 与 `policies`。 |
| **社会工程 & 组织政治** | 假定单一受访者具备全局真相与裁决权，跨领域冲突缺乏 RACI 归属保护。 | **康威定律探针 + RACI 越权拦截**：在 `00-charter.md` 建立领域 Owner 映射；跨上下文推翻已生效不变量时，若当前受访者非上游 Owner，写入 `.ddd/00-parking-lot.md` 挂起待裁决。 |
| **软件工程 & 逆向 DDD** | 教条执行“1秒最终一致必拆聚合”，且将遗留代码 `@Transactional` 盲信为真实业务边界（幸存者偏差）。 | **竞争感知型聚合切分 + 事务坏味道审计**：引入 `architecture_profile` 与 `contention_profile`；逆向探针优先审计乐观锁/悲观锁与状态枚举，剥离大事务中的报表查询（CQRS `read_models`）与远程 I/O。 |
| **Agent Harness & 记忆溯源** | `01-raw-facts.md` 缺乏契约格式导致正则静默丢数据；压缩丢失 `Why` 与溯源指针，使局部重算失效。 | **全链路血缘溯源 (`traces_to`)**：统一定义 `## [FACT-001]` Markdown 契约；`compile_events.py` 采用 RFC JSON 双引号转义，保留 `fact_id`、`evidence_tier`、`rationale` 与 `traces_to`。 |
| **确定性静态守卫 (`dmml_linter.py`)** | 无 PyYAML 时降级为 `{"raw": content}` 导致死循环；缺失跨上下文环检测与 ID-Only 校验；状态机 BFS 布尔逻辑错误。 | **真·图论静态分析器**：内置零依赖 YAML 子集解析器；实现跨上下文 **DFS 环检测**、跨聚合 **ID-Only 引用强制拦截**、状态机 **BFS 可达性/死胡同/守卫确定性校验** 及 **`INVALIDATED` 脏节点阻断**。 |

---

## 二、 七阶段闭环执行状态机

```text
[Phase 0: 干系人宪章与术语校准] ──► .ddd/00-charter.md + .ddd/00-parking-lot.md
        │
[Phase 1: 认知友好深度访谈 / 代码逆向] ──► .ddd/01-raw-facts.md (## [FACT-001] 契约)
        │
[Phase 2: 溯源事件蒸馏压缩] ──(compile_events.py)──► .ddd/02-events.yaml (含 traces_to & rationale)
        │
[Phase 3: 战略划界与上下文拓扑] ──► .ddd/03-context-map.md ──► [人工门禁 1: 战略边界确认]
        │
[Phase 4: 战术模型并发装配] ──(按上下文切片)──► .ddd/04-models/<context>.yaml (DMML v2.0)
        │
[Phase 5: 确定性图校验与溯源审计] ──(dmml_linter.py)──► [人工门禁 2: 终审放行]
        │
[Phase 6: 领域宪法幂等注入] ──► 项目根目录 AGENTS.md (渐进式披露索引 + 4级规则守卫)
```

---

## 三、 组件清单与职责矩阵

- `SKILL.md`：主编排器工作流、7 阶段门禁协议与 Spartan 铁律。
- `probes/tpipeose-interrogation.md`：面向人类的 CIT 叙事访谈法、影子流程探针、`T-P-I-P-O-S-E` 因果链、`CRUDA` 生命周期矩阵、`0/1/N` 并发探针、CQRS 读模型探针及 `.ddd/01-raw-facts.md` 标准格式规范。
- `probes/falsification-probe.md`：四级证据认识论分层（含 Chesterton's Fence 合规保护）与跨领域冲突四步回溯协议（含 RACI 越权拦截）。
- `probes/legacy-code-probe.md`：反幸存者偏差的遗留代码逆向协议（状态机与锁优先审计、事务坏味道剥离、CQRS 读模型分离、ACL 防腐层提取）。
- `references/dmml-specification.md`：DMML v2.0 完整 YAML Schema（含 `invariants`、`state_machine.guard`、`policies`、`domain_services`、`sagas`、`read_models`、`traces_to`）。
- `references/agents-md-template.md`：幂等注入项目根目录 `AGENTS.md` 的三层渐进式披露宪法模板。
- `scripts/compile_events.py`：确定性 Markdown 事实编译器（支持中英文标点、JSON 安全引号转义、血缘溯源与零事件硬报错）。
- `scripts/dmml_linter.py`：确定性 DMML 静态分析器（内置无依赖 YAML 解析器、跨上下文 DAG 环检测、ID-Only 引用检查、状态机 BFS 可达性与 `INVALIDATED` 溯源阻断）。
