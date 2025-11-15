/**
 * Crud 组件类型定义
 * 基于配置驱动的 CRUD 组件系统
 */

/**
 * 页面配置
 */
export interface PageConfig {
  /** 启用搜索表单 */
  enableSearch?: boolean
  /** 启用工具栏 */
  enableToolbar?: boolean
  /** 启用分页 */
  enablePagination?: boolean
  /** 启用行选择 */
  enableSelection?: boolean
}

/**
 * 表单字段配置
 */
export interface FormFieldSchema {
  /** 字段名 */
  fieldName: string
  /** 组件类型 */
  component: string
  /** 标签 */
  label: string
  /** 验证规则 */
  rules?: string
  /** 组件属性 */
  componentProps?: Record<string, any>
  /** 表单项样式类 */
  formItemClass?: string
  /** 默认值 */
  defaultValue?: any
}

/**
 * 表单配置
 */
export interface FormOptions {
  /** 表单字段配置 */
  schema?: FormFieldSchema[]
  /** 标签宽度 */
  labelWidth?: number
  /** 布局方式 */
  layout?: 'horizontal' | 'vertical' | 'inline'
}

/**
 * 表格列配置
 */
export interface GridColumn {
  /** 字段名 */
  field: string
  /** 列标题 */
  title: string
  /** 列宽度 */
  width?: number
  /** 最小宽度 */
  minWidth?: number
  /** 是否可排序 */
  sortable?: boolean
  /** 溢出显示方式 */
  showOverflow?: boolean | 'tooltip' | 'ellipsis'
  /** 自定义插槽 */
  slots?: {
    default?: string
    header?: string
  }
  /** 操作按钮配置 */
  actions?: ActionItem[]
}

/**
 * 操作项配置
 */
export interface ActionItem {
  /** 按钮标签 */
  label: string
  /** 组件类型 */
  component: string
  /** 组件属性 */
  componentProps?: Record<string, any>
  /** 是否使用表单模态框 */
  useFormModal?: boolean
  /** 模态框类型 */
  modalType?: 'modal' | 'drawer'
  /** 模态框属性 */
  modalProps?: Record<string, any>
  /** 表单属性 */
  formProps?: {
    schema?: FormFieldSchema[]
    labelWidth?: number
    layout?: 'horizontal' | 'vertical' | 'inline'
  }
  /** API 配置 */
  apiConfig?: {
    url: string
    method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  }
  /** 钩子函数 */
  hooks?: {
    onOpened?: (params: { context: any; instance: any }) => void | Promise<void>
    beforeSubmit?: (values: any) => any
    onSubmitSuccess?: () => void
    onClick?: (row: any) => void
  }
  /** 点击事件 */
  onClick?: (row: any) => void
}

/**
 * 工具栏操作项
 */
export interface ToolbarAction {
  /** 按钮标签 */
  label: string
  /** 组件类型 */
  component: string
  /** 组件属性 */
  componentProps?: Record<string, any>
  /** 点击事件 */
  onClick?: () => void
}

/**
 * 表格配置
 */
export interface GridOptions {
  /** 列配置 */
  columns: GridColumn[]
  /** 数据源配置 */
  proxyConfig?: {
    ajax: {
      query: (params: { page: any }, formValues: any) => Promise<{ items: any[]; count: number }>
    }
  }
  /** 是否自适应列宽 */
  fit?: boolean
  /** 分页配置 */
  pagerConfig?: {
    enabled: boolean
    pageSize: number
    pageSizes?: number[]
  }
  /** 排序配置 */
  sortConfig?: {
    remote: boolean
    defaultSort?: { field: string; order: 'asc' | 'desc' }
  }
}

/**
 * 本地 Crud 配置
 */
export interface LocalCrudConfig {
  /** 页面标题 */
  title: string
  /** 页面配置 */
  pageConfig?: PageConfig
  /** API 端点（列表接口） */
  api?: string
  /** 其他选项 */
  options: {
    /** 表单配置 */
    formOptions?: FormOptions
    /** 工具栏操作 */
    toolbarActions?: ToolbarAction[]
    /** 表格配置 */
    gridOptions: GridOptions
  }
}

