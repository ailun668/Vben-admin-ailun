<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 左侧登录表单 -->
      <div class="login-form-section">
        <!-- 语言选择器 -->
        <div class="language-selector">
          <div class="language-btn">
            <i class="fas fa-globe"></i>
            <span>简体中文</span>
          </div>
        </div>

        <div class="form-wrapper">
          <!-- Logo 图标 -->
          <div class="logo-icon">
            <i class="fas fa-lock"></i>
          </div>

          <!-- 标题区域 -->
          <h1 class="logo-text">Enterprise-level framework</h1>
          <p class="tagline">现代化企业管理系统</p>

          <!-- 快速登录按钮组 -->
          <div class="quick-login-section">
            <p class="section-title">快速登录（本地）</p>
            <div class="quick-login-buttons">
              <button
                v-for="(user, index) in quickLoginUsers"
                :key="user.username"
                type="button"
                :class="['quick-login-btn', index === 0 ? 'admin-btn' : 'user-btn']"
                @click="quickLogin(user)"
                :disabled="loading"
              >
                <i :class="index === 0 ? 'fas fa-user-shield' : 'fas fa-user'"></i>
                <span>{{ user.realName }}</span>
              </button>
            </div>
          </div>

          <!-- 分隔线 -->
          <div class="divider">或使用账号密码登录</div>

          <!-- 登录表单 -->
          <div class="form-group">
            <label for="username" class="form-label">邮箱或手机号</label>
            <div class="input-with-icon">
              <i class="fas fa-user input-icon"></i>
              <input
                type="text"
                id="username"
                v-model="formState.username"
                class="input-field"
                placeholder="您的邮箱或手机号码"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="password" class="form-label">密码</label>
            <div class="input-with-icon">
              <i class="fas fa-lock input-icon"></i>
              <input
                :type="showPassword ? 'text' : 'password'"
                id="password"
                v-model="formState.password"
                class="input-field"
                placeholder="输入您的密码"
                @keyup.enter="onFinish"
              />
              <button class="password-toggle" @click="togglePassword" type="button">
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
          </div>

          <!-- 记住密码 & 忘记密码 -->
          <div class="remember-forgot">
            <label class="remember-me">
              <input type="checkbox" v-model="formState.rememberMe" class="checkbox" />
              记住我
            </label>
            <a href="#" class="forgot-link">忘记密码？</a>
          </div>

          <!-- 登录按钮 -->
          <button
            class="login-button"
            @click="onFinish"
            :disabled="loading"
            type="button"
          >
            <i :class="loading ? 'fas fa-spinner fa-spin' : 'fas fa-sign-in-alt'"></i>
            {{ loading ? '登录中...' : '登录账户' }}
          </button>

          <!-- 安全徽章 -->
          <div class="security-badge">
            <i class="fas fa-shield-alt"></i>
            <span>256位银行级加密保护</span>
          </div>

          <!-- 社交登录 -->
          <div class="social-login">
            <div class="social-btn">
              <i class="fab fa-google"></i>
            </div>
            <div class="social-btn">
              <i class="fab fa-facebook-f"></i>
            </div>
            <div class="social-btn">
              <i class="fab fa-twitter"></i>
            </div>
          </div>

          <!-- 注册链接 -->
          <div class="signup-link">
            还没有账号？ <a href="#">马上注册</a>
          </div>

          <!-- 指示器 -->
          <div class="indicator">
            <div class="indicator-dot active"></div>
            <div class="indicator-dot"></div>
            <div class="indicator-dot"></div>
          </div>

          <!-- 登录统计 -->
          <div class="login-stats">
            <div class="stat-item">
              <div class="stat-value">96.7%</div>
              <div class="stat-label">系统稳定</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">10M+</div>
              <div class="stat-label">注册用户</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">99.8%</div>
              <div class="stat-label">安全认证</div>
            </div>
          </div>

          <!-- 浮动图标 -->
          <svg class="floating-icon icon-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12,2A10,10,0,1,0,22,12,10,10,0,0,0,12,2Zm0,18a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z" />
            <path d="M12,6a6,6,0,1,0,6,6A6,6,0,0,0,12,6Zm0,10a4,4,0,1,1,4-4A4,4,0,0,1,12,16Z" />
          </svg>

          <svg class="floating-icon icon-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" />
          </svg>

          <!-- 通知气泡 -->
          <div class="notification-bubble">
            <div class="notification-title">安全提示</div>
            <div class="notification-content">
              在输入凭证前，请确保网址以"https://"开头并带有安全锁图标
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧横幅区域 -->
      <div class="banner-section">
        <h2 class="welcome">欢迎使用</h2>
        <p class="sub-heading">印度领先的安全支付平台，提供最可靠的交易服务</p>

        <div id="chart" ref="chartRef" style="width: 100%; height: 200px"></div>

        <div id="features" style="display: flex; gap: 20px; margin-top: 2.5rem">
          <div style="text-align: center">
            <div
              style="
                width: 50px;
                height: 50px;
                background: #ff572233;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto;
              "
            >
              <i class="fas fa-shield-alt" style="color: #ff5722; font-size: 24px"></i>
            </div>
            <p style="color: white; margin-top: 10px; font-size: 0.9rem">银行级安全</p>
          </div>
          <div style="text-align: center">
            <div
              style="
                width: 50px;
                height: 50px;
                background: #3b82f633;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto;
              "
            >
              <i class="fas fa-bolt" style="color: #3b82f6; font-size: 24px"></i>
            </div>
            <p style="color: white; margin-top: 10px; font-size: 0.9rem">实时支付</p>
          </div>
          <div style="text-align: center">
            <div
              style="
                width: 50px;
                height: 50px;
                background: #10b98133;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto;
              "
            >
              <i class="fas fa-rupee-sign" style="color: #10b981; font-size: 24px"></i>
            </div>
            <p style="color: white; margin-top: 10px; font-size: 0.9rem">支持UPI</p>
          </div>
        </div>

        <div
          style="
            margin-top: 2.5rem;
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.8rem;
            text-align: center;
            max-width: 400px;
          "
        >
          <p>印度支付通是经RBI认证的支付系统提供商，严格遵守PCI DSS安全标准</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/store/modules/user'
