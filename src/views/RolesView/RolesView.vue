<template>
  <div class="roles-view">
    <Crud ref="crudRef" :config="roleCrudConfig" />
    <AddRoleDrawer
      :open="addRoleModalVisible"
      @cancel="addRoleModalVisible = false"
      @success="handleAddRoleSuccess"
    />
  </div>
</template>

<script setup lang="ts">
/**
 * @fileoverview 角色管理页面
 * @author 开发团队
 * @date 2025-01-15
 */

import { ref, computed, h } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { Tag, Badge } from 'ant-design-vue'
import { Crud } from '@/components/Crud'
import type { LocalCrudConfig } from '@/components/Crud'
import AddRoleDrawer from './AddRoleDrawer.vue'
import dayjs from 'dayjs'

// 组件引用
const crudRef = ref()
const addRoleModalVisible = ref(false)

/**
 * 共享表单 Schema
 * ⭐ 关键点：Add 和 Edit 操作共用此 Schema
 * - ID 字段：在 Edit 时显示并设为只读，Add 时不显示
 */
const roleFormSchema = [
  {
    fieldName: 'id',
    component: 'Input',
    label: '角色ID',
    componentProps: {
      disabled: true,
      placeholder: '自动生成'
    }
  },
  {
    fieldName: 'name',
    component: 'Input',
    label: '角色名称',
    rules: 'required',
    componentProps: {
      placeholder: '请输入角色名称（如：管理员）',
      allowClear: true
    }
  },
  {
    fieldName: 'code',
    component: 'Input',
    label: '角色代码',
    rules: 'required',
    componentProps: {
      placeholder: '请输入角色代码（如：admin）',
      allowClear: true
    }
  },
  {
    fieldName: 'description',
    component: 'Input',
    label: '角色描述',
    componentProps: {
      placeholder: '请输入角色描述',
      allowClear: true
    }
  },
  {
    fieldName: 'permissions',
    component: 'Select',
    label: '权限',
    rules: 'required',
    componentProps: {
      mode: 'multiple',
      placeholder: '请选择权限',
      options: [
        { label: 'user.view', value: 'user.view' },
        { label: 'user.create', value: 'user.create' },
        { label: 'user.edit', value: 'user.edit' },
        { label: 'user.delete', value: 'user.delete' },
        { label: 'role.view', value: 'role.view' },
        { label: 'role.create', value: 'role.create' },
        { label: 'role.edit', value: 'role.edit' },
        { label: 'role.delete', value: 'role.delete' },
        { label: 'permission.view', value: 'permission.view' },
        { label: 'permission.create', value: 'permission.create' },
        { label: 'permission.edit', value: 'permission.edit' },
        { label: 'permission.delete', value: 'permission.delete' }
      ],
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
 * 生成模拟角色列表数据
 */
function generateMockRoleList(count: number = 25) {
  const statuses = ['active', 'inactive'] as const
  const permissionGroups = [
    ['user.view', 'user.create', 'user.edit', 'user.delete', 'role.view', 'role.create', 'role.edit', 'role.delete', 'permission.view', 'permission.create', 'permission.edit', 'permission.delete'],
    ['user.view', 'user.create', 'user.edit'],
    ['user.view'],
    ['user.view', 'role.view', 'permission.view'],
    ['user.view', 'user.edit', 'role.view']
  ]
  
  const roles = []
  const roleNames = [
    { name: '管理员', code: 'admin' },
    { name: '普通用户', code: 'user' },
    { name: '编辑', code: 'editor' },
    { name: '查看者', code: 'viewer' },
    { name: '审核员', code: 'auditor' },
    { name: '运营', code: 'operator' },
    { name: '财务', code: 'finance' },
    { name: '客服', code: 'support' }
  ]

  for (let i = 1; i <= count; i++) {
    const roleName = roleNames[i % roleNames.length]!
    const permissions = permissionGroups[i % permissionGroups.length]!
    roles.push({
      id: `${i}`,
      name: `${roleName.name}${i > roleNames.length ? ` ${Math.floor(i / roleNames.length)}` : ''}`,
      code: `${roleName.code}${i > roleNames.length ? i : ''}`,
      description: `${roleName.name}角色，拥有相关权限`,
      permissions: permissions,
      userCount: Math.floor(Math.random() * 50) + 1,
      status: statuses[i % 2],
      createTime: dayjs()
        .subtract(Math.floor(Math.random() * 90), 'day')
        .format('YYYY-MM-DD HH:mm:ss'),
      updateTime: dayjs()
        .subtract(Math.floor(Math.random() * 30), 'day')
        .format('YYYY-MM-DD HH:mm:ss')
    })
  }

  return roles
}

/**
 * 角色管理 Crud 配置
 */
const roleCrudConfig = computed<LocalCrudConfig>(() => ({
  title: '角色管理',
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
            placeholder: '搜索角色名称、代码、描述',
            allowClear: true
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
        label: '新增角色',
        component: 'Button',
        componentProps: {
          type: 'primary',
          icon: PlusOutlined
        },
        onClick: () => {
          addRoleModalVisible.value = true
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
        defaultSort: { field: 'createTime', order: 'desc' as const }
      },
      // 数据代理配置
      proxyConfig: {
        ajax: {
          query: async ({ page }: { page: any }, formValues: any) => {
            const mockData = generateMockRoleList(25)
            
            // 搜索过滤
            let filtered = mockData
            if (formValues?.search) {
              const searchText = formValues.search.toLowerCase()
              filtered = filtered.filter(
                (r: any) =>
                  r.name.toLowerCase().includes(searchText) ||
                  r.code.toLowerCase().includes(searchText) ||
                  r.description.toLowerCase().includes(searchText)
              )
            }
            if (formValues?.status) {
              filtered = filtered.filter((r: any) => r.status === formValues.status)
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
          title: '角色名称',
          minWidth: 120,
          sortable: true,
          showOverflow: 'ellipsis'
        },
        {
          field: 'code',
          title: '角色代码',
          minWidth: 120,
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
          field: 'permissions',
          title: '权限数',
          minWidth: 100,
          slots: {
            default: ({ row }: any) => {
              return h('span', row.permissions?.length || 0)
            }
          }
        },
        {
          field: 'userCount',
          title: '用户数',
          minWidth: 100,
          sortable: true
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
                title: '编辑角色',
                width: 600,
                maskClosable: true
              },
              formProps: {
                schema: [...roleFormSchema],
                labelWidth: 100,
                layout: 'horizontal'
              },
              // ⭐ 使用 apiConfig 模式
              apiConfig: {
                url: '/api/role/{id}',
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
                    permissions: values.permissions,
                    status: values.status
                  }
                },
                onSubmitSuccess: () => {
                  message.success('角色更新成功')
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
 * 新增角色成功回调
 */
function handleAddRoleSuccess() {
  addRoleModalVisible.value = false
  if (crudRef.value) {
    crudRef.value.reload()
  }
}

/**
 * 删除角色
 */
function handleDelete(row: any) {
  Modal.confirm({
    title: '确认删除',
    content: `是否确认删除角色 "${row.name}"?`,
    okText: '确认',
    cancelText: '取消',
    onOk: async () => {
      try {
        await new Promise(resolve => setTimeout(resolve, 500))
        message.success('角色已删除')
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
.roles-view {
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

