/**
 * 系统日志相关类型定义
 */

/**
 * 系统日志项
 */
export interface SysLog {
  id: string
  userId: string
  username: string
  realName: string
  operationType: string
  operationTarget: string
  operationDesc: string
  operationStatus: 'success' | 'failed'
  ipAddress: string
  ipLocation?: string          // IP归属地
  userAgent: string
  browser?: string             // 浏览器信息
  os?: string                  // 操作系统
  duration?: number            // 操作耗时（毫秒）
  startTime?: string           // 操作开始时间
  endTime?: string             // 操作结束时间
  createTime: string           // 创建时间（记录时间）
  remark?: string
}

/**
 * 操作类型枚举
 */
export enum OperationType {
  CREATE = 'create',
  UPDATE = 'update',
  DELETE = 'delete',
  QUERY = 'query',
  EXPORT = 'export',
  IMPORT = 'import',
  LOGIN = 'login',
  LOGOUT = 'logout'
}

/**
 * 操作状态枚举
 */
export enum OperationStatus {
  SUCCESS = 'success',
  FAILED = 'failed'
}

/**
 * 操作目标枚举
 */
export enum OperationTarget {
  USER = 'user',
  ROLE = 'role',
  PERMISSION = 'permission',
  SYSTEM = 'system',
  DATA = 'data'
}

/**
 * 操作类型选项
 */
export const operationTypeOptions = [
  { label: '新增', value: OperationType.CREATE },
  { label: '编辑', value: OperationType.UPDATE },
  { label: '删除', value: OperationType.DELETE },
  { label: '查询', value: OperationType.QUERY },
  { label: '导出', value: OperationType.EXPORT },
  { label: '导入', value: OperationType.IMPORT },
  { label: '登录', value: OperationType.LOGIN },
  { label: '登出', value: OperationType.LOGOUT }
]

/**
 * 操作状态选项
 */
export const operationStatusOptions = [
  { label: '成功', value: OperationStatus.SUCCESS },
  { label: '失败', value: OperationStatus.FAILED }
]

/**
 * 操作目标选项
 */
export const operationTargetOptions = [
  { label: '用户', value: OperationTarget.USER },
  { label: '角色', value: OperationTarget.ROLE },
  { label: '权限', value: OperationTarget.PERMISSION },
  { label: '系统', value: OperationTarget.SYSTEM },
  { label: '数据', value: OperationTarget.DATA }
]
