---
name: modern-userscript
description: Build, refactor, audit, and distribute modern Userscripts (油猴脚本) with Vite, vite-plugin-monkey, Shadow DOM micro-frontend isolation, reactive cross-tab store, network interception (Proxy), GreasyFork/SleazyFork compliance, and CI/CD gatekeeping. Use when developing, optimizing, or fixing userscripts, migrating from Webpack to Vite, handling GreasyFork compliance reviews, or architecting injected UIs.
metadata:
  short-description: Modern userscript engineering, architecture & compliance
---

# Modern Userscript Development & Compliance (现代油猴脚本架构与合规全景指南)

This skill provides an industrial-grade engineering standard for **Userscripts (Tampermonkey, Violentmonkey, ScriptCat)**. It transforms userscript development from the "stone-age" (single-file scripts, brittle DOM scraping, global CSS pollution) into an **injected micro-frontend architecture** that is fast, robust, and compliant with community distribution platforms (GreasyFork & SleazyFork).

---

## 1. 核心架构哲学 (Core Architecture)

Modern userscripts should be treated as **injected micro-frontends**, not simple DOM-manipulating snippets.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      用户脚本微前端全景架构                              │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. 构建底座：Vite + vite-plugin-monkey (ES2020+ IIFE, 毫秒级构建, HMR)    │
│ 2. 界面隔离：Custom Element + Shadow DOM + adoptedStyleSheets (双向无污染)│
│ 3. 数据通信：ES6 Proxy 拦截器 (window/unsafeWindow fetch & XHR 媒体嗅探) │
│ 4. 状态联动：GM_addValueChangeListener + ReactiveStore (无后端多标签热同步)│
│ 5. 高阶存储：IndexedDB 原生 Promise 封装 (突破单 key 5MB 上限)          │
│ 6. 安全门禁：AST 静态合规审查 + 2.0MB 预算硬防 + GitHub Actions 隔离发版   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 必须严守的平台合规红线 (GreasyFork / SleazyFork Red Lines)

每次开发、发版与审查时，必须无条件遵循以下铁律，违者将面临脚本下架或账号永久封禁：

### 🚨 绝对禁止项
1. **严禁未经披露的负面功能 (Zero Undisclosed Tracking / Antifeatures)**
   - 任何涉及设备指纹分析、网址收集、播放时长打点、点击流上报的行为，属于平台最高级别红线。
   - **优先策略**：坚决推行 **100% 纯本地运行**，彻底剔除外部遥测与追踪服务器；
   - 若确有必要，必须在 Header 强制声明 `// @antifeature tracking <说明>` 并在 UI 中提供默认关闭（Opt-in）的显式开关。
2. **严禁代码混淆与压缩 (No Obfuscation / No Mangling)**
   - 必须保持源码完全透明、可读且便于管理员和社区审计。
   - 构建配置必须永久配置 **`minify: false`** 与 **`mangle: false`**。
   - 严禁采用 `eval(function(p,a,c,k...))`、JSFuck 等任何加密变体。
3. **单文件体积硬红线**
   - 平台硬性限制单脚本体积不得超过 **2.0 MB**。
   - 推荐构建门禁设置：**> 1.0 MB 告警，> 1.8 MB 强制阻断**。
   - 优先通过原生 Web API 消除第三方库，或使用公共 CDN `@require` 外部化。

### ⚠️ 经典踩坑与血泪教训
1. **严格模式分号陷阱 (The "use strict" ASI Hazard)**
   - 现象：`vite-plugin-monkey` 或 Rollup 模板注入 `"use strict"` 时若末尾缺少分号，紧接着内层 IIFE `(function() {` 会被 JS 引擎解析为函数调用：`"use strict"(function() ...)`，导致运行时抛出致命错误 `TypeError: "use strict" is not a function`，脚本直接原地崩溃。
   - 对策：在 Vite 配置中增加 post-bundle 插件，确保严格模式声明后必带分号。
