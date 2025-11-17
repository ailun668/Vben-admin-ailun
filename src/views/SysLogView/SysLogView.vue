<template>
  <div class="syslog-view">
    <Crud ref="crudRef" :config="syslogCrudConfig" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { message, Modal } from 'ant-design-vue'
import dayjs from 'dayjs'
import { Crud } from '@/components/Crud'
import type { LocalCrudConfig } from '@/components/Crud'
import { http } from '@/api/http'
import type { SysLog } from './types'
import {
  operationTypeOptions,
  operationStatusOptions,
  operationTargetOptions
} from './types'
import {
  DeleteOutlined,
  DownloadOutlined
} from '@ant-design/icons-vue'

// ============ Ref 定义 ============
const crudRef = ref()

// ============ 模拟数据生成函数 ============
/**
 * 生成模拟系统日志数据
 * @param count 生成数量
 * @returns 系统日志列表
 */
function generateMockSysLogList(count: number = 100): SysLog[] {
  const operationTypes = ['create', 'update', 'delete', 'query', 'export', 'import', 'login', 'logout']
  const operationTargets = ['user', 'role', 'permission', 'system', 'data']
  const operationStatus = ['success', 'failed']
  const ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102', '10.0.0.1', '10.0.0.2']
  const ipLocations = [
    '中国 北京市 海淀区',
    '中国 上海市 浦东新区',
    '中国 广东省 深圳市',
    '日本 东京都 千代田区',
    '美国 加利福尼亚州 旧金山'
  ]
  const browsers = ['Chrome 120', 'Firefox 121', 'Safari 17', 'Edge 120']
  const osList = ['Windows 11', 'macOS 14', 'Ubuntu 22.04', 'iOS 17', 'Android 14']
  const userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
  ]

  const logs: SysLog[] = []

  for (let i = 1; i <= count; i++) {
    const createDate = dayjs().subtract(Math.floor(Math.random() * 30), 'day')
    const opType = operationTypes[Math.floor(Math.random() * operationTypes.length)]
    const opTarget = operationTargets[Math.floor(Math.random() * operationTargets.length)]
    const duration = Math.floor(Math.random() * 5000) + 10 // 10-5010ms
    
    // 计算开始时间和结束时间
    const startTime = createDate.subtract(Math.floor(Math.random() * 10), 'second')
    const endTime = startTime.add(duration, 'millisecond')
    
    logs.push({
      id: `${i}`,
      userId: `user${Math.floor(i / 10) + 1}`,
      username: `admin`,
      realName: `用户${Math.floor(i / 10) + 1}`,
      operationType: opType,
      operationTarget: opTarget,
      operationDesc: `${opTarget === 'user' ? '用户管理' : opTarget === 'role' ? '角色管理' : opTarget === 'permission' ? '权限管理' : opTarget === 'system' ? '系统设置' : '数据管理'} API`,
      operationStatus: operationStatus[Math.floor(Math.random() * operationStatus.length)] as 'success' | 'failed',
      ipAddress: ips[Math.floor(Math.random() * ips.length)],
      ipLocation: ipLocations[Math.floor(Math.random() * ipLocations.length)],
      userAgent: userAgents[Math.floor(Math.random() * userAgents.length)],
      browser: browsers[Math.floor(Math.random() * browsers.length)],
      os: osList[Math.floor(Math.random() * osList.length)],
      duration: duration,
      startTime: startTime.format('YYYY-MM-DD HH:mm:ss'),
      endTime: endTime.format('YYYY-MM-DD HH:mm:ss'),
      createTime: createDate.format('YYYY-MM-DD HH:mm:ss'),
      remark: i % 5 === 0 ? '操作备注说明' : undefined
    })
  }

  return logs
}

