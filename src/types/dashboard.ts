/**
 * @fileoverview Dashboard 相关类型定义
 * @author AI Developer
 * @date 2024-01-XX
 */

/**
 * KPI 卡片数据接口
 */
export interface KPICard {
  /** 卡片名称 */
  name: string
  /** 卡片值 */
  value: string | number
  /** 趋势类型 */
  trend: 'up' | 'down'
  /** 趋势百分比 */
  trendValue: string
  /** 图标颜色 */
  iconColor: string
  /** 图标名称 */
  iconName: string
}

/**
 * 图表数据类型
 */
export interface ChartData {
  /** 折线图数据 */
  lineChart: {
    /** X 轴数据 */
    xAxis: string[]
    /** 系列数据 */
    series: Array<{
      name: string
      data: number[]
      color: string
    }>
  }
  /** 柱状图数据 */
  barChart: {
    /** X 轴数据 */
    xAxis: string[]
    /** 系列数据 */
    series: Array<{
      name: string
      data: number[]
      color: string
    }>
  }
  /** 饼图数据 */
  pieChart: Array<{
    name: string
    value: number
  }>
  /** 仪表盘数据 */
  gaugeChart: {
    value: number
    name: string
  }
}

/**
 * 进度项接口
 */
export interface ProgressItem {
  /** 项目名称 */
  name: string
  /** 进度百分比 */
  percent: number
  /** 颜色 */
  color: string
}

/**
 * 活动记录接口
 */
export interface ActivityRecord {
  /** 任务名称 */
  task: string
  /** 负责人 */
  assignee: string
  /** 截止时间 */
  deadline: string
  /** 状态 */
  status: 'active' | 'pending' | 'completed'
  /** 进度百分比 */
  progress: number
}

