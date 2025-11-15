<template>
  <div class="permissions-view">
    <Crud ref="crudRef" :config="permissionCrudConfig" />
    <AddPermissionDrawer
      v-if="addPermissionModalVisible"
      :open="addPermissionModalVisible"
      @cancel="addPermissionModalVisible = false"
      @success="handleAddPermissionSuccess"
    />
  </div>
</template>

<script setup lang="ts">
/**
 * @fileoverview 权限管理页面
 * @author 开发团队
 * @date 2025-01-15
 */

import { ref, computed, h } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { Badge } from 'ant-design-vue'
import { Crud } from '@/components/Crud'
import type { LocalCrudConfig } from '@/components/Crud'
import AddPermissionDrawer from './AddPermissionDrawer.vue'
import dayjs from 'dayjs'

// 组件引用
const crudRef = ref()
const addPermissionModalVisible = ref(false)

/**
 * 共享表单 Schema
 * ⭐ 关键点：Add 和 Edit 操作共用此 Schema
 */
const permissionFormSchema = [
  {
    fieldName: 'id',
    component: 'Input',
    label: '权限ID',
    componentProps: {
      disabled: true,
      placeholder: '自动生成'
    }
  },
  {
    fieldName: 'name',
    component: 'Input',
    label: '权限名称',
    rules: 'required',
    componentProps: {
      placeholder: '请输入权限名称（如：user.view）',
      allowClear: true
    }
  },
  {
    fieldName: 'code',
    component: 'Input',
    label: '权限代码',
    rules: 'required',
    componentProps: {
      placeholder: '请输入权限代码（如：user.view）',
      allowClear: true
    }
  },
  {
    fieldName: 'description',
    component: 'Input',
    label: '权限描述',
    componentProps: {
      placeholder: '请输入权限描述',
      allowClear: true
    }
  },
  {
    fieldName: 'resource',
    component: 'Select',
    label: '资源',
    rules: 'required',
    componentProps: {
      placeholder: '请选择资源',
      options: [
        { label: 'user', value: 'user' },
        { label: 'role', value: 'role' },
        { label: 'permission', value: 'permission' },
        { label: 'dashboard', value: 'dashboard' },
        { label: 'settings', value: 'settings' }
      ],
      allowClear: true
    }
  },
  {
    fieldName: 'action',
    component: 'Select',
    label: '操作',
    rules: 'required',
    componentProps: {
      placeholder: '请选择操作',
      options: [
        { label: 'view', value: 'view' },
        { label: 'create', value: 'create' },
        { label: 'edit', value: 'edit' },
        { label: 'delete', value: 'delete' },
        { label: 'export', value: 'export' },
        { label: 'import', value: 'import' }
      ],
      allowClear: true
    }
  },
  {
    fieldName: 'category',
    component: 'Input',
    label: '分类',
    componentProps: {
      placeholder: '请输入分类（如：用户管理）',
      allowClear: true
    }
  },
  {
    fieldName: 'status',
    component: 'Select',
    label: '状态',
    rules: 'required',
    componentProps: {
      placeholder: '请选择状态',
      options: [
        { label: '活跃', value: 'active' },
        { label: '停用', value: 'inactive' }
      ]
    }
  }
]

/**
 * 生成模拟权限列表数据
 */
