<template>
  <div v-if="!isLoginPage" class="app-container">
    <a-layout class="app-layout">
      <a-layout-sider
        v-model:collapsed="collapsed"
        :collapsed-width="64"
        :width="208"
        collapsible
        class="layout-sider"
        :theme="menuTheme"
        :trigger="null"
      >
        <div class="sider-content">
          <!-- Logo 区域 -->
          <div class="logo" :class="{ collapsed: collapsed }">
            <div class="logo-icon">
              <img src="/1.png" alt="Logo" class="logo-img" />
            </div>
            <h2 v-if="!collapsed" class="logo-title">Vue App</h2>
          </div>

          <!-- 菜单区域 -->
          <div class="menu-container">
            <a-menu
              v-model:selectedKeys="selectedKeys"
              v-model:openKeys="openKeys"
              :theme="menuTheme"
              mode="inline"
              :inline-collapsed="collapsed"
              :items="menuItems"
              @click="handleMenuClick"
            />
          </div>

          <!-- 用户信息区域 -->
          <div class="user-info" :class="{ collapsed: collapsed }">
            <div class="user-avatar">
              <a-avatar :size="collapsed ? 32 : 40" :style="{ backgroundColor: '#1890ff' }">
                {{ userName.charAt(0).toUpperCase() }}
              </a-avatar>
            </div>
            <div v-if="!collapsed" class="user-details">
              <div class="user-name">{{ userName }}</div>
              <a-button
                type="text"
                size="small"
                @click="handleLogout"
                class="logout-btn"
              >
                登出
              </a-button>
            </div>
          </div>
        </div>
      </a-layout-sider>
      <a-layout class="main-layout">
        <a-layout-header class="layout-header">
          <div class="header-left">
            <menu-unfold-outlined
              v-if="collapsed"
              class="trigger"
              @click="collapsed = false"
            />
            <menu-fold-outlined v-else class="trigger" @click="collapsed = true" />
            <a-breadcrumb class="breadcrumb">
              <a-breadcrumb-item>
                <home-outlined />
              </a-breadcrumb-item>
              <a-breadcrumb-item>{{ currentPageTitle }}</a-breadcrumb-item>
            </a-breadcrumb>
          </div>
          <HeaderRight />
        </a-layout-header>
        <MultiTabs />
        <a-layout-content class="layout-content">
          <div class="content-wrapper">
            <router-view v-if="isRouterAlive" />
          </div>
        </a-layout-content>
        <a-layout-footer class="layout-footer">
          My Vue App © 2025 Created by Vue + Vite
        </a-layout-footer>
      </a-layout>
    </a-layout>
  </div>
  <div v-else>
    <router-view v-if="isRouterAlive" />
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch, h, provide, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/store/modules/user'
import { usePermissionStore } from '@/store/modules/permission'
import { resetRouteAdded } from '@/router'
import type { Component } from 'vue'
import type { MenuProps } from 'ant-design-vue'
import {
  PieChartOutlined,
  DashboardOutlined,
  UserOutlined,
  TeamOutlined,
  LockOutlined,
  SettingOutlined,
  HomeOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined
} from '@ant-design/icons-vue'
import type { RouteItem } from '@/api/types'
import { HeaderRight } from '@/components/HeaderRight'
import MultiTabs from '@/components/MultiTabs/MultiTabs.vue'

const isRouterAlive = ref(true)
const reloadPage = () => {
  isRouterAlive.value = false
  nextTick(() => {
    isRouterAlive.value = true
  })
}
provide('reloadPage', reloadPage)

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const permissionStore = usePermissionStore()

// 侧边栏折叠状态
const collapsed = ref<boolean>(false)
// 选中的菜单项
const selectedKeys = ref<string[]>([route.path])
// 打开的菜单项（用于子菜单）
const openKeys = ref<string[]>([])
// 菜单主题
const menuTheme = ref<'light' | 'dark'>('dark')

/**
 * 检查是否在登录页面
 */
const isLoginPage = computed(() => {
  return route.path === '/login'
})

/**
 * 获取可访问的路由列表（过滤掉登录页）
 */
