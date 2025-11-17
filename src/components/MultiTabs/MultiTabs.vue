<!-- src/components/MultiTabs/MultiTabs.vue -->
<template>
  <div class="multi-tabs-container">
    <a-tabs
      v-model:activeKey="activeKey"
      type="editable-card"
      hide-add
      @tab-click="handleTabClick"
      @edit="handleTabEdit"
    >
      <a-tab-pane
        v-for="tab in tabsStore.tabsList"
        :key="tab.path"
      >
        <template #tab>
          <a-dropdown :trigger="['contextmenu']">
            <span>{{ tab.title }}</span>
            <template #overlay>
              <a-menu @click="({ key }: { key: string }) => handleMenuClick(key, tab.path)">
                <a-menu-item key="reload">重新加载</a-menu-item>
                <a-menu-item key="close">关闭</a-menu-item>
                <a-menu-divider />
                <a-menu-item key="closeOther">关闭其它</a-menu-item>
                <a-menu-item key="closeAll">关闭全部</a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </template>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<script setup lang="ts">
import { computed, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useTabsStore } from '@/store/modules/tabs'

const reloadPage = inject('reloadPage') as () => void

const router = useRouter()
const tabsStore = useTabsStore()

const activeKey = computed({
  get: () => tabsStore.activeTabPath,
  set: (val) => tabsStore.activeTabPath = val
})

// 点击标签页
const handleTabClick = (path: string) => {
  router.push(path)
}

// 关闭标签页
const handleTabEdit = (targetKey: string, action: 'add' | 'remove') => {
  if (action === 'remove') {
    tabsStore.removeTab(targetKey as string)
  }
}

// 右键菜单点击
const handleMenuClick = (key: string, path: string) => {
  switch (key) {
    case 'reload':
      if (reloadPage) reloadPage()
      break
    case 'close':
      tabsStore.removeTab(path)
      break
    case 'closeOther':
      tabsStore.closeOtherTabs(path)
      break
    case 'closeAll':
      tabsStore.closeAllTabs()
      break
  }
}
</script>

<style scoped>
.multi-tabs-container {
  /* 应用玻璃效果 */
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  padding: 8px 16px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

/* 移除 antd 默认背景和边框 */
:deep(.ant-tabs) {
  background: transparent;
}
:deep(.ant-tabs-nav) {
  margin-bottom: 0 !important;
}
:deep(.ant-tabs-nav::before) {
  border-bottom: none !important;
}

/* 标签页样式 */
:deep(.ant-tabs-tab) {
  background: rgba(255, 255, 255, 0.5) !important;
  border: 1px solid transparent !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
  border-radius: 8px 8px 0 0 !important;
  transition: all 0.3s ease;
}

/* 激活的标签页 */
:deep(.ant-tabs-tab-active) {
  background: #fff !important;
  border-color: rgba(0, 0, 0, 0.05) !important;
  border-bottom-color: #fff !important;
  font-weight: 600;
  color: #4F46E5 !important;
}
</style>