function generateMockPermissionList(count: number = 35) {
  const statuses = ['active', 'inactive'] as const
  const resources = ['user', 'role', 'permission', 'dashboard', 'settings']
  const actions = ['view', 'create', 'edit', 'delete', 'export', 'import']
  const categories = ['用户管理', '角色管理', '权限管理', '仪表盘', '系统设置']
  
  const permissions = []
  let id = 1

  // 为每个资源生成常见操作
  resources.forEach((resource, resourceIndex) => {
    const category = categories[resourceIndex] || '其他'
    actions.forEach((action) => {
      if (id > count) return
      
      const name = `${resource}.${action}`
      permissions.push({
        id: `${id}`,
        name: name,
        code: name,
        description: `${category} - ${action === 'view' ? '查看' : action === 'create' ? '创建' : action === 'edit' ? '编辑' : action === 'delete' ? '删除' : action === 'export' ? '导出' : '导入'}`,
        resource: resource,
        action: action,
        category: category,
        status: statuses[id % 2],
        createTime: dayjs()
          .subtract(Math.floor(Math.random() * 120), 'day')
          .format('YYYY-MM-DD HH:mm:ss'),
        updateTime: dayjs()
          .subtract(Math.floor(Math.random() * 30), 'day')
          .format('YYYY-MM-DD HH:mm:ss')
      })
      id++
    })
  })

  return permissions
}

/**
 * 权限管理 Crud 配置
 */
