import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 应用全局配置
  const sidebarCollapsed = ref(false)
  const theme = ref<'light' | 'dark'>('light')
  const language = ref('zh-CN')

  /**
   * 切换侧边栏
   */
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  /**
   * 设置侧边栏状态
   */
  function setSidebarCollapsed(collapsed: boolean) {
    sidebarCollapsed.value = collapsed
  }

  /**
   * 切换主题
   */
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }

  /**
   * 设置主题
   */
  function setTheme(newTheme: 'light' | 'dark') {
    theme.value = newTheme
  }

  /**
   * 设置语言
   */
  function setLanguage(lang: string) {
    language.value = lang
  }

  return {
    sidebarCollapsed,
    theme,
    language,
    toggleSidebar,
    setSidebarCollapsed,
    toggleTheme,
    setTheme,
    setLanguage
  }
})
