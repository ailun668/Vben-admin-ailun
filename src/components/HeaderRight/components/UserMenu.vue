<template>
  <a-dropdown
    v-model:open="dropdownOpen"
    :trigger="['hover']"
    placement="bottomRight"
    :mouseEnterDelay="0"
    :mouseLeaveDelay="200"
  >
    <div class="user-menu-trigger" :class="{ 'is-open': dropdownOpen }">
      <a-avatar
        :size="32"
        :src="userStore.userInfo?.avatar"
        :style="{ backgroundColor: '#1890ff' }"
      >
        {{ userName.charAt(0).toUpperCase() }}
      </a-avatar>
      <span class="user-name">{{ userName }}</span>
      <down-outlined class="dropdown-icon" :class="{ 'is-rotated': dropdownOpen }" />
    </div>
    
    <template #overlay>
      <a-menu @click="handleMenuClick">
        <a-menu-item key="profile">
          <template #icon>
            <user-outlined />
          </template>
          个人中心
        </a-menu-item>
        
        <a-menu-item key="settings">
          <template #icon>
            <setting-outlined />
          </template>
          账户设置
        </a-menu-item>
        
        <a-menu-divider />
        
        <a-menu-item key="logout" danger>
          <template #icon>
            <logout-outlined />
          </template>
          退出登录
        </a-menu-item>
      </a-menu>
    </template>
  </a-dropdown>
</template>

<script lang="ts" setup>
/**
 * @fileoverview 用户菜单组件
 * @author 开发团队
 * @date 2025-01-15
 */

import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  UserOutlined,
  SettingOutlined,
  LogoutOutlined,
  DownOutlined
} from '@ant-design/icons-vue'
import { useUserStore } from '@/store/modules/user'
import { usePermissionStore } from '@/store/modules/permission'
import { resetRouteAdded } from '@/router'
import { message, Modal } from 'ant-design-vue'

const router = useRouter()
const userStore = useUserStore()
const permissionStore = usePermissionStore()

/**
 * 下拉菜单打开状态
 */
const dropdownOpen = ref(false)

/**
 * 用户名
 */
const userName = computed(() => {
  return userStore.userName || '用户'
})

/**
 * 菜单点击处理
 * @param param0 菜单点击事件参数
 */
function handleMenuClick({ key }: { key: string }) {
  // 点击菜单项后关闭下拉菜单
  dropdownOpen.value = false
  
  switch (key) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      handleLogout()
      break
  }
}

/**
 * 登出处理
 */
async function handleLogout() {
  Modal.confirm({
    title: '确认退出',
    content: '确定要退出登录吗？',
    okText: '确定',
    cancelText: '取消',
    onOk: async () => {
      try {
        await userStore.logout()
        permissionStore.resetPermission()
        resetRouteAdded()
        message.success('已安全退出')
        router.push('/login')
      } catch (error) {
        console.error('登出失败:', error)
        message.error('登出失败，请重试')
      }
    }
  })
}
</script>

<style scoped>
.user-menu-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}

.user-menu-trigger:hover,
.user-menu-trigger.is-open {
  background: rgba(0, 0, 0, 0.06);
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-icon.is-rotated {
  transform: rotate(180deg);
}
</style>