const accessibleRoutes = computed(() => {
  return permissionStore.accessibleRoutes.filter(
    (r) => r.path && r.path !== '/login'
  )
})

/**
 * 获取用户名（优先显示真实姓名，其次用户名，最后显示默认值）
 */
const userName = computed(() => {
  return userStore.userName || '用户'
})

/**
 * 获取当前页面标题
 */
const currentPageTitle = computed(() => {
  return (route.meta?.title as string) || '首页'
})

/**
 * 图标映射表
 */
const iconMap: Record<string, Component> = {
  home: HomeOutlined,
  dashboard: DashboardOutlined,
  user: UserOutlined,
  team: TeamOutlined,
  lock: LockOutlined,
  setting: SettingOutlined
}

/**
 * 根据图标名称获取对应的图标组件
 * @param iconName - 图标名称
 * @returns 图标组件或 undefined
 */
function getIcon(iconName?: string): Component | undefined {
  if (!iconName) {
    return iconMap.home
  }
  return iconMap[iconName]
}

/**
 * 将路由转换为菜单项
 */
function routeToMenuItems(routes: RouteItem[]): MenuProps['items'] {
  return routes
    .filter((route) => route.meta?.title)
    .map((route) => {
      const IconComponent = route.meta?.icon ? getIcon(route.meta.icon) : undefined

      // 如果有子菜单
      if (route.children && route.children.length > 0) {
        const children = routeToMenuItems(route.children)
        const menuItem: any = {
          key: route.path,
          icon: IconComponent
            ? () => h(IconComponent as Component)
            : undefined,
          label: route.meta?.title
        }
        if (children && children.length > 0) {
          menuItem.children = children
        }
        return menuItem
      }

      // 普通菜单项
      return {
        key: route.path,
        icon: IconComponent ? () => h(IconComponent as Component) : undefined,
        label: route.meta?.title
      }
    })
}

/**
 * 菜单项数据
 */
const menuItems = computed(() => {
  return routeToMenuItems(accessibleRoutes.value)
})

/**
 * 菜单点击处理
 */
const handleMenuClick: MenuProps['onClick'] = (e) => {
  const path = e.key as string
  router.push(path)
  selectedKeys.value = [path]
}

/**
 * 登出处理
 * 清除用户状态、权限状态和路由状态，然后跳转到登录页
 */
async function handleLogout() {
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

// 监听路由变化，更新选中的菜单项和打开的菜单项
watch(
  () => route.path,
  (newPath) => {
    selectedKeys.value = [newPath]
    // 自动展开包含当前路由的父菜单
    const findParentPath = (routes: RouteItem[], targetPath: string): string | null => {
      for (const route of routes) {
        if (route.path === targetPath) {
          return null
        }
        if (route.children) {
          for (const child of route.children) {
            if (child.path === targetPath) {
              return route.path
            }
            const grandChild = findParentPath([child], targetPath)
            if (grandChild) {
              return route.path
            }
          }
        }
      }
      return null
    }
    const parentPath = findParentPath(accessibleRoutes.value, newPath)
    if (parentPath && !openKeys.value.includes(parentPath)) {
      openKeys.value.push(parentPath)
    }
  },
  { immediate: true }
)

// 监听折叠状态，折叠时清空 openKeys
watch(collapsed, (val) => {
  if (val) {
    openKeys.value = []
  }
})
</script>

<style scoped>
/* 侧边栏样式 */
.layout-sider {
  position: relative;
  box-shadow: 2px 0 8px 0 rgba(29, 35, 41, 0.05);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              min-width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              max-width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  height: 100%;
  flex-shrink: 0; /* 防止侧边栏被压缩 */
  overflow: hidden;
  will-change: width; /* 优化动画性能 */
}

/* 增强侧边栏过渡动画 - 确保打开和关闭都有平滑滑动 */
:deep(.ant-layout-sider) {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              min-width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              max-width 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  overflow: hidden !important;
}

:deep(.ant-layout-sider-collapsed) {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              min-width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              max-width 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  overflow: hidden !important;
}

/* 确保侧边栏内容区域也有过渡动画 */
:deep(.ant-layout-sider-children) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.sider-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Logo 区域 */
.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  gap: 12px;
}

