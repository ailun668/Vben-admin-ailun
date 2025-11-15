<template>
  <a-button
    type="text"
    class="header-action-btn"
    @click="handleToggle"
    :title="isDark ? '切换到浅色主题' : '切换到深色主题'"
  >
    <template #icon>
      <setting-outlined />
    </template>
  </a-button>
</template>

<script lang="ts" setup>
/**
 * @fileoverview 主题切换组件
 * @author 开发团队
 * @date 2025-01-15
 */

import { computed } from 'vue'
import { SettingOutlined } from '@ant-design/icons-vue'
import { useAppStore } from '@/store/modules/app'
import { message } from 'ant-design-vue'

const appStore = useAppStore()

/**
 * 是否为深色主题
 */
const isDark = computed(() => appStore.theme === 'dark')

/**
 * 切换主题
 */
function handleToggle() {
  const newTheme = isDark.value ? 'light' : 'dark'
  appStore.setTheme(newTheme)
  message.success(`已切换到${newTheme === 'dark' ? '深色' : '浅色'}主题`)
  
  // 更新 HTML 类名，用于主题样式切换
  document.documentElement.setAttribute('data-theme', newTheme)
  
  // 如果使用 Ant Design Vue 的主题切换，可以在这里添加额外逻辑
  // 例如：更新 Ant Design Vue 的 ConfigProvider theme
}
</script>

<style scoped>
.header-action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  color: rgba(0, 0, 0, 0.65);
  border-radius: 4px;
  transition: all 0.2s;
  cursor: pointer;
}

.header-action-btn:hover {
  color: rgba(0, 0, 0, 0.85);
  background: rgba(0, 0, 0, 0.06);
}

.header-action-btn:active {
  transform: scale(0.95);
}
</style>

