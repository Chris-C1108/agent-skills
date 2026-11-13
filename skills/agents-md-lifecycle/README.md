# `agents-md-lifecycle` (AGENTS.md 生命周期与自演进管理器)

> **基于学术界“脚手架自进化 (Scaffolding Self-Improvement)”理论与工业界 ADHD/Spartan 零废话规范构建的生产级 AI 规范自治技能。**

---

## 🌟 核心价值

在现代 AI Coding Agent（如 Codex、Claude Code、Windsurf、Cursor、Cline）协作中，`AGENTS.md` 扮演着核心系统提示词与规则契约的角色。然而传统维护模式存在三大痛点：
1. **真实性缺失**：依赖 AI 凭空假定项目规范，产生大量与实际环境冲突的“幻觉规则”；
2. **废话稀释注意力**：大量礼貌用语（Please、Remember to）与模糊表述严重占用上下文预算并导致核心约束被忽略（Attention Drift）；
3. **静态失真**：项目演化与用户日常纠偏无法自动沉淀回文档，Agent 屡屡犯下相同的错误。

`agents-md-lifecycle` 提供了一整套从**真实性嗅探**、**双原型区分（软件开发 vs 调研报告/PPT）**、**ADHD 极致高信噪比压缩**到**会话运行时自演进闭环**的完整工程方案。

---

## 📁 目录架构

```text
skills/agents-md-lifecycle/
├── SKILL.md                             # 核心调度规范与触发器定义
├── README.md                            # 技能使用说明与实战指南
├── references/
│   ├── adhd-style-guide.md              # ADHD/Spartan 零废话表达与成对约束指南
│   ├── software-template.md             # 软件工程专用骨架模板
│   ├── non-software-template.md         # 调研报告/PPT/分析类非代码项目专用骨架模板
│   └── evolution-prompts.md             # Meta-Agent 文本梯度反思与演化契约
└── scripts/
    └── audit_agents_md.py               # 真实性、行数预算与高信噪比静态审计脚本
```

---

## 🚀 核心工作流与命令

### 1. 从零初始化 AGENTS.md
当项目根目录不存在 `AGENTS.md` 时，Agent 将自动嗅探项目特征：
- **软件项目**：检查 `package.json` / `go.mod` / `pyproject.toml`，提取准确包管理器、测试与构建脚本。
- **非代码项目**：分析大纲、格式要求，并仅针对低置信度（< 90%）要素向用户发起 2-4 个关键提问，严禁无端猜测。

### 2. 存量文档真实性校准与审计
执行内置审计脚本：
```bash
python scripts/audit_agents_md.py --file AGENTS.md --max-lines 150
```
- 校验行数预算（严格 <= 150 行）；
- 扫描并拦截所有低熵客套废话（"Please", "Kindly", "You should" 等）；
- 校验渐进式披露链接（`-> path/to/file.md`）物理存在性。

### 3. 会话运行时自演进 (Fast Loop -> Slow Loop)
- **触发条件**：用户纠偏、工具报错回退或重大规范变更。
- **演化动作**：提取自然语言梯度，转化为 `FORBIDDEN: Old -> USE: New` 格式，安全 Patch 写入 `AGENTS.md`，并单行通知用户。

---

## 📄 许可证

基于 MIT License 开源。
