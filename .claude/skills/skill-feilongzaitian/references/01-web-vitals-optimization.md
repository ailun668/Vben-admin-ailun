# Web Vitals 性能优化完全指南

> 对标 Google 性能标准，帮你将网站性能评分从 F 提升到 A

## 快速诊断

```bash
# 使用 Lighthouse 诊断
npx lighthouse https://example.com --output-path=report.html

# 或者在浏览器中按 F12 → Lighthouse 标签
```

---

## 📊 四大 Web Vitals 指标

### 1. LCP (Largest Contentful Paint) - 最大内容绘制

**目标：≤ 2.5 秒**

#### 什么是 LCP？
最大内容块（文本、图片、视频）首次出现在用户视口中的时间。

#### 为什么重要？
影响用户对页面"加载完成"的感知。如果 LCP > 2.5s，用户会感觉页面很慢。

#### 常见原因和解决方案

| 原因 | 优化方案 | 预期改进 |
|------|--------|--------|
| **关键资源加载慢** | 优化 JS/CSS 大小，使用代码分割 | 20-40% |
| **服务器响应慢（TTFB）** | 使用 CDN，数据库优化，缓存 | 30-50% |
| **首屏图片未优化** | WebP 格式，响应式图片，lazy loading | 20-30% |
| **渲染阻塞资源** | 使用 async/defer，关键 CSS inline | 15-25% |

#### 实战案例：电商首页优化

```
优化前：LCP = 3.2s

问题诊断：
1. 首屏图片 2MB 未压缩 → 使用 WebP 压缩到 400KB
2. 初始 JS 包 600KB → 代码分割到 150KB（懒加载）
3. 服务器响应 1.5s → 使用 CDN，TTFB 降到 300ms
4. 关键 CSS 在 JS 中 → 提取关键 CSS inline

优化后：LCP = 1.6s ✅
用户体验提升 50%，转化率上升 12%
```

---

### 2. FID / INP (First Input Delay / Interaction to Next Paint) - 交互响应速度

**目标：≤ 100ms（FID，已废弃）/ ≤ 200ms（INP，新指标）**

#### 什么是 INP？
用户与页面交互（点击按钮、输入框输入等）到浏览器响应这个交互的时间。

#### 常见原因和解决方案

| 原因 | 优化方案 |
|------|--------|
| **主线程被 JavaScript 阻塞** | 减少长任务，使用 requestIdleCallback |
| **第三方脚本** | 延迟加载分析脚本、广告脚本 |
| **大量 DOM 操作** | 批量更新，使用 DocumentFragment |
| **复杂的组件重渲染** | 使用 React.memo，避免不必要的 re-render |

#### 代码优化示例

```javascript
// ❌ 坏做法：长任务阻塞主线程
function processData(largeArray) {
  for (let i = 0; i < largeArray.length; i++) {
    // 耗时操作，阻塞主线程
    complexCalculation(largeArray[i]);
  }
}

// ✅ 好做法：分段处理，避免长任务
function processDataOptimized(largeArray) {
  let index = 0;

  function processChunk() {
    const chunkSize = 100;
    const endIndex = Math.min(index + chunkSize, largeArray.length);

    for (let i = index; i < endIndex; i++) {
      complexCalculation(largeArray[i]);
    }

    index = endIndex;

    if (index < largeArray.length) {
      // 让浏览器处理用户交互，然后继续处理
      requestIdleCallback(processChunk);
    }
  }

  processChunk();
}
```

---

### 3. CLS (Cumulative Layout Shift) - 视觉稳定性

**目标：≤ 0.1**

#### 什么是 CLS？
页面元素意外移动的累计量。值越小越好。

#### 常见原因和解决方案

| 原因 | 解决方案 |
|------|--------|
| **图片/视频未指定尺寸** | `<img width="800" height="600">` 或 CSS aspect-ratio |
| **动态内容（广告、通知）** | 为动态内容预留空间 |
| **Web Font 加载导致文本重排** | font-display: swap（优先显示备用字体） |
| **无大小的嵌入式内容** | `<iframe>` 必须指定 width/height |

#### 代码优化示例

```html
<!-- ❌ 导致 CLS 的做法 -->
<img src="image.jpg" />
<!-- 图片加载时，下面的文字会被挤下去 -->

<!-- ✅ 正确做法 -->
<img src="image.jpg" width="800" height="600" />

<!-- 或使用 aspect-ratio -->
<div style="aspect-ratio: 16/9">
  <img src="image.jpg" style="width: 100%; height: 100%;" />
</div>
```

```css
/* CSS aspect-ratio 方式 */
img {
  aspect-ratio: auto;
  width: 100%;
}

/* Web Font 优化 */
@font-face {
  font-display: swap; /* 立即显示备用字体，web font 加载后替换 */
}
```

---

### 4. TTFB (Time to First Byte) - 首字节时间

