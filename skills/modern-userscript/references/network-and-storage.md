# 网络层嗅探 (Proxy Hook) 与跨标签响应式状态机实战

## 1. 为什么需要网络层底层嗅探？
传统油猴脚本通常采用“页面渲染后从 DOM 或 HTML 源码正则爬取视频播放地址”的模式，存在三个致命缺陷：
1. **反爬与混淆**：现代视频站大量使用动态类名、虚拟列表与混淆加密，DOM 节点随时会变动；
2. **时序滞后**：必须等待原网页播放器初始化完成并挂载 DOM 后才能提取，启动极慢；
3. **分片与加密丢失**：无法直接截获高清 master.m3u8 与动态 auth 鉴权 token。

### 原生 Fetch / XHR Proxy 嗅探实现
在 `@run-at document-start` 阶段安全代理全局与沙箱环境：
```javascript
const originalFetch = window.fetch;
window.fetch = new Proxy(originalFetch, {
    apply(target, thisArg, args) {
        try {
            const req = args[0];
            const url = typeof req === 'string' ? req : (req && req.url ? req.url : '');
            if (url.includes('.m3u8') || url.includes('.mp4')) {
                mediaSniffer.recordStream(url, 'fetch');
            }
        } catch (_) {}
        return Reflect.apply(target, thisArg, args);
    }
});
```

## 2. 跨标签响应式状态机 (ReactiveStore)
利用油猴原生的 `GM_addValueChangeListener` 接口，在前端实现多窗口零后端实时同步：
- 当用户在标签页 A 修改设置（例如开启音效、修改快捷键、设置播放倍速）；
- `proxy.setting = value` 自动调用 `GM_setValue`；
- 标签页 B 的 `GM_addValueChangeListener` 收到通知（`remote === true`），状态机自动响应并更新 UI，彻底解决多标签状态打架与数据脱节。

## 3. IndexedDB 高阶本地离线持久化
当脚本需要保存大量数据（如海量历史播放记录、高频 A-B 点打点标记、全站点离线评论缓存）时：
- `localStorage`（5MB 上限）与 `GM_setValue`（针对超长字符串易卡顿）无法胜任；
- 必须基于原生 `window.indexedDB` 构建结构化 ObjectStore，异步高吞吐读写，容量无忧。
