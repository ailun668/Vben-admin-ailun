# 支付状态机设计

## 概述

支付系统的核心是一个精心设计的**状态机**，确保交易的每一步都可控且可追踪。

## 支付流程状态机

```
┌─────────────────────────────────────────────────────────────────┐
│                    支付交易完整状态机                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  START                                                            │
│   │                                                               │
│   ├─ (用户输入金额、收款人)                                      │
│   │                                                               │
│   ▼                                                               │
│  [IDLE] ◀─────────────── (超时、用户取消)                        │
│   │                                                               │
│   │  submitPayment()                                             │
│   ▼                                                               │
│  [VALIDATING]                                                     │
│   │                                                               │
│   ├─ 验证余额: balance >= amount                                │
│   ├─ 验证KYC等级: kyc_tier allows amount                        │
│   ├─ 验证收款人: recipient_id exists & not blocked             │
│   ├─ 验证限制: transaction_count < daily_limit                 │
│   │                                                               │
│   ├─ ✅ ALL PASS ──────────────────────┐                        │
│   │                                    ▼                         │
│   │                                [OTP_PENDING]                │
│   │                                    │                         │
│   │                                    ├─ sendOTP()             │
│   │                                    ├─ 等待用户输入OTP        │
│   │                                    │                         │
│   │                                    ├─ verifyOTP()           │
│   │                                    │                         │
│   │                                    ├─ ✅ OTP正确 ──────┐    │
│   │                                    │                   ▼    │
│   │                                    │              [PROCESSING]
│   │                                    │                   │    │
│   │                                    │  ❌ OTP错误/过期 ──┤   │
│   │                                    │                   │   │
│   │                                    └─────────────┬─────┘   │
│   │                                                 │           │
│   └──── ❌ VALIDATION FAIL ─────────────────────────┤           │
│                                                     ▼           │
│                                                  [FAILED]       │
│                                                     │           │
│                                        (返回错误提示，可重试)    │
│                                                     │           │
│                                        (5分钟后自动清除)        │
│                                                     ▼           │
│                                                  [IDLE]         │
│                                                                 │
│  [PROCESSING] 处理中                                            │
│   │                                                             │
│   ├─ callPaymentAPI() with Idempotency-Key                    │
│   ├─ waitForBackendConfirm() (超时5分钟)                       │
│   ├─ 重试逻辑: 最多3次                                          │
│   │                                                             │
│   ├─ ✅ SUCCESS ─────────────┐                                 │
│   │                          ▼                                  │
│   │                      [SUCCESS]                             │
│   │                          │                                  │
│   │                  (更新余额、发送通知)                        │
│   │                          │                                  │
│   │                  (5分钟后可新建)                            │
│   │                                                             │
│   └─ ❌ FAILURE ─────────────┐                                 │
│                              ▼                                  │
│                          [FAILED]                              │
│                              │                                  │
│                  (显示错误原因、建议重试)                        │
│                              │                                  │
│                  (5分钟后可重新开始)                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 状态定义

### IDLE (空闲)
- **描述**: 初始状态，等待用户输入
- **操作**: 用户可以输入收款人和金额
- **触发转换**: `submitPayment()` 转向 VALIDATING
- **超时**: 无（用户可以停留在此状态）

### VALIDATING (验证中)
- **描述**: 验证支付的可行性
- **检查项**:
  ```typescript
  {
    余额检查: balance >= amount,
    KYC限额: kycTier_limit >= amount,
    收款人有效: recipient.status === 'active',
    日交易限额: dailyTransactionCount < limit,
    冷却期: lastTransactionTime + cooldown_ms < now(),
  }
  ```
- **成功**: 转向 OTP_PENDING
- **失败**: 转向 FAILED，显示错误信息
- **超时**: 30秒（自动失败）

### OTP_PENDING (OTP待验证)
- **描述**: 等待用户输入OTP验证码
- **OTP**:
  - 生成新OTP（6位数字）
  - 发送到注册手机号
  - 有效期: 5分钟
  - 最多允许3次错误尝试
- **成功**: 转向 PROCESSING
- **失败**: 返回错误提示，可重新请求OTP
- **超时**: 5分钟无输入，自动失败

### PROCESSING (处理中)
- **描述**: 向后端提交支付请求
- **操作**:
  ```typescript
  {
    发送加密请求: encryptPaymentData(),
    包含幂等性Key: Idempotency-Key header,
    等待后端响应: 5分钟超时,
    自动重试: 最多3次 (间隔10秒),
  }
  ```
- **成功**: 转向 SUCCESS
- **失败**: 转向 FAILED
- **超时**: 5分钟，显示"处理中..."

### SUCCESS (成功)
- **描述**: 支付已成功完成
- **操作**:
  ```typescript
  {
    更新本地余额: optimistic update confirm,
    保存交易记录: save to local db,
    发送通知: push notification,
    记录到服务器: audit log,
  }
  ```
- **显示**: 成功提示，显示交易ID
- **下一步**: 可返回钱包或进行新交易
- **自动清除**: 5分钟后从历史中清除待处理

### FAILED (失败)
- **描述**: 支付失败或被拒绝
- **原因**:
  - 余额不足
  - KYC限额不足
  - OTP失败
  - 后端拒绝（风险控制）
  - 网络超时
- **显示**: 显示具体错误原因和建议
- **下一步**: 允许用户重试或返回
- **清除**: 5分钟后可发起新支付

## 状态转换表

| 当前状态 | 触发条件 | 下一状态 | 备注 |
|---------|--------|--------|------|
| IDLE | submitPayment() | VALIDATING | 用户点击"下一步" |
| VALIDATING | ✅ 所有检查通过 | OTP_PENDING | 发送OTP |
| VALIDATING | ❌ 检查失败 | FAILED | 显示错误 |
| VALIDATING | ⏱️ 30秒超时 | FAILED | 自动失败 |
| OTP_PENDING | verifyOTP(正确) | PROCESSING | 开始支付 |
| OTP_PENDING | verifyOTP(错误) | OTP_PENDING | 显示错误，可重试 |
| OTP_PENDING | 3次失败 | FAILED | 锁定OTP |
| OTP_PENDING | 5分钟无操作 | FAILED | 自动超时 |
| PROCESSING | 后端确认✅ | SUCCESS | 交易成功 |
| PROCESSING | 后端拒绝❌ | FAILED | 显示原因 |
| PROCESSING | 5分钟无响应 | FAILED | 网络超时 |
| SUCCESS | 用户确认 | IDLE | 返回钱包 |
| FAILED | 用户重试 | IDLE | 重新开始 |
| FAILED | 用户取消 | IDLE | 返回主页 |

## 实现示例

### TypeScript状态机

```typescript
// src/infrastructure/state-machine/paymentStateMachine.ts