// ============ 共享表单 Schema ============
const syslogFormSchema = [
  {
    fieldName: 'id',
    component: 'Input',
    label: '日志ID',
    componentProps: {
      disabled: true,
      placeholder: '自动生成'
    }
  },
  {
    fieldName: 'username',
    component: 'Input',
    label: '操作用户',
    rules: 'required',
    componentProps: {
      placeholder: '请输入用户名',
      disabled: true
    }
  },
  {
    fieldName: 'realName',
    component: 'Input',
    label: '真实姓名',
    componentProps: {
      placeholder: '请输入真实姓名',
      disabled: true
    }
  },
  {
    fieldName: 'operationType',
    component: 'Select',
    label: '操作类型',
    rules: 'required',
    componentProps: {
      placeholder: '请选择操作类型',
      options: operationTypeOptions,
      disabled: true
    }
  },
  {
    fieldName: 'operationTarget',
    component: 'Select',
    label: '操作目标',
    rules: 'required',
    componentProps: {
      placeholder: '请选择操作目标',
      options: operationTargetOptions,
      disabled: true
    }
  },
  {
    fieldName: 'operationDesc',
    component: 'TextArea',
    label: '操作描述',
    componentProps: {
      placeholder: '请输入操作描述',
      disabled: true,
      rows: 3
    }
  },
  {
    fieldName: 'operationStatus',
    component: 'Select',
    label: '操作状态',
    rules: 'required',
    componentProps: {
      placeholder: '请选择操作状态',
      options: operationStatusOptions,
      disabled: true
    }
  },
  {
    fieldName: 'ipAddress',
    component: 'Input',
    label: '操作IP',
    componentProps: {
      placeholder: '请输入操作IP',
      disabled: true
    }
  },
  {
    fieldName: 'startTime',
    component: 'Input',
    label: '开始时间',
    componentProps: {
      placeholder: '操作开始时间',
      disabled: true
    }
  },
  {
    fieldName: 'endTime',
    component: 'Input',
    label: '结束时间',
    componentProps: {
      placeholder: '操作结束时间',
      disabled: true
    }
  },
  {
    fieldName: 'duration',
    component: 'Input',
    label: '操作耗时',
    componentProps: {
      placeholder: '操作耗时',
      disabled: true
    }
  },
  {
    fieldName: 'createTime',
    component: 'Input',
    label: '记录时间',
    componentProps: {
      placeholder: '日志记录时间',
      disabled: true
    }
  },
  {
    fieldName: 'remark',
    component: 'TextArea',
    label: '备注',
    componentProps: {
      placeholder: '请输入备注',
      rows: 2,
      disabled: true
    }
  }
]