import { usePermissionStore } from '@/store/modules/permission'
import * as echarts from 'echarts'

const router = useRouter()
const userStore = useUserStore()
const permissionStore = usePermissionStore()

const loading = ref(false)
const showPassword = ref(false)
const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null

// 快速登录用户列表
const quickLoginUsers = [
  {
    username: 'admin',
    password: 'admin123',
    realName: '管理员'
  },
  {
    username: 'user',
    password: 'user123',
    realName: '普通用户'
  }
]

const formState = reactive({
  username: 'admin',
  password: 'admin123',
  rememberMe: true
})

/**
 * 切换密码显示/隐藏
 */
function togglePassword() {
  showPassword.value = !showPassword.value
}

/**
 * 快速登录（本地）- 不走接口，直接进入系统
 */
async function quickLogin(user: { username: string; password: string; realName: string }) {
  loading.value = true
  try {
    // 本地模拟用户数据（不调用 API）
    const mockUserData = {
      id: user.username === 'admin' ? '1' : '2',
      username: user.username,
      realName: user.realName,
      email: user.username === 'admin' ? 'admin@example.com' : 'user@example.com',
      avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
      roles: user.username === 'admin' ? ['admin'] : ['user'],
      permissions: user.username === 'admin'
        ? [
            'system:user:list',
            'system:user:add',
            'system:user:edit',
            'system:user:delete',
            'system:role:list',
            'system:role:add',
            'system:role:edit',
            'system:role:delete',
            'system:permission:list',
            'system:permission:add',
            'system:permission:edit',
            'system:permission:delete'
          ]
        : ['system:user:list']
    }

    // 直接设置用户信息和 token（不调用 API）
    userStore.setToken(`local_${user.username}_token_${Date.now()}`)
    userStore.setUserInfo(mockUserData)
    permissionStore.generateRoutes(mockUserData.roles)

    message.success(`欢迎，${user.realName}！`)

    const redirect = (router.currentRoute.value.query.redirect as string) || '/'
    setTimeout(() => {
      router.push(redirect)
    }, 500)
  } catch (error) {
    message.error(`${user.realName}登录失败`)
  } finally {
    loading.value = false
  }
}

/**
 * 初始化 ECharts 图表
 */
