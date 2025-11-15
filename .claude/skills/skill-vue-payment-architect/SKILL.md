---
name: vue-payment-architect
description: Expert Vue 3 fullstack architect for fintech payment platforms. Specializes in secure transaction flows, KYC/AML compliance, real-time state management, offline-first architecture, and Indian payment ecosystem (UPI, RBI regulations). Builds production-grade payment systems with PCI-DSS compliance, high concurrency handling, and resilience for low-bandwidth networks.
---

# Vue支付平台全栈架构指南

## 核心价值与定位

### 什么是这个Skill

这个Skill是一份**金融级别的Vue 3全栈开发指南**，专注于构建**支付平台系统**的前端架构和工程实现。它不仅仅是代码片段库，而是一套完整的方法论，涵盖：

- 🏗️ **架构设计** - 从零开始规划支付平台的前端结构
- 🔐 **金融安全** - PCI-DSS合规、敏感数据加密、审计日志
- ⚡ **高性能** - 高并发支付、低延迟实时更新、低带宽优化
- 🌍 **印度本地化** - UPI支持、多语言、RBI合规、离线弹性
- 📊 **状态管理** - 复杂的支付状态机、事务一致性
- 🛡️ **容错能力** - 网络不稳定下的优雅降级、离线-在线无缝同步

### 何时使用这个Skill

✅ **正确的场景**：
- 从零开始构建支付平台前端
- 重构现有支付系统的架构
- 添加新的支付功能（KYC、转账、理财等）
- 解决高并发或安全相关的问题
- 适配印度市场（UPI、多语言、低网络）

❌ **不适合的场景**：
- 简单的代码片段查询（用通用的Vue文档即可）
- 非金融相关的业务需求
- 仅需要UI组件的项目

---

## 第一章：支付平台架构基础

### 支付系统的三大支柱

支付平台的前端架构围绕三个核心支柱展开：

```
┌─────────────────────────────────────────────────────────┐
│              支付平台前端架构三大支柱                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🔐 安全性 (Security)                                    │
│  ├─ PCI-DSS合规: 卡号、密码、OTP从不在前端存储          │
│  ├─ 加密传输: HTTPS + TLS 1.3, 字段级加密              │
│  ├─ 无日志原则: 不记录敏感数据到任何地方               │
│  └─ 前端防护: XSS、CSRF、中间人攻击防护                │
│                                                          │
│  ⚡ 高并发 (High Concurrency)                           │
│  ├─ 秒杀场景: 支付高峰期的流量控制                     │
│  ├─ 实时状态: WebSocket连接的管理和重连机制           │
│  ├─ 乐观更新: 前端先更新，后端确认                     │
│  └─ 竞态条件: 防止重复支付的幂等性设计                │
│                                                          │
│  🌐 实时性 (Real-time Responsiveness)                  │
│  ├─ 余额同步: 实时反映账户余额变化                     │
│  ├─ 交易状态: 支付过程的每一步都有反馈                │
│  ├─ 风险提示: 异常活动的实时告警                       │
│  └─ 离线优先: 网络中断时的本地缓存和同步              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Vue 3在支付平台中的角色

Vue 3的Composition API特别适合支付系统：

| 特性 | 支付场景 | Vue 3优势 |
|------|---------|----------|
| **响应式状态** | 实时余额更新、交易状态 | 细粒度响应性，避免不必要重渲染 |
| **组合式函数** | KYC、支付、结算等独立流程 | 逻辑复用，易于测试 |
| **TypeScript** | 确保类型安全，减少运行时错误 | 严格模式下的完美支持 |
| **Teleport** | 模态对话框、风险提示 | 避免z-index混乱 |
| **Suspense** | 异步数据加载（KYC审核结果） | 优雅的加载状态 |

### RBI与NPCI的关键要求

支付平台必须满足的核心要求：

```yaml
RBI (印度央行) 要求:
  数据本地化: 所有用户数据必须存储在印度服务器
  加密强度: AES-256用于敏感数据
  审计日志: 6年以上的完整审计日志
  身份验证: 强身份验证，如OTP、生物识别
  风险管理: 实时反欺诈和AML检测

NPCI (国家支付公司) UPI要求:
  交易超时: 5分钟内完成或失败
  重试机制: 自动重试3次，间隔10秒
  金额限额: 单笔支付限额₹100,000
  交易频率: 限制异常频繁的交易
