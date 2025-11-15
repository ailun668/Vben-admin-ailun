<template>
  <div class="users-view">
    <Crud ref="crudRef" :config="userCrudConfig" />
    <AddUserDrawer
      v-if="addUserModalVisible"
      :open="addUserModalVisible"
      @cancel="addUserModalVisible = false"
      @success="handleAddUserSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { PlusOutlined, DownloadOutlined } from '@ant-design/icons-vue'
import { Button, Tag, Badge } from 'ant-design-vue'
import { Crud } from '@/components/Crud'
import type { LocalCrudConfig } from '@/components/Crud'
import AddUserDrawer from './AddUserDrawer.vue'
import { http } from '@/api/http'
import dayjs from 'dayjs'

// 组件引用
const crudRef = ref()
const addUserModalVisible = ref(false)

/**
 * 共享表单 Schema
 * ⭐ 关键点：Add 和 Edit 操作共用此 Schema
 * - ID 字段：在 Edit 时显示并设为只读，Add 时不显示
 */
const userFormSchema = [
  {
    fieldName: 'id',
    component: 'Input',
    label: '用户ID',
    componentProps: {
      disabled: true, // 始终禁用
      placeholder: '自动生成'
    }
  },
  {
    fieldName: 'username',
    component: 'Input',
    label: '用户名',
    rules: 'required',
    componentProps: {
      placeholder: '请输入用户名',
      allowClear: true
    }
  },
  {
    fieldName: 'realName',
    component: 'Input',
    label: '真实姓名',
    rules: 'required',
    componentProps: {
      placeholder: '请输入真实姓名',
      allowClear: true
    }
  },
  {
    fieldName: 'email',
    component: 'Input',
    label: '邮箱',
    rules: 'required|email',
    componentProps: {
      placeholder: '请输入邮箱',
      allowClear: true
    }
  },
  {
    fieldName: 'roles',
    component: 'Select',
    label: '角色',
    rules: 'required',
    componentProps: {
      mode: 'multiple',
      placeholder: '请选择角色',
      options: [
        { label: '管理员', value: 'admin' },
        { label: '普通用户', value: 'user' },
        { label: '编辑', value: 'editor' },
        { label: '查看者', value: 'viewer' }
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
 * 用户管理 Crud 配置
 */
const userCrudConfig = computed(() => ({
  title: '用户管理',
  pageConfig: {
    enableSearch: true,
    enableToolbar: true,
    enablePagination: true
  },
  api: '/api/user/list',
  options: {
    // 搜索表单配置
    formOptions: {
      schema: [
        {
          fieldName: 'search',
          component: 'Input',
          label: '搜索',
          componentProps: {
            placeholder: '搜索用户名、邮箱、姓名',
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
        label: '新增用户',
        component: 'Button',
        componentProps: {
          type: 'primary',
          icon: PlusOutlined
        },
        onClick: () => {
          addUserModalVisible.value = true
        }
      },
      {
        label: '导出Excel',
        component: 'Button',
        componentProps: {
          icon: DownloadOutlined
        },
        onClick: handleExportExcel
      }
    ],
    // 表格配置
    gridOptions: {
      fit: true, // 自适应列宽
      pagerConfig: {
        enabled: true,
        pageSize: 10,
        pageSizes: [5, 10, 20, 50, 100]
      },
      sortConfig: {
        remote: true,
        defaultSort: { field: 'createTime', order: 'desc' }
      },
      // 数据代理配置（使用静态模拟数据）
      proxyConfig: {
        ajax: {
          query: async ({ page }: { page: any }, formValues: any) => {
            // 使用静态模拟数据
            const mockData = generateMockUserList(100)
            
            // 搜索过滤
            let filtered = mockData
            if (formValues?.search) {
              const searchText = formValues.search.toLowerCase()
              filtered = filtered.filter(
                (u: any) =>
                  u.username.toLowerCase().includes(searchText) ||
                  u.realName.toLowerCase().includes(searchText) ||
                  u.email.toLowerCase().includes(searchText)
              )
            }
            if (formValues?.status) {
              filtered = filtered.filter((u: any) => u.status === formValues.status)
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
          field: 'username',
          title: '用户名',
          minWidth: 120,
          sortable: true,
          showOverflow: 'ellipsis'
        },
        {
          field: 'realName',
          title: '真实姓名',
          minWidth: 120,
          showOverflow: 'ellipsis'
        },
        {
          field: 'email',
          title: '邮箱',
          minWidth: 180,
          showOverflow: 'ellipsis'
        },
        {
          field: 'roles',
          title: '角色',
          minWidth: 150,
          slots: {
            default: ({ row }: any) => {
              return h('div', { style: 'display: flex; gap: 4px; justify-content: center;' },
                row.roles.map((role: string) =>
                  h(Tag, { color: 'blue', key: role }, () => role)
                )
              )
            }
          }
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
          minWidth: 120,
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
                title: '编辑用户',
                width: 600,
                maskClosable: true
              },
              formProps: {
                schema: [...userFormSchema], // 使用共享 Schema
                labelWidth: 100,
                layout: 'horizontal'
              },
              // ⭐ 使用 apiConfig 模式
              apiConfig: {
                url: '/api/user/{id}',
                method: 'PATCH'
              },
              hooks: {
                onOpened: async ({ context, instance }: { context: any; instance: any }) => {
                  // 数据回显：直接使用 context 数据
                  const data = { ...context }
                  instance.setValues(data)
                },
                beforeSubmit: (values: any) => {
                  // 提交前数据转换
                  return {
                    id: values.id,
                    username: values.username,
                    realName: values.realName,
                    email: values.email,
                    roles: values.roles,
                    status: values.status
                  }
                },
                onSubmitSuccess: () => {
                  message.success('用户更新成功')
                  // 刷新表格
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
 * 生成模拟用户列表数据
 */
function generateMockUserList(count: number = 100) {
  const statuses = ['active', 'inactive'] as const
  const rolesList = [['admin'], ['user'], ['user', 'editor'], ['viewer']]
  const users = []

  for (let i = 1; i <= count; i++) {
    users.push({
      id: `${i}`,
      username: `user${i}`,
      realName: `用户${i}`,
      email: `user${i}@example.com`,
      avatar: 'https://avatars.githubusercontent.com/u/120364369?s=200&v=4',
      roles: rolesList[i % rolesList.length],
      status: statuses[i % 2],
      createTime: dayjs().subtract(Math.floor(Math.random() * 30), 'day').format('YYYY-MM-DD HH:mm:ss'),
      permissions: i % 2 === 0 ? ['user:view', 'user:edit'] : ['user:view']
    })
  }

  return users
}

/**
 * 打开新增用户弹窗
 */
function openAddUserModal() {
  addUserModalVisible.value = true
}

/**
 * 新增用户成功回调
 */
function handleAddUserSuccess() {
  addUserModalVisible.value = false
  // 刷新表格
  if (crudRef.value) {
    crudRef.value.reload()
  }
}

/**
 * 删除用户
 */
function handleDelete(row: any) {
  Modal.confirm({
    title: '确认删除',
    content: `是否确认删除用户 "${row.realName}"?`,
    okText: '确认',
    cancelText: '取消',
    onOk: async () => {
      try {
        // 模拟删除 API 调用
        await new Promise(resolve => setTimeout(resolve, 500))
        message.success('用户已删除')
        // 刷新表格
        if (crudRef.value) {
          crudRef.value.reload()
        }
      } catch (error) {
        message.error('删除失败')
      }
    }
  })
}

/**
 * 导出 Excel
 */
function handleExportExcel() {
  message.info('导出功能开发中...')
  // TODO: 实现 Excel 导出功能
}
</script>

<style scoped>
.users-view {
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

