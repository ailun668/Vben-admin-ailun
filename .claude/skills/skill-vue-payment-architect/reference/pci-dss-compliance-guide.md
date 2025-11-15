# PCI-DSS合规指南

支付卡产业数据安全标准 (PCI Data Security Standard)

## 概述

PCI-DSS是由主要信用卡品牌(Visa、Mastercard、American Express等)制定的全球性标准。任何处理、存储或传输支付卡数据的组织都必须遵守。

## 支付平台的PCI-DSS关键需求

### 1. 建立和维护安全网络

#### 1.1 安装和维护防火墙配置
```
前端要求:
❌ 不要处理原始卡号
✅ 使用Token化: 向支付网关请求Token，存储Token而不是卡号
✅ 使用第三方服务: Stripe, Square等处理卡数据

前端示例:
// ❌ 错误
const processPayment = (cardNumber, cvv) => {
  sendToBackend({ cardNumber, cvv })
}

// ✅ 正确
const processPayment = async (cardNumber, cvv) => {
  // 1. 向Stripe API发送卡数据（使用HTTPS）
  const { token } = await stripe.createToken({
    number: cardNumber,
    cvc: cvv,
  })

  // 2. 只发送Token给后端
  sendToBackend({ token })
}
```

#### 1.2 不使用供应商提供的默认密码
```typescript
// ❌ 错误
axios.defaults.headers.common['Authorization'] = 'Basic admin:admin'

// ✅ 正确
const apiKey = process.env.NUXT_PUBLIC_API_KEY // 从环境变量获取
axios.defaults.headers.common['Authorization'] = `Bearer ${apiKey}`
```

### 2. 不存储敏感身份验证数据

这是PCI-DSS中最关键的要求。

#### 2.1 永远不存储

```typescript
// ❌ 严禁：这些数据永远不应该出现在前端
const NEVER_STORE = {
  cardNumber: '4532-1234-5678-9010',        // 卡号
  cvv: '123',                                // CVV/CVC
  trackData: '[track data]',                 // 磁条数据
  pin: '1234',                               // PIN
  otp: '654321',                             // 一次性密码
  password: 'secret123',                     // 密码
}

// ❌ 也不要存储在localStorage/sessionStorage
localStorage.setItem('cardData', JSON.stringify(cardData))
sessionStorage.setItem('pin', pin)

// ❌ 也不要存储在日志中
console.log('Card data:', cardData)
```

#### 2.2 可以安全存储的数据

```typescript
// ✅ 这些数据可以在前端存储
const SAFE_TO_STORE = {
  token: 'tok_visa_4242424242424242',      // Payment token
  last4: '4242',                            // 卡号最后4位
  brand: 'visa',                            // 卡种
  expiryMonth: 12,                          // 过期月份
  expiryYear: 2025,                         // 过期年份
  authToken: 'eyJhbGc...',                  // 认证Token
  userId: 'user_12345',                     // 用户ID
}

// ✅ 存储在localStorage中
localStorage.setItem('paymentToken', SAFE_TO_STORE.token)
```

### 3. 保护已存储的持卡人数据

#### 3.1 数据加密

```typescript
// ✅ 加密任何敏感数据（如果必须存储）
import CryptoJS from 'crypto-js'

const encryptPaymentToken = (token: string): string => {
  const secretKey = process.env.NUXT_PUBLIC_ENCRYPTION_KEY
  return CryptoJS.AES.encrypt(token, secretKey).toString()
}

const decryptPaymentToken = (encrypted: string): string => {
  const secretKey = process.env.NUXT_PUBLIC_ENCRYPTION_KEY
  const bytes = CryptoJS.AES.decrypt(encrypted, secretKey)
  return bytes.toString(CryptoJS.enc.Utf8)
}

// ✅ 使用Web Crypto API（更安全）
const encryptWithWebCrypto = async (
  data: string,
  key: CryptoKey
): Promise<string> => {
  const iv = window.crypto.getRandomValues(new Uint8Array(12))
  const encoded = new TextEncoder().encode(data)

  const encrypted = await window.crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    encoded
  )

  // 返回 IV + 密文
  const combined = new Uint8Array(iv.length + encrypted.byteLength)
  combined.set(iv, 0)
  combined.set(new Uint8Array(encrypted), iv.length)

  return btoa(String.fromCharCode(...combined))
}
```

#### 3.2 访问控制

```typescript
// ✅ 仅在需要时访问敏感数据
const getPaymentToken = async (userId: string): Promise<string | null> => {
  // 验证当前用户
  const currentUser = await auth.getCurrentUser()
  if (currentUser.id !== userId) {
    throw new Error('Unauthorized access')
  }

  // 从安全位置获取
  return getFromSecureStorage(userId)
}
```

