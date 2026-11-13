# Personal Agent Skills Studio (个人 AI Agent 技能研发与治理工作台)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Agent: Codex | Claude Code | OpenCode](https://img.shields.io/badge/Agent-Codex%20%7C%20Claude%20Code%20%7C%20OpenCode%20%7C%20Windsurf-blueviolet)](#)
[![Skills Count: 2](https://img.shields.io/badge/Skills-2%20Active-brightgreen)](#)

本工作台是面向现代 AI Agent（**Codex、Claude Code、OpenCode、Windsurf、Cursor** 等）的**个人专属技能研发、测试、静态审查与多端同步中心**。

将前沿架构规约、真实一线踩坑复盘与自我演进能力固化为工业级技能契约，让 Agent 在不同项目协作中始终具备专家级工程执行力。

---

## 📚 技能索引清单 (Skills Catalog)

| 技能名称 | 适用领域与核心能力 | 链接与文档 |
| :--- | :--- | :--- |
| **`agents-md-lifecycle`** <br>*(新增 · 自我提升)* | **AGENTS.md 全生命周期治理与会话自演进**<br>基于学术界“脚手架自进化”理论与 ADHD 零废话模式。自动区分软件开发与知识调研/PPT 双原型，无端猜测严禁发生（高置信度发问）；会话中自动计算自然语言梯度并 Patch 规则；内置行数预算与静态审计器。 | [👉 技能主页](./skills/agents-md-lifecycle/README.md)<br>[📄 核心规约 (SKILL.md)](./skills/agents-md-lifecycle/SKILL.md) |
| **`modern-userscript`** | **现代油猴脚本微前端架构与平台合规**<br>涵盖 Vite + vite-plugin-monkey 快速构建、Shadow DOM 样式强隔离、Proxy 底层媒体流嗅探、跨标签页响应式状态机、AST 合规审查门禁与 GitHub Actions 标签化安全发版。 | [👉 技能主页](./skills/modern-userscript/README.md)<br>[📄 核心规约 (SKILL.md)](./skills/modern-userscript/SKILL.md) |

---

## 🛠️ 工作台目录架构 (Workspace Layout)

```text
agent-skills/
├── AGENTS.md                            # 本工作台自解释规则契约 (ADHD Spartan 模式)
├── package.json                         # 工作台命令调度契约
├── skills/                              # 技能源码库 (核心资产)
│   ├── agents-md-lifecycle/             # AGENTS.md 生命周期与自我演进技能
│   │   ├── SKILL.md                     # 技能调度入口与触发器
│   │   ├── references/                  # ADHD 规范、软件/非代码模板、演化 Prompt
│   │   └── scripts/                     # audit_agents_md.py 静态审计脚本
│   └── modern-userscript/               # 现代油猴开发与合规治理技能
├── docs/
│   └── rules/
│       └── skill-authoring.md           # 技能研发与渐进式披露规范
├── scripts/
│   ├── new-skill.js                     # 新建技能脚手架生成器
│   ├── lint-skills.js                   # 技能库质量与合规性静态审查器
│   └── install.js                       # 一键同步/安装至本地多 Agent 环境
└── README.md                            # 工作台全貌与操作指南
```

---

## ⚡ 极速操作工作流 (Developer Commands)

### 1. 新建一个技能 (Scaffold a New Skill)
```bash
npm run new-skill <skill-name> -- --desc "技能定位简述"
# 示例：npm run new-skill cloudflare-worker-arch -- --desc "Cloudflare Workers 架构与性能调优技能"
```
> 该脚本会自动在 `skills/<skill-name>/` 生成符合 Anthropic 标准的标准骨架，包含 `SKILL.md`、`references/`、`scripts/`、`assets/` 与 `README.md`。

### 2. 静态审查与合规体检 (Linting)
```bash
npm run lint
```
> 审查所有技能的 YAML frontmatter 完整性、行数预算（`SKILL.md` <= 200 行）、ADHD 零废话检查（拦截 "Please", "Kindly", "You should" 等）、以及引用路径的物理有效性。

### 3. 本地多 Agent 环境一键热同步 (Multi-Target Sync)
```bash
# 同步全部技能至全局目录（~/.agents/skills 和 ~/.codex/skills）
npm run install:all

# 仅同步至 Claude Code / OpenCode / Windsurf
npm run install:agents

# 仅同步至 Codex App / CLI
npm run install:codex

# 仅同步指定技能
node scripts/install.js --skill agents-md-lifecycle
```

### 4. 静态审计 AGENTS.md 规范 (Audit AGENTS.md)
```bash
npm run audit:agents-md
```

---

## 🤝 技能研发核心准则 (Authoring Axioms)

1. **真实战火检验 (Ground Truth First)**：拒绝纸上谈兵，所有指令与脚本必须在真实命令行或容器中可执行；
2. **ADHD / Spartan 零废话 (Zero Fluff)**：全篇采用动宾结构、成对约束（`FORBIDDEN: X -> USE: Y`），严禁前置寒暄；
3. **渐进式信息披露 (Progressive Disclosure)**：`SKILL.md` 保持在 200 行以内作为调度总线，深度细节拆分至 `references/*.md`。

---

## 📄 开源许可证

本项目基于 [MIT License](./LICENSE) 开源。