.logo.collapsed {
  padding: 0;
  justify-content: center;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  overflow: hidden;
  border-radius: 6px;
}

.logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.logo-title {
  color: white;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 1;
  transform: translateX(0);
}

.logo.collapsed .logo-title {
  opacity: 0;
  transform: translateX(-10px);
  width: 0;
}

/* 菜单容器 */
.menu-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 8px 0;
  min-height: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-container::-webkit-scrollbar {
  width: 6px;
}

.menu-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.menu-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 用户信息区域 */
.user-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  padding: 16px;
  box-sizing: border-box;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info.collapsed {
  padding: 12px;
  justify-content: center;
  flex-direction: column;
  gap: 8px;
}

.user-avatar {
  flex-shrink: 0;
}

.user-details {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 1;
  transform: translateX(0);
}

.user-info.collapsed .user-details {
  opacity: 0;
  transform: translateX(-10px);
  width: 0;
  overflow: hidden;
  pointer-events: none;
}

.user-name {
  color: white;
  font-size: 14px;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.logout-btn {
  color: rgba(255, 255, 255, 0.85) !important;
  padding: 0;
  height: auto;
  font-size: 12px;
  width: 100%;
  text-align: left;
}

.logout-btn:hover {
  color: white !important;
  background: rgba(255, 255, 255, 0.1);
}

/* 头部样式 - 固定在顶部 */
.layout-header {
  flex-shrink: 0; /* 防止头部被压缩 */
  background: #fff;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  z-index: 1;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.trigger {
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: rgba(0, 0, 0, 0.65);
  transform: rotate(0deg);
}

.trigger:hover {
  color: #1890ff;
  transform: scale(1.1);
}

.breadcrumb {
  display: flex;
  align-items: center;
}


/* 应用容器 - 固定高度，防止浏览器滚动 */
.app-container {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
}

/* 应用布局 - 使用 Flex 布局 */
.app-layout {
  display: flex;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

/* 主布局容器 - 使用 Flex 布局 */
.main-layout {
  display: flex;
  flex-direction: column;
  flex: 1;
  height: 100%;
  overflow: hidden;
  min-width: 0; /* 防止 flex 子元素溢出 */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 内容区域 - 使用 Flex 自动填充剩余空间，成为滚动容器 */
.layout-content {
  flex: 1;
  margin: 16px;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0; /* 重要：允许 flex 子元素缩小 */
  height: 0; /* 配合 flex: 1 使用，确保正确计算高度 */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.content-wrapper {
  padding: 24px;
  background: #fff;
  min-height: 100%;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
}

/* 底部样式 - 固定在底部 */
.layout-footer {
  flex-shrink: 0; /* 防止 Footer 被压缩 */
  text-align: center;
  background: #fff;
  border-top: 1px solid #f0f0f0;
  padding: 16px 50px;
  color: rgba(0, 0, 0, 0.45);
  margin-top: auto; /* 确保 Footer 在底部 */
}

/* 菜单样式优化 */
:deep(.ant-menu) {
  border-right: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 菜单项过渡动画 */
:deep(.ant-menu-item),
:deep(.ant-menu-submenu-title) {
  margin: 4px 8px !important;
  border-radius: 4px;
  height: 40px;
  line-height: 40px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

:deep(.ant-menu-item-selected) {
  background-color: #1890ff !important;
}

:deep(.ant-menu-item-selected::after) {
  display: none;
}

:deep(.ant-menu-submenu-title) {
  padding-left: 16px !important;
}

:deep(.ant-menu-item) {
  padding-left: 16px !important;
}

:deep(.ant-menu-item-icon) {
  font-size: 16px;
}

/* 折叠状态下的菜单样式 */
:deep(.ant-menu-inline-collapsed) .ant-menu-item,
:deep(.ant-menu-inline-collapsed) .ant-menu-submenu-title {
  padding: 0 16px !important;
  text-align: center;
}

:deep(.ant-menu-inline-collapsed) .ant-menu-item-icon {
  margin-right: 0;
}
</style>