function initChart() {
  if (!chartRef.value) return

  chartInstance = echarts.init(chartRef.value)

  const option = {
    grid: {
      top: 20,
      bottom: 20,
      left: 40,
      right: 20
    },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月'],
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.5)'
        }
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.8)'
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.5)'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      },
      axisLabel: {
        color: 'rgba(255, 255, 255, 0.8)',
        formatter: '{value} k'
      }
    },
    series: [
      {
        data: [125, 168, 145, 210, 280, 260, 305],
        type: 'line',
        smooth: true,
        lineStyle: {
          width: 4,
          color: '#FF5722'
        },
        symbol: 'circle',
        symbolSize: 8,
        itemStyle: {
          color: '#FF5722'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 87, 34, 0.5)' },
            { offset: 1, color: 'rgba(255, 87, 34, 0)' }
          ])
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

/**
 * 表单登录（本地验证，不走接口）
 */
async function onFinish() {
  loading.value = true
  
  // 查找匹配的用户
  const user = quickLoginUsers.find(
    (u) => u.username === formState.username && u.password === formState.password
  )

  if (!user) {
    message.error('用户名或密码错误')
    loading.value = false
    return
  }

  try {
    // 模拟登录，直接设置用户信息
    const token = `dev_mock_token_${user.username}`
    userStore.setToken(token)
    
    // 构建完整的用户信息
    const userInfo = {
      id: user.username === 'admin' ? '1' : '2',
      username: user.username,
      realName: user.realName,
      email: `${user.username}@example.com`,
      avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
      roles: user.username === 'admin' ? ['admin'] : ['user'],
      permissions:
        user.username === 'admin'
          ? [
              'system:user:list',
              'system:user:add',
              'system:user:edit',
              'system:user:delete',
              'system:role:list',
              'system:role:add',
              'system:role:edit',
              'system:role:delete',
              'system:permission:list',
              'system:permission:add',
              'system:permission:edit',
              'system:permission:delete'
            ]
          : ['system:user:list', 'system:user:edit']
    }
    
    userStore.setUserInfo(userInfo)
    permissionStore.generateRoutes(userInfo.roles)

    message.success(`欢迎，${user.realName}！`)

    const redirect = (router.currentRoute.value.query.redirect as string) || '/'
    setTimeout(() => {
      router.push(redirect)
    }, 500)
  } catch (error) {
    message.error('登录失败，请重试')
  } finally {
    loading.value = false
  }
}

/**
 * 组件挂载时初始化图表
 */
onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

/**
 * 组件卸载时销毁图表
 */
onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  window.removeEventListener('resize', handleResize)
})

/**
 * 窗口大小变化时调整图表
 */
function handleResize() {
  if (chartInstance) {
    chartInstance.resize()
  }
}
</script>

<style scoped>
.login-page {
  --primary: #ff5722;
  --secondary: #1e40af;
  --accent: #3b82f6;
  --light: #f5f7fb;
  --dark: #1f2937;
  --success: #10b981;
  --border: #d1d5db;
  
  font-family: 'Noto Sans SC', 'PingFang SC', sans-serif;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  color: #1f2937;
  padding: 1rem;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-container {
  display: flex;
  max-width: 1200px;
  width: 100%;
  background-color: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

/* Login Form Styling */
.login-form-section {
  width: 100%;
  max-width: 400px;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  position: relative;
}

/* Banner Styling */
.banner-section {
  flex: 1;
  background: linear-gradient(135deg, #1e40af 0%, #4b5563 100%);
  padding: 3rem 2rem;
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.logo-icon {
  background: var(--primary);
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: white;
  font-size: 1.5rem;
}

.logo-text {
  font-weight: 700;
  font-size: 2rem;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.tagline {
  color: var(--dark);
  font-size: 1.1rem;
  margin-bottom: 2rem;
  text-align: center;
  max-width: 350px;
  opacity: 0.8;
}

.welcome {
  font-size: 2.3rem;
  color: white;
  font-weight: 600;
  margin-bottom: 1rem;
  text-align: center;
}

.sub-heading {
  font-size: 1.15rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1.5rem;
  text-align: center;
  max-width: 350px;
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--dark);
}

.input-with-icon {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--secondary);
  font-size: 1rem;
}

.input-field {
  width: 100%;
  padding: 14px 20px 14px 45px;
  border: 2px solid var(--border);
  border-radius: 10px;
  font-size: 1rem;
  font-family: 'Noto Sans SC', sans-serif;
  transition: all 0.3s ease;
}

.input-field:focus {
  border-color: var(--secondary);
  box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.2);
  outline: none;
}

.password-toggle {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--secondary);
  cursor: pointer;
  font-size: 1.1rem;
}

.remember-forgot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0 1.5rem;
  font-size: 0.9rem;
}

