# RBI合规性检查清单

印度央行 (Reserve Bank of India) 对支付平台的核心要求

## 1. 数据本地化要求

### 核心原则
所有客户数据（个人、财务、交易）必须存储在印度服务器上。

```typescript
// ✅ 正确: 所有敏感数据都在印度数据中心
const apiClient = axios.create({
  baseURL: 'https://payment-india.example.com', // 印度服务器
})

// ❌ 错误: 将数据发送到国外服务器
const wrongClient = axios.create({
  baseURL: 'https://payment-us.example.com', // 违反RBI规则
})

// ✅ 数据分类
interface UserData {
  // 必须本地化
  personalInfo: {
    name: string
    aadharId: string  // 印度身份证
    phone: string
    address: string
  }

  // 必须本地化
  financialData: {
    bankAccount: string
    transactions: Transaction[]
    balance: number
  }

  // 可以在国外备份副本，但主体必须在印度
  auditLogs: AuditLog[]
}
```

### 检查清单

- [ ] 所有用户PII存储在印度服务器
- [ ] 所有交易数据存储在印度服务器
- [ ] 所有支付凭证存储在印度服务器
- [ ] 备份系统位置文件化
- [ ] 有明确的数据流程图
- [ ] 数据中心合规证书就位

## 2. 加密和数据保护

### 加密标准

```typescript
// RBI要求的最低标准
const encryptionStandards = {
  // 传输层加密
  transport: {
    protocol: 'TLS 1.2+',  // 最低版本
    cipherSuite: [
      'ECDHE-RSA-AES128-GCM-SHA256',
      'ECDHE-RSA-AES256-GCM-SHA384',
    ],
  },

  // 存储层加密
  storage: {
    algorithm: 'AES-256-CBC',  // 或更强
    keyLength: 256,
  },

  // 密钥管理
  keyManagement: {
    generation: 'FIPS 140-2 approved',
    storage: 'Hardware Security Module (HSM)',
    rotation: '每12个月',
    backup: '加密备份，至少2份',
  },
}

// ✅ 实现示例
const secureTransport = {
  // HTTPS/TLS配置
  tlsConfig: {
    minVersion: 'TLSv1.2',
    maxVersion: 'TLSv1.3',
    ciphers: [
      'ECDHE-RSA-AES128-GCM-SHA256',
      'ECDHE-RSA-AES256-GCM-SHA384',
      'DHE-RSA-AES128-GCM-SHA256',
      'DHE-RSA-AES256-GCM-SHA384',
    ],
    sessionTimeout: 300, // 5分钟
  },

  // 敏感数据加密
  dataEncryption: async (data: string) => {
    const key = await getEncryptionKeyFromHSM()
    const iv = crypto.randomBytes(16)
    const cipher = crypto.createCipheriv('aes-256-cbc', key, iv)

    let encrypted = cipher.update(data, 'utf8', 'hex')
    encrypted += cipher.final('hex')

    // 返回 IV + 加密数据
    return iv.toString('hex') + ':' + encrypted
  },
}
```

### 密钥管理

```typescript
// ✅ 密钥轮换策略
interface KeyRotationPolicy {
  frequency: 'every 12 months',
  process: [
    '1. 生成新密钥',
    '2. 在HSM中存储',
    '3. 使用新密钥加密新数据',
    '4. 旧数据使用旧密钥解密后重新加密',
    '5. 安全销毁旧密钥',
  ],
  auditLog: 'detailed record of key rotation',
}

// ❌ 禁止
const badKeyManagement = {
  // 不要硬编码密钥
  apiKey: 'sk_live_abc123',  // 错误！

  // 不要在代码中存储
  masterKey: 'hardcoded_key_12345',  // 错误！

  // 不要长期使用同一密钥
  keyRotation: 'never',  // 错误！
}
```

## 3. 身份验证和授权

### KYC (了解你的客户) 要求