```

---

## 第二章：支付平台项目架构

### 推荐的项目结构

```
payment-platform/
│
├── src/
│   ├── features/                    # 功能模块（按业务域组织）
│   │   ├── auth/                    # 身份认证与KYC
│   │   │   ├── components/
│   │   │   │   ├── LoginForm.vue
│   │   │   │   ├── OTPVerify.vue
│   │   │   │   └── KYCUpload.vue
│   │   │   ├── composables/
│   │   │   │   ├── useAuth.ts
│   │   │   │   └── useKYC.ts
│   │   │   ├── stores/
│   │   │   │   └── authStore.ts
│   │   │   └── types/
│   │   │       └── auth.ts
│   │   │
│   │   ├── wallet/                  # 钱包与余额管理
│   │   │   ├── components/
│   │   │   │   ├── WalletCard.vue
│   │   │   │   ├── BalanceDisplay.vue
│   │   │   │   └── RechargeModal.vue
│   │   │   ├── composables/
│   │   │   │   ├── useWallet.ts
│   │   │   │   └── useBalance.ts
│   │   │   └── stores/
│   │   │       └── walletStore.ts
│   │   │
│   │   ├── transaction/             # 交易管理（支付、转账）
│   │   │   ├── components/
│   │   │   │   ├── PaymentForm.vue
│   │   │   │   ├── TransactionStatus.vue
│   │   │   │   └── TransactionHistory.vue
│   │   │   ├── composables/
│   │   │   │   ├── usePayment.ts
│   │   │   │   └── useTransactionState.ts
│   │   │   └── stores/
│   │   │       └── transactionStore.ts
│   │   │
│   │   ├── risk-control/            # 风险控制与反欺诈
│   │   │   ├── composables/
│   │   │   │   ├── useRiskDetection.ts
│   │   │   │   └── useAnomalyAlert.ts
│   │   │   └── stores/
│   │   │       └── riskStore.ts
│   │   │
│   │   └── settlement/              # 清算与对账
│   │       ├── composables/
│   │       │   └── useSettlement.ts
│   │       └── stores/
│   │           └── settlementStore.ts
│   │
│   ├── shared/                      # 共享功能
│   │   ├── security/                # 安全相关
│   │   │   ├── encryption.ts        # 加密/解密工具
│   │   │   ├── audit.ts             # 审计日志
│   │   │   └── validation.ts        # 输入验证
│   │   │
│   │   ├── realtime/                # 实时通信
│   │   │   ├── websocket.ts         # WebSocket管理
│   │   │   ├── reconnect.ts         # 自动重连
│   │   │   └── handlers.ts          # 消息处理器
│   │   │
│   │   ├── offline/                 # 离线支持
│   │   │   ├── sync.ts              # 数据同步
│   │   │   ├── storage.ts           # 本地存储
│   │   │   └── queue.ts             # 离线队列
│   │   │
│   │   ├── components/              # 通用组件
│   │   │   ├── ErrorBoundary.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   └── ConfirmDialog.vue
│   │   │
│   │   └── composables/             # 通用组合函数
│   │       ├── useNetworkStatus.ts
│   │       ├── useErrorHandler.ts
│   │       └── useLocalization.ts
│   │
│   ├── infrastructure/              # 基础设施
│   │   ├── state-machine/           # 状态机
│   │   │   ├── paymentStateMachine.ts
│   │   │   └── transactionFlow.ts
│   │   │
│   │   ├── error-recovery/          # 错误恢复
│   │   │   ├── retryStrategy.ts
│   │   │   └── fallback.ts
│   │   │
│   │   ├── api/                     # API调用层
│   │   │   ├── client.ts
│   │   │   ├── interceptors.ts
│   │   │   └── types.ts
│   │   │
│   │   └── i18n/                    # 国际化（11种印度语言）
│   │       ├── en.ts
│   │       ├── hi.ts
│   │       └── ...
│   │
│   ├── pages/                       # 页面路由
│   │   ├── index.vue
│   │   ├── wallet.vue
│   │   ├── transaction/
│   │   │   ├── payment.vue
│   │   │   └── transfer.vue
│   │   ├── kyc/
│   │   │   ├── upload.vue
│   │   │   └── verify.vue
│   │   └── ...
│   │
│   ├── layouts/                     # 布局组件
│   │   ├── default.vue
│   │   └── auth.vue
│   │
│   ├── app.vue
│   └── main.ts
│
├── tests/
│   ├── unit/                        # 单元测试
│   ├── integration/                 # 集成测试
│   └── e2e/                         # 端到端测试
│
├── scripts/                         # 工具脚本（来自Skill的scripts/）
│   ├── security-audit.py
│   ├── architecture-validator.py
│   └── ...
│
├── nuxt.config.ts                   # Nuxt 3配置
├── vitest.config.ts                 # 测试配置
├── tailwind.config.ts               # Tailwind配置
├── tsconfig.json                    # TypeScript配置（strict mode）
├── .env.example                     # 环境变量模板
└── README.md
```

### 模块依赖关系

```
auth (认证) ──→ wallet (钱包)
                 ├─→ transaction (交易)
                 │   ├─→ risk-control (风险)
                 │   └─→ settlement (清算)
                 └─→ user profile

shared (共享) ←── 所有模块依赖
 ├─ security
 ├─ realtime
 └─ offline

infrastructure ←── 所有模块依赖
 ├─ state-machine
 ├─ error-recovery
 ├─ api
 └─ i18n
```

---

## 第三章：支付安全最佳实践

### PCI-DSS合规核心原则

**原则1：敏感数据永远不存储在前端**

```typescript
// ❌ 错误做法
const handlePayment = async (cardNumber: string, cvv: string) => {
  // 永远不要在前端保存这些信息！
  localStorage.setItem('cardNumber', cardNumber)
  localStorage.setItem('cvv', cvv)
}

// ✅ 正确做法
const handlePayment = async (cardToken: string) => {
  // 只在前端保存来自后端的无害token
  const response = await api.processPayment({ token: cardToken })
}
```

**原则2：所有通信必须加密**

```typescript
// HTTPS + TLS 1.3 (必须)
const apiClient = axios.create({
  baseURL: 'https://api.payment.example.com', // 注意：https不是http
  timeout: 5000,
})

// 请求级别加密（字段级）
const encryptPaymentData = (data: PaymentData): string => {
  const cipher = crypto.subtle.encrypt(
    {
      name: 'AES-GCM',
      iv: generateRandomIV(),
    },
    key,
    new TextEncoder().encode(JSON.stringify(data))
  )
  return btoa(cipher) // Base64编码
}
```

**原则3：无日志原则**

```typescript
// ❌ 错误做法
console.log('支付信息:', {
  cardNumber: '4532xxxxxxxxxxxx',
  amount: 1000,
})

// ✅ 正确做法
console.log('支付处理中，金额:', amount)
// 日志中完全不记录cardNumber

// 安全的日志函数
const safeLog = (action: string, data: any) => {
  const sanitized = sanitizeSensitiveData(data)
  console.log(`[${action}]`, sanitized)
  // 发送到后端安全的审计系统
  auditLog.record(action, sanitized)
}
```

### 前端安全防护

#### 防XSS（跨站脚本攻击）

```typescript
// Vue 3 自动转义HTML
// ✅ 安全
<template>
  <div>{{ userInput }}</div> <!-- 自动转义 -->
</template>

// ❌ 危险
<template>
  <div v-html="userInput"></div> <!-- 仅在信任的内容中使用 -->
</template>

// CSP（内容安全策略）
// 在HTML头部添加
<meta
  http-equiv="Content-Security-Policy"
  content="default-src 'self'; script-src 'self' 'unsafe-inline';">
```

#### 防CSRF（跨站请求伪造）

```typescript
// 1. 获取CSRF令牌
const getCsrfToken = async () => {
  const response = await fetch('/api/csrf-token')
  return response.json().token
}

// 2. 在每个修改请求中包含
const api = axios.create({
  headers: {
    'X-CSRF-Token': csrfToken,
  },
})

// 3. 同源请求检查
// 在请求拦截器中验证
api.interceptors.request.use((config) => {
  if (['post', 'put', 'delete'].includes(config.method?.toLowerCase())) {
    config.headers['X-CSRF-Token'] = getCsrfToken()
  }
  return config
})
```

#### 防中间人攻击

```typescript
// 1. 证书绑定（Certificate Pinning）
const createSecureClient = () => {
  return axios.create({
    baseURL: 'https://api.payment.example.com',
    httpAgent: new http.Agent({
      rejectUnauthorized: true,
    }),
    httpsAgent: new https.Agent({
      rejectUnauthorized: true,
      ca: [fs.readFileSync('path/to/certificate.pem')],
    }),
  })
}

// 2. 子资源完整性（SRI）
// 在HTML中加载脚本时
<script
  src="https://cdn.example.com/library.js"
  integrity="sha384-hash">
</script>
```

### 敏感数据加密策略

```typescript
// 加密Key管理
class EncryptionManager {
  private key: CryptoKey

