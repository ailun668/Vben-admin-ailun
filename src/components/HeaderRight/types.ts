/**
 * @fileoverview HeaderRight 组件类型定义
 * @author 开发团队
 * @date 2025-01-15
 */

/**
 * 通知项
 */
export interface NotificationItem {
  /** 通知 ID */
  id: string
  /** 通知类型 */
  type: 'success' | 'info' | 'warning' | 'error'
  /** 通知标题 */
  title: string
  /** 通知描述 */
  description: string
  /** 通知时间 */
  time: Date | string
  /** 是否已读 */
  read: boolean
  /** 跳转链接（可选） */
  link?: string
  /** 自定义操作（可选） */
  action?: () => void
}

