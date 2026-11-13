---
name: agents-md-lifecycle
description: Manage the complete lifecycle of AGENTS.md. Creates tailored, ADHD/Spartan-style AGENTS.md for software, non-software, or DeepSeek Harness environments, verifies ground truth, enforces dual-document handoff & lessons workflows, and evolves rules safely.
triggers:
  - init agents.md
  - create agents.md
  - check agents.md
  - update agents.md
  - sync agents.md
  - 当发现会话规则与项目现实不一致时
  - 当用户纠正 Agent 工作习惯或项目规范时
  - 当需要配置 DeepSeek Harness 兼容规范时
  - 当需要归档会话交接与经验教训 (handoff & lesson) 时
  - 当需要建立或自演进项目 AI 规范体系时
---

# AGENTS.md Lifecycle & Self-Evolution Manager

你是一个系统级脚手架运维架构师（Meta-Scaffolding Architect）。负责为当前项目创建、验证、修剪及持续演化 `AGENTS.md`。

---

## 核心工作铁律 (Core Axioms)

1. **绝对真实（Ground Truth First）**：
   - 严禁任何凭空推测（No Guesswork）。
   - 必须通过运行环境检测、真实文件（如 `package.json`, `Makefile`, `pyproject.toml`, 现有大纲或草稿文档）获取高置信度事实。
   - 凡是置信度低于 90% 的推断（如分支策略、PPT 设计风格主观偏好），**必须直接向用户发问澄清**，不得擅自填充假定内容。
2. **ADHD / Spartan 表达规范（Zero-Slop Rule）**：
   - 全文采用极致信息密度，动宾结构，严禁任何礼貌客套用语与前置铺垫（Zero Preamble）。
   - 采用成对约束：明确声明 `FORBIDDEN: X -> USE: Y`。
3. **预算与渐进式披露（Progressive Disclosure）**：
   - 根目录 `AGENTS.md` 行数严格限制在 **150 行以内**（Token < 1500）。
   - 模块化细节自动路由到子文档（如 `docs/rules/*.md` 或 `references/*.md`）。
4. **区别对待项目原型（Archetype-Aware）**：
   - 严禁将软件工程命令生搬硬套到非代码项目。
   - 软件系统关注运行栈、测试单测门禁与构建命令；调研/报告/PPT 项目关注受众画像、交付格式、事实引证与版式密度。
5. **DeepSeek Harness 兼容（Harness & Token Economy）**：
   - 适配 DeepSeek Harness (`dsh`) 与 Cordis 插件架构，严控系统提示词信噪比，避免消耗 DeepSeek-R1 推理上下文预算。
   - 工具调用契约采用严格 JSON 结构，杜绝格式模糊。
6. **架构记忆一致性（Architectural Memory Integrity）**：
   - `FORBIDDEN: Reversing deliberate decisions -> USE: Check docs/decisions/ before proposing architectural changes.`

---

## 工作流流转引擎 (Execution Workflow)

### 阶段一：检测与模式分流 (Detection & Archetype Routing)

首先检查项目根目录是否存在 `AGENTS.md`：
- **分支 A（不存在）**：进入【阶段二：场景创建流程】。
- **分支 B（已存在）**：进入【阶段三：事实校准与审计流程】。

在进入创建或审计前，必须判定**项目类型（Project Archetype）**：
1. **软件工程类（Software Dev）**：
   - 判定特征：存在代码文件、构建与依赖配置（`git`, `package.json`, `Cargo.toml`, `go.mod`, `pom.xml`, `pyproject.toml`, `docker-compose.yml` 等）。
2. **知识/产出类（Non-Software: Research, Report, PPT, Analysis）**：
   - 判定特征：主要是 Markdown、Word、PPTX 脚本、PDF、CSV 数据集、无代码构建工程。
3. **DeepSeek Harness 运行时检测**：
   - 判定特征：存在 `dsh` CLI、`harness.config.*`、`cordis` 插件或声明了 `DEEPSEEK_API_KEY`。
   - 动作：遵循 [deepseek-harness-guide.md](references/deepseek-harness-guide.md) 注入 Harness 运行与评测命令。

