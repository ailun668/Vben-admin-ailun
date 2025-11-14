/**
 * API 响应格式
 */
export interface ApiResponse<T = any> {
  code: number
  data: T
  message: string
}

/**
 * 登录请求参数
 */
export interface LoginRequest {
  username: string
  password: string
}

/**
 * 登录响应数据
 */
export interface LoginResponse {
  token: string
  user: UserInfo
}

/**
 * 用户信息
 */
export interface UserInfo {
  id: string
  username: string
  realName: string
  email: string
  avatar: string
  roles: string[]
  permissions: string[]
}

/**
 * 路由项
 */
export interface RouteItem {
  path: string
  name: string
  component?: string
  meta?: {
    title?: string
    icon?: string
    requiresAuth?: boolean
    roles?: string[]
  }
  children?: RouteItem[]
}

/**
 * 权限项
 */
export interface PermissionItem {
  id: string
  name: string
  code: string
  type: 'menu' | 'button' | 'api'
  path?: string
}
