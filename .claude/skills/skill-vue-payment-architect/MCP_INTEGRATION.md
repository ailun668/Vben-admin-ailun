# MCP工具链集成指南

这个Skill与Multiple Context Protocol (MCP)工具链的集成方案

## 概述

当Claude调用此Skill时，它会自动获得对以下MCP工具的访问权限：

- **context7**: 实时文档查询和最佳实践研究
- **playwright**: 自动化性能测试和E2E测试
- 其他专业工具链

## Context7 集成

### 用途

`context7` 是一个文档查询和知识库工具，用于获取最新的技术文档、最佳实践和相关资料。

### 集成场景

#### 1. Vue 3/Nuxt 3 文档查询

当需要了解Vue或Nuxt的最新最佳实践时：

```
Claude: "我需要在Nuxt 3中实现一个复杂的状态管理方案用于支付流程"

Claude使用context7查询:
  query: "Nuxt 3 state management with Pinia for complex workflows"
  topics: ["Pinia", "Composition API", "store patterns"]

context7返回:
  - Nuxt 3官方文档链接
  - Pinia最佳实践
  - 状态管理模式
  - 性能优化建议
```

#### 2. 安全性和合规性查询

```
Claude: "确保KYC流程符合RBI规定"

Claude使用context7查询:
  query: "RBI KYC requirements for fintech 2024"
  topics: ["RBI guidelines", "KYC standards", "India fintech"]

context7返回:
  - RBI最新通函
  - KYC的法律要求
  - 审计日志标准
  - 合规示例
```

#### 3. 性能优化查询

```
Claude: "优化支付表单在4G网络上的性能"

Claude使用context7查询:
  query: "Vue 3 performance optimization for low-bandwidth networks"
  topics: ["Core Web Vitals", "image optimization", "code splitting"]

context7返回:
  - Lighthouse最佳实践
  - 图片优化技术
  - 代码分割策略
  - 低网络条件优化
```

#### 4. 框架兼容性检查

```
Claude: "检查Vite中的最新缓存策略"

Claude使用context7查询:
  query: "Vite 5.0 caching strategies and optimization"
  topics: ["Vite configuration", "build optimization", "caching"]

context7返回:
  - Vite官方文档
  - 最新缓存方案
  - 配置示例
  - 性能对比数据
```

### API使用示例

```python
# context7 的调用方式
context_query = {
    "query": "Vue 3 WebSocket real-time updates patterns",
    "topics": ["Vue 3", "WebSocket", "real-time"],
    "language": "zh-CN",  # 支持中文
    "depth": "comprehensive"  # 深度查询
}

# 返回结构
context_result = {
    "sources": [
        {
            "title": "Vue 3 官方文档",
            "url": "https://vuejs.org",
            "relevance": 0.95,
            "excerpt": "..."
        },
        # ... 更多源
    ],
    "summary": "综合摘要",
    "recommendations": ["推荐1", "推荐2"]
}
```

## Playwright 集成

### 用途

`playwright` 是浏览器自动化工具，用于：
- E2E测试支付流程
- 性能测试（Core Web Vitals）
- 跨浏览器兼容性测试
- 可访问性验证

### 集成场景

#### 1. 支付流程E2E测试

```typescript
// Claude使用playwright自动化测试完整的支付流程
const paymentFlowTest = {
  scenario: "完整的KYC → 支付 → 成功流程",

  steps: [
    {
      action: "navigate",
      url: "http://localhost:3000/kyc"
    },
    {
      action: "fill_form",
      selectors: {
        name: "#kyc-name",
        phone: "#kyc-phone",
        aadhaar: "#kyc-aadhaar"
      }
    },
    {
      action: "wait_for",
      element: ".otp-section",
      timeout: 5000
    },
    {
      action: "fill",
      selector: "#otp-input",
      value: "123456"
    },
    {
      action: "click",
      selector: "button:has-text('验证')"
    },
    {
      action: "assert",
      message: "支付成功",
      selector: ".success-message"
    }
  ]
}
```

#### 2. 性能测试 (低网络模拟)