### 4. 通过公网传输时加密持卡人数据

#### 4.1 HTTPS/TLS要求

```typescript
// ✅ 所有支付请求必须使用HTTPS
const paymentClient = axios.create({
  baseURL: 'https://api.payment.example.com', // 注意: https
  timeout: 5000,
})

// ❌ 禁止使用HTTP
const badClient = axios.create({
  baseURL: 'http://api.payment.example.com', // 错误！
})

// ✅ 配置TLS版本
const httpsAgent = new https.Agent({
  minVersion: 'TLSv1.2',
  maxVersion: 'TLSv1.3',
  ciphers: [
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES256-GCM-SHA384',
  ],
})

const secureClient = axios.create({
  httpsAgent,
})
```

#### 4.2 证书验证

```typescript
// ✅ 验证服务器证书
const https = require('https')

const agent = new https.Agent({
  rejectUnauthorized: true, // 拒绝无效证书
  ca: [fs.readFileSync('/path/to/ca-cert.pem')], // 服务器CA
})

// ✅ 检查证书固定 (Certificate Pinning)
const verifyServerCertificate = (cert: any): boolean => {
  const expectedFingerprint = '4a5c1d3f2b8e9a0c7d6e5f4a3b2c1d0e'
  const actualFingerprint = crypto
    .createHash('sha256')
    .update(cert.public_key)
    .digest('hex')

  return actualFingerprint === expectedFingerprint
}
```

### 5. 使用和定期更新防病毒软件

在浏览器层面的防护：

```typescript
// ✅ 使用CSP (Content Security Policy) 防止注入
<meta
  http-equiv="Content-Security-Policy"
  content="
    default-src 'self';
    script-src 'self' 'unsafe-inline' api.payment.example.com;
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    connect-src 'self' https://api.payment.example.com;
    frame-src 'none';
    base-uri 'self';
    form-action 'self';
  "
/>

// ✅ 防XSS
// Vue自动转义HTML
<template>
  <div>{{ userInput }}</div> <!-- 自动转义 -->
</template>

// ✅ 避免innerHTML
// ❌ 错误
document.getElementById('payment-form').innerHTML = userInput

// ✅ 正确
const div = document.createElement('div')
div.textContent = userInput
```

### 6. 维护和实现安全的应用程序

#### 6.1 输入验证

```typescript
// ✅ 验证所有输入
const validatePaymentInput = (data: any): boolean => {
  // 金额验证
  if (!Number.isInteger(data.amount) || data.amount <= 0) {
    throw new Error('Invalid amount')
  }

  // 收款人ID验证
  if (!isValidRecipientId(data.recipientId)) {
    throw new Error('Invalid recipient ID')
  }

  // 卡号验证（Luhn算法）
  if (!isValidCardNumber(data.cardNumber)) {
    throw new Error('Invalid card number')
  }

  return true
}

// ✅ 白名单验证
const ALLOWED_CURRENCIES = ['INR', 'USD', 'EUR']
const validateCurrency = (currency: string): boolean => {
  return ALLOWED_CURRENCIES.includes(currency)
}
```

#### 6.2 错误处理（不暴露敏感信息）

```typescript
// ❌ 错误的做法
try {
  processPayment(cardData)
} catch (error) {
  console.error('Payment failed:', error.message) // 可能暴露信息
  alert(`Payment failed: Card number is invalid`) // 暴露正在使用的字段
}

// ✅ 正确的做法
try {
  processPayment(cardData)
} catch (error) {
  // 记录详细错误到服务器日志（不记录敏感数据）
  auditLog.error('Payment processing failed', {
    errorCode: 'PAYMENT_FAILED',
    // 不记录: cardNumber, cvv, 等
  })

  // 显示通用错误给用户
  alert('Payment failed. Please try again or contact support.')
}
```

### 7. 限制访问持卡人数据

#### 7.1 最小权限原则

```typescript
// ✅ 仅在需要时访问
const processPayment = async (token: string) => {
  // 只需要token，不需要卡号
  const response = await api.payment({ token })
  return response
}

// ✅ 基于角色的访问控制
const canAccessPaymentHistory = (user: User): boolean => {
  return (
    user.role === 'admin' ||
    user.role === 'finance' ||
    (user.role === 'customer' && user.id === currentUser.id)
  )
}

const PaymentHistory = (props: { userId: string }) => {
  const currentUser = useAuthStore().state
  const canAccess = canAccessPaymentHistory(currentUser)

  if (!canAccess) {
    return <div>Access Denied</div>
  }

  return <HistoryList userId={props.userId} />
}
```

### 8. 识别和分配访问ID