type PaymentState =
  | 'idle'
  | 'validating'
  | 'otp_pending'
  | 'processing'
  | 'success'
  | 'failed'

interface PaymentContext {
  recipientId?: string
  amount?: number
  otpSent: boolean
  otpAttempts: number
  processingAttempts: number
  error?: string
  transactionId?: string
  timestamp: number
}

class PaymentStateMachine {
  private state: PaymentState = 'idle'
  private context: PaymentContext = {
    otpSent: false,
    otpAttempts: 0,
    processingAttempts: 0,
    timestamp: Date.now(),
  }

  // 合法的状态转换
  private transitions = {
    idle: ['validating'],
    validating: ['otp_pending', 'failed'],
    otp_pending: ['processing', 'failed'],
    processing: ['success', 'failed'],
    success: ['idle'],
    failed: ['idle'],
  }

  // 状态的守卫条件
  private guards = {
    validating: async (amount: number) => {
      const balance = await getBalance()
      const kyc = await getKYCTier()
      const recipient = await validateRecipient(this.context.recipientId)

      return (
        balance >= amount &&
        getKYCLimit(kyc) >= amount &&
        recipient.status === 'active'
      )
    },

    otp_pending: async () => {
      return this.context.otpSent === true
    },

    processing: async () => {
      return (
        this.context.otpAttempts < 3 &&
        Date.now() - this.context.timestamp < 5 * 60 * 1000
      )
    },
  }

  canTransition(toState: PaymentState): boolean {
    return this.transitions[this.state]?.includes(toState) ?? false
  }

  async transition(toState: PaymentState): Promise<boolean> {
    // 检查转换合法性
    if (!this.canTransition(toState)) {
      throw new Error(
        `Cannot transition from ${this.state} to ${toState}`
      )
    }

    // 执行守卫
    const guard = this.guards[toState]
    if (guard && !(await guard())) {
      throw new Error(`Guard failed for state ${toState}`)
    }

    // 执行转换前的hook
    await this.onExitState(this.state)

    // 更新状态
    this.state = toState

    // 执行转换后的hook
    await this.onEnterState(toState)

    return true
  }