const permissionCrudConfig = computed<LocalCrudConfig>(() => ({
  title: '权限管理',
  pageConfig: {
    enableSearch: true,
    enableToolbar: true,
    enablePagination: true
  },
  options: {
    // 搜索表单配置
    formOptions: {
      schema: [
        {
          fieldName: 'search',
          component: 'Input',
          label: '搜索',
          componentProps: {
            placeholder: '搜索权限名称、代码、描述',
            allowClear: true
          }
        },
        {
          fieldName: 'resource',
          component: 'Select',
          label: '资源',
          componentProps: {
            placeholder: '选择资源',
            allowClear: true,
            options: [
              { label: 'user', value: 'user' },
              { label: 'role', value: 'role' },
              { label: 'permission', value: 'permission' },
              { label: 'dashboard', value: 'dashboard' },
              { label: 'settings', value: 'settings' }
            ]
          }
        },
        {
          fieldName: 'action',
          component: 'Select',
          label: '操作',
          componentProps: {
            placeholder: '选择操作',
            allowClear: true,
            options: [
              { label: 'view', value: 'view' },
              { label: 'create', value: 'create' },
              { label: 'edit', value: 'edit' },
              { label: 'delete', value: 'delete' },
              { label: 'export', value: 'export' },
              { label: 'import', value: 'import' }
            ]
          }
        },
        {
          fieldName: 'status',
          component: 'Select',
          label: '状态',
          componentProps: {
            placeholder: '选择状态',
            allowClear: true,
            options: [
              { label: '活跃', value: 'active' },
              { label: '停用', value: 'inactive' }
            ]
          }
        }
      ],
      labelWidth: 80,
      layout: 'inline'
    },
    // 工具栏操作
    toolbarActions: [
      {
        label: '新增权限',
        component: 'Button',
        componentProps: {
          type: 'primary',
          icon: PlusOutlined
        },
        onClick: () => {
          addPermissionModalVisible.value = true
        }
      }
    ],
    // 表格配置
    gridOptions: {
      fit: true,
      pagerConfig: {
        enabled: true,
        pageSize: 10,
        pageSizes: [5, 10, 20, 50, 100]
      },
      sortConfig: {
        remote: true,
        defaultSort: { field: 'createTime', order: 'desc' }
      },
      // 数据代理配置
      proxyConfig: {
        ajax: {
          query: async ({ page }: { page: any }, formValues: any) => {
            const mockData = generateMockPermissionList(35)
            
            // 搜索过滤
            let filtered = mockData
            if (formValues?.search) {
              const searchText = formValues.search.toLowerCase()
              filtered = filtered.filter(
                (p: any) =>
                  p.name.toLowerCase().includes(searchText) ||
                  p.code.toLowerCase().includes(searchText) ||
                  p.description.toLowerCase().includes(searchText)
              )
            }
            if (formValues?.resource) {
              filtered = filtered.filter((p: any) => p.resource === formValues.resource)
            }
            if (formValues?.action) {
              filtered = filtered.filter((p: any) => p.action === formValues.action)
            }
            if (formValues?.status) {
              filtered = filtered.filter((p: any) => p.status === formValues.status)
            }

            // 分页
            const total = filtered.length
            const start = (page.currentPage - 1) * page.pageSize
            const end = start + page.pageSize
            const list = filtered.slice(start, end)

            // 模拟网络延迟
            await new Promise(resolve => setTimeout(resolve, 300))

            return {
              items: list,
              count: total
            }
          }
        }
      },
      columns: [
        {
          field: 'id',
          title: 'ID',
          width: 80,
          sortable: true
        },
        {
          field: 'name',
          title: '权限名称',
          minWidth: 150,
          sortable: true,
          showOverflow: 'ellipsis'
        },
        {
          field: 'code',
          title: '权限代码',
          minWidth: 150,
          sortable: true,
          showOverflow: 'ellipsis'
        },
        {
          field: 'description',
          title: '描述',
          minWidth: 200,
          showOverflow: 'ellipsis'
        },
        {
          field: 'resource',
          title: '资源',
          minWidth: 100,
          sortable: true
        },
        {
          field: 'action',
          title: '操作',
          minWidth: 100,
          sortable: true
        },
        {
          field: 'category',
          title: '分类',
          minWidth: 120,
          showOverflow: 'ellipsis'
        },
        {
          field: 'status',
          title: '状态',
          minWidth: 100,
          slots: {
            default: ({ row }: any) => {
              return h(Badge, {
                status: row.status === 'active' ? 'success' : 'error',
                text: row.status === 'active' ? '活跃' : '停用'
              })
            }
          }
        },
        {
          field: 'createTime',
          title: '创建时间',
          minWidth: 160,
          sortable: true
        },
        {
          field: 'action',
          title: '操作',
          width: 150,
          fixed: 'right',
          actions: [
            {
              label: '编辑',
              component: 'Button',
              componentProps: {
                type: 'link',
                size: 'small'
              },
              useFormModal: true,
              modalType: 'drawer',
              modalProps: {
                title: '编辑权限',
                width: 600,
                maskClosable: true
              },
              formProps: {
                schema: [...permissionFormSchema],
                labelWidth: 100,
                layout: 'horizontal'
              },
              // ⭐ 使用 apiConfig 模式
              apiConfig: {
                url: '/api/permission/{id}',
                method: 'PATCH'
              },
              hooks: {
                onOpened: async ({ context, instance }: { context: any; instance: any }) => {
                  const data = { ...context }
                  instance.setValues(data)
                },
                beforeSubmit: (values: any) => {
                  return {
                    id: values.id,
                    name: values.name,
                    code: values.code,
                    description: values.description,
                    resource: values.resource,
                    action: values.action,
                    category: values.category,
                    status: values.status
                  }
                },
                onSubmitSuccess: () => {
                  message.success('权限更新成功')
                  if (crudRef.value) {
                    crudRef.value.reload()
                  }
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
              onClick: (row: any) => {
                handleDelete(row)
              }
            }
          ]
        }
      ]
    }
  }
}))

/**
 * 新增权限成功回调
 */
function handleAddPermissionSuccess() {
  addPermissionModalVisible.value = false
  if (crudRef.value) {
    crudRef.value.reload()
  }
}

/**
 * 删除权限
 */
function handleDelete(row: any) {
  Modal.confirm({
    title: '确认删除',
    content: `是否确认删除权限 "${row.name}"?`,
    okText: '确认',
    cancelText: '取消',
    onOk: async () => {
      try {
        await new Promise(resolve => setTimeout(resolve, 500))
        message.success('权限已删除')
        if (crudRef.value) {
          crudRef.value.reload()
        }
      } catch (error) {
        message.error('删除失败')
      }
    }
  })
}
</script>

<style scoped>
.permissions-view {
  padding: 16px;
}

/* Standard CSS for VxeGrid Alignment Fix */
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
</style>