每个用户都应该有唯一的ID：

```typescript
// ✅ 每个操作都与用户关联
const submitPayment = async (paymentData: any) => {
  const user = await auth.getCurrentUser()

  await auditLog.record({
    userId: user.id,              // 唯一用户ID
    action: 'payment_submitted',
    timestamp: Date.now(),
    ipAddress: getClientIpAddress(), // 来源IP
    userAgent: navigator.userAgent,   // 设备信息
  })
}
```

### 9. 限制对网络资源的物理和逻辑访问

前端安全：

```typescript
// ✅ 使用HTTPS保护传输
// ✅ 禁用第三方Cookie
<meta http-equiv="Set-Cookie" content="SameSite=Strict" />

// ✅ 启用Secure标志
document.cookie = `sessionToken=${token}; Secure; HttpOnly; SameSite=Strict`

// ✅ 防点击劫持
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta http-equiv="X-Frame-Options" content="DENY" />

// ✅ 禁用缓存敏感页面
<meta http-equiv="Cache-Control" content="no-store, no-cache, must-revalidate" />
```

### 10. 跟踪和监控网络访问

#### 10.1 审计日志

```typescript
// ✅ 记录所有关键操作
const auditLog = {
  async record(event: AuditEvent) {
    // 不记录敏感数据
    const sanitized = {
      userId: event.userId,
      action: event.action,
      timestamp: event.timestamp,
      status: event.status,
      // 不记录: cardNumber, password, token等
    }

    // 发送到后端审计系统
    await fetch('/api/audit-logs', {
      method: 'POST',
      body: JSON.stringify(sanitized),
      headers: { 'Content-Type': 'application/json' },
    })
  },
}

// 使用
auditLog.record({
  userId: 'user_123',
  action: 'payment_submitted',
  timestamp: Date.now(),
  status: 'success',
})
```

#### 10.2 监控异常

```typescript
// ✅ 检测异常支付活动
const detectAnomalies = async (paymentData: PaymentData) => {
  const user = await getUserWithHistory(paymentData.userId)

  const anomalies = []

  // 异常1: 短时间内多个支付
  if (
    user.recentPayments.filter(p => Date.now() - p.timestamp < 60000)
      .length > 3
  ) {
    anomalies.push('Multiple payments in short time')
  }

  // 异常2: 异常大金额
  if (
    paymentData.amount >
    user.averagePaymentAmount * 5
  ) {
    anomalies.push('Unusual large amount')
  }

  // 异常3: 新收款人
  if (!user.frequentRecipients.includes(paymentData.recipientId)) {
    anomalies.push('New recipient')
  }

  if (anomalies.length > 0) {
    // 触发额外验证
    await requireStepupAuthentication()
  }
}
```

## PCI-DSS合规检查清单

### 网络安全
- [ ] 防火墙配置完整
- [ ] 所有密码已更改默认值
- [ ] 禁用不必要的端口
- [ ] 已配置入侵检测系统

### 数据保护
- [ ] 所有敏感数据都已加密
- [ ] 无敏感数据在日志中
- [ ] TLS 1.2+用于所有传输
- [ ] 强加密算法 (AES-256等)

### 访问控制
- [ ] 每个用户有唯一ID
- [ ] 实施最小权限原则
- [ ] 定期审核访问权限
- [ ] 强密码策略

### 测试和监控
- [ ] 定期进行安全测试
- [ ] 有审计日志系统
- [ ] 能追踪所有访问
- [ ] 监控异常活动
- [ ] 有事件响应流程

### 维护
- [ ] 依赖包定期更新
- [ ] 安全补丁及时应用
- [ ] 定期安全审计
- [ ] 员工安全培训

## 印度特定要求

### RBI (印度央行) 要求
- ✅ 数据本地化: 所有用户数据存储在印度
- ✅ 加密强度: AES-256
- ✅ 审计日志: 至少保留6年

### NPCI (国家支付公司) 要求
- ✅ UPI安全标准
- ✅ Token化处理
- ✅ 两因素认证强制

## 常见错误

| 错误 | 风险 | 修正 |
|------|------|------|
| 在localStorage存储卡号 | CRITICAL | 只存储Token，卡号由支付网关处理 |
| console.log(cardData) | CRITICAL | 移除所有敏感数据日志 |
| 使用HTTP | HIGH | 始终使用HTTPS |
| 硬编码API密钥 | HIGH | 使用环境变量 |
| 在前端验证密码 | MEDIUM | 后端验证，前端只显示错误 |
| 过宽CORS配置 | HIGH | 指定具体的允许源 |

---

**遵守PCI-DSS不仅是法律要求，更重要的是保护用户的财务安全。**
