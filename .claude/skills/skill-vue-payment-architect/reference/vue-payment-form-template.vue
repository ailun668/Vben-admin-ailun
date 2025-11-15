<template>
  <div class="payment-form-container">
    <!-- 错误提示 -->
    <div v-if="error" class="alert alert-danger" role="alert">
      <span class="alert-icon">⚠️</span>
      <span class="alert-text">{{ error }}</span>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p>处理支付中...</p>
    </div>

    <!-- 支付表单（仅在非加载状态下显示） -->
    <form v-if="!isLoading" @submit.prevent="handleSubmit" class="payment-form">
      <!-- 步骤1: 基本信息 -->
      <fieldset v-if="currentStep === 'basic'" class="form-section">
        <legend class="section-title">支付信息</legend>

        <!-- 金额输入 -->
        <div class="form-group">
          <label for="amount" class="form-label">
            金额 <span class="required">*</span>
          </label>
          <div class="input-wrapper">
            <span class="currency-symbol">₹</span>
            <input
              id="amount"
              v-model.number="formData.amount"
              type="number"
              class="form-input amount-input"
              placeholder="0.00"
              min="0.01"
              step="0.01"
              max="999999.99"
              :disabled="isProcessing"
              @blur="validateAmount"
              required
            />
          </div>
          <small v-if="availableBalance" class="help-text">
            可用余额: ₹{{ formatCurrency(availableBalance) }}
          </small>
          <small v-if="amountError" class="error-text">
            {{ amountError }}
          </small>
        </div>

        <!-- 收款人信息 -->
        <div class="form-group">
          <label for="recipient" class="form-label">
            收款人账户 <span class="required">*</span>
          </label>
          <input
            id="recipient"
            v-model.trim="formData.recipientId"
            type="text"
            class="form-input"
            placeholder="手机号或账户ID"
            :disabled="isProcessing"
            @blur="validateRecipient"
            required
          />
          <small v-if="recipientError" class="error-text">
            {{ recipientError }}
          </small>
        </div>

        <!-- 转账说明（可选） -->
        <div class="form-group">
          <label for="description" class="form-label">
            转账说明 <span class="optional">(可选)</span>
          </label>
          <textarea
            id="description"
            v-model="formData.description"
            class="form-input textarea"
            placeholder="添加备注信息（仅自己可见）"
            maxlength="100"
            :disabled="isProcessing"
            rows="3"
          />
          <small class="help-text">
            {{ formData.description.length }}/100
          </small>
        </div>

        <!-- 确认按钮 -->
        <div class="form-actions">
          <button
            type="button"
            class="btn btn-secondary"
            @click="resetForm"
            :disabled="isProcessing"
          >
            清除
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="!canProceed || isProcessing"
          >
            下一步
          </button>
        </div>
      </fieldset>

      <!-- 步骤2: 确认信息 -->
      <fieldset v-if="currentStep === 'confirm'" class="form-section">
        <legend class="section-title">确认交易信息</legend>

        <div class="summary-item">
          <span class="summary-label">金额:</span>
          <span class="summary-value">₹{{ formatCurrency(formData.amount) }}</span>
        </div>

        <div class="summary-item">
          <span class="summary-label">收款人:</span>
          <span class="summary-value">{{ maskRecipient(formData.recipientId) }}</span>
        </div>

        <div v-if="formData.description" class="summary-item">
          <span class="summary-label">说明:</span>
          <span class="summary-value">{{ formData.description }}</span>
        </div>

        <!-- 风险提示（如果适用） -->
        <div v-if="riskWarning" class="alert alert-warning">
          <span class="alert-icon">⚠️</span>
          <span class="alert-text">{{ riskWarning }}</span>
        </div>

        <!-- 确认复选框 -->
        <div class="form-group checkbox">
          <input
            id="confirm-agree"
            v-model="formData.confirmAgreed"
            type="checkbox"
            class="form-checkbox"
            :disabled="isProcessing"
            required
          />
          <label for="confirm-agree" class="checkbox-label">
            我已确认上述交易信息正确，并同意进行支付
          </label>
        </div>

        <div class="form-actions">
          <button
            type="button"
            class="btn btn-secondary"
            @click="goBack"
            :disabled="isProcessing"
          >
            返回修改
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="!formData.confirmAgreed || isProcessing"
          >
            继续 → OTP验证
          </button>
        </div>
      </fieldset>

      <!-- 步骤3: OTP验证 -->
      <fieldset v-if="currentStep === 'otp'" class="form-section">
        <legend class="section-title">验证身份</legend>

        <p class="info-text">
          我们已向您的注册手机号 {{ maskPhoneNumber(userPhone) }} 发送了验证码
        </p>

        <div class="form-group">
          <label for="otp-input" class="form-label">
            验证码 <span class="required">*</span>
          </label>
          <input
            id="otp-input"
            v-model="formData.otp"
            type="text"
            class="form-input otp-input"
            placeholder="输入6位验证码"
            maxlength="6"
            pattern="[0-9]{6}"
            :disabled="isProcessing"
            @input="formData.otp = formData.otp.replace(/[^0-9]/g, '')"
            required
          />
          <small v-if="otpError" class="error-text">
            {{ otpError }}
          </small>
          <small class="help-text">
            OTP有效期: {{ otpTimeLeft }}秒
          </small>
        </div>

        <!-- 重新发送OTP -->
        <div class="otp-actions">
          <button
            v-if="!canResendOtp"
            type="button"
            class="btn-text"
            disabled
          >
            {{ otpResendCountdown }}秒后可重新发送
          </button>
          <button
            v-else
            type="button"
            class="btn-text"
            @click="resendOTP"
            :disabled="isProcessing"
          >
            重新发送验证码
          </button>
        </div>

        <div class="form-actions">
          <button
            type="button"
            class="btn btn-secondary"
            @click="goBack"
            :disabled="isProcessing"
          >
            返回
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="formData.otp.length !== 6 || isProcessing"
          >
            验证
          </button>
        </div>
      </fieldset>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useTransferStore } from '../stores/transferStore'
