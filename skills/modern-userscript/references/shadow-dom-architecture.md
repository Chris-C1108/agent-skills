# Shadow DOM 微前端架构与 adoptedStyleSheets 实战指南

## 1. 为什么用户脚本必须使用 Shadow DOM？
在过去，油猴脚本通常直接向宿主网页的 document.body 插入裸 DOM 元素，并通过 style 标签注入样式。这在面对现代前端网站时会引发严重的“样式双向污染”：
1. **宿主污染脚本**：宿主网页的 CSS Reset（如 * { box-sizing: content-box !important; margin: 0; }）或超高权重选择器会轻易击穿脚本组件，导致按钮扭曲、文字偏移；
2. **脚本污染宿主**：脚本的全局基础变量、通用类名（如 .btn, .modal）会意外篡改原网页的排版；
3. **权重大战**：脚本被迫大量使用 !important 和极高 z-index，代码越来越难以维护。

## 2. 原生 Web Component + Shadow DOM 封装模式

### Step 1: 声明透明无盒模型的自定义宿主元素
```javascript
if (typeof customElements !== 'undefined' && !customElements.get('my-script-root')) {
    customElements.define('my-script-root', class MyScriptRoot extends HTMLElement {
        constructor() {
            super();
            this.attachShadow({ mode: 'open' });
        }
    });
}
```
在 CSS 中为宿主赋予 `:host { display: contents !important; }`，使其在文档树中保持纯净透明，零物理盒模型占用，彻底杜绝任何父级排版或文档流挤压。

### Step 2: 现代 adoptedStyleSheets 样式强隔离注入
利用 Vite 原生支持的 `?inline` 语法获取编译后的纯 CSS 字符串：
```javascript
import componentStyles from './style.css?inline';

export function injectShadowStyles(shadowRoot) {
    if (!shadowRoot) return;
    try {
        if (shadowRoot.adoptedStyleSheets && typeof CSSStyleSheet !== 'undefined') {
            const sheet = new CSSStyleSheet();
            sheet.replaceSync(componentStyles);
            shadowRoot.adoptedStyleSheets = [sheet];
            return;
        }
    } catch (_) {}

    // 平滑降级
    const styleEl = document.createElement('style');
    styleEl.textContent = componentStyles;
    shadowRoot.appendChild(styleEl);
}
```

### Step 3: CSS 变量在 Shadow DOM 内部的流转
在样式表中，将变量定义同时挂载到 `:root` 与 `:host`：
```css
:root, :host {
    --brand-color: #fe628e;
    --bg-card: rgba(13, 13, 13, 0.95);
    --text-primary: #ffffff;
}
```

### Step 4: Light DOM 边界划分原则
并不是所有元素都能放进 Shadow DOM，必须严格划分边界：
- **留在 Light DOM 的元素**：
  - 脚本唤起前的常驻入口（如浮动按钮 .tm-floating-button，挂在 document.body 上）；
  - 全局 Toast / Alert 弹窗（若需要在全屏时跨层级展示）；
  - 劫持的媒体源 <video> 元素（当借出给 Shadow DOM 视窗全屏播放，关闭时必须原位归还给 Light DOM 占位符）。
- **全部封装进 Shadow DOM 的元素**：
  - 核心控制面板、进度条、工具栏、侧边栏、设置面板、自定义输入框。