  async initialize() {
    // 从后端获取加密密钥（永远不在前端生成）
    const keyMaterial = await window.crypto.subtle.importKey(
      'raw',
      new Uint8Array(await fetch('/api/encryption-key').then(r => r.arrayBuffer())),
      { name: 'AES-GCM' },
      false,
      ['encrypt', 'decrypt']
    )
    this.key = keyMaterial
  }

  async encrypt(data: string): Promise<string> {
    const iv = window.crypto.getRandomValues(new Uint8Array(12))
    const encrypted = await window.crypto.subtle.encrypt(
      { name: 'AES-GCM', iv },
      this.key,
      new TextEncoder().encode(data)
    )
    // 返回 IV + 密文（IV不是密钥，可以明文传输）
    return btoa(String.fromCharCode(...new Uint8Array(iv)) +
               String.fromCharCode(...new Uint8Array(encrypted)))
  }

  async decrypt(encrypted: string): Promise<string> {
    const data = atob(encrypted)
    const iv = new Uint8Array(data.charCodeAt(0), /* ... */)
    const ciphertext = new Uint8Array(data.slice(12).split('').map(c => c.charCodeAt(0)))
    const decrypted = await window.crypto.subtle.decrypt(
      { name: 'AES-GCM', iv },
      this.key,
      ciphertext
    )
    return new TextDecoder().decode(decrypted)
  }
}

// 使用示例
const encManager = new EncryptionManager()
await encManager.initialize()
const encrypted = await encManager.encrypt(sensitiveData)
const decrypted = await encManager.decrypt(encrypted)
```

---

## 第四章：关键业务流程架构

### 支付交易完整流程

支付从开始到结束的完整状态机：

```
┌─────────────────────────────────────────────────────────────┐
│                  支付交易状态机                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  [初始化状态] ─SUBMIT─→ [待验证]                            │
│       ↓                      ↓                                │
│   用户输入               验证余额、限额                      │
│   金额、收款人           检查KYC状态                         │
│                          ↓                                    │
│  [失败]←─NO─[验证通过?]─YES→ [发送OTP]                     │
│       ↓                      ↓                                │
│   返回错误                用户输入OTP                        │
│   提示重试                ↓                                    │
│                    [验证OTP] ─NO→ [重试提示]                │
│                          ↓                                    │
│                         YES                                   │
│                          ↓                                    │
│                   [支付处理中]                               │
│                   ├─ 发送加密请求                           │
│                   ├─ 等待后端确认                           │
│                   ├─ 超时处理（5分钟）                     │
│                   └─ 重试机制（最多3次）                    │
│                          ↓                                    │
│              [交易成功] 或 [交易失败]                        │
│                   ↓              ↓                            │
│              更新余额         显示错误                        │
│              发送通知         建议重试/联系客服             │
│              记录交易         同步到服务器                   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### TypeScript中的状态机实现

```typescript
// 定义所有可能的状态
type PaymentState =
  | 'idle'
  | 'validating'
  | 'otp_pending'
  | 'processing'
  | 'success'
  | 'failed'
  | 'cancelled'

// 定义状态转换规则
const paymentTransitions: Record<PaymentState, PaymentState[]> = {
  idle: ['validating', 'cancelled'],
  validating: ['otp_pending', 'failed'],
  otp_pending: ['processing', 'failed'],
  processing: ['success', 'failed'],
  success: ['idle'],
  failed: ['idle', 'validating'],
  cancelled: ['idle'],
}

// 状态机类
class PaymentStateMachine {
  private currentState: PaymentState = 'idle'
  private readonly transitions = paymentTransitions

  canTransition(toState: PaymentState): boolean {
    return this.transitions[this.currentState]?.includes(toState) ?? false
  }

  transition(toState: PaymentState): boolean {
    if (!this.canTransition(toState)) {
      throw new Error(
        `Cannot transition from ${this.currentState} to ${toState}`
      )
    }
    this.currentState = toState
    return true
  }

  getState(): PaymentState {
    return this.currentState
  }
}

// 使用示例
const paymentSM = new PaymentStateMachine()
paymentSM.transition('validating') // ✅ 允许
paymentSM.transition('processing') // ❌ 错误：不能从validating直接到processing
```

### KYC（了解你的客户）身份验证流程

KYC是支付平台的核心，需要多步验证：

```
[用户注册]
    ↓
[输入基本信息] (姓名、电话、邮箱)
    ↓
[OTP验证电话号码]
    ↓
[输入地址信息]
    ↓
[上传身份证件]
    │├─ Aadhaar (印度唯一身份号)
    │├─ 驾照
    │└─ 护照
    ↓
[照片上传 + 活体检测]
    ├─ 前脸照片
    ├─ 活体检测（眨眼、转头）
    └─ 与身份证对比
    ↓
[等待审核] (由人工或AI审核)
    ├─ ✅ 已批准 → KYC完成
    ├─ ❌ 被拒绝 → 显示原因，可重新申请
    └─ ⏳ 审核中 → 显示进度
    ↓
[用户获得不同级别的支付限额]
    ├─ Tier 1 (KYC Lite): ₹100,000/天
    ├─ Tier 2 (完整KYC): ₹500,000/天
    └─ Tier 3 (增强KYC): 无限制
```

#### Vue组件实现：

```typescript
// composables/useKYCFlow.ts
import { ref, computed } from 'vue'

type KYCStep =
  | 'basic_info'
  | 'phone_verify'
  | 'address'
  | 'document_upload'
  | 'liveness_check'
  | 'pending_review'
  | 'completed'

export const useKYCFlow = () => {
  const currentStep = ref<KYCStep>('basic_info')
  const kycData = ref({
    basicInfo: {},
    address: {},
    document: null,
    livenessCheck: {},
  })

  const canProceedToNextStep = computed(() => {
    switch (currentStep.value) {
      case 'basic_info':
        return kycData.value.basicInfo.name &&
               kycData.value.basicInfo.phone
      case 'phone_verify':
        return !!kycData.value.basicInfo.otpVerified
      case 'address':
        return !!kycData.value.address.fullAddress
      case 'document_upload':
        return !!kycData.value.document
      case 'liveness_check':
        return !!kycData.value.livenessCheck.passed
      default:
        return false
    }
  })

  const nextStep = () => {
    const steps: KYCStep[] = [
      'basic_info', 'phone_verify', 'address',
      'document_upload', 'liveness_check', 'pending_review'
    ]
    const currentIndex = steps.indexOf(currentStep.value)
    if (currentIndex < steps.length - 1) {
      currentStep.value = steps[currentIndex + 1]
    }
  }

  const submitKYC = async () => {
    try {
      const response = await api.submitKYC(kycData.value)
      currentStep.value = 'pending_review'
      return response
    } catch (error) {
      console.error('KYC提交失败:', error)
      throw error
    }
  }

  return {
    currentStep,
    kycData,
    canProceedToNextStep,
    nextStep,
    submitKYC,
  }
}

// 组件使用
<template>
  <div class="kyc-flow">
    <div v-if="currentStep === 'basic_info'">
      <BasicInfoForm @submit="nextStep" />
    </div>
    <div v-else-if="currentStep === 'phone_verify'">
      <PhoneVerifyForm @submit="nextStep" />
    </div>
    <!-- ... 其他步骤 -->
    <div v-else-if="currentStep === 'pending_review'">
      <PendingMessage />
    </div>
  </div>
</template>
```