import { useWalletStore } from '../../wallet/stores/walletStore'
import { useAuthStore } from '../../auth/stores/authStore'

// Store
const transferStore = useTransferStore()
const walletStore = useWalletStore()
const authStore = useAuthStore()

// 表单数据
const formData = ref({
  amount: 0,
  recipientId: '',
  description: '',
  otp: '',
  confirmAgreed: false,
})

// 状态
const currentStep = ref<'basic' | 'confirm' | 'otp'>('basic')
const isProcessing = ref(false)
const isLoading = ref(false)
const error = ref('')
const amountError = ref('')
const recipientError = ref('')
const otpError = ref('')

// 风险提示
const riskWarning = ref('')

// OTP计时器
const otpTimeLeft = ref(300) // 5分钟
const otpResendCountdown = ref(0)
const canResendOtp = computed(() => otpResendCountdown.value === 0)

// 获取数据
const availableBalance = computed(() => walletStore.state.balance)
const userPhone = computed(() => authStore.state.phone)

// 校验
const canProceed = computed(() => {
  return (
    formData.value.amount > 0 &&
    !amountError.value &&
    formData.value.recipientId.trim() !== '' &&
    !recipientError.value
  )
})

// 金额验证
const validateAmount = async () => {
  amountError.value = ''

  const amount = formData.value.amount

  // 检查格式
  if (!Number.isFinite(amount) || amount <= 0) {
    amountError.value = '金额必须大于0'
    return
  }

  // 检查余额
  if (amount > availableBalance.value) {
    amountError.value = '余额不足'
    return
  }

  // 检查KYC限额
  const kycTier = authStore.state.kycTier
  const limits: Record<string, number> = {
    'tier1': 100000,
    'tier2': 500000,
    'tier3': Infinity,
  }

  if (amount > limits[kycTier]) {
    amountError.value = `您的KYC等级限制单笔转账₹${limits[kycTier]}`
    return
  }
}

// 收款人验证
const validateRecipient = async () => {
  recipientError.value = ''
  const recipientId = formData.value.recipientId

  if (!recipientId) {
    recipientError.value = '请输入收款人账户'
    return
  }

  // 验证格式
  if (!isValidRecipientId(recipientId)) {
    recipientError.value = '收款人账户格式不正确'
    return
  }

  // 调用API验证
  try {
    const valid = await api.validateRecipient({ recipientId })
    if (!valid) {
      recipientError.value = '收款人账户不存在'
    }
  } catch (err) {
    recipientError.value = '验证收款人失败，请重试'
  }
}

// 提交表单
const handleSubmit = async () => {
  if (currentStep.value === 'basic') {
    await handleBasicSubmit()
  } else if (currentStep.value === 'confirm') {
    await handleConfirmSubmit()
  } else if (currentStep.value === 'otp') {
    await handleOtpSubmit()
  }
}

const handleBasicSubmit = async () => {
  isProcessing.value = true
  try {
    // 再次验证
    await validateAmount()
    await validateRecipient()

    if (amountError.value || recipientError.value) {
      isProcessing.value = false
      return
    }

    // 检查风险
    const riskResult = await checkPaymentRisk()
    if (riskResult.score > 0.7) {
      riskWarning.value = `检测到异常活动，风险评分: ${(riskResult.score * 100).toFixed(0)}%`
    }

    currentStep.value = 'confirm'
  } finally {
    isProcessing.value = false
  }
}