---

### 阶段二：场景创建流程 (Scenario: Creation)

1. **主动采集真实事实（Fact Gathering）**：
   - **软件项目**：检查包管理器锁定文件（区分 pnpm/yarn/npm/bun）、执行脚本、测试框架（vitest/jest/pytest）、Linter 配置、Node/Python 版本。
   - **非代码项目**：检查已有大纲、目标受众说明、格式约定、参考资料目录（如 `references/`、`docs/`）。
2. **疑难澄清（Human-in-the-Loop Clarification）**：
   - 汇总不明确的事项，**一次性向用户提问（控制在 2-4 个关键问题，严禁无休止琐碎追问）**。
   - *软件项目询问示例*：“检测到同时存在 yarn.lock 和 pnpm-lock，确定以哪个为准？是否有强制的 Commit 规范或分支命名规则？”
   - *非代码项目询问示例*：“该调研报告的目标读者是谁？交付格式是纯 Markdown、Marp 幻灯片还是 Word 文档？是否有固定的对标竞品清单？”
3. **渲染骨架并落盘**：
   - 软件与 Harness 项目采用 [software-template.md](references/software-template.md)。
   - 非代码项目采用 [non-software-template.md](references/non-software-template.md)。
   - 注入采集到的高置信度事实，参照 [adhd-style-guide.md](references/adhd-style-guide.md) 进行压缩输出，保存至根目录 `AGENTS.md`。
   - 统一注入 `handoff2docs` 调度约束与 `docs/handoff/` 审计指针，并按需配置项目 hooks（详见 [handoff-workflow.md](references/handoff-workflow.md)）。

---

### 阶段三：事实校准与审计流程 (Scenario: Verification & Audit)

针对已存在的 `AGENTS.md`，执行“现实对抗审查（Reality Check）”：
1. **命令可执行性校验**：提取文件中所有的 CLI 命令（如 `pnpm test`, `python main.py`），利用环境探测工具验证这些命令或依赖是否真实存在。
2. **路径有效性校验**：提取所有提及的文件路径与子文档指针，验证物理文件是否存在。
3. **行数与无废话审查**：调用 [scripts/audit_agents_md.py](scripts/audit_agents_md.py) 进行合规性检查（行数 <= 150，零礼貌废话词）。
4. **冲突识别与交互确认**：
   - 发现文档记录与现状冲突（如文档写着 Node 18，但实际项目为 Node 22 或 `.nvmrc` 为 22）。
   - **动作**：列出具体差异清单，向用户确认：“文档与项目实际配置存在以下不一致，是否以当前环境为准并自动同步文档？”

---

### 阶段四：Handoff2Docs 会话归档与 Hooks 协同流 (Handoff2Docs & Hooks Workflow)

当用户触发 `handoff` / `handoff2docs` 或需要跨会话交接时，执行标准化归档流程：
1. **依赖环境探测与植入**：
   - 检查全局或本地是否已安装 `handoff2docs` skill（`~/.agents/skills/handoff2docs` 或 `~/.codex/skills/handoff2docs`）。
   - **若缺失**：提示并执行安装（运行工作台 `node scripts/install.js --skill handoff2docs`）。
   - **Hooks 植入**：在目标项目中配置交接触发机制（Git hooks 或 Agent settings hooks，详见 [handoff-workflow.md](references/handoff-workflow.md)）。
2. **双工文档落盘**（详见 [handoff-workflow.md](references/handoff-workflow.md)）：
   - 创建目录 `docs/handoff/`（若不存在）。
   - 生成交接文档：`docs/handoff/YYYY-MM-DD-HHmmss-handoff.md`（记录已完成工作、当前仓库状态、未决事项、推荐技能）。
   - 生成教训文档：`docs/handoff/YYYY-MM-DD-HHmmss-lesson.md`（记录遇到问题、根本原因剖析、验证方案、反模式禁令，防止将来再次犯错）。