2. **泛域名与根域名匹配陷阱 (The Apex Domain @match Hazard)**
   - 现象：声明 `@match *://*.example.com/*` 时，**仅匹配子域名**（如 `www.example.com`），而**绝不匹配根域名** `https://example.com/`！导致用户在主站访问时油猴根本不注入脚本。
   - 对策：元数据中必须同时声明根域名与泛子域名：
     ```javascript
     // @match *://example.com/*
     // @match *://*.example.com/*
     ```
3. **ES5 转译垫片假阳性报警**
   - 现代油猴宿主均在最新浏览器中运行。使用 Babel 降级到 ES5 会注入带有单字母变量（`a, e, r, t`）的大量 polyfill（如 `_classCallCheck`、`_typeof`），会被审计机器人误判为“混淆代码”。必须将编译目标锁定为 **`es2020`** 或更高。
4. **危机公关核心纪律 (Incident Response SOP)**
   - 收到违规举报或挑刺问询时，**绝对不要在无代码事实前去争辩动机**；
   - 遵循标准四步走：**本地彻底清除涉事代码 -> 打包推送到 GitHub 同步线上 -> 携带 Commit 实证前往申诉区客观陈述 -> 申请管理员结案**。

---

## 3. 现代化工程基座：Vite + `vite-plugin-monkey`

彻底废弃臃肿慢速的 Webpack 5 + Babel 单体构建，全面采用 Vite 快速响应脚手架。

### 为什么选择 Vite？
- **构建耗时从 10 秒+ 降至 0.7 秒**，热重载提速 15 倍以上；
- **原生 HMR 极速热更新**：启动 `vite` 后生成本地代理脚本（`http://localhost:5173/__monkey.user.js`），在油猴安装一次，后续保存代码页面自动热更新，无需反复重装；
- **AST 级 `@grant` 智能推导**：自动分析源码中调用的 GM API，杜绝权限漏配或过度越权。

配置模板详见 [assets/template-vite.config.mjs](./assets/template-vite.config.mjs)。

---

## 4. UI 强隔离：Shadow DOM 微前端化实践

向宿主页面注入复杂 UI 时，直接操作 Light DOM 样式是万恶之源（导致样式穿透、`!important` 权重大战与布局塌陷）。

### 最佳实践模式：
1. **宿主容器**：向页面注册自定义元素 `<custom-script-root>`，赋予 `display: contents !important;`，实现零盒模型占用；
2. **Shadow Root**：调用 `attachShadow({ mode: 'open' })`，内部装配全部组件与弹窗；
3. **样式注入**：通过 `import styles from './style.css?inline'` 获取样式文本，调用原生 `shadowRoot.adoptedStyleSheets = [sheet]` 瞬时注入，隔绝宿主全局 CSS；
4. **Light DOM 边界处理**：仅在播放器唤醒前必需的启动入口（如浮动按钮）挂载在 Light DOM，并使用 `GM_addStyle` 赋予固定定位（`position: fixed`）。

架构细节详见 [references/shadow-dom-architecture.md](./references/shadow-dom-architecture.md)。

---

## 5. 底层数据与网络：Proxy 嗅探 + 跨标签响应式状态机

### 1. 网络层底层嗅探 (Media & API Sniffer)
- 放弃脆弱易破损的 DOM 节点与页面源码正则爬取；
- 在 `@run-at document-start` 阶段，利用 ES6 `Proxy` 对 `window.fetch`、`unsafeWindow.fetch` 以及 `XMLHttpRequest.prototype.open` 实施统一代理；
- 零延迟捕获媒体播放地址（`.m3u8`、`.mp4`）、高清分片与结构化后端 API JSON。

### 2. 跨标签响应式 Store (ReactiveStore)
- 依托油猴原生 `GM_addValueChangeListener` 接口；
- 使用 Proxy 包装状态对象，属性修改自动调用 `GM_setValue`；
- 远端标签页检测到 `remote === true` 时自动触发本地视图响应，实现多窗口配置与播放进度实时接力。