const handleConfirmSubmit = async () => {
  isProcessing.value = true
  try {
    // 发送OTP
    await sendOtp()
    currentStep.value = 'otp'
    startOtpTimer()
    startOtpResendCountdown()
  } catch (err) {
    error.value = '发送验证码失败，请重试'
  } finally {
    isProcessing.value = false
  }
}

const handleOtpSubmit = async () => {
  isProcessing.value = true
  try {
    // 验证OTP
    const success = await verifyOtp()
    if (success) {
      // 执行支付
      await submitPayment()
      emit('success', { transactionId: transferStore.state.transactionId })
    }
  } catch (err) {
    otpError.value = err.message || '验证失败，请重试'
  } finally {
    isProcessing.value = false
  }
}

// API调用
const sendOtp = async () => {
  // 实现API调用
}

const verifyOtp = async (): Promise<boolean> => {
  // 实现OTP验证
  return true
}

const submitPayment = async () => {
  // 实现支付提交
}

const checkPaymentRisk = async () => {
  // 实现风险检查
  return { score: 0.2 }
}

// 工具函数
const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-IN').format(amount)
}

const maskRecipient = (id: string): string => {
  return id.length > 4 ? `****${id.slice(-4)}` : id
}

const maskPhoneNumber = (phone: string): string => {
  return `****${phone.slice(-4)}`
}

const isValidRecipientId = (id: string): boolean => {
  return /^[0-9]{10}$|^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/.test(id)
}

// 计时器
const startOtpTimer = () => {
  otpTimeLeft.value = 300
  const timer = setInterval(() => {
    otpTimeLeft.value--
    if (otpTimeLeft.value <= 0) {
      clearInterval(timer)
      error.value = '验证码已过期，请重新获取'
      currentStep.value = 'confirm'
    }
  }, 1000)
}

const startOtpResendCountdown = () => {
  otpResendCountdown.value = 30
  const timer = setInterval(() => {
    otpResendCountdown.value--
    if (otpResendCountdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const resendOTP = async () => {
  try {
    await sendOtp()
    startOtpTimer()
    startOtpResendCountdown()
    otpError.value = ''
  } catch (err) {
    error.value = '重新发送失败，请重试'
  }
}

// 导航
const goBack = () => {
  if (currentStep.value === 'confirm') {
    currentStep.value = 'basic'
  } else if (currentStep.value === 'otp') {
    currentStep.value = 'confirm'
  }
}

const resetForm = () => {
  formData.value = {
    amount: 0,
    recipientId: '',
    description: '',
    otp: '',
    confirmAgreed: false,
  }
  currentStep.value = 'basic'
  error.value = ''
  riskWarning.value = ''
}

// 事件
const emit = defineEmits<{
  success: [{ transactionId: string }]
  cancel: []
}>()

// 生命周期
onMounted(() => {
  // 初始化
})

onUnmounted(() => {
  // 清理
})
</script>

<style scoped>
.payment-form-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.alert {
  padding: 12px 16px;
  border-radius: 4px;
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-warning {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
}

.alert-icon {
  flex-shrink: 0;
}

.form-section {
  border: none;
  margin: 0;
  padding: 0;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.required {
  color: #dc3545;
}

.optional {
  color: #999;
  font-size: 12px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.form-input:disabled {
  background-color: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.input-wrapper {
  position: relative;
}

.currency-symbol {
  position: absolute;
  left: 12px;
  top: 12px;
  color: #666;
}

.amount-input {
  padding-left: 36px;
}

.textarea {
  resize: vertical;
  min-height: 80px;
}

.help-text {
  display: block;
  margin-top: 6px;
  color: #999;
  font-size: 12px;
}

.error-text {
  display: block;
  margin-top: 6px;
  color: #dc3545;
  font-size: 12px;
}

.checkbox {
  display: flex;
  gap: 12px;
}

.form-checkbox {
  margin-top: 2px;
  cursor: pointer;
}

.checkbox-label {
  font-size: 14px;
  line-height: 1.5;
  cursor: pointer;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.summary-label {
  font-weight: 500;
  color: #666;
}

.summary-value {
  color: #333;
}

.otp-input {
  font-size: 18px;
  letter-spacing: 8px;
  text-align: center;
  font-family: monospace;
}

.otp-actions {
  text-align: center;
  margin-bottom: 20px;
}

.btn-text {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 14px;
  padding: 0;
}

.btn-text:disabled {
  color: #ccc;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #f0f0f0;
  color: #333;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  z-index: 1000;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.info-text {
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
}
</style>