```typescript
// 模拟印度4G网络的性能
const performanceTest = {
  scenario: "4G网络性能测试",

  networkProfile: {
    downloadSpeed: 2000,  // 2Mbps
    uploadSpeed: 500,     // 0.5Mbps
    latency: 100,         // 100ms
  },

  metrics: {
    // Core Web Vitals
    lcp: {
      target: 2500,       // 2.5s
      warning: 4000,      // 4s
    },
    fid: {
      target: 100,        // 100ms
      warning: 300,
    },
    cls: {
      target: 0.1,
      warning: 0.25,
    },

    // 其他指标
    timeToInteractive: {
      target: 3500,       // 3.5s
    },
    firstContentfulPaint: {
      target: 1800,       // 1.8s
    },
  },

  test: async (page: Page) => {
    // 导航到支付页面
    await page.goto('http://localhost:3000/payment')

    // 测量LCP
    const metrics = await page.evaluate(() => {
      const lcp = new PerformanceObserver((list) => {
        const entries = list.getEntries()
        return entries[entries.length - 1]?.renderTime
      })
      lcp.observe({ entryTypes: ['largest-contentful-paint'] })
      return { lcp }
    })

    return metrics
  }
}
```

#### 3. 跨浏览器兼容性测试

```typescript
// 在多个浏览器上测试支付表单
const crossBrowserTest = {
  scenario: "支付表单跨浏览器兼容性",

  browsers: [
    "chromium",    // Chrome, Edge等
    "firefox",     // Firefox
    "webkit",      // Safari
    // 移动浏览器
    "mobile-chrome",
    "mobile-safari"
  ],

  test: async (page: Page) => {
    // 测试支付表单
    await page.goto('http://localhost:3000/payment-form')

    // 验证表单元素
    const amountInput = await page.locator('#amount-input')
    await amountInput.fill('1000')

    // 验证OTP输入
    const otpInput = await page.locator('#otp-input')
    await expect(otpInput).toBeVisible()

    // 测试提交
    const submitBtn = await page.locator('button:has-text("submit")')
    await submitBtn.click()

    // 验证结果
    await expect(page.locator('.success-message')).toBeVisible()
  }
}
```

#### 4. 可访问性测试

```typescript
// 验证支付表单的无障碍访问
const accessibilityTest = {
  scenario: "支付表单可访问性验证",

  checks: {
    // WCAG 2.1 AA标准
    wcagLevel: "AA",

    // 键盘导航
    keyboardNavigation: {
      tabOrder: [
        "#amount-input",
        "#recipient-input",
        "#description-input",
        "#submit-button"
      ]
    },

    // 屏幕阅读器兼容性
    screenReaderCompatibility: {
      landmarks: ["main", "form"],
      labels: "all form inputs have labels",
      ariaDescriptions: "error messages have aria-describedby"
    },

    // 色彩对比
    colorContrast: {
      minRatio: 4.5,  // AA标准
      checkAgainst: "background"
    },

    // 焦点管理
    focusManagement: {
      visibleFocus: true,
      trapFocus: "in dialog"
    }
  }
}
```

#### 5. 离线功能测试

```typescript
// 测试离线支持和数据同步
const offlineTest = {
  scenario: "离线支付和重新连接",

  steps: [
    {
      action: "navigate",
      url: "http://localhost:3000/payment"
    },
    {
      action: "fill_form",
      data: {
        amount: "1000",
        recipient: "9876543210"
      }
    },
    {
      action: "simulate",
      event: "network_offline"  // 模拟网络断开
    },
    {
      action: "click",
      selector: "button:has-text('提交')"
    },
    {
      action: "assert",
      message: "应显示离线提示",
      selector: ".offline-message"
    },
    {
      action: "simulate",
      event: "network_online"  // 恢复网络
    },
    {
      action: "wait_for",
      message: "数据同步完成",
      timeout: 5000
    },
    {
      action: "assert",
      message: "支付成功",
      selector: ".success-message"
    }
  ]
}
```

## 集成工作流

### 工作流1: 新功能开发

```
1. Claude接到任务: "实现KYC文档上传功能"

2. Claude使用context7查询:
   - 最新的RBI KYC要求
   - Vue 3文件上传最佳实践
   - 安全的文件处理方式

3. Claude编写代码

4. Claude使用playwright验证:
   - 文件上传功能测试
   - 跨浏览器兼容性
   - 可访问性检查
   - 性能测试

5. 生成测试报告和建议
```

### 工作流2: 性能优化

```
1. Claude接到任务: "优化支付表单的加载速度"

2. Claude使用playwright进行基准测试:
   - 当前Lighthouse评分
   - Core Web Vitals指标
   - 瓶颈识别

3. Claude使用context7查询:
   - 最新的性能优化技术
   - Vue 3性能最佳实践
   - 图片和资源优化

4. Claude实施优化

5. Claude再次使用playwright验证:
   - 新的性能指标
   - 对比改进前后
   - 生成优化报告
```

### 工作流3: 合规性审计