**目标：≤ 600ms**

#### 什么是 TTFB？
从浏览器请求资源到收到第一字节的时间（衡量服务器响应速度）。

#### 常见原因和解决方案

| 原因 | 解决方案 | 预期效果 |
|------|--------|--------|
| **地理距离** | 使用 CDN 或边缘计算（Cloudflare Workers） | 40-60% 改进 |
| **服务器过载** | 增加服务器资源、使用负载均衡 | 30-50% 改进 |
| **数据库查询慢** | 添加索引、使用 Redis 缓存 | 20-40% 改进 |
| **重定向过多** | 减少重定向（301/302）链 | 10-30% 改进 |

#### 实战：使用 CDN 优化

```javascript
// 使用 Cloudflare Workers 作为边缘计算层
export default {
  async fetch(request) {
    // 静态资源直接返回（缓存在全球边缘节点）
    if (request.url.includes('/api/')) {
      return fetch(request);
    }

    // 其他请求使用缓存
    const cache = caches.default;
    const cachedResponse = await cache.match(request);

    if (cachedResponse) {
      return cachedResponse;
    }

    const response = await fetch(request);
    // 缓存响应
    await cache.put(request, response.clone());
    return response;
  }
}
```

---

## 🎯 性能优化 5 阶法则

### 第 1 阶：诊断（Measure）

```bash
# 1. 运行 Lighthouse
npx lighthouse https://example.com

# 2. 查看 Core Web Vitals
# 在 Google Search Console 查看

# 3. 使用 WebPageTest
# https://www.webpagetest.org
```

### 第 2 阶：快速胜利（Quick Wins）

- ✅ 压缩图片（75% 网站有未优化的图片）
- ✅ 启用 Gzip 压缩
- ✅ 为图片指定宽高
- ✅ 延迟加载第三方脚本

**预期改进：15-30%**

### 第 3 阶：代码优化（Code）

- ✅ 代码分割（Code Splitting）
- ✅ Tree Shaking（移除死代码）
- ✅ 减少 JavaScript 大小
- ✅ 关键 CSS 提取

**预期改进：20-40%**

### 第 4 阶：基础设施（Infrastructure）

- ✅ CDN 部署
- ✅ HTTP/2 或 HTTP/3
- ✅ 数据库优化和缓存
- ✅ 服务器地理分布

**预期改进：30-50%**

### 第 5 阶：高级优化（Advanced）

- ✅ Server Components（Next.js）
- ✅ Edge Computing（Cloudflare Workers）
- ✅ 预渲染（Pre-rendering）
- ✅ 持久化缓存策略

**预期改进：50-70%**

---

## 📈 性能监控

### 实时监控代码

```javascript
// 使用 web-vitals 库监控性能
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

// 上报到分析服务
const reportVital = (vital) => {
  // 发送到服务器进行分析
  navigator.sendBeacon('/analytics', JSON.stringify(vital));
};

getCLS(reportVital);
getFID(reportVital);
getFCP(reportVital);
getLCP(reportVital);
getTTFB(reportVital);
```

### 性能指标对比表

| 指标 | 差 | 需改进 | 良好 |
|------|-----|-------|------|
| LCP | > 4s | 2.5-4s | ≤ 2.5s |
| FID | > 300ms | 100-300ms | ≤ 100ms |
| CLS | > 0.25 | 0.1-0.25 | ≤ 0.1 |
| TTFB | > 1s | 600ms-1s | ≤ 600ms |

---

## 💡 完整优化计划模板

使用此模板规划你的性能优化项目：

```markdown
# 性能优化计划

## 当前状态
- LCP: 3.2s (需改进)
- FID: 180ms (需改进)
- CLS: 0.15 (需改进)
- TTFB: 900ms (差)

## 目标
- LCP: 2.0s
- FID: 100ms
- CLS: 0.1
- TTFB: 500ms

## 优化路线图

### 阶段 1（1-2 周）：快速胜利
- [ ] 压缩图片
- [ ] 启用 Gzip
- [ ] 为图片指定宽高
预期改进: 20%

### 阶段 2（2-4 周）：代码优化
- [ ] 代码分割
- [ ] 移除 unused CSS
- [ ] 优化 JavaScript
预期改进: 30%

### 阶段 3（1 个月）：基础设施
- [ ] 部署 CDN
- [ ] 优化数据库
- [ ] 配置缓存
预期改进: 40%

## 测量和验证
- 每周运行 Lighthouse
- 每周检查 CrUX 数据
- 记录改进前后的对比
```

---

## 📚 参考资源

- [Google Web.dev Performance](https://web.dev/performance)
- [Web Vitals 官方指南](https://web.dev/vitals/)
- [Lighthouse 文档](https://developers.google.com/web/tools/lighthouse)
- [WebPageTest](https://www.webpagetest.org)