```typescript
// RBI要求的KYC等级
type KYCTier = 'simplified' | 'full' | 'enhanced'

interface KYCRequirements {
  simplified: {
    documents: ['PAN card 或国际护照'],
    limits: {
      singleTransaction: 100000,  // ₹1 lakh
      monthlyLimit: 500000,        // ₹5 lakh
    },
    retentionPeriod: '5 years',
  },

  full: {
    documents: [
      'Aadhaar (首选)',
      'PAN card',
      '地址证明 (电费单/水费单)',
      '职业证明',
    ],
    limits: {
      singleTransaction: 500000,   // ₹5 lakh
      monthlyLimit: 5000000,        // ₹50 lakh
    },
    retentionPeriod: '6 years',
  },

  enhanced: {
    documents: [
      'Aadhaar + 生物识别',
      'PAN card',
      '完整地址验证',
      '银行/工作证明',
      '活体检测',
    ],
    limits: {
      singleTransaction: Infinity,
      monthlyLimit: Infinity,
    },
    retentionPeriod: '10 years',
  },
}

// ✅ KYC验证流程
const kycVerificationFlow = async (userId: string) => {
  const kycData = {
    // 1. 文件上传
    documents: {
      aadhaar: 'image/verified',
      pan: 'image/verified',
      address: 'image/verified',
    },

    // 2. 生物识别验证
    biometric: {
      faceRecognition: 'passed',
      liveness: 'passed',  // 活体检测
      fingerprint: 'optional',
    },

    // 3. 服务器端验证（后端完成）
    verification: {
      documentOCR: 'passed',
      faceMatch: 'passed',
      backgroundCheck: 'passed',
    },

    // 4. KYC状态
    status: 'approved',  // 或 'pending', 'rejected'
    approvedAt: Date.now(),
    expiresAt: Date.now() + (6 * 365 * 24 * 60 * 60 * 1000), // 6年有效期
  }

  return kycData
}

// ✅ KYC重新验证
const kycReVerification = {
  // 每6年必须重新验证
  interval: 6 * 365 * 24 * 60 * 60 * 1000,

  // 如果金额或风险评分变化
  triggerOnAmountChange: 'transactions > ₹10 lakh',
  triggerOnRiskScore: 'if risk score > 0.8',
}
```

## 4. 审计日志和追踪

### 审计要求

```typescript
// ✅ 必须记录的事件
interface AuditEvent {
  // 用户认证事件
  userLogin: {
    userId: string
    timestamp: number
    ipAddress: string
    deviceId: string
    status: 'success' | 'failed'
    failureReason?: string
  },

  // 支付事件
  paymentSubmitted: {
    transactionId: string
    userId: string
    amount: number
    recipientId: string
    timestamp: number
    status: 'submitted'
  },

  paymentCompleted: {
    transactionId: string
    status: 'success' | 'failed' | 'pending'
    amount: number
    completedAt: number
    settlementId?: string
  },

  // 风险事件
  anomalyDetected: {
    userId: string
    type: string  // 'unusual_amount', 'rapid_transactions', etc
    riskScore: number
    action: 'blocked' | 'flagged' | 'allowed'
    timestamp: number
  },

  // 数据访问
  dataAccess: {
    userId: string
    dataType: string  // 'personal_info', 'payment_history', etc
    accessTime: number
    accessedBy: string
    purpose: string
  },

  // KYC更新
  kycStatusChanged: {
    userId: string
    oldStatus: string
    newStatus: string
    changedAt: number
    changedBy: string
    reason: string
  },
}

// ✅ 审计日志存储
class AuditLogger {
  // 必须存储6年以上
  async recordEvent(event: AuditEvent) {
    // 1. 加密敏感信息
    const encrypted = this.encryptSensitiveData(event)

    // 2. 写入持久化存储
    await this.persistToDatabase(encrypted)

    // 3. 不可修改的备份
    await this.backupToArchive(encrypted)

    // 4. 生成消息摘要以验证完整性
    const hash = this.calculateHash(encrypted)
    await this.storeHash(hash)
  }

  // 验证日志完整性
  async verifyIntegrity(eventId: string) {
    const event = await this.getEvent(eventId)
    const storedHash = await this.getHash(eventId)
    const calculatedHash = this.calculateHash(event)

    return storedHash === calculatedHash
  }
}
```

