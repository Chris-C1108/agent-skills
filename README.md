# Agent Skills (工业级 AI Agent 技能库)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#)
[![Agent: Codex | Claude Code | OpenCode](https://img.shields.io/badge/Agent-Codex%20%7C%20Claude%20Code%20%7C%20OpenCode-blueviolet)](#)

一套面向现代 AI Coding Agent（**Codex、Claude Code、OpenCode、Antigravity、Cursor、Cline、Roo Code** 等）的**生产级、可复用领域技能库（Skills Collection）**。

将真实一线项目踩坑复盘、危机公关经验与前沿架构规范固化为标准化知识契约，让 AI Agent 在跨项目协作中直接具备专家级工程执行力。

---

## 📚 技能索引清单 (Skills Catalog)

| 技能名称 | 适用领域与核心能力 | 链接与文档 |
| :--- | :--- | :--- |
| **`modern-userscript`** | **现代油猴脚本微前端架构与平台合规**<br>涵盖 Vite + vite-plugin-monkey 快速构建、Shadow DOM 样式强隔离、Proxy 底层媒体流嗅探、跨标签页响应式状态机、AST 合规审查门禁与 GitHub Actions 标签化安全发版。 | [👉 技能主页](./skills/modern-userscript/README.md)<br>[📄 核心规约 (SKILL.md)](./skills/modern-userscript/SKILL.md) |

---

## ⚡ 快速安装与配置指南

### 方式 1：一键安装至全局技能池（最推荐，所有项目免配生效）
克隆本仓库到本地并执行内置安装脚本：
```bash
git clone https://github.com/Chris-C1108/agent-skills.git
cd agent-skills
node scripts/install.js
```
> 该脚本会自动将 `skills/` 目录下的所有技能拷贝至当前用户的全局技能目录 `~/.agents/skills/`。**Codex、Claude Code、OpenCode** 等工具在任何项目启动时将自动识别并加载。

### 方式 2：项目私有集成（团队协同与开源仓库随附）
若希望将某个技能直接固化在特定代码仓库中：
```bash
# 在你的目标项目根目录中
mkdir -p .agents/skills
cp -r /path/to/agent-skills/skills/modern-userscript .agents/skills/
```
并在目标项目的 `AGENTS.md` 中加入：
```markdown
本项目遵循 [.agents/skills/modern-userscript/SKILL.md](./.agents/skills/modern-userscript/SKILL.md) 开发与合规标准。
```

---

## 💡 各场景使用提示词与实战参考 (Scenario Playbooks)

安装完成后，在日常开发对话中，你可以直接通过自然语言或 `$` 引用触发对应的技能专家。以下是入选技能的典型实操指令：

### 场景 A：从零新建现代油猴项目
> **用户提示词**：  
> *“请使用 `$modern-userscript` 技能，为我新建一个基于 Vite + `vite-plugin-monkey` 的油猴脚本工程，配置好本地 HMR 开发环境与基础架构。”*
* **Agent 执行动作**：
  1. 调取 `assets/template-vite.config.mjs` 搭建脚手架；
  2. 配置原生 ES2020+ 输出，开启 `minify: false` 与 `mangle: false`；
  3. 配置本地代理脚本 `dist/[name].proxy.user.js`，支持保存代码后浏览器自动热更新。

---

### 场景 B：存量老脚本五维体检与现代化改造
> **用户提示词**：  
> *“请使用 `$modern-userscript` 的重构工作流（Refactoring Mode），对当前老旧油猴脚本进行架构诊断，列出改造点清单并在根目录落地 `TODO.md`。”*
* **Agent 执行动作**：
  1. 执行五维现状扫描（构建耗时、三方库体积、DOM 注入方式、数据爬取时序、发版安全）；
  2. 输出《改造点诊断清单》；
  3. 在项目根目录生成 Phase 1 至 Phase 5 的分步演进任务看板；
  4. 遵从双轨并行实施纪律（保留老打包命令，绝不破坏原有 `@namespace`）。

---

### 场景 C：规避 GreasyFork / SleazyFork 封禁与危机公关
> **用户提示词**：  
> *“我的油猴脚本在 GreasyFork 被举报‘包含未声明的追踪与混淆代码’，请根据 `$modern-userscript` 的危机处置 SOP 协助我完成整改与申诉。”*
* **Agent 执行动作**：
  1. 彻底清除涉事模块与指纹采集算法，从 `@connect` 移除敏感端点；
  2. 修复 Babel 降级垫片（升至 ES2020 消除单字母变量），修补严格模式分号隐患；
  3. 打包发布新版本并推送至 GitHub；
  4. 生成符合社区规范的中英双语客观申诉文案，协助管理员顺利结案。

---

### 场景 D：界面微前端化与样式强隔离 (Shadow DOM)
> **用户提示词**：  
> *“本项目注入的播放器/悬浮面板经常与宿主网页的全局 CSS 发生冲突，请参考 `$modern-userscript` 将其重构成 Web Component 与 Shadow DOM 强隔离架构。”*
* **Agent 执行动作**：
  1. 注册原生自定义元素 `<custom-script-root>`，赋予 `display: contents !important;`；
  2. 通过 `adoptedStyleSheets` + `?inline` CSS 注入样式，构筑双向物理防火墙；
  3. 将常驻唤起按钮留在 Light DOM，并通过 `GM_addStyle` 赋予固定定位，消除样式坍塌。

---

### 场景 E：网络数据层底层嗅探 (Proxy Hook)
> **用户提示词**：  
> *“当前脚本靠 DOM 页面渲染后抓取数据经常因网页改版而失效，请参考 `$modern-userscript` 引入网络层底层嗅探。”*
* **Agent 执行动作**：
  1. 在 `@run-at document-start` 阶段利用 ES6 `Proxy` 代理全局 `window.fetch` 与 `XMLHttpRequest`；
  2. 无感截获后端 API 响应与高清视频流清单（`.m3u8`、`.mp4`）；
  3. 引入 `reactiveStore.js`（通过 `GM_addValueChangeListener` 实现多标签页实时联动）与 `indexedDB.js` 突破存储容量限制。

---

### 场景 F：接入工业级 CI/CD 与发版安全防御门禁
> **用户提示词**：  
> *“每次推送到 GitHub 都直接被 Webhook 抓到线上发布太危险了，请参考 `$modern-userscript` 为本项目配置本地静态审查门禁与 GitHub Actions 标签发版流。”*
* **Agent 执行动作**：
  1. 落地 `scripts/compliance-lint.js`（扫描体积预算 < 1.8MB、违规域名黑名单、AST 语法树反混淆检查）；
  2. 落地 `scripts/ci-test.js`（版本强同步校验、无头 VM 沙箱仿真启动测试）；
  3. 配置 `.github/workflows/ci-release.yml`：将日常推送与正式发版严格解耦，仅在打上 `git tag v*` 且门禁全绿灯时才发布。

---

## 🤝 贡献指南 (Contributing)

欢迎提交新的生产级 Agent Skills！提交时请遵循以下质量准则：
1. **真实战火检验**：技能必须来自真实生产环境或实战项目的沉淀，拒绝纸上谈兵与泛泛而谈的理论；
2. **结构完整严谨**：每个技能需包含主文档 `SKILL.md`、细分文档 `references/` 以及开箱即用的工程模板 `assets/`；
3. **自包含与低开销**：遵循技能的渐进式信息披露（Progressive Disclosure）原则，避免在主文档堆砌无关细节。

---

## 📄 开源许可证

本项目基于 [MIT License](./LICENSE) 开源。