---

## 第五章：高并发与实时性设计

### WebSocket实时状态更新架构

支付平台需要实时推送：余额、交易状态、风险提示等。

```typescript
// composables/useRealtimeUpdates.ts
import { ref, onMounted, onUnmounted } from 'vue'

interface RealtimeUpdate {
  type: 'balance' | 'transaction' | 'alert' | 'kyc_status'
  data: any
  timestamp: number
}

export const useRealtimeUpdates = () => {
  const ws = ref<WebSocket | null>(null)
  const balance = ref(0)
  const transactionStatus = ref<Record<string, any>>({})
  const alerts = ref<RealtimeUpdate[]>([])
  const isConnected = ref(false)
  const reconnectAttempts = ref(0)
  const maxReconnectAttempts = 5

  const connect = () => {
    try {
      // 使用 wss:// (WebSocket Secure)
      ws.value = new WebSocket(
        'wss://api.payment.example.com/realtime',
        ['payment-v1'] // 子协议用于版本控制
      )

      ws.value.onopen = () => {
        console.log('实时连接已建立')
        isConnected.value = true
        reconnectAttempts.value = 0

        // 认证
        ws.value?.send(JSON.stringify({
          type: 'auth',
          token: getAuthToken(),
        }))

        // 订阅感兴趣的事件
        ws.value?.send(JSON.stringify({
          type: 'subscribe',
          channels: ['balance', 'transactions', 'alerts'],
        }))
      }

      ws.value.onmessage = (event) => {
        const update: RealtimeUpdate = JSON.parse(event.data)
        handleUpdate(update)
      }

      ws.value.onerror = (error) => {
        console.error('WebSocket错误:', error)
        isConnected.value = false
      }

      ws.value.onclose = () => {
        console.log('连接关闭，尝试重连...')
        isConnected.value = false
        attemptReconnect()
      }
    } catch (error) {
      console.error('WebSocket连接失败:', error)
      attemptReconnect()
    }
  }

  const handleUpdate = (update: RealtimeUpdate) => {
    switch (update.type) {
      case 'balance':
        // 乐观更新验证：仅在签名有效时更新
        if (verifySignature(update)) {
          balance.value = update.data.balance
        }
        break
      case 'transaction':
        transactionStatus.value[update.data.txId] = update.data
        break
      case 'alert':
        alerts.value.push(update)
        // 自动移除旧警告（5分钟后）
        setTimeout(() => {
          alerts.value = alerts.value.filter(a => a.timestamp !== update.timestamp)
        }, 5 * 60 * 1000)
        break
      case 'kyc_status':
        // KYC状态更新，通知用户
        emitEvent('kyc-updated', update.data)
        break
    }
  }

  const attemptReconnect = () => {
    if (reconnectAttempts.value < maxReconnectAttempts) {
      reconnectAttempts.value++
      // 指数退避：1s, 2s, 4s, 8s, 16s
      const delay = Math.pow(2, reconnectAttempts.value - 1) * 1000
      console.log(`${delay}ms后重新连接...`)
      setTimeout(connect, delay)
    } else {
      console.error('无法重新连接，请刷新页面')
      // 通知用户手动刷新
      emitEvent('connection-failed')
    }
  }

  const disconnect = () => {
    if (ws.value) {
      ws.value.close()
      ws.value = null
    }
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    balance,
    transactionStatus,
    alerts,
    isConnected,
    disconnect,
  }
}
```

### 乐观更新 vs 强一致性

支付系统中的权衡：

```typescript
// 使用场景：转账金额输入
const optimisticUpdateBalance = async (amount: number) => {
  // 1. 立即在前端更新（乐观）
  const previousBalance = balance.value
  balance.value -= amount

  try {
    // 2. 发送请求到后端
    const response = await api.transfer({
      amount,
      toUserId: recipientId.value
    })

    // 3. 后端确认，同步真实余额
    balance.value = response.newBalance

    return response
  } catch (error) {
    // 4. 如果失败，回滚到之前的状态
    balance.value = previousBalance
    throw error
  }
}

// 使用场景：支付状态查询
const getTransactionStatusRealtime = async (txId: string) => {
  // 不使用乐观更新，直接获取最新状态
  const status = await api.getTransactionStatus(txId)
  transactionStatus.value = status
  return status
}
```

### 防止重复支付（幂等性）

```typescript
// 使用Idempotency Key防止重复扣款
const submitPayment = async (paymentData: PaymentData) => {
  // 1. 生成唯一的请求ID（在客户端生成）
  const idempotencyKey = generateIdempotencyKey(paymentData)

  // 2. 在所有支付请求中包含此Key
  const config = {
    headers: {
      'Idempotency-Key': idempotencyKey,
    },
  }

  try {
    // 3. 第一次请求执行支付
    const response = await api.payment(paymentData, config)
    return response
  } catch (error) {
    // 4. 如果网络错误，重试使用相同的Key
    // 后端会识别重复请求，返回缓存的结果
    const retryResponse = await api.payment(paymentData, config)
    return retryResponse
  }
}

// 生成Idempotency Key的方法
const generateIdempotencyKey = (data: PaymentData): string => {
  const key = `${userId}-${data.recipientId}-${data.amount}-${Date.now()}`
  return crypto.createHash('sha256').update(key).digest('hex')
}
```

---

## 第六章：离线优先架构（Offline-First）

印度网络环境的特殊考虑：
- 3G/4G信号不稳定
- 用户可能进入隧道/地下室
- 高峰期网络拥塞

### 离线数据同步策略