## 5. 风险管理和反欺诈

### AML/KYC合规

```typescript
// RBI要求的风险管理
interface RiskManagementFramework {
  // 1. 交易监控
  transactionMonitoring: {
    // 检测异常交易模式
    frequencyCheck: 'alert if > 5 transactions/hour',
    amountCheck: 'alert if amount > ₹10 lakh',
    velocityCheck: 'alert if amount > 3x average',

    // 可疑交易报告 (STR)
    suspiciousTransaction: {
      report: 'within 7 days to FIU',
      format: 'XBRL XML format',
      // 不通知用户（RBI规定）
    },
  },

  // 2. 风险评分
  riskScoring: {
    factors: [
      'transaction_amount',
      'transaction_frequency',
      'new_recipient',
      'geographic_anomaly',
      'device_change',
      'time_of_day',
      'deviation_from_pattern',
    ],
    threshold: {
      low: '< 0.3',
      medium: '0.3 - 0.7',
      high: '> 0.7',  // 需要额外验证
    },
  },

  // 3. 黑名单检查
  blocklistCheck: {
    // 检查OFAC、UN制裁等
    sources: [
      'OFAC SDN',
      'UN Consolidated List',
      'EU Consolidated List',
      'UK Office of Financial Sanctions',
    ],
    frequency: 'every transaction',
  },
}

// ✅ 风险评分实现
const calculateRiskScore = async (transaction: Transaction) => {
  let score = 0

  // 异常金额
  const avgAmount = await getUserAverageTransactionAmount()
  if (transaction.amount > avgAmount * 3) {
    score += 0.3
  }

  // 新收款人
  const isNewRecipient = !await isFrequentRecipient(transaction.recipientId)
  if (isNewRecipient) {
    score += 0.2
  }

  // 快速交易
  const recentTransactions = await getRecentTransactions(7) // 7天内
  if (recentTransactions.length > 5) {
    score += 0.2
  }

  // 地理异常
  const location = await getUserLocation()
  if (location !== getUserPreviousLocation()) {
    score += 0.1
  }

  // 异常时间
  const hour = new Date().getHours()
  if (hour < 6 || hour > 22) {
    score += 0.1
  }

  return Math.min(score, 1.0) // Cap at 1.0

  // 如果score > 0.7，需要步进式认证
  if (score > 0.7) {
    await requireStepupAuthentication()
  }
}
```

## 6. 通知和披露

### 必须提供的信息

```typescript
// ✅ 用户必须同意的条款
const mandatoryDisclosures = {
  // 1. 条款和条件
  termsAndConditions: 'user must explicitly accept',

  // 2. 隐私政策
  privacyPolicy: {
    content: 'explain data collection and usage',
    languages: 'in regional languages',
    updates: 'notify user within 7 days of change',
  },

  // 3. 收费和费率
  chargesAndRates: {
    transactionFees: 'clearly displayed',
    interestRates: 'if applicable',
    penalties: 'clearly mentioned',
    updateFrequency: 'notify 30 days before',
  },

  // 4. 风险披露
  riskDisclosure: {
    transactionRisk: 'explain potential risks',
    counterpartyRisk: 'explain if applicable',
    technologyRisk: 'explain outage risks',
  },

  // 5. 投诉流程
  complaintRedressal: {
    channel: 'provide multiple channels',
    sla: '7 days for acknowledgment',
    escalation: 'if unresolved in 30 days',
  },
}

// ✅ 必须在支付前显示
const paymentDisclosure = {
  // 1. 收款人详情
  recipientDetails: 'confirm recipient name & account',

  // 2. 交易金额
  transactionAmount: 'clearly show amount in INR',

  // 3. 费用
  charges: 'show applicable fees',

  // 4. 总金额
  totalAmount: 'show total debit from account',

  // 5. 处理时间
  processingTime: 'show expected settlement time',

  // 6. 确认步骤
  confirmation: 'require explicit user confirmation',
}
```

