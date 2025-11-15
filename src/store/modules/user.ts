import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/api/user'
import type { UserInfo, LoginRequest } from '@/api/types'

export const useUserStore = defineStore(
  'user',
  () => {
    // 状态
    const token = ref<string>('')
    const userInfo = ref<UserInfo | null>(null)
    const loading = ref(false)

    // 计算属性
    const isLoggedIn = computed(() => !!token.value)
    const userName = computed(() => userInfo.value?.realName || userInfo.value?.username || '')
    const userRoles = computed(() => userInfo.value?.roles || [])
    const userPermissions = computed(() => userInfo.value?.permissions || [])

    /**
     * 登录
     */
    async function login(loginData: LoginRequest) {
      loading.value = true
      try {
        const response = await userApi.login(loginData)
        token.value = response.data.token
        userInfo.value = response.data.user
        return response.data
      } finally {
        loading.value = false
      }
    }

    /**
     * 获取当前用户信息
     */
    async function getCurrentUser() {
      loading.value = true
      try {
        const response = await userApi.getCurrentUser()
        userInfo.value = response.data
        return response.data
      } finally {
        loading.value = false
      }
    }

    /**
     * 设置用户信息（用于恢复存储的状态）
     */
    function setUserInfo(info: UserInfo) {
      userInfo.value = info
    }

    /**
     * 设置 Token（用于恢复存储的状态）
     */
    function setToken(newToken: string) {
      token.value = newToken
    }

    /**
     * 检查用户是否有指定角色
     */
    function hasRole(role: string): boolean {
      return userRoles.value.includes(role)
    }

    /**
     * 检查用户是否有指定权限
     */
    function hasPermission(permission: string): boolean {
      return userPermissions.value.includes(permission)
    }

    /**
     * 登出
     */
    async function logout() {
      loading.value = true
      try {
        // 调用登出接口
        await userApi.logout()
      } catch (error) {
        console.error('登出失败:', error)
      } finally {
        // 无论是否成功，都清除本地数据
        token.value = ''
        userInfo.value = null
        loading.value = false
      }
    }

    /**
     * 重置状态
     */
    function resetStore() {
      token.value = ''
      userInfo.value = null
      loading.value = false
    }

    return {
      // 状态
      token,
      userInfo,
      loading,
      // 计算属性
      isLoggedIn,
      userName,
      userRoles,
      userPermissions,
      // 方法
      login,
      getCurrentUser,
      setUserInfo,
      setToken,
      hasRole,
      hasPermission,
      logout,
      resetStore
    }
  },
  {
    persist: {
      enabled: true,
      strategies: [
        {
          key: 'user_store',
          storage: localStorage,
          paths: ['token', 'userInfo']
        }
      ]
    }
  }
)
