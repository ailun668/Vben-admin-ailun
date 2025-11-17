<template>
  <div class="crud-container">
    <!-- 页面标题 -->
    <a-card :title="config.title" :bordered="false">
      <!-- 搜索表单 -->
      <div v-if="pageConfig.enableSearch && formFields.length > 0" class="search-form">
        <a-form :model="searchForm" layout="inline" @finish="handleSearch">
          <a-form-item
            v-for="field in formFields"
            :key="field.fieldName"
            :label="field.label"
            :name="field.fieldName"
          >
            <component
              :is="getFormComponent(field.component)"
              v-model:value="searchForm[field.fieldName]"
              v-bind="field.componentProps || {}"
              :placeholder="field.componentProps?.placeholder || `请输入${field.label}`"
            />
          </a-form-item>
          <a-form-item>
            <a-space>
              <a-button type="primary" html-type="submit">搜索</a-button>
              <a-button @click="handleReset">重置</a-button>
            </a-space>
          </a-form-item>
        </a-form>
      </div>

      <!-- 工具栏 -->
      <div v-if="pageConfig.enableToolbar && toolbarActions.length > 0" class="toolbar">
        <a-space>
          <component
            v-for="(action, index) in toolbarActions"
            :key="index"
            :is="getFormComponent(action.component)"
            v-bind="getButtonProps(action.componentProps || {})"
            @click="action.onClick"
          >
            <template v-if="hasIconSlot(action.componentProps)" #icon>
              <RenderIcon :icon="action.componentProps?.icon" />
            </template>
            {{ action.label }}
          </component>
        </a-space>
      </div>

      <!-- 表格 -->
      <div class="table-wrapper">
        <vxe-table
          ref="tableRef"
          :data="tableData"
          :loading="loading"
          border="outer"
          resizable
          :pager-config="tablePagerConfig"
          :sort-config="gridOptions.sortConfig"
          @page-change="handlePageChange"
          @sort-change="handleSortChange"
        >
          <!-- 动态渲染列 -->
          <template v-for="column in gridOptions.columns" :key="column.field">
            <!-- 操作列 -->
            <vxe-column
              v-if="column.actions && column.actions.length > 0"
              :field="column.field"
              :title="column.title"
              :width="column.width"
              :min-width="column.minWidth"
              :fixed="column.fixed"
            >
              <template #default="{ row }">
                <a-space size="small">
                  <a-button
                    v-for="(action, index) in column.actions"
                    :key="index"
                    :type="action.componentProps?.type || 'link'"
                    :size="action.componentProps?.size || 'small'"
                    :danger="action.componentProps?.danger"
                    @click="() => handleAction(action, row)"
                  >
                    {{ action.label }}
                  </a-button>
                </a-space>
              </template>
            </vxe-column>
            <!-- 有自定义插槽的列 -->
            <vxe-column
              v-else-if="column.slots?.default"
              :field="column.field"
              :title="column.title"
              :width="column.width"
              :min-width="column.minWidth"
              :sortable="column.sortable"
              :show-overflow="column.showOverflow"
              :fixed="column.fixed"
            >
              <template #default="{ row }">
                <RenderSlot :render="() => column.slots?.default?.({ row })" />
              </template>
            </vxe-column>
            <!-- 普通列 -->
            <vxe-column
              v-else
              :field="column.field"
              :title="column.title"
              :width="column.width"
              :min-width="column.minWidth"
              :sortable="column.sortable"
              :show-overflow="column.showOverflow"
              :fixed="column.fixed"
            />
          </template>
        </vxe-table>
        
        <!-- 分页器 -->
        <vxe-pager
          v-if="pageConfig.enablePagination && tablePagerConfig"
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="tablePagerConfig.pageSizes"
          :layouts="tablePagerConfig.layouts"
          @page-change="handlePageChange"
        />
      </div>
    </a-card>

    <!-- 编辑表单模态框/侧边栏 -->
    <!-- Modal 模式 -->
    <a-modal
      v-if="editModalType === 'modal'"
      v-model:open="editModalVisible"
      :title="editModalTitle"
      :width="editModalWidth"
      :confirm-loading="submitLoading"
      :mask-closable="editModalMaskClosable"
      @ok="handleEditSubmit"
      @cancel="handleDrawerClose"
    >
      <a-form
        ref="editFormRef"
        :model="editFormData"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
      >
        <a-form-item
          v-for="field in editFormSchema"
          :key="field.fieldName"
          :label="field.label"
          :name="field.fieldName"
          :rules="getFormRules(field.rules)"
        >
          <component
            :is="getFormComponent(field.component)"
            v-model:value="editFormData[field.fieldName]"
            v-bind="field.componentProps || {}"
            :disabled="field.componentProps?.disabled"
          />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- Drawer 模式 - 使用 :open 属性控制显示，确保关闭动画正常播放 -->
    <a-drawer
      :open="editModalVisible"
      :title="editModalTitle"
      :width="editDrawerWidth"
      :mask-closable="editModalMaskClosable"
      :destroy-on-close="false"
      placement="right"
      @close="handleDrawerClose"
    >
        <a-form
          ref="editFormRef"
          :model="editFormData"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 18 }"
        >
          <a-form-item
            v-for="field in editFormSchema"
            :key="field.fieldName"
            :label="field.label"
            :name="field.fieldName"
            :rules="getFormRules(field.rules)"
          >
            <component
              :is="getFormComponent(field.component)"
              v-model:value="editFormData[field.fieldName]"
              v-bind="field.componentProps || {}"
              :disabled="field.componentProps?.disabled"
            />
          </a-form-item>
        </a-form>
        <template #footer>
          <div style="text-align: right">
            <a-button style="margin-right: 8px" @click="handleDrawerClose">
              取消
            </a-button>
            <a-button type="primary" :loading="submitLoading" @click="handleEditSubmit">
              确认
            </a-button>
          </div>
        </template>
      </a-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, h, defineComponent } from 'vue'
