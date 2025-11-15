// src/store/modules/tabs.ts

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import type { RouteLocationNormalized } from 'vue-router'

// 定义 Tab 类型
export interface TabItem {
  path: string
  fullPath: string
  name: string
  title: string
  icon?: string
}

export const useTabsStore = defineStore('tabs', () => {
  const router = useRouter()

  // 状态
  const tabsList = ref<TabItem[]>([])
  const activeTabPath = ref<string>('')

  // Actions
  /**
   * 添加一个新标签页
   * @param route - 路由信息
   */
  function addTab(route: RouteLocationNormalized) {
    // 忽略特定路由
    if (route.path === '/login' || route.meta?.hideInTab) {
      return
    }

    // 检查标签页是否已存在
    const isExists = tabsList.value.some(tab => tab.path === route.path)
    if (!isExists) {
      tabsList.value.push({
        path: route.path,
        fullPath: route.fullPath,
        name: route.name as string,
        title: route.meta.title as string,
        icon: route.meta.icon as string,
      })
    }
    activeTabPath.value = route.path
  }

  /**
   * 移除一个标签页
   * @param path - 标签页路径
   */
  function removeTab(path: string) {
    const index = tabsList.value.findIndex(tab => tab.path === path)
    if (index === -1) return

    // 如果关闭的是当前激活的 tab，则需要切换到其他 tab
    if (activeTabPath.value === path) {
      const nextTab = tabsList.value[index + 1] || tabsList.value[index - 1]
      if (nextTab) {
        router.push(nextTab.path)
      } else {
        router.push('/') // 如果没有其他 tab，回到首页
      }
    }
    tabsList.value.splice(index, 1)
  }

  /**
   * 关闭其他标签页
   * @param path - 保留的标签页路径
   */
  function closeOtherTabs(path: string) {
    tabsList.value = tabsList.value.filter(tab => tab.path === path)
    if (activeTabPath.value !== path) {
        router.push(path)
    }
  }

  /**
   * 关闭所有标签页
   */
  function closeAllTabs() {
    tabsList.value = []
    router.push('/')
  }
  
  // ... 其他关闭方法（如 closeLeft, closeRight）的实现

  return {
    tabsList,
    activeTabPath,
    addTab,
    removeTab,
    closeOtherTabs,
    closeAllTabs,
  }
}, {
  persist: true // 启用持久化
})