.remember-me {
  display: flex;
  align-items: center;
}

.checkbox {
  margin-right: 8px;
  width: 18px;
  height: 18px;
  accent-color: var(--primary);
}

.forgot-link {
  color: var(--secondary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: var(--primary);
  text-decoration: underline;
}

.login-button {
  background: var(--primary);
  color: white;
  border: none;
  padding: 14px;
  width: 100%;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Noto Sans SC', sans-serif;
}

.login-button:hover {
  background: #e64a19;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 87, 34, 0.3);
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 2rem 0;
  color: var(--dark);
  opacity: 0.7;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--border);
}

.divider:not(:empty)::before {
  margin-right: 1rem;
}

.divider:not(:empty)::after {
  margin-left: 1rem;
}

.social-login {
  display: none;
}

.social-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  color: var(--dark);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.25rem;
}

.social-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border-color: var(--secondary);
  color: var(--secondary);
}

.signup-link {
  color: var(--dark);
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
}

.signup-link a {
  color: var(--secondary);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.signup-link a:hover {
  color: var(--primary);
  text-decoration: underline;
}

.language-selector {
  position: absolute;
  top: 20px;
  right: 20px;
}

.language-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid var(--border);
  padding: 8px 16px;
  border-radius: 30px;
  color: var(--dark);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.language-btn:hover {
  background: var(--light);
  border-color: var(--secondary);
}

.floating-icon {
  display: none;
}

.icon-1 {
  top: 50px;
  right: 50px;
  width: 100px;
  height: 100px;
}

.icon-2 {
  bottom: 70px;
  left: 40px;
  width: 80px;
  height: 80px;
}

.indicator {
  display: none;
}

.indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--border);
  transition: all 0.3s ease;
}

.indicator-dot.active {
  background: var(--primary);
  width: 25px;
  border-radius: 4px;
}

.login-stats {
  display: none;
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-value {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.75rem;
  color: #666;
}

.notification-bubble {
  display: none;
  position: absolute;
  bottom: 30px;
  right: 30px;
  background: white;
  border-radius: 15px;
  padding: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  max-width: 280px;
  animation: slideIn 0.5s ease-out;
  border-left: 4px solid var(--success);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.notification-title {
  font-weight: 600;
  color: var(--dark);
  margin-bottom: 5px;
}

.notification-content {
  font-size: 0.85rem;
  color: #666;
}

.security-badge {
  display: none;
}

.security-badge i {
  margin-right: 8px;
}

/* Quick Login Section Styling */
.quick-login-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.section-title {
  font-weight: 700;
  color: var(--dark);
  font-size: 0.75rem;
  margin-bottom: 1rem;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.8;
}

.quick-login-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quick-login-btn {
  padding: 16px 20px;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-family: 'Noto Sans SC', sans-serif;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quick-login-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.quick-login-btn:hover::before {
  left: 100%;
}

.quick-login-btn i {
  font-size: 1.1rem;
  flex-shrink: 0;
}

.quick-login-btn span {
  font-size: 1rem;
  letter-spacing: 0.5px;
}

/* 管理员按钮样式 */
.admin-btn {
  background: linear-gradient(135deg, #ff5722 0%, #ff8a50 100%);
  box-shadow: 0 4px 12px rgba(255, 87, 34, 0.3);
}

.admin-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(255, 87, 34, 0.4);
  background: linear-gradient(135deg, #e64a19 0%, #ff7a3d 100%);
}

.admin-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 87, 34, 0.3);
}

/* 普通用户按钮样式 */
.user-btn {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
}

.user-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(30, 64, 175, 0.4);
  background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
}

.user-btn:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
}

.quick-login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

.quick-login-btn:disabled::before {
  display: none;
}

@media (min-width: 768px) {
  .banner-section {
    display: flex;
  }

  .login-container {
    min-height: 700px;
  }
}

@media (max-width: 768px) {
  .login-form-section {
    max-width: 100%;
    padding: 2rem 1.5rem;
  }

  .tagline {
    font-size: 1rem;
  }

  .notification-bubble {
    max-width: 240px;
    bottom: 20px;
    right: 20px;
  }
}
</style>