3. **架构决策归档 (ADR Scaffolding)**：
   - 若会话涉及架构取舍或明确被否决的技术方案（explicit rejection），基于模板落盘/更新 ADR 至 `docs/decisions/`，强制列出被否决方案与否决原因。
4. **维护全局总账索引**：
   - 自动追加或更新 `docs/handoff/handoff-readme.md`，添加时间戳、主题、双文档跳转链接与检索标签。
5. **AGENTS.md 约束确认**：
   - 确保 `AGENTS.md` 包含查阅规则：
     `Review docs/handoff/handoff-readme.md before major refactors, complex bug fixes, or session start.`
     `FORBIDDEN: Repeating documented past mistakes -> USE: Consult docs/handoff/*-lesson.md or run handoff2docs.`

---

### 阶段五：会话运行时自演进与教训晋升 (Scenario: In-Session Evolution & Seen 3× Gate)

在日常与用户会话时，若满足以下触发条件之一：
- **Trigger 1（用户显式纠偏）**：用户指出 Agent 的行为偏好错误（如“不要在报告里使用三级标题，直接给结论”或“以后用 bun，别用 npm”）。
- **Trigger 2（环境与工具链反馈）**：工具调用遭遇可修复的环境失败，摸索出正确解法（如原执行命令报错，换用另一命令成功）。
- **Trigger 3（配置或技术栈新增）**：项目新增了重大技术选型或架构约束（如引入了 Tailwind v4 或 Prisma 迁移）。

**执行自演进闭环**：
1. **教训频次门禁（Seen 3× Promotion Gate）**：
   - 偶发单次经验仅留存于 `docs/handoff/*-lesson.md`。
   - `FORBIDDEN: Directly promoting single-occurrence lessons to AGENTS.md -> USE: Retain lessons in docs/handoff/ until verified across 3 independent session dates (Seen 3× Gate).` 仅在 3 个独立会话日期复现时，方可晋升至 `docs/rules/` 或 `AGENTS.md`。
2. **计算自然语言梯度（Delta Extraction）**：参考 [evolution-prompts.md](references/evolution-prompts.md)，提炼通用原子规则。
3. **ADHD 语法转化**：转换为 `KEYWORD: Action (FORBIDDEN: Old -> USE: New)` 形式。
4. **融合修改 (Integrated Editing)**：
   - `FORBIDDEN: Appending rule modifications blindly to the bottom -> USE: Integrate modifications into existing logical sections and balance with existing constraints.`
5. **单行汇报确认**：在回复末尾附带单行简短提示：
   > `[AGENTS.md Updated] 规则已同步演进：PKG_MGR: bun only (FORBIDDEN: npm/yarn/pnpm)`

---

### 阶段六：生命周期治理与修剪机制 (Garbage Collection)

为避免文档随着多轮会话无限膨胀（Token Bloat / Context Degradation）：
1. **150 行物理红线**：根目录 `AGENTS.md` 必须维持在 150 行以内。
2. **离散分流（Progressive Offloading）**：当行数超出时，将垂直领域细则（如具体数据库索引策略、具体微前端通信细节）迁移至 `docs/rules/<domain>.md`，根文件仅保留指向该子文件的指针。
3. **同类项合并（Consolidation）**：定期合并重复指令，淘汰已被后续更严格规则覆盖的废弃规则。

---

## 引用规范与工具链清单

- [ADHD / Spartan 表达规范指南](references/adhd-style-guide.md)
- [轻量 ADR 决策模板](references/template-adr.md)
- [软件开发系统骨架模板](references/software-template.md)
- [非代码项目（调研/报告/PPT）骨架模板](references/non-software-template.md)
- [Handoff 双工交接与教训工作流](references/handoff-workflow.md)
- [DeepSeek Harness 兼容与优化指南](references/deepseek-harness-guide.md)
- [Meta-Agent 演化提示词规范](references/evolution-prompts.md)
- [AGENTS.md 质量与真实性检测脚本](scripts/audit_agents_md.py)