```
1. Claude接到任务: "验证项目的PCI-DSS合规性"

2. Claude使用scripts中的security-audit.py扫描代码

3. Claude使用context7查询:
   - 最新的PCI-DSS标准
   - RBI规定更新
   - 安全最佳实践

4. Claude生成合规性报告

5. Claude使用playwright验证:
   - HTTPS配置
   - CSP策略
   - 敏感数据处理
```

## 配置文件

### .claude/mcp-config.json

```json
{
  "integrations": {
    "context7": {
      "enabled": true,
      "options": {
        "language": "zh-CN",
        "sources": [
          "official_documentation",
          "best_practices",
          "community_resources"
        ],
        "depth": "comprehensive",
        "cache": true
      }
    },
    "playwright": {
      "enabled": true,
      "options": {
        "browsers": ["chromium", "firefox", "webkit"],
        "headless": true,
        "slowDown": 0,
        "timeout": 30000,
        "screenshot": "only-on-failure",
        "video": "retain-on-failure"
      },
      "networkProfiles": {
        "fast4g": {
          "downloadSpeed": 4000,
          "uploadSpeed": 3000,
          "latency": 50
        },
        "slow4g": {
          "downloadSpeed": 2000,
          "uploadSpeed": 500,
          "latency": 100
        },
        "3g": {
          "downloadSpeed": 1600,
          "uploadSpeed": 400,
          "latency": 200
        },
        "offline": {
          "downloadSpeed": 0,
          "uploadSpeed": 0,
          "latency": -1
        }
      }
    }
  },
  "skill_capabilities": {
    "architecture_design": {
      "uses": ["context7"],
      "description": "查询最新的架构模式和最佳实践"
    },
    "security_audit": {
      "uses": ["scripts"],
      "description": "自动化安全审计和扫描"
    },
    "performance_testing": {
      "uses": ["playwright"],
      "description": "自动化性能测试和优化验证"
    },
    "e2e_testing": {
      "uses": ["playwright"],
      "description": "端到端测试支付流程"
    },
    "compliance_verification": {
      "uses": ["context7", "scripts"],
      "description": "验证RBI/PCI-DSS合规性"
    }
  }
}
```

## 最佳实践

### 1. 合理使用Context7

```
✅ 好的用法:
- 查询特定技术的最新文档
- 了解行业最佳实践的最新进展
- 搜索相关的安全标准和规定

❌ 过度使用:
- 重复查询相同内容
- 查询非常基础的信息
- 查询与项目无关的内容
```

### 2. 有效的Playwright测试

```
✅ 好的用法:
- 测试关键用户流程（支付、KYC）
- 在多种网络条件下测试
- 验证无障碍可访问性
- 监控性能指标

❌ 过度使用:
- 测试每一个UI元素
- 频繁地运行完整的测试套件
- 不必要的截图和视频录制
```

### 3. 缓存和优化

```typescript
// 利用MCP缓存机制
const smartQueryUsage = {
  // ✅ 利用缓存：查询一次，多次使用
  queryOnce: () => {
    const vueBestPractices = context7.query("Vue 3 best practices 2024")
    // 在多个地方使用这个结果
    applyToProject(vueBestPractices)
    generateDocumentation(vueBestPractices)
  },

  // ❌ 避免重复查询
  dontQueryRepeatedly: () => {
    const result1 = context7.query("Vue 3 best practices")
    const result2 = context7.query("Vue 3 best practices")  // 重复！
  }
}
```

## 故障排除

### 问题1: Context7查询返回不相关的结果

**解决**:
- 更具体地指定查询主题
- 使用相关的关键词组合
- 指定特定的时间范围（如"2024年最新"）

### 问题2: Playwright测试在CI中失败

**解决**:
- 增加超时时间
- 检查网络模拟设置
- 验证选择器的稳定性
- 使用 `waitForNavigation()` 处理异步操作

### 问题3: MCP工具超时

**解决**:
- 减少单次操作的复杂性
- 分解为多个较小的任务
- 检查网络连接和API可用性

## 监控和日志

所有MCP工具的使用都会被记录：

```
logs/mcp-usage.log:
  [2024-11-15 10:30:45] context7 query: "Vue 3 state management"
  [2024-11-15 10:30:46] context7 response: 5 sources found
  [2024-11-15 10:31:02] playwright test: payment_form_e2e started
  [2024-11-15 10:31:45] playwright test: passed in 43.2s
  [2024-11-15 10:32:10] playwright metrics: LCP=1.2s, FID=45ms, CLS=0.05
```

查看日志：
```bash
tail -f logs/mcp-usage.log
```

---

**通过有效的MCP工具集成，Claude可以提供最专业和最新的支付平台开发指导。**