// ============ CRUD 配置 ============
const syslogCrudConfig = computed<LocalCrudConfig>(() => ({
  title: '系统日志',
  pageConfig: {
    enableSearch: true,
    enableToolbar: true,
    enablePagination: true
  },
  options: {
    formOptions: {
      schema: [
        {
          fieldName: 'search',
          component: 'Input',
          label: '搜索',
          componentProps: {
            placeholder: '搜索用户名、IP、操作描述'
          }
        },
        {
          fieldName: 'timeRange',
          component: 'RangePicker',
          label: '操作时间',
          componentProps: {
            placeholder: ['选择开始时间', '选择结束时间'],
            showTime: true,
            format: 'YYYY-MM-DD HH:mm:ss',
            valueFormat: 'YYYY-MM-DD HH:mm:ss',
            allowClear: true,
            style: { width: '100%' },
            separator: '至',
            ranges: {
              '今天': [dayjs().startOf('day'), dayjs().endOf('day')],
              '昨天': [dayjs().subtract(1, 'day').startOf('day'), dayjs().subtract(1, 'day').endOf('day')],
              '最近7天': [dayjs().subtract(7, 'day').startOf('day'), dayjs().endOf('day')],
              '最近30天': [dayjs().subtract(30, 'day').startOf('day'), dayjs().endOf('day')],
              '本月': [dayjs().startOf('month'), dayjs().endOf('month')],
              '上月': [dayjs().subtract(1, 'month').startOf('month'), dayjs().subtract(1, 'month').endOf('month')]
            },
            disabledDate: (current: any) => {
              // 禁用未来日期
              return current && current > dayjs().endOf('day')
            }
          }
        },
        {
          fieldName: 'operationType',
          component: 'Select',
          label: '操作类型',
          componentProps: {
            placeholder: '请选择操作类型',
            options: operationTypeOptions,
            allowClear: true
          }
        },
        {
          fieldName: 'operationStatus',
          component: 'Select',
          label: '操作状态',
          componentProps: {
            placeholder: '请选择操作状态',
            options: operationStatusOptions,
            allowClear: true
          }
        },
        {
          fieldName: 'operationTarget',
          component: 'Select',
          label: '操作目标',
          componentProps: {
            placeholder: '请选择操作目标',
            options: operationTargetOptions,
            allowClear: true
          }
        }
      ]
    },
    toolbarActions: [
      {
        label: '导出Excel',
        component: 'Button',
        componentProps: {
          icon: DownloadOutlined
        },
        onClick: handleExportExcel
      }
    ],
    gridOptions: {
      columns: [
        {
          field: 'createTime',
          title: '操作时间',
          minWidth: 160,
          showOverflow: 'ellipsis',
          sortable: true
        },
        {
          field: 'username',
          title: '操作用户',
          minWidth: 120,
          showOverflow: 'ellipsis'
        },
        {
          field: 'operationDesc',
          title: '操作对象',
          minWidth: 180,
          showOverflow: 'ellipsis'
        },
        {
          field: 'ipAddress',
          title: 'IP地址',
          minWidth: 140,
          showOverflow: 'ellipsis',
          formatter: ({ row }: { row: SysLog }) => {
            return row.ipLocation 
              ? `${row.ipAddress} (${row.ipLocation})`
              : row.ipAddress
          }
        },
        {
          field: 'userAgent',
          title: '操作系统/浏览器',
          minWidth: 200,
          showOverflow: 'ellipsis',
          formatter: ({ row }: { row: SysLog }) => {
            const parts = []
            if (row.os) parts.push(row.os)
            if (row.browser) parts.push(row.browser)
            return parts.length > 0 ? parts.join(' / ') : row.userAgent
          }
        },
        {
          field: 'operationType',
          title: '类型',
          minWidth: 100,
          showOverflow: 'ellipsis',
          formatter: ({ cellValue }: { cellValue: string }) => {
            const option = operationTypeOptions.find(
              (opt) => opt.value === cellValue
            )
            return option?.label || cellValue
          }
        },
        {
          field: 'operationStatus',
          title: '状态',
          minWidth: 80,
          showOverflow: 'ellipsis',
          formatter: ({ cellValue }: { cellValue: string }) => {
            const icon = cellValue === 'success' 
              ? '<span class="status-dot status-success"></span>'
              : '<span class="status-dot status-failed"></span>'
            const text = cellValue === 'success' ? '成功' : '失败'
            return `${icon} ${text}`
          }
        },
        {
          field: 'duration',
          title: '耗时',
          minWidth: 100,
          showOverflow: 'ellipsis',
          formatter: ({ cellValue }: { cellValue: number }) => {
            if (!cellValue) return '-'
            if (cellValue < 1000) return `${cellValue}ms`
            return `${(cellValue / 1000).toFixed(2)}s`
          }
        },
        {
          field: 'action',
          title: '操作',
          width: 180,
          fixed: 'right',
          actions: [
            {
              label: '查看详情',
              component: 'Button',
              componentProps: {
                type: 'link',
                size: 'small'
              },
              useFormModal: true,
              modalType: 'drawer',
              modalProps: {
                title: '查看日志详情',
                width: 700,
                maskClosable: true,
                destroyOnClose: false
              },
              formProps: {
                schema: [...syslogFormSchema],
                labelWidth: 100,
                layout: 'horizontal'
              },
              hooks: {
                /**
                 * 数据回显：从后端数据转换为表单数据
                 * @description 当抽屉打开时，将当前行数据设置到表单中
                 */
                onOpened: async ({ context, instance }: { context: any; instance: any }) => {
                  const data = { ...context }
                  
                  // 格式化耗时显示
                  if (data.duration) {
                    if (data.duration < 1000) {
                      data.duration = `${data.duration}ms`
                    } else {
                      data.duration = `${(data.duration / 1000).toFixed(2)}s`
                    }
                  }
                  
                  // 设置表单值
                  instance.setValues(data)
                }
              }
            },
            {
              label: '删除',
              component: 'Button',
              componentProps: {
                type: 'link',
                size: 'small',
                danger: true
              },
              onClick: (row: SysLog) => {
                handleDelete(row)
              }
            }
          ]
        }
      ],
      proxyConfig: {
        ajax: {
          query: async ({ page }: { page: any }, formValues: any) => {
            // 获取模拟数据
            const mockData = generateMockSysLogList(200)

            // 搜索过滤
            let filtered = mockData
            if (formValues?.search) {
              const searchText = formValues.search.toLowerCase()
              filtered = filtered.filter(
                (log: SysLog) =>
                  log.username.toLowerCase().includes(searchText) ||
                  log.ipAddress.toLowerCase().includes(searchText) ||
                  log.operationDesc.toLowerCase().includes(searchText)
              )
            }

            // 操作类型过滤
            if (formValues?.operationType) {
              filtered = filtered.filter(
                (log: SysLog) => log.operationType === formValues.operationType
              )
            }

            // 操作状态过滤
            if (formValues?.operationStatus) {
              filtered = filtered.filter(
                (log: SysLog) => log.operationStatus === formValues.operationStatus
              )
            }

            // 操作目标过滤
            if (formValues?.operationTarget) {
              filtered = filtered.filter(
                (log: SysLog) => log.operationTarget === formValues.operationTarget
              )
            }

            // 操作时间区间过滤
            if (formValues?.timeRange && formValues.timeRange.length === 2) {
              const [startTime, endTime] = formValues.timeRange
              filtered = filtered.filter((log: SysLog) => {
                const logTime = dayjs(log.createTime)
                return logTime.isAfter(dayjs(startTime)) && logTime.isBefore(dayjs(endTime))
              })
            }

            // 分页处理
            const total = filtered.length
            const start = (page.currentPage - 1) * page.pageSize
            const end = start + page.pageSize
            const list = filtered.slice(start, end)

            // 模拟网络延迟
            await new Promise((resolve) => setTimeout(resolve, 300))

            return {
              items: list,
              count: total
            }
          }
        }
      },
      pagerConfig: {
        enabled: true,
        pageSize: 10,
        pageSizes: [5, 10, 20, 50, 100]
      }
    }
  }
}))