import { message, Modal, Drawer } from 'ant-design-vue'
import {
  Input,
  InputNumber,
  Select,
  DatePicker,
  Switch,
  Button
} from 'ant-design-vue'

const { RangePicker } = DatePicker
import { PlusOutlined } from '@ant-design/icons-vue'
import type { VxeTableInstance, VxeTableProps } from 'vxe-table'
import { http } from '@/api/http'
import type { LocalCrudConfig, ActionItem } from './types'

interface Props {
  config: LocalCrudConfig
}

const props = defineProps<Props>()

// 组件引用
const tableRef = ref<VxeTableInstance>()
const editFormRef = ref()

// 状态
const loading = ref(false)
const submitLoading = ref(false)
const editModalVisible = ref(false)
const editFormData = reactive<Record<string, any>>({})
const currentEditRow = ref<any>(null)
const currentEditAction = ref<ActionItem | null>(null)

// 搜索表单数据
const searchForm = reactive<Record<string, any>>({})

// 计算属性
const pageConfig = computed(() => ({
  enableSearch: true,
  enableToolbar: true,
  enablePagination: true,
  ...props.config.pageConfig
}))

const formFields = computed(() => {
  return props.config.options.formOptions?.schema || []
})

const toolbarActions = computed(() => {
  return props.config.options.toolbarActions || []
})

const gridOptions = computed(() => props.config.options.gridOptions)

const actionColumns = computed(() => {
  return gridOptions.value.columns.filter(col => col.actions && col.actions.length > 0)
})

const columnsWithSlots = computed(() => {
  return gridOptions.value.columns.filter(col => col.slots?.default)
})

function getSlotName(field: string) {
  // VXE Table 的插槽名称就是字段名
  return field
}

// 渲染插槽的辅助组件
const RenderSlot = defineComponent({
  props: {
    render: {
      type: Function,
      required: true
    }
  },
  setup(props) {
    return () => props.render()
  }
})

// 渲染图标的辅助组件（支持组件和 VNode）
const RenderIcon = defineComponent({
  props: {
    icon: {
      type: [Object, Function],
      required: true
    }
  },
  setup(props) {
    return () => {
      // 如果是 VNode（有 __v_isVNode 属性），直接返回
      if (props.icon && typeof props.icon === 'object' && '__v_isVNode' in props.icon) {
        return props.icon as any
      }
      // 否则作为组件渲染
      return h(props.icon as any)
    }
  }
})


