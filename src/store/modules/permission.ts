import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { RouteItem } from '@/api/types'
import { useUserStore } from './user'

/**
 * 完整的路由列表（包含所有权限的路由）
 */
const ALL_ROUTES: RouteItem[] = [
  {
    path: '/',
    name: 'Home',
    component: 'HomeView',
    meta: {
      title: '首页',
      icon: 'home',
      requiresAuth: true,
      roles: ['admin', 'user']
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: 'DashboardView',
    meta: {
      title: '仪表盘',
      icon: 'dashboard',
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/users',
    name: 'Users',
    component: 'UsersView',
    meta: {
      title: '用户管理',
      icon: 'user',
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/roles',
    name: 'Roles',
    component: 'RolesView',
    meta: {
      title: '角色管理',
      icon: 'team',
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/permissions',
    name: 'Permissions',
    component: 'PermissionsView',
    meta: {
      title: '权限管理',
      icon: 'lock',
      requiresAuth: true,
      roles: ['admin']
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: 'SettingsView',
    meta: {
      title: '设置',
      icon: 'setting',
      requiresAuth: true,
      roles: ['admin', 'user']
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: 'LoginView',
    meta: {
      title: '登录',
      requiresAuth: false
    }
  }
]

export const usePermissionStore = defineStore('permission', () => {
  const routes = ref<RouteItem[]>([])
  const addedRoutes = ref<string[]>([])

  /**
   * 根据用户角色生成可访问的路由
   */
  function generateRoutes(roles: string[]): RouteItem[] {
    if (!roles || roles.length === 0) {
      return [
        {
          path: '/login',
          name: 'Login',
          component: 'LoginView',
          meta: {
            title: '登录',
            requiresAuth: false
          }
        }
      ]
    }

    // 过滤路由：根据用户角色
    const filtered = filterRoutes(ALL_ROUTES, roles)
    routes.value = filtered
    addedRoutes.value = filtered.map((r) => r.path)
    return filtered
  }

  /**
   * 过滤路由（递归处理）
   */
  function filterRoutes(routes: RouteItem[], roles: string[]): RouteItem[] {
    const res: RouteItem[] = []

    routes.forEach((route) => {
      // 检查路由是否需要身份验证
      if (route.meta?.requiresAuth === false) {
        // 登录页面等不需要验证的路由始终可访问
        res.push(route)
        return
      }

      // 检查用户是否有访问该路由的权限
      const routeRoles = route.meta?.roles
      if (!routeRoles || routeRoles.length === 0) {
        // 如果路由没有指定角色要求，则所有已登录用户可访问
        res.push(route)
        return
      }

      // 检查用户是否拥有路由要求的任一角色
      if (roles.some((role) => routeRoles.includes(role))) {
        if (route.children) {
          route.children = filterRoutes(route.children, roles)
        }
        res.push(route)
      }
    })

    return res
  }

  /**
   * 获取可访问的菜单路由（用于菜单展示）
   */
  const accessibleRoutes = computed(() => {
    return routes.value.filter((route: RouteItem) => {
      // 只返回有 title（菜单项）的路由
      return route.meta?.title
    })
  })

  /**
   * 检查路由是否可访问
   */
  function canAccessRoute(path: string): boolean {
    return addedRoutes.value.includes(path)
  }

  /**
   * 重置权限
   */
  function resetPermission() {
    routes.value = []
    addedRoutes.value = []
  }

  return {
    routes,
    addedRoutes,
    accessibleRoutes,
    generateRoutes,
    canAccessRoute,
    resetPermission
  }
})