```typescript
// composables/useOfflineSync.ts
import { ref } from 'vue'

interface OfflineAction {
  id: string
  type: 'payment' | 'transfer' | 'recharge'
  data: any
  timestamp: number
  status: 'pending' | 'synced' | 'failed'
}

export const useOfflineSync = () => {
  const offlineQueue = ref<OfflineAction[]>([])
  const isOnline = ref(navigator.onLine)
  const syncInProgress = ref(false)

  // 监听网络状态
  window.addEventListener('online', () => {
    isOnline.value = true
    syncOfflineActions()
  })
  window.addEventListener('offline', () => {
    isOnline.value = false
  })

  // 当在线时添加到队列
  const queueAction = async (
    type: OfflineAction['type'],
    data: any
  ): Promise<boolean> => {
    const action: OfflineAction = {
      id: generateId(),
      type,
      data,
      timestamp: Date.now(),
      status: 'pending',
    }

    if (isOnline.value) {
      // 直接执行
      try {
        await executeAction(action)
        action.status = 'synced'
        return true
      } catch (error) {
        // 即使在线也失败，加入队列重试
        offlineQueue.value.push(action)
        return false
      }
    } else {
      // 离线状态，加入本地队列
      offlineQueue.value.push(action)
      saveQueueToStorage()
      return true
    }
  }

  // 同步所有离线动作
  const syncOfflineActions = async () => {
    if (syncInProgress.value) return

    syncInProgress.value = true
    const pendingActions = offlineQueue.value.filter(
      a => a.status === 'pending'
    )

    for (const action of pendingActions) {
      try {
        await executeAction(action)
        action.status = 'synced'
      } catch (error) {
        console.error(`同步失败: ${action.id}`, error)
        action.status = 'failed'
      }
    }

    // 清理已同步的action
    offlineQueue.value = offlineQueue.value.filter(
      a => a.status !== 'synced'
    )
    saveQueueToStorage()
    syncInProgress.value = false
  }

  const executeAction = async (action: OfflineAction) => {
    switch (action.type) {
      case 'payment':
        return await api.payment(action.data)
      case 'transfer':
        return await api.transfer(action.data)
      case 'recharge':
        return await api.recharge(action.data)
    }
  }

  // IndexedDB持久化
  const saveQueueToStorage = () => {
    const db = openIndexedDB()
    const tx = db.transaction('offlineActions', 'readwrite')
    tx.objectStore('offlineActions').clear()
    offlineQueue.value.forEach(action => {
      tx.objectStore('offlineActions').add(action)
    })
  }

  const loadQueueFromStorage = () => {
    const db = openIndexedDB()
    const tx = db.transaction('offlineActions', 'readonly')
    const store = tx.objectStore('offlineActions')
    const request = store.getAll()
    request.onsuccess = () => {
      offlineQueue.value = request.result
    }
  }

  return {
    offlineQueue,
    isOnline,
    syncInProgress,
    queueAction,
    syncOfflineActions,
    loadQueueFromStorage,
  }
}
```

### 本地缓存策略

```typescript
// 使用Service Worker缓存
// public/service-worker.js

const CACHE_VERSION = 'v1'
const CACHE_NAME = `payment-app-${CACHE_VERSION}`

const CACHE_URLS = [
  '/',
  '/index.html',
  '/app.js',
  '/app.css',
  '/logo.png',
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CACHE_URLS)
    })
  )
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // API请求：网络优先，缓存备用
  if (url.pathname.startsWith('/api')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // 缓存成功的响应
          if (response.status === 200) {
            const responseToCache = response.clone()
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, responseToCache)
            })
          }
          return response
        })
        .catch(() => {
          // 网络失败，尝试缓存
          return caches.match(request)
        })
    )
  } else {
    // 静态资源：缓存优先
    event.respondWith(
      caches.match(request).then(response => {
        return response || fetch(request)
      })
    )
  }
})
```

---

## 第七章：多国市场支持（国际化）

### 印度语言支持

印度有11种官方语言，支付平台必须支持主要的：

```
- 英语 (en) - 常用于技术和官方文件
- 印地语 (hi) - 最广泛使用，~43%人口
- 马拉地语 (mr) - 西部（马哈拉施特拉邦）
- 泰米尔语 (ta) - 南部
- 泰卢固语 (te) - 南部
- 古吉拉特语 (gu) - 西部
- 卡纳达语 (kn) - 南部
- 旁遮普语 (pa) - 北部
- 孟加拉语 (bn) - 东部
- 乌尔都语 (ur) - 少数民族
- 奥里亚语 (or) - 东部
```

### 使用 vue-i18n 配置

```typescript
// src/infrastructure/i18n/index.ts
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import hi from './locales/hi.json'
import mr from './locales/mr.json'
// ... 其他语言

const messages = {
  en,
  hi,
  mr,
  // ...
}

// 检测用户的首选语言
const detectLanguage = (): string => {
  // 1. 检查本地存储
  const saved = localStorage.getItem('preferredLanguage')
  if (saved) return saved

  // 2. 检查浏览器语言
  const browserLang = navigator.language.split('-')[0]
  if (Object.keys(messages).includes(browserLang)) return browserLang

  // 3. 默认英语
  return 'en'
}

export const i18n = createI18n({
  legacy: false,
  locale: detectLanguage(),
  fallbackLocale: 'en',
  messages,
  globalInjection: true,
  compositionOnly: true,
})

// 语言切换函数
export const setLanguage = (lang: string) => {
  i18n.global.locale.value = lang
  localStorage.setItem('preferredLanguage', lang)
  // 更新HTML lang属性
  document.documentElement.lang = lang
}
```

### 多货币支持

```typescript
// src/infrastructure/i18n/currency.ts
import { ref } from 'vue'

type Currency = 'INR' | 'USD' | 'EUR' | 'GBP'

const exchangeRates = ref({
  'INR': 1,
  'USD': 0.012,
  'EUR': 0.011,
  'GBP': 0.0095,
})

const formatCurrency = (amount: number, currency: Currency = 'INR'): string => {
  const formatter = new Intl.NumberFormat(
    getLocaleForCurrency(currency),
    {
      style: 'currency',
      currency,
      minimumFractionDigits: 2,
    }
  )
  return formatter.format(amount)
}

const getLocaleForCurrency = (currency: Currency): string => {
  const localeMap: Record<Currency, string> = {
    'INR': 'en-IN',
    'USD': 'en-US',
    'EUR': 'en-DE',
    'GBP': 'en-GB',
  }
  return localeMap[currency]
}

// 使用
const displayAmount = formatCurrency(1000, 'INR') // ₹1,000.00
```

---

## 第八章：性能优化与低端设备支持

### Lighthouse性能目标

```
支付平台的Lighthouse评分目标：
  性能 (Performance): > 90
  可访问性 (Accessibility): > 90
  最佳实践 (Best Practices): > 85
  SEO: > 90

核心Web指标 (Core Web Vitals):
  LCP (最大内容绘制): < 2.5s
  FID (首次输入延迟): < 100ms
  CLS (累积布局偏移): < 0.1
```

### 低端设备优化（印度用户多使用4G+低内存设备）

