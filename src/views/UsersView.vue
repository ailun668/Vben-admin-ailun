<template>
  <div class="users-view">
    <a-card title="用户管理" :bordered="false">
      <!-- 搜索和工具栏 -->
      <div class="toolbar">
        <a-input-search
          v-model:value="searchText"
          placeholder="搜索用户名、邮箱、姓名"
          style="width: 250px; margin-right: 16px"
          @search="handleSearch"
          @change="handleSearch"
        />

        <a-select
          v-model:value="statusFilter"
          placeholder="选择状态"
          style="width: 150px; margin-right: 16px"
          @change="handleSearch"
          allow-clear
        >
          <a-select-option value="active">活跃</a-select-option>
          <a-select-option value="inactive">停用</a-select-option>
        </a-select>

        <a-button type="primary" style="margin-right: 8px">
          <template #icon>
            <plus-outlined />
          </template>
          新增用户
        </a-button>

        <a-button @click="handleExportExcel">
          <template #icon>
            <download-outlined />
          </template>
          导出 Excel
        </a-button>
      </div>

      <!-- VXE-Table -->
      <div class="table-wrapper">
        <vxe-table
          ref="xTable"
          :data="tableData"
          :columns="columns"
          :loading="loading"
          :pager-config="pageConfig"
          :sort-config="sortConfig"
          border="outer"
          resizable
          height="auto"
          @page-change="handlePageChange"
          @sort-change="handleSortChange"
        >
          <vxe-table-column type="seq" width="60" title="序号"></vxe-table-column>
          <vxe-table-column
            field="username"
            title="用户名"
            min-width="120"
            sortable
            show-overflow
          ></vxe-table-column>
          <vxe-table-column
            field="realName"
            title="真实名称"
            min-width="120"
            show-overflow
          ></vxe-table-column>
          <vxe-table-column
            field="email"
            title="邮箱"
            min-width="180"
            show-overflow
          ></vxe-table-column>
          <vxe-table-column field="roles" title="角色" min-width="120">
            <template #default="{ row }">
              <a-space size="small">
                <a-tag v-for="role in row.roles" :key="role" color="blue">
                  {{ role }}
                </a-tag>
              </a-space>
            </template>
          </vxe-table-column>
          <vxe-table-column field="status" title="状态" min-width="100">
            <template #default="{ row }">
              <a-badge
                :status="row.status === 'active' ? 'success' : 'error'"
                :text="row.status === 'active' ? '活跃' : '停用'"
              />
            </template>
          </vxe-table-column>
          <vxe-table-column
            field="createTime"
            title="创建时间"
            min-width="120"
            sortable
          ></vxe-table-column>
          <vxe-table-column title="操作" width="150" fixed="right">
            <template #default="{ row }">
              <a-space size="small">
                <a-button type="link" size="small" @click="handleEdit(row)">编辑</a-button>
                <a-button type="link" size="small" danger @click="handleDelete(row)">
                  删除
                </a-button>
              </a-space>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { message, Modal } from 'ant-design-vue'
import { PlusOutlined, DownloadOutlined } from '@ant-design/icons-vue'
import { http } from '@/api/http'
import type { VxeTableInstance } from 'vxe-table'

interface User {
  id: string
  username: string
  realName: string
  email: string
  roles: string[]
  status: 'active' | 'inactive'
  createTime: string
  avatar: string
  permissions: string[]
}

interface ListResponse {
  list: User[]
  page: number
  pageSize: number
  total: number
  pageCount: number
}

// 表格实例
const xTable = ref<VxeTableInstance>()

// 表格数据和配置
const tableData = ref<User[]>([])
const loading = ref(false)
const searchText = ref('')
const statusFilter = ref('')

// 分页配置
const pageConfig = reactive({
  enabled: true,
  pageSize: 10,
  currentPage: 1,
  total: 0,
  pageSizes: [5, 10, 20, 50, 100],
  layouts: [
    'PrevJump',
    'PrevPage',
    'JumpNumber',
    'NextPage',
    'NextJump',
    'Sizes',
    'Total'
  ]
})

// 排序配置
const sortConfig = reactive<any>({
  remote: true,
  defaultSort: { field: 'createTime', order: 'desc' as const }
})

// 表格列定义
const columns = [
  { type: 'seq', width: 60, title: '序号' },
  { field: 'username', title: '用户名', minWidth: 120, sortable: true },
  { field: 'realName', title: '真实名称', minWidth: 120 },
  { field: 'email', title: '邮箱', minWidth: 180 },
  { field: 'roles', title: '角色', minWidth: 120 },
  { field: 'status', title: '状态', minWidth: 100 },
  { field: 'createTime', title: '创建时间', minWidth: 120, sortable: true },
  { title: '操作', width: 150, fixed: 'right' }
]

// 加载用户列表数据
async function loadUserList(page = 1, pageSize = 10) {
  loading.value = true
  try {
    const params = {
      page,
      pageSize,
      search: searchText.value,
      status: statusFilter.value
    }

    const response = await http.get<ListResponse>('/user/list', { params })

    if (response.code === 0) {
      tableData.value = response.data.list
      pageConfig.total = response.data.total
      pageConfig.currentPage = response.data.page
      pageConfig.pageSize = response.data.pageSize
    } else {
      message.error(response.message || '加载用户列表失败')
    }
  } catch (error) {
    message.error('加载用户列表失败')
    console.error('加载用户列表错误:', error)
  } finally {
    loading.value = false
  }
}

// 处理搜索
function handleSearch() {
  pageConfig.currentPage = 1
  loadUserList(1, pageConfig.pageSize)
}

// 处理分页
function handlePageChange({ currentPage, pageSize }: any) {
  pageConfig.currentPage = currentPage
  pageConfig.pageSize = pageSize
  loadUserList(currentPage, pageSize)
}

// 处理排序
function handleSortChange({ field, order }: any) {
  console.log('排序:', field, order)
  // 这里可以根据排序字段和方向重新加载数据
  loadUserList(pageConfig.currentPage, pageConfig.pageSize)
}

// 编辑用户
function handleEdit(row: User) {
  message.info(`编辑用户: ${row.username}`)
}

// 删除用户
function handleDelete(row: User) {
  Modal.confirm({
    title: '确认删除',
    content: `是否确认删除用户 "${row.realName}"?`,
    okText: '确认',
    cancelText: '取消',
    onOk() {
      message.success('用户已删除')
    }
  })
}

// 导出 Excel
async function handleExportExcel() {
  const table = xTable.value
  if (table) {
    const exportApi = table.exportData({
      filename: `用户列表_${new Date().toISOString().split('T')[0]}.xlsx`,
      sheetName: '用户数据',
      isHeader: true,
      original: false
    })
    message.success('数据已导出为 Excel 文件')
  }
}

// 挂载时加载数据
onMounted(() => {
  loadUserList(1, pageConfig.pageSize)
})
</script>

<style scoped>
.users-view {
  padding: 16px;
}

.toolbar {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 8px;
}

.table-wrapper {
  margin-top: 16px;
}

:deep(.vxe-table) {
  font-size: 14px;
}

:deep(.vxe-table--header-wrapper) {
  background-color: #fafafa;
}

:deep(.vxe-table--body-wrapper) {
  max-height: calc(100vh - 400px);
}
</style>