### 3. 本地高阶离线存储 (IndexedDB)
- 原生 Promise 封装 `IndexedDB`，划分专项 Object Store（如切片打点、离线评论缓存）；
- 彻底解除单 key 存储容量上限，保障离线大数据量检索的高吞吐量。

代码模板详见 [references/network-and-storage.md](./references/network-and-storage.md)。

---

## 6. 自动化 CI/CD 与合规门禁流水线

将合规防御与发版安全性固化为代码脚本：

1. **静态合规审查门禁 (`scripts/compliance-lint.js`)**：
   - 自动审计体积预算（< 1.8 MB）；
   - 递归扫描黑名单违规追踪域名；
   - 校验 `@namespace` 与版本一致性；
   - AST 语法树健康审计与变量反混淆分布检查。
2. **端到端仿真测试 (`scripts/ci-test.js`)**：
   - 校验版本号跨文件强一致性；
   - 自动化调用 Vite 打包；
   - 在无头 Node.js VM 沙箱中模拟浏览器运行产物，杜绝语法与未定义全局变量错误。
3. **GitHub Actions 隔离发版 (`.github/workflows/ci-release.yml`)**：
   - 日常代码推送仅触发门禁核验，**绝不直接上线**；
   - 仅在推送正式标签（如 `git tag v1.0.0 && git push --tags`）且所有测试全绿灯时，才触发 GitHub Release 资产生成并通知分发。

CI 模板详见 [assets/template-compliance-lint.js](./assets/template-compliance-lint.js) 与 [assets/template-ci-release.yml](./assets/template-ci-release.yml)。

---

## 7. 存量老项目现代化改造标准工作流 (Refactoring Mode SOP)

当用户要求**“改造现有老项目”**、**“现代化升级”**或**“排查老脚本架构隐患”**时，Agent **无需创建新技能**，直接激活本重构工作流，按以下三步标准化推进：

### 第一步：五维现状诊断 (Gap Analysis)
首先扫描现有项目的工程配置、依赖与源码，对照下表输出**《改造点诊断清单》**：

| 审查维度 | 传统常见反模式 (Legacy Traps) | 现代化演进目标 (Modern Standard) |
| :--- | :--- | :--- |
| **1. 构建底座** | Webpack 4/5、Gulp、Rollup 或无构建单文件 | 迁移到 **Vite + vite-plugin-monkey** (0.7s 构建 + 本地 HMR) |
| **2. 依赖与体积**| 内联打包大型三方库，代码体积 > 1.0 MB | **原生 Web API 代替或 CDN @require**，实现零运行时依赖 |
| **3. 界面隔离** | 裸 DOM 挂在 document.body，全局 CSS 权重大战 | **Custom Element + Shadow DOM + adoptedStyleSheets** 强隔离 |
| **4. 数据流向** | 页面加载后靠 DOM 选择器/正则爬取 | **ES6 Proxy 拦截器** 嗅探原生 fetch/XHR 媒体流与 API JSON |
| **5. 安全与发版**| 本地 build 后 push 即触发全网发布，无门禁 | **AST 静态合规门禁 + GitHub Actions Tag 隔离发版** |

### 第二步：输出定制化重构计划 (落地 TODO.md)
在目标项目根目录下生成标准化任务看板 TODO.md，将改造拆解为 5 个原子化阶段（Phase 1 至 Phase 5），每阶段设立明确的验收指标。

### 第三步：双轨并行实施纪律 (Zero Regression)
1. **绝不破坏主键**：严格保留原有 @namespace 与主脚本名，保护已安装用户的自动更新通道；
2. **双轨构建脚本**：在 package.json 中保留旧打包命令（如 npm run build:legacy），新建 vite.config.mjs，确保随时可无损回滚；
3. **真实浏览器实机核验**：每完成一个阶段，使用 huashu-chrome 在真实页面执行快照与截图比对，验证功能与样式 100% 无降级。