```typescript
// 1. 代码分割和懒加载
import { defineAsyncComponent } from 'vue'

const PaymentForm = defineAsyncComponent(
  () => import('@/features/transaction/components/PaymentForm.vue')
)
const KYCUpload = defineAsyncComponent(
  () => import('@/features/auth/components/KYCUpload.vue')
)

// 2. 虚拟滚动（处理长交易列表）
import { VirtualScroller } from 'vue-virtual-scroller'

<template>
  <VirtualScroller
    :items="transactions"
    :item-size="100"
    key-field="id"
  >
    <template #default="{ item }">
      <TransactionItem :transaction="item" />
    </template>
  </VirtualScroller>
</template>

// 3. 图片优化
<template>
  <!-- 使用现代格式 (WebP) + 降级 -->
  <picture>
    <source srcset="/logo.webp" type="image/webp">
    <img src="/logo.png" alt="支付平台">
  </picture>

  <!-- 响应式图片 -->
  <img
    srcset="
      /wallet-small.png 400w,
      /wallet-medium.png 800w,
      /wallet-large.png 1200w
    "
    sizes="(max-width: 600px) 400px, 800px"
    src="/wallet-medium.png"
    alt="钱包">
</template>

// 4. 压缩和Tree Shaking
// vite.config.ts
export default {
  build: {
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          'vue': ['vue'],
          'crypto': ['crypto-js'],
        },
      },
    },
  },
}
```

### 网络优化（4G环境）

```typescript
// 针对弱网环境的优化
const apiClient = axios.create({
  baseURL: 'https://api.payment.example.com',
  timeout: 10000, // 较长的超时时间
})

// 请求压缩
import compression from 'compression-webpack-plugin'

apiClient.interceptors.request.use((config) => {
  // 对大请求体进行压缩
  if (config.data && JSON.stringify(config.data).length > 1000) {
    config.headers['Content-Encoding'] = 'gzip'
  }
  return config
})

// 响应缓存策略
const cache = new Map<string, { data: any; timestamp: number }>()

apiClient.interceptors.response.use((response) => {
  // 缓存GET请求的响应（5分钟有效期）
  if (response.config.method === 'get') {
    const cacheKey = response.config.url
    cache.set(cacheKey, {
      data: response.data,
      timestamp: Date.now(),
    })
  }
  return response
})

// 使用缓存
const getCachedData = (url: string) => {
  const cached = cache.get(url)
  if (cached && Date.now() - cached.timestamp < 5 * 60 * 1000) {
    return cached.data
  }
  return null
}
```

---

## 第九章：完整案例 - 转账功能实现

从需求到代码的完整示例，展示前面所有概念的实际应用。

**功能需求**：
1. 用户输入收款人账号和金额
2. 验证KYC等级限额
3. 发送OTP验证
4. 确认转账
5. 处理转账
6. 显示结果

### 状态管理 (Pinia Store)

```typescript
// src/features/transaction/stores/transferStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface TransferState {
  recipientId: string
  amount: number
  description: string
  status: 'idle' | 'validating' | 'otp_sent' | 'processing' | 'success' | 'failed'
  error: string | null
  otpSent: boolean
  transactionId: string | null
}

export const useTransferStore = defineStore('transfer', () => {
  const state = ref<TransferState>({
    recipientId: '',
    amount: 0,
    description: '',
    status: 'idle',
    error: null,
    otpSent: false,
    transactionId: null,
  })

  const canTransfer = computed(() => {
    return (
      state.value.recipientId &&
      state.value.amount > 0 &&
      state.value.status === 'idle'
    )
  })

  const resetForm = () => {
    state.value = {
      recipientId: '',
      amount: 0,
      description: '',
      status: 'idle',
      error: null,
      otpSent: false,
      transactionId: null,
    }
  }

  return {
    state,
    canTransfer,
    resetForm,
  }
})
```

### 组合函数 (Business Logic)

```typescript
// src/features/transaction/composables/useTransfer.ts
import { ref } from 'vue'
import { useTransferStore } from '../stores/transferStore'
import { useWalletStore } from '../../wallet/stores/walletStore'
import { useAuthStore } from '../../auth/stores/authStore'

export const useTransfer = () => {
  const transferStore = useTransferStore()
  const walletStore = useWalletStore()
  const authStore = useAuthStore()
  const otp = ref('')

  // 验证转账可行性
  const validateTransfer = async (): Promise<boolean> => {
    const { recipientId, amount } = transferStore.state

    // 1. 检查余额
    if (amount > walletStore.state.balance) {
      transferStore.state.error = '余额不足'
      return false
    }

    // 2. 检查KYC等级限额
    const kycTier = authStore.state.kycTier
    const limits: Record<string, number> = {
      'tier1': 100000,
      'tier2': 500000,
      'tier3': Infinity,
    }

    if (amount > limits[kycTier]) {
      transferStore.state.error = `您的KYC等级限制单笔转账${limits[kycTier]}`
      return false
    }

    // 3. 验证收款人
    try {
      const recipientValid = await api.validateRecipient({
        recipientId,
      })
      if (!recipientValid) {
        transferStore.state.error = '收款人账户不存在'
        return false
      }
    } catch (error) {
      transferStore.state.error = '验证收款人失败，请重试'
      return false
    }

    return true
  }

  // 请求OTP
  const sendOTP = async (): Promise<boolean> => {
    transferStore.state.status = 'validating'

    try {
      if (!(await validateTransfer())) {
        transferStore.state.status = 'idle'
        return false
      }

      // 发送OTP
      await api.sendOTP({
        transactionType: 'transfer',
        amount: transferStore.state.amount,
      })

      transferStore.state.status = 'otp_sent'
      transferStore.state.otpSent = true
      transferStore.state.error = null
      return true
    } catch (error) {
      transferStore.state.error = '发送OTP失败'
      transferStore.state.status = 'idle'
      return false
    }
  }

  // 验证OTP并处理转账
  const confirmTransfer = async (): Promise<boolean> => {
    if (!otp.value || otp.value.length !== 6) {
      transferStore.state.error = 'OTP格式不正确'
      return false
    }

    transferStore.state.status = 'processing'

    try {
      // 生成幂等性Key，防止重复
      const idempotencyKey = generateIdempotencyKey({
        recipientId: transferStore.state.recipientId,
        amount: transferStore.state.amount,
      })

      // 执行转账
      const response = await api.transfer(
        {
          recipientId: transferStore.state.recipientId,
          amount: transferStore.state.amount,
          description: transferStore.state.description,
          otp: otp.value,
        },
        {
          headers: {
            'Idempotency-Key': idempotencyKey,
          },
        }
      )

      // 乐观更新余额
      walletStore.state.balance -= transferStore.state.amount

      transferStore.state.status = 'success'
      transferStore.state.transactionId = response.transactionId
      transferStore.state.error = null

      return true
    } catch (error) {
      if (error.code === 'INVALID_OTP') {
        transferStore.state.error = 'OTP无效或已过期'
      } else if (error.code === 'INSUFFICIENT_BALANCE') {
        transferStore.state.error = '余额不足'
      } else {
        transferStore.state.error = '转账失败，请重试'
      }

      transferStore.state.status = 'failed'
      return false
    }
  }

  return {
    otp,
    sendOTP,
    confirmTransfer,
    validateTransfer,
  }
}
```

