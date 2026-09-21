# modern-userscript (现代油猴微前端架构与合规治理)

> **工业级 Userscript 开发、重构、样式强隔离与 GreasyFork/SleazyFork 合规门禁标准技能**

---

## 📖 技能简介

`modern-userscript` 是专为 AI Coding Agent（如 Codex、Claude Code、OpenCode、Antigravity、Cursor）打造的油猴脚本开发全景规范。它将脚本从“单文件直接操作 DOM”的石器时代，提升至以 **Vite 构建底座 + Shadow DOM 样式隔离 + ES6 Proxy 网络流嗅探 + 跨标签响应式状态机 + 自动化合规门禁** 为核心的微前端架构。

---

## 🎯 核心解决的问题

1. **解决被 GreasyFork / SleazyFork 举报封禁风险**：
   - 杜绝未经披露的遥测追踪（提供 100% 本地化策略与 `@antifeature` 规则）；
   - 彻底关闭代码混淆（`mangle: false`）；
   - 解决 Babel ES5 降级辅助函数被平台误判为混淆的假阳性问题；
   - 严格守卫 2.0 MB 单文件体积红线。
2. **解决样式双向污染与权重大战**：
   - 引入 Web Component 与 Shadow DOM，使用 `adoptedStyleSheets` 强隔离注入样式；
   - 原网页 CSS 重置与脚本样式互不侵犯。
3. **解决数据获取时序滞后与反爬失效**：
   - 在 `document-start` 阶段利用 ES6 Proxy 代理原生 `fetch` 与 `XHR`；
   - 底层直取 `.m3u8`、`.mp4` 高清视频流与结构化后端 API JSON。
4. **解决开发调试效率低下**：
   - 使用 `vite-plugin-monkey` 替代 Webpack，构建耗时由 10s+ 降至 0.7s；
   - 启动本地代理脚本，享受真正的毫秒级 HMR 热更新。

---

## 🛠️ 目录与资产清单

- `SKILL.md`：Agent 执行核心准则、合规红线与老项目重构三步法 SOP
- `references/`：
  - `greasyfork-rules.md`：全量审核规则与危机公关 SOP
  - `shadow-dom-architecture.md`：Web Component + Shadow DOM 封装实战
  - `network-and-storage.md`：Proxy 网络嗅探 + 响应式 Store + IndexedDB
- `assets/`（可直接拷贝使用的工业级工程模板）：
  - `template-vite.config.mjs`：Vite + Monkey 生产打包配置
  - `template-compliance-lint.js`：AST 语法树 + 体积预算 + 敏感域名本地合规 Linter
  - `template-ci-test.js`：版本一致性校验 + 无头 VM 沙箱防报错测试
  - `template-ci-release.yml`：GitHub Actions 标签化安全发版工作流
  - `template-media-sniffer.js`：底层流媒体嗅探器
  - `template-reactive-store.js`：跨标签页响应式状态机
  - `template-indexeddb.js`：大容量离线对象存储

---

## 💡 使用方法

在任意项目中对 Agent 输入：
```text
使用 $modern-userscript 技能，为本项目搭建基于 Vite 的油猴脚本微前端工程。
```
或
```text
使用 $modern-userscript 对当前老项目进行架构体检，输出五维改造点清单并落地 TODO.md。
```
