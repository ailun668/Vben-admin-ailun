import { http } from './http'
import type { LoginRequest, LoginResponse, UserInfo } from './types'

/**
 * 用户相关 API
 */
export const userApi = {
  /**
   * 登录
   */
  login(params: LoginRequest) {
    return http.post<LoginResponse>('/api/user/login', params)
  },

  /**
   * 获取当前用户信息
   */
  getCurrentUser() {
    return http.get<UserInfo>('/api/user/info')
  },

  /**
   * 登出
   */
  logout() {
    return http.post('/api/user/logout')
  }
}