### Vue组件

```vue
<!-- src/features/transaction/pages/Transfer.vue -->
<template>
  <div class="transfer-page">
    <!-- 步骤指示器 -->
    <StepIndicator
      :current-step="currentStep"
      :steps="['输入信息', '验证OTP', '确认转账', '结果']"
    />

    <!-- 错误提示 -->
    <div v-if="transferStore.state.error" class="error-message">
      ⚠️ {{ transferStore.state.error }}
    </div>

    <!-- 步骤1: 输入收款人和金额 -->
    <form v-if="currentStep === 1" @submit.prevent="handleNext">
      <div class="form-group">
        <label for="recipient">收款人账户</label>
        <input
          id="recipient"
          v-model="transferStore.state.recipientId"
          type="text"
          placeholder="输入收款人账户或手机号"
          required
        />
      </div>

      <div class="form-group">
        <label for="amount">转账金额 (₹)</label>
        <input
          id="amount"
          v-model.number="transferStore.state.amount"
          type="number"
          placeholder="0"
          min="0"
          required
        />
        <small>可用余额: ₹{{ walletStore.state.balance }}</small>
      </div>

      <div class="form-group">
        <label for="description">转账说明 (可选)</label>
        <textarea
          id="description"
          v-model="transferStore.state.description"
          placeholder="添加备注信息"
        />
      </div>

      <button
        type="submit"
        :disabled="!transferStore.canTransfer"
        class="btn-primary"
      >
        下一步
      </button>
    </form>

    <!-- 步骤2: OTP验证 -->
    <form v-if="currentStep === 2" @submit.prevent="handleVerifyOTP">
      <div class="otp-section">
        <p>我们已向您的注册手机号发送了验证码</p>
        <div class="form-group">
          <label for="otp">验证码</label>
          <input
            id="otp"
            v-model="otp"
            type="text"
            placeholder="输入6位验证码"
            maxlength="6"
            pattern="[0-9]{6}"
            required
          />
        </div>

        <button type="submit" class="btn-primary">
          {{ transferStore.state.status === 'processing' ? '处理中...' : '验证' }}
        </button>

        <button type="button" @click="handleResendOTP" class="btn-secondary">
          重新发送 ({{ resendCountdown }}s)
        </button>
      </div>
    </form>

    <!-- 步骤3: 确认转账 -->
    <div v-if="currentStep === 3" class="confirm-section">
      <div class="summary">
        <p><strong>收款人:</strong> {{ transferStore.state.recipientId }}</p>
        <p><strong>金额:</strong> ₹{{ transferStore.state.amount }}</p>
        <p v-if="transferStore.state.description">
          <strong>说明:</strong> {{ transferStore.state.description }}
        </p>
      </div>

      <button @click="handleConfirm" class="btn-primary">
        确认转账
      </button>
      <button @click="handleCancel" class="btn-secondary">
        取消
      </button>
    </div>

    <!-- 步骤4: 结果 -->
    <div v-if="currentStep === 4" class="result-section">
      <div v-if="transferStore.state.status === 'success'" class="success">
        <div class="icon">✅</div>
        <h2>转账成功</h2>
        <p>交易ID: {{ transferStore.state.transactionId }}</p>
        <button @click="handleNewTransfer" class="btn-primary">
          进行新的转账
        </button>
      </div>

      <div v-else class="failure">
        <div class="icon">❌</div>
        <h2>转账失败</h2>
        <p>{{ transferStore.state.error }}</p>
        <button @click="handleRetry" class="btn-primary">
          重试
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTransferStore } from '../stores/transferStore'
import { useWalletStore } from '../../wallet/stores/walletStore'
import { useTransfer } from '../composables/useTransfer'

const transferStore = useTransferStore()
const walletStore = useWalletStore()
const { otp, sendOTP, confirmTransfer } = useTransfer()

const currentStep = ref(1)
const resendCountdown = ref(0)

const handleNext = async () => {
  if (!(await sendOTP())) return
  currentStep.value = 2
}

const handleVerifyOTP = async () => {
  if (await confirmTransfer()) {
    currentStep.value = 4
  }
}

const handleResendOTP = async () => {
  resendCountdown.value = 30
  const timer = setInterval(() => {
    resendCountdown.value--
    if (resendCountdown.value <= 0) clearInterval(timer)
  }, 1000)
  await sendOTP()
}

const handleConfirm = async () => {
  await confirmTransfer()
  currentStep.value = 4
}

const handleCancel = () => {
  transferStore.resetForm()
  currentStep.value = 1
}

const handleNewTransfer = () => {
  transferStore.resetForm()
  currentStep.value = 1
}

const handleRetry = () => {
  currentStep.value = 1
}
</script>

<style scoped>
.transfer-page {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group small {
  display: block;
  margin-top: 4px;
  color: #666;
}

.btn-primary,
.btn-secondary {
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  margin-right: 8px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.confirm-section,
.result-section {
  text-align: center;
}

.success,
.failure {
  padding: 40px 20px;
}

.success .icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.success h2 {
  color: #28a745;
  margin-bottom: 10px;
}

.failure .icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.failure h2 {
  color: #dc3545;
  margin-bottom: 10px;
}
</style>
```

---

## 第十章：支付系统的测试策略

### 单元测试

```typescript
// src/features/transaction/composables/__tests__/useTransfer.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useTransfer } from '../useTransfer'
import { useTransferStore } from '../../stores/transferStore'
import { useWalletStore } from '../../../wallet/stores/walletStore'

describe('useTransfer', () => {
  let transferStore: any
  let walletStore: any

  beforeEach(() => {
    vi.clearAllMocks()
    transferStore = useTransferStore()
    walletStore = useWalletStore()

    // 初始化store数据
    transferStore.state.recipientId = '9876543210'
    transferStore.state.amount = 1000
    walletStore.state.balance = 10000
  })

  it('应该验证余额充足', async () => {
    const { validateTransfer } = useTransfer()
    const result = await validateTransfer()
    expect(result).toBe(true)
  })

  it('应该拒绝余额不足的转账', async () => {
    walletStore.state.balance = 500
    const { validateTransfer } = useTransfer()
    const result = await validateTransfer()
    expect(result).toBe(false)
    expect(transferStore.state.error).toContain('余额不足')
  })

  it('应该验证KYC限额', async () => {
    transferStore.state.amount = 200000 // 超过tier1限额
    const { validateTransfer } = useTransfer()
    const result = await validateTransfer()
    expect(result).toBe(false)
    expect(transferStore.state.error).toContain('KYC等级')
  })
})
```