  private async onExitState(state: PaymentState) {
    // 离开状态时的清理
    switch (state) {
      case 'processing':
        await this.cancelProcessing()
        break
    }
  }

  private async onEnterState(state: PaymentState) {
    // 进入状态时的初始化
    switch (state) {
      case 'otp_pending':
        await this.sendOTP()
        break
      case 'processing':
        this.context.processingAttempts = 0
        await this.processPayment()
        break
    }
  }

  getState(): PaymentState {
    return this.state
  }

  getContext(): PaymentContext {
    return this.context
  }

  private async sendOTP() {
    // 发送OTP逻辑
    this.context.otpSent = true
    this.context.timestamp = Date.now()
  }

  private async processPayment() {
    // 处理支付逻辑
  }

  private async cancelProcessing() {
    // 取消处理逻辑
  }
}
```

## 风险控制集成

状态机与风险控制系统的集成：

```typescript
interface RiskCheckResult {
  allowed: boolean
  score: number
  reason?: string
  flags: string[]
}

// 在VALIDATING状态添加风险检查
private async validatePayment(): Promise<boolean> {
  const riskResult = await riskDetection.evaluate({
    userId: this.context.userId,
    amount: this.context.amount,
    recipientId: this.context.recipientId,
    deviceId: getDeviceId(),
    location: await getLocation(),
  })

  if (!riskResult.allowed) {
    this.context.error = `支付被安全系统拒绝: ${riskResult.reason}`
    return false
  }

  // 高风险提示但允许
  if (riskResult.score > 0.7) {
    await promptUserConfirmation(
      `检测到异常活动，是否继续? 风险评分: ${(riskResult.score * 100).toFixed(0)}%`
    )
  }

  return true
}
```

## 幂等性与重试

防止重复支付：

```typescript
// 在PROCESSING状态使用幂等性Key
const idempotencyKey = generateIdempotencyKey({
  userId: currentUser.id,
  recipientId: this.context.recipientId,
  amount: this.context.amount,
  timestamp: this.context.timestamp,
})

const response = await api.payment(
  {
    recipientId: this.context.recipientId,
    amount: this.context.amount,
  },
  {
    headers: {
      'Idempotency-Key': idempotencyKey,
    },
  }
)

// 后端保证相同Key的请求只处理一次
// 重试时使用相同的Key，后端返回缓存结果
```

## 网络中断处理

支付中断网络时的状态转移：

```typescript
// 检测网络状态
window.addEventListener('offline', async () => {
  if (this.state === 'processing') {
    // 保存当前状态到本地
    saveToLocalStorage('payment_state', {
      state: this.state,
      context: this.context,
      idempotencyKey: this.idempotencyKey,
    })

    // 显示"正在重试..."
    showMessage('网络中断，支付已离线保存，恢复连接后自动重试')
  }
})

window.addEventListener('online', async () => {
  // 恢复支付
  const saved = getFromLocalStorage('payment_state')
  if (saved && saved.state === 'processing') {
    await this.resumePayment(saved)
  }
})
```

## 测试场景

### 单元测试

```typescript
describe('PaymentStateMachine', () => {
  it('should transition from idle to validating', async () => {
    const sm = new PaymentStateMachine()
    await sm.transition('validating')
    expect(sm.getState()).toBe('validating')
  })

  it('should reject invalid transitions', () => {
    const sm = new PaymentStateMachine()
    expect(() => sm.transition('success')).toThrow()
  })

  it('should call guard before transition', async () => {
    const sm = new PaymentStateMachine()
    // 模拟guard失败
    vi.mock('balance', 0) // 余额为0
    await expect(sm.transition('otp_pending')).rejects.toThrow()
  })
})
```

## 监控和日志

每个状态转换都应该被记录：

```typescript
private async logStateTransition(
  from: PaymentState,
  to: PaymentState,
  success: boolean
) {
  await auditLog.record({
    type: 'state_transition',
    from,
    to,
    success,
    context: {
      amount: this.context.amount,
      recipientId: this.context.recipientId,
    },
    timestamp: Date.now(),
  })
}
```

---

支付状态机的设计确保了每一笔交易都能被精确控制和追踪，这是支付系统的核心。