// ============ 事件处理 ============

/**
 * 导出Excel
 */
function handleExportExcel() {
  if (!crudRef.value) {
    message.error('表格组件未初始化')
    return
  }

  try {
    // 调用VXE Table的导出功能
    crudRef.value.$refs.gridRef?.$refs.gridBody.exportData({
      filename: `系统日志_${dayjs().format('YYYY-MM-DD')}.xlsx`
    })
    message.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    message.error('导出失败，请重试')
  }
}

/**
 * 删除日志
 */
function handleDelete(row: SysLog) {
  Modal.confirm({
    title: '确认删除',
    content: `是否确认删除该条日志记录？`,
    okText: '确认',
    cancelText: '取消',
    onOk: async () => {
      try {
        // 模拟删除API调用
        // await http.delete(`/api/syslog/${row.id}`)
        message.success('日志已删除')
        // 刷新表格
        if (crudRef.value) {
          crudRef.value.reload()
        }
      } catch (error) {
        console.error('删除失败:', error)
        message.error('删除失败，请重试')
      }
    }
  })
}
</script>

<style scoped>
/* VXE Table 对齐修复 - 标准样式 */
:deep(.vxe-table--main-wrapper table) {
  width: 100% !important;
  table-layout: fixed !important;
}

:deep(.vxe-table--header-wrapper),
:deep(.vxe-table--body-wrapper) {
  width: 100% !important;
}

:deep(.vxe-header--row) th,
:deep(.vxe-body--row) td {
  padding: 8px 16px !important;
  text-align: center !important;
}

:deep(.vxe-header--column),
:deep(.vxe-body--column) {
  box-sizing: border-box;
  height: 48px;
}

:deep(.vxe-cell) {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
}

:deep(.vxe-cell--title) {
  display: inline-flex !important;
  justify-content: center !important;
  width: 100% !important;
}

/* 页面容器 */
.syslog-view {
  padding: 16px;
}

/* 状态样式 */
:deep(.status-dot) {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
}

:deep(.status-dot.status-success) {
  background-color: #52c41a;
}

:deep(.status-dot.status-failed) {
  background-color: #ff4d4f;
}

:deep(.status-success) {
  color: #52c41a;
  font-weight: 500;
}

:deep(.status-failed) {
  color: #ff4d4f;
  font-weight: 500;
}

/* ============ 侧边栏弹窗动画优化 ============ */
/**
 * 抽屉动画优化
 * @description Drawer动画由Crud组件统一管理，这里无需额外配置
 * @reference 技术规范: 01-侧边栏弹窗动画优化.md
 * @note Crud组件已实现完整的打开/关闭动画机制，包括：
 *       1. 使用 v-if + :open 组合控制显示
 *       2. triggerDrawerClose() 实现延迟关闭
 *       3. drawer-closing-state CSS类控制关闭动画
 *       4. 0.3s 统一过渡时间和 cubic-bezier(0.4, 0, 0.2, 1) 缓动函数
 */
</style>