### E2E测试 (使用Playwright)

```typescript
// tests/e2e/transfer.spec.ts
import { test, expect } from '@playwright/test'

test.describe('转账流程', () => {
  test.beforeEach(async ({ page }) => {
    // 登录
    await page.goto('http://localhost:5173/login')
    await page.fill('input[type="text"]', 'testuser@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button:has-text("登录")')
    await page.waitForURL('http://localhost:5173/wallet')
  })

  test('完整的转账流程', async ({ page }) => {
    // 导航到转账页面
    await page.click('a:has-text("转账")')
    await expect(page).toHaveURL(/.*transfer/)

    // 步骤1: 输入收款人和金额
    await page.fill('input[placeholder*="账户"]', '9876543210')
    await page.fill('input[placeholder*="金额"]', '1000')
    await page.click('button:has-text("下一步")')

    // 步骤2: 等待OTP页面
    await expect(page.locator('text=验证码')).toBeVisible()

    // 输入OTP (模拟OTP)
    const otpInput = page.locator('input[placeholder*="验证码"]')
    await otpInput.fill('123456')
    await page.click('button:has-text("验证")')

    // 步骤3: 确认转账
    await expect(page.locator('text=确认转账')).toBeVisible()
    await page.click('button:has-text("确认转账")')

    // 步骤4: 成功提示
    await expect(page.locator('text=转账成功')).toBeVisible()
    const txId = await page.locator('text=交易ID').textContent()
    expect(txId).toMatch(/[0-9a-f]{32}/)
  })

  test('应该拒绝余额不足的转账', async ({ page }) => {
    await page.click('a:has-text("转账")')
    await page.fill('input[placeholder*="账户"]', '9876543210')
    await page.fill('input[placeholder*="金额"]', '50000') // 超过余额
    await page.click('button:has-text("下一步")')

    await expect(page.locator('text=余额不足')).toBeVisible()
  })
})
```

---

## 第十一章：生产部署清单

### 部署前的安全检查

```
☑️ 安全性检查
  ☐ 所有API请求都使用HTTPS
  ☐ 没有敏感数据在localStorage或console中
  ☐ 有效的CSP (Content Security Policy)
  ☐ X-Frame-Options设置为DENY或SAMEORIGIN
  ☐ X-Content-Type-Options设置为nosniff
  ☐ 实施CORS白名单
  ☐ 依赖包无已知漏洞 (npm audit)
  ☐ 完整的错误边界处理

☑️ 性能检查
  ☐ Lighthouse性能评分 > 90
  ☐ Bundle大小 < 500KB (gzipped)
  ☐ LCP < 2.5s
  ☐ FID < 100ms
  ☐ CLS < 0.1
  ☐ 启用了Service Worker
  ☐ 所有关键资源预加载
  ☐ 图片优化和懒加载

☑️ 可用性检查
  ☐ 离线模式可用
  ☐ 网络错误时有适当的降级方案
  ☐ 所有关键流程都有重试机制
  ☐ 用户反馈和加载状态清晰

☑️ 合规性检查
  ☐ PCI-DSS合规性审计通过
  ☐ RBI数据本地化要求满足
  ☐ GDPR隐私政策就位
  ☐ 服务条款和风险披露
  ☐ 审计日志系统完整
```

---

## 第十二章：常见问题与故障排除

### 常见问题

**Q: 如何处理支付中的网络中断？**

A: 使用离线队列（见第六章）。用户的支付请求被缓存，当网络恢复时自动重试。确保使用幂等性Key防止重复扣款。

**Q: OTP验证失败了怎么办？**

A: OTP可能过期（通常5分钟）。提供"重新发送"选项，但限制频率（如30秒冷却时间）。

**Q: 用户投诉支付被扣了两次？**

A: 检查幂等性Key实现。如果Key未正确传递，后端可能会处理重复请求。同时检查网络重试的频率。

**Q: 支付表单在低网络速度下加载缓慢？**

A: 启用Service Worker缓存，使用图片优化和代码分割（见第八章）。考虑预加载支付表单。

### 性能调试

```typescript
// 使用 Performance API 测量关键操作
const measurePaymentTime = async () => {
  const startMark = performance.now()

  try {
    await confirmTransfer()
  } finally {
    const endMark = performance.now()
    const duration = endMark - startMark

    console.log(`支付耗时: ${duration.toFixed(2)}ms`)

    // 上报到分析服务
    analytics.event('payment_duration', { duration })

    // 如果超过预期，发送告警
    if (duration > 5000) {
      alerting.warn('支付处理缓慢', { duration })
    }
  }
}
```

---

## 第十三章：总结与最佳实践

### 支付平台前端的核心要点

1. **安全第一** - PCI-DSS合规不是可选的，是必须的
2. **用户体验** - 即使在低网络条件下也要保持流畅
3. **可靠性** - 离线支持、重试机制、错误处理无处不在
4. **可维护性** - 模块化架构、清晰的状态管理、全面的测试
5. **可扩展性** - 支持新的支付方式、新的市场、新的功能

### 必读资源

- [OWASP 前端安全TOP 10](https://owasp.org/www-project-top-10/)
- [PCI DSS 要求](https://www.pcisecuritystandards.org/)
- [RBI支付系统规定](https://www.rbi.org.in/)
- [NPCI UPI标准](https://www.npci.org.in/)

### 下一步

当Claude调用这个Skill时，它将能够：

1. **初始化项目** - 使用提供的脚本生成项目结构
2. **设计架构** - 参考章节二的项目结构建议
3. **实现功能** - 查看详细的代码示例和最佳实践
4. **确保安全** - 遵循第三章的安全指南
5. **优化性能** - 应用第八章的优化策略
6. **测试和部署** - 使用脚本工具进行自动化检查

---

## 附录：关键概念速查

| 概念 | 说明 | 章节 |
|------|------|------|
| **PCI-DSS** | 支付卡产业数据安全标准 | 第三、十章 |
| **KYC** | 了解你的客户 | 第四、五章 |
| **OTP** | 一次性密码（短信验证码） | 第四、五章 |
| **幂等性** | 同样请求重复调用不变 | 第五章 |
| **状态机** | 定义有限的状态和转换 | 第四、五章 |
| **离线优先** | 假设网络离线，缓存和同步 | 第六章 |
| **乐观更新** | 先更新UI，后确认服务器 | 第五章 |
| **WebSocket** | 双向实时通信 | 第五章 |
| **Service Worker** | 浏览器后台工作进程，用于缓存 | 第六、八章 |
| **Lighthouse** | Google的网站质量审计工具 | 第八、十一章 |

---

**这是一份完整的印度支付平台前端开发指南。Claude在调用此Skill时，将具备构建生产级支付系统所需的所有知识。**