const tablePagerConfig = computed<any>(() => {
  if (!pageConfig.value.enablePagination) {
    return undefined
  }
  return {
    enabled: true,
    pageSize: gridOptions.value.pagerConfig?.pageSize || 10,
    pageSizes: gridOptions.value.pagerConfig?.pageSizes || [5, 10, 20, 50, 100],
    layouts: ['PrevJump', 'PrevPage', 'JumpNumber', 'NextPage', 'NextJump', 'Sizes', 'Total'],
    currentPage: currentPage.value,
    total: total.value
  }
})

// 表格数据
const tableData = ref<any[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const editModalTitle = computed(() => {
  return currentEditAction.value?.modalProps?.title || '编辑'
})

const editModalType = computed(() => {
  return currentEditAction.value?.modalType || 'modal'
})

const editModalWidth = computed(() => {
  return currentEditAction.value?.modalProps?.width || '800px'
})

const editDrawerWidth = computed(() => {
  // Drawer 宽度，如果是数字则直接使用，如果是字符串则解析
  const width = currentEditAction.value?.modalProps?.width || 600
  if (typeof width === 'number') {
    return width
  }
  // 如果是字符串如 '600px'，提取数字
  const match = String(width).match(/(\d+)/)
  return match && match[1] ? parseInt(match[1], 10) : 600
})

const editModalMaskClosable = computed(() => {
  return currentEditAction.value?.modalProps?.maskClosable !== false
})

const editFormSchema = computed(() => {
  return currentEditAction.value?.formProps?.schema || []
})

// 方法
function getFormComponent(componentName: string) {
  const componentMap: Record<string, any> = {
    Input,
    InputNumber,
    Select,
    DatePicker,
    RangePicker,
    Switch,
    Button
  }
  return componentMap[componentName] || Input
}

function getFormRules(rules?: string) {
  if (!rules) return []
  const rulesArray = rules.split('|').map(r => r.trim())
  const formRules: any[] = []

  if (rulesArray.includes('required')) {
    formRules.push({ required: true, message: '此字段为必填项' })
  }

  return formRules
}

// 检查是否有图标需要渲染（通过插槽）
function hasIconSlot(componentProps?: any) {
  if (!componentProps) return false
  // 检查 icon 是否存在，并且是组件或 VNode
  return componentProps.icon !== undefined && componentProps.icon !== null
}

// 获取按钮属性，移除 icon（因为通过插槽渲染）
function getButtonProps(componentProps: any) {
  if (!componentProps) return {}
  const { icon, ...restProps } = componentProps
  return restProps
}

async function loadData() {
  loading.value = true
  try {
    let result: { items: any[]; count: number }

    if (gridOptions.value.proxyConfig?.ajax?.query) {
      // 使用配置的代理函数
      result = await gridOptions.value.proxyConfig.ajax.query(
        { page: { currentPage: currentPage.value, pageSize: pageSize.value } },
        searchForm
      )
    } else if (props.config.api) {
      // 使用默认 API
      const params = {
        page: currentPage.value,
        pageSize: pageSize.value,
        ...searchForm
      }

      const response = await http.get(props.config.api, { params })
      
      if (response.code === 0) {
        const data = response.data
        result = {
          items: data.list || data.items || [],
          count: data.total || data.count || 0
        }
      } else {
        throw new Error(response.message || '加载数据失败')
      }
    } else {
      result = { items: [], count: 0 }
    }

    tableData.value = result.items || []
    total.value = result.count || 0
  } catch (error: any) {
    console.error('加载数据失败:', error)
    message.error(error?.message || '加载数据失败')
    tableData.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  currentPage.value = 1
  loadData()
}

function handleReset() {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = undefined
  })
  handleSearch()
}

function handlePageChange({ currentPage: page, pageSize: size }: any) {
  currentPage.value = page
  pageSize.value = size
  loadData()
}