## 7. 故障和中断处理

### 可用性要求

```typescript
// RBI要求的可用性标准
const availabilityRequirements = {
  // 支付服务可用性
  paymentService: {
    targetUptime: '99.9%',  // 年度可用性
    maxDowntime: '43 分钟/年',
    maintenance: 'non-critical hours only',
  },

  // 故障通知
  failureNotification: {
    notifyWithin: '30 分钟',
    notifyVia: ['website', 'email', 'SMS'],
    includeDetails: 'scope and expected resolution time',
  },

  // 恢复要求
  failureRecovery: {
    rto: '4 hours',  // Recovery Time Objective
    rpo: '1 hour',   // Recovery Point Objective
    backup: 'geographic redundancy required',
  },
}

// ✅ 故障处理流程
const failureHandling = {
  // 1. 故障检测
  detection: {
    healthCheck: 'every 60 seconds',
    alertThreshold: 'if > 10% requests fail',
  },

  // 2. 故障升级
  escalation: {
    p1: 'immediate alerting',
    p2: 'within 15 minutes',
    p3: 'within 1 hour',
  },

  // 3. 用户通知
  userNotification: {
    timing: 'within 30 minutes',
    channels: ['SMS', 'email', 'push notification', 'website banner'],
  },

  // 4. 恢复验证
  recoveryVerification: {
    testing: 'test recovery procedure quarterly',
    documentation: 'maintain recovery playbooks',
  },
}
```

## 8. 定期合规检查

### 实施清单

```typescript
// 月度检查
const monthlyCompliance = {
  items: [
    '[ ] 审计日志完整性验证',
    '[ ] 关键风险事件回顾',
    '[ ] KYC更新统计',
    '[ ] 系统可用性监控',
    '[ ] 安全补丁应用状态',
    '[ ] 数据备份完整性检查',
  ],
}

// 季度审查
const quarterlyCompliance = {
  items: [
    '[ ] 完整安全审计',
    '[ ] 风险评估更新',
    '[ ] 合规政策回顾',
    '[ ] 员工培训验证',
    '[ ] 第三方审计',
    '[ ] 用户反馈分析',
  ],
}

// 年度审计
const annualCompliance = {
  items: [
    '[ ] 完整合规审计',
    '[ ] 外部审计师评估',
    '[ ] 管理委员会报告',
    '[ ] 政策和程序更新',
    '[ ] 系统功能增强评估',
    '[ ] RBI通函遵守情况',
  ],
}
```

## 常见违规及罚款

| 违规项 | 罚款范围 | 说明 |
|--------|---------|------|
| 未能本地化数据 | ₹50-100 lakh | 最严重的违规 |
| KYC不完整 | ₹10-25 lakh | 根据级别 |
| 审计日志缺失 | ₹5-15 lakh | 追溯6年 |
| AML合规失败 | ₹25-75 lakh | 可能吊销许可证 |
| 未及时报告故障 | ₹1-10 lakh | 根据影响范围 |
| 数据安全漏洞 | ₹50+ lakh | 严重影响下 |

## 相关法规

- **RBI通函 – 2021年8月** (关于支付平台的安全要求)
- **RBI通函 – 2019年11月** (关于数据本地化)
- **NPCI UPI标准** (统一支付接口)
- **Payment and Settlement Systems Act, 2007**
- **Prevention of Money Laundering Act (PMLA), 2002**
- **Aadhaar (Targeted Delivery of Financial and Other Subsidies, Benefits and Services) Act, 2016**

---

**定期更新本清单，确保与最新RBI规定保持一致。**

最后更新: 2024年11月
