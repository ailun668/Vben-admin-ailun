<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h1>My Vue App</h1>
        <p>现代化企业管理系统</p>
      </div>

      <!-- 快速登录选项 -->
      <div class="quick-login-section">
        <p class="quick-login-title">快速登录（本地）</p>
        <div class="quick-login-buttons">
          <a-button
            v-for="user in quickLoginUsers"
            :key="user.username"
            type="primary"
            :block="true"
            size="large"
            @click="quickLogin(user)"
            class="quick-login-btn"
          >
            {{ user.realName }}
          </a-button>
        </div>
      </div>

      <a-divider>或使用账号密码登录</a-divider>

      <a-form
        :model="formState"
        :rules="rules"
        layout="vertical"
        @finish="onFinish"
      >
        <a-form-item label="用户名" name="username">
          <a-input
            v-model:value="formState.username"
            placeholder="请输入用户名"
            size="large"
            autocomplete="username"
          >
            <template #prefix>
              <user-outlined />
            </template>
          </a-input>
        </a-form-item>

        <a-form-item label="密码" name="password">
          <a-input-password
            v-model:value="formState.password"
            placeholder="请输入密码"
            size="large"
            autocomplete="current-password"
          >
            <template #prefix>
              <lock-outlined />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item>
          <a-button
            type="default"
            block
            size="large"
            html-type="submit"
            :loading="loading"
          >
            {{ loading ? '登录中...' : '调用后端 API 登录' }}
          </a-button>
        </a-form-item>
      </a-form>

      <div class="login-tips">
        <p>
          <strong>💡 提示:</strong>
        </p>
        <ul>
          <li>点击上面的按钮可快速登录（不走接口）</li>
          <li>或输入用户名密码通过后端 API 登录</li>
          <li>管理员密码：admin123</li>
          <li>普通用户密码：user123</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/store/modules/user'
import { usePermissionStore } from '@/store/modules/permission'
import type { UserInfo } from '@/api/types'

const router = useRouter()
const userStore = useUserStore()
const permissionStore = usePermissionStore()

const loading = ref(false)
const formState = reactive({
  username: 'admin',
  password: 'admin123'
})

const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  password: [{ required: true, message: '请输入密码' }]
}

// 本地用户数据（不走接口的快速登录）
const quickLoginUsers = ref<UserInfo[]>([
  {
    id: '1',
    username: 'admin',
    realName: '管理员',
    email: 'admin@example.com',
    avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
    roles: ['admin'],
    permissions: [
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
  },
  {
    id: '2',
    username: 'user',
    realName: '普通用户',
    email: 'user@example.com',
    avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
    roles: ['user'],
    permissions: [
      'system:user:list',
      'system:user:edit'
    ]
  }
])

/**
 * 快速登录（本地，不走接口）
 */
function quickLogin(user: UserInfo) {
  const token = `dev_mock_token_${user.username}`

  // 直接设置用户信息和 token
  userStore.setToken(token)
  userStore.setUserInfo(user)

  // 生成可访问的路由
  permissionStore.generateRoutes(user.roles)

  message.success(`已登录为 ${user.realName}`)

  // 获取重定向路径
  const redirect = (router.currentRoute.value.query.redirect as string) || '/'

  // 跳转到目标页面
  setTimeout(() => {
    router.push(redirect)
  }, 300)
}

/**
 * 通过 API 登录
 */
async function onFinish() {
  loading.value = true
  try {
    // 调用登录接口
    const result = await userStore.login({
      username: formState.username,
      password: formState.password
    })

    message.success('登录成功')

    // 生成可访问的路由
    permissionStore.generateRoutes(result.user.roles)

    // 获取重定向路径（从路由查询参数中获取，如果没有则跳转到首页）
    const redirect = (router.currentRoute.value.query.redirect as string) || '/'

    // 延迟跳转，确保路由已更新
    // 路由守卫会自动处理动态路由的添加
    setTimeout(() => {
      router.push(redirect)
    }, 500)
  } catch (error) {
    message.error((error as any)?.message || '登录失败，请检查后端服务是否启动')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.login-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
  color: #333;
}

.login-header p {
  margin: 8px 0 0;
  font-size: 14px;
  color: #666;
}

.login-tips {
  margin-top: 20px;
  padding: 12px;
  background-color: #f5f5f5;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

.login-tips p {
  margin: 0 0 8px;
  font-weight: 500;
}

.login-tips ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.login-tips li {
  margin: 4px 0;
  display: flex;
  justify-content: space-between;
}

.login-tips .label {
  font-weight: 500;
}

.login-tips .value {
  font-family: monospace;
  color: #333;
}

/* 快速登录样式 */
.quick-login-section {
  margin-bottom: 24px;
}

.quick-login-title {
  text-align: center;
  margin: 0 0 12px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.quick-login-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-login-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  font-weight: 500;
}

.quick-login-btn:hover {
  opacity: 0.9;
}
</style>