function handleSortChange() {
  // 排序变化时重新加载数据
  loadData()
}

async function handleAction(action: ActionItem, row: any) {
  if (action.onClick) {
    action.onClick(row)
    return
  }

  if (action.useFormModal) {
    currentEditRow.value = row
    currentEditAction.value = action

    // 初始化表单数据
    Object.keys(editFormData).forEach(key => {
      delete editFormData[key]
    })
    Object.assign(editFormData, { ...row })

    // 调用 onOpened 钩子
    if (action.hooks?.onOpened) {
      const instance = {
        setValues: (values: any) => {
          Object.assign(editFormData, values)
        }
      }
      await action.hooks.onOpened({
        context: row,
        instance
      })
    }

    editModalVisible.value = true
  }
}

async function handleEditSubmit() {
  if (!currentEditAction.value) return

  try {
    await editFormRef.value?.validate()
    submitLoading.value = true

    let submitData = { ...editFormData }

    // 调用 beforeSubmit 钩子
    if (currentEditAction.value.hooks?.beforeSubmit) {
      submitData = currentEditAction.value.hooks.beforeSubmit(submitData)
    }

    // 提交数据
    if (currentEditAction.value.apiConfig) {
      const { url, method } = currentEditAction.value.apiConfig
      // 替换 URL 中的 {id} 占位符
      const finalUrl = url.replace('{id}', currentEditRow.value?.id || '')

      await http.request({
        url: finalUrl,
        method: method.toLowerCase() as any,
        data: submitData
      })

      message.success('操作成功')

      // 调用 onSubmitSuccess 钩子
      if (currentEditAction.value.hooks?.onSubmitSuccess) {
        currentEditAction.value.hooks.onSubmitSuccess()
      }

      // 关闭 Drawer
      handleDrawerClose()

      // 刷新数据
      loadData()
    }
  } catch (error: any) {
    if (error?.errorFields) {
      // 表单验证错误
      return
    }
    console.error('提交失败:', error)
    message.error(error?.message || '操作失败')
  } finally {
    submitLoading.value = false
  }
}

/**
 * 处理Drawer关闭
 * @description 根据侧边栏弹窗动画优化规范，使用简单的状态控制
 *              Ant Design Vue 会自动管理打开/关闭动画
 */
function handleDrawerClose() {
  editModalVisible.value = false
  
  // 清理数据（在动画完成后）
  setTimeout(() => {
    currentEditRow.value = null
    currentEditAction.value = null
    
    // 清理表单数据
    Object.keys(editFormData).forEach(key => {
      delete editFormData[key]
    })
  }, 300) // 等待动画完成
}

// 暴露方法
defineExpose({
  reload: () => {
    loadData()
  },
  query: (params?: any) => {
    if (params) {
      Object.assign(searchForm, params)
    }
    handleSearch()
  }
})

// 初始化
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.crud-container {
  padding: 16px;
}

.search-form {
  margin-bottom: 16px;
  padding: 16px;
  background: #fafafa;
  border-radius: 4px;
}

.toolbar {
  margin-bottom: 16px;
}

.table-wrapper {
  margin-top: 16px;
}

/* ========== Drawer 动画配置 ========== */
/**
 * 侧边栏弹窗动画优化
 * @description 统一的打开/关闭动画效果，使用 Material Design 标准缓动函数
 * @reference 技术规范: 01-侧边栏弹窗动画优化.md
 */

/* 抽屉容器动画 - 统一过渡效果 */
:deep(.ant-drawer) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 抽屉内容包裹层 - 关键：确保滑入滑出效果一致 */
:deep(.ant-drawer-content-wrapper) {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 抽屉内容区域 */
:deep(.ant-drawer-content) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 抽屉头部 */
:deep(.ant-drawer-header) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 抽屉主体 */
:deep(.ant-drawer-body) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 关闭按钮动画 - 保持与其他元素一致的时间 */
:deep(.ant-drawer-close) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

:deep(.ant-drawer-close:hover) {
  transform: scale(1.1);
}

/* 遮罩层动画 - 确保淡入淡出效果一致 */
:deep(.ant-drawer-mask) {
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
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

