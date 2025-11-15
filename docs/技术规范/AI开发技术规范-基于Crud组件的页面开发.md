# AI 开发技术规范 - 基于 Crud 组件的页面开发

> **文档版本**: v1.0  
> **创建日期**: 2025-01-15  
> **基于示例**: `UsersView.vue`  
> **适用场景**: 使用 Crud 核心组件进行 CRUD 页面开发

---

## 📋 目录

1. [核心原则](#核心原则)
2. [项目结构规范](#项目结构规范)
3. [配置驱动开发模式](#配置驱动开发模式)
4. [表单 Schema 设计规范](#表单-schema-设计规范)
5. [数据管理规范](#数据管理规范)
6. [操作配置规范](#操作配置规范)
7. [组件通信规范](#组件通信规范)
8. [类型安全规范](#类型安全规范)
9. [样式规范](#样式规范)
10. [开发工作流](#开发工作流)
11. [常见问题与解决方案](#常见问题与解决方案)

---

## 🎯 核心原则

### 1.1 配置驱动原则

**黄金法则**: **一切皆配置，配置即代码**

- ✅ **推荐**: 通过 `LocalCrudConfig` 配置对象声明式定义 UI 和行为
- ❌ **禁止**: 在模板中硬编码业务逻辑
- ✅ **推荐**: 配置对象是唯一的真实数据源（Single Source of Truth）

### 1.2 组件化原则

- 核心功能使用 `Crud` 组件
- 特殊业务逻辑使用独立组件（如 `AddUserDrawer`）
- 保持组件职责单一，高内聚低耦合

### 1.3 类型安全原则

- 所有配置对象使用 TypeScript 类型定义
- 使用 `computed` 确保配置的响应式
- 避免使用 `any` 类型，优先使用具体类型

---

## 📁 项目结构规范

### 2.1 标准目录结构

```
src/views/
  └── [FeatureName]View/
      ├── [FeatureName]View.vue      # 主页面组件
      ├── Add[FeatureName]Drawer.vue # 新增抽屉组件（可选）
      ├── Add[FeatureName]Modal.vue  # 新增模态框组件（可选）
      └── types.ts                    # 类型定义（可选）
```

### 2.2 文件命名规范

- **主页面**: `[FeatureName]View.vue` (PascalCase)
- **子组件**: `Add[FeatureName]Drawer.vue` 或 `Add[FeatureName]Modal.vue`
- **类型文件**: `types.ts` (小写)

**示例**:
- `UsersView.vue` - 用户管理主页面
- `AddUserDrawer.vue` - 新增用户抽屉
- `AddUserModal.vue` - 新增用户模态框

---

## ⚙️ 配置驱动开发模式

### 3.1 配置对象结构

```typescript
import { ref, computed } from 'vue'
import type { LocalCrudConfig } from '@/components/Crud'

const crudRef = ref()

const userCrudConfig = computed(() => ({
  title: '用户管理',                    // 页面标题
  pageConfig: {                         // 功能开关
    enableSearch: true,                 // 启用搜索
    enableToolbar: true,                // 启用工具栏
    enablePagination: true              // 启用分页
  },
  api: '/api/user/list',                // 列表 API（可选，如果使用 proxyConfig 可省略）
  options: {
    formOptions: { /* 搜索表单配置 */ },
    toolbarActions: [ /* 工具栏操作 */ ],
    gridOptions: { /* 表格配置 */ }
  }
}))
```

### 3.2 响应式配置

**必须使用 `computed`** 确保配置的响应式更新：

```typescript
// ✅ 正确：使用 computed
const userCrudConfig = computed(() => ({
  // ... 配置
}))

// ❌ 错误：直接使用对象
const userCrudConfig = {
  // ... 配置
}
```

### 3.3 组件引用

```vue
<template>
  <div class="users-view">
    <Crud ref="crudRef" :config="userCrudConfig" />
    <!-- 其他子组件 -->
  </div>
</template>

<script setup lang="ts">
const crudRef = ref()
</script>
```

---

## 📝 表单 Schema 设计规范

### 4.1 共享 Schema 原则

**核心思想**: Add 和 Edit 操作共用同一个 Schema，避免代码重复。

```typescript
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
      disabled: true,        // 始终禁用
      placeholder: '自动生成'
    }
  },
  {
    fieldName: 'username',
    component: 'Input',
    label: '用户名',
    rules: 'required',       // 验证规则
    componentProps: {
      placeholder: '请输入用户名',
      allowClear: true
    }
  },
  // ... 更多字段
]
```

### 4.2 Schema 字段规范

#### 4.2.1 必填字段

```typescript
{
  fieldName: 'username',
  component: 'Input',
  label: '用户名',
  rules: 'required',  // 必填验证
  componentProps: {
    placeholder: '请输入用户名'
  }
}
```

#### 4.2.2 邮箱验证

```typescript
{
  fieldName: 'email',
  component: 'Input',
  label: '邮箱',
  rules: 'required|email',  // 必填 + 邮箱格式
  componentProps: {
    placeholder: '请输入邮箱'
  }
}
```

#### 4.2.3 下拉选择（单选）

```typescript
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
```

#### 4.2.4 下拉选择（多选）

```typescript
{
  fieldName: 'roles',
  component: 'Select',
  label: '角色',
  rules: 'required',
  componentProps: {
    mode: 'multiple',  // 多选模式
    placeholder: '请选择角色',
    options: [
      { label: '管理员', value: 'admin' },
      { label: '普通用户', value: 'user' }
    ],
    allowClear: true
  }
}
```

### 4.3 Schema 复用

在 Edit 操作中直接使用共享 Schema：

```typescript
{
  field: 'action',
  title: '操作',
  actions: [
    {
      label: '编辑',
      useFormModal: true,
      formProps: {
        schema: [...userFormSchema],  // ⭐ 直接使用共享 Schema
        labelWidth: 100,
        layout: 'horizontal'
      }
    }
  ]
}
```

---

## 💾 数据管理规范

### 5.1 数据代理模式（推荐）

使用 VXE Table 的 `proxyConfig` 进行数据管理，支持本地数据处理和模拟数据：

```typescript
gridOptions: {
  proxyConfig: {
    ajax: {
      query: async ({ page }: { page: any }, formValues: any) => {
        // 1. 获取数据源（可以是模拟数据或 API 调用）
        const mockData = generateMockUserList(100)
        
        // 2. 搜索过滤
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

        // 3. 分页处理
        const total = filtered.length
        const start = (page.currentPage - 1) * page.pageSize
        const end = start + page.pageSize
        const list = filtered.slice(start, end)

        // 4. 模拟网络延迟（可选）
        await new Promise(resolve => setTimeout(resolve, 300))

        // 5. 返回标准格式
        return {
          items: list,
          count: total
        }
      }
    }
  }
}
```

### 5.2 模拟数据生成

创建可复用的模拟数据生成函数：

```typescript
/**
 * 生成模拟用户列表数据
 * @param count 生成数量
 * @returns 用户列表
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
      createTime: dayjs()
        .subtract(Math.floor(Math.random() * 30), 'day')
        .format('YYYY-MM-DD HH:mm:ss'),
      permissions: i % 2 === 0 ? ['user:view', 'user:edit'] : ['user:view']
    })
  }

  return users
}
```

### 5.3 API 调用模式（生产环境）

```typescript
proxyConfig: {
  ajax: {
    query: async ({ page }: { page: any }, formValues: any) => {
      try {
        const response = await http.get('/api/user/list', {
          params: {
            page: page.currentPage,
            pageSize: page.pageSize,
            ...formValues
          }
        })
        return {
          items: response.data.list,
          count: response.data.total
        }
      } catch (error) {
        console.error('获取用户列表失败:', error)
        message.error('获取用户列表失败')
        return {
          items: [],
          count: 0
        }
      }
    }
  }
}
```

---

## 🎬 操作配置规范

### 6.1 工具栏操作

```typescript
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
]
```

### 6.2 表格行操作 - 编辑

**关键点**:
1. 使用 `apiConfig` 定义 API 端点（不要使用 `api` 函数）
2. 使用 `hooks.onOpened` 处理数据回显
3. 使用 `hooks.beforeSubmit` 处理数据转换
4. 使用 `hooks.onSubmitSuccess` 处理成功回调

```typescript
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
      modalType: 'drawer',  // 或 'modal'
      modalProps: {
        title: '编辑用户',
        width: 600,
        maskClosable: true
      },
      formProps: {
        schema: [...userFormSchema],  // 使用共享 Schema
        labelWidth: 100,
        layout: 'horizontal'
      },
      // ⭐ 使用 apiConfig 模式（关键！）
      apiConfig: {
        url: '/api/user/{id}',  // {id} 会自动替换为当前行的 id
        method: 'PATCH'
      },
      hooks: {
        // 数据回显：从后端数据转换为表单数据
        onOpened: async ({ context, instance }: { context: any; instance: any }) => {
          const data = { ...context }
          // 如果需要数据转换，在这里处理
          // 例如：日期字符串 -> dayjs 对象
          instance.setValues(data)
        },
        // 提交前数据转换：从表单数据转换为后端格式
        beforeSubmit: (values: any) => {
          return {
            id: values.id,
            username: values.username,
            realName: values.realName,
            email: values.email,
            roles: values.roles,
            status: values.status
          }
        },
        // 提交成功回调
        onSubmitSuccess: () => {
          message.success('用户更新成功')
          // 刷新表格
          if (crudRef.value) {
            crudRef.value.reload()
          }
        }
      }
    }
  ]
}
```

### 6.3 表格行操作 - 删除

```typescript
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
```

**删除处理函数**:

```typescript
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
        // 调用删除 API
        await http.delete(`/api/user/${row.id}`)
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
```

---

## 🔄 组件通信规范

### 7.1 父子组件通信

#### 7.1.1 父组件调用子组件方法

```vue
<template>
  <Crud ref="crudRef" :config="userCrudConfig" />
</template>

<script setup lang="ts">
const crudRef = ref()

// 刷新表格
function refreshTable() {
  if (crudRef.value) {
    crudRef.value.reload()
  }
}
</script>
```

#### 7.1.2 子组件向父组件发送事件

```vue
<!-- AddUserDrawer.vue -->
<script setup lang="ts">
const emit = defineEmits<{
  cancel: []
  success: []
}>()

function handleSuccess() {
  emit('success')
}
</script>

<!-- UsersView.vue -->
<template>
  <AddUserDrawer
    :open="addUserModalVisible"
    @cancel="addUserModalVisible = false"
    @success="handleAddUserSuccess"
  />
</template>

<script setup lang="ts">
function handleAddUserSuccess() {
  addUserModalVisible.value = false
  // 刷新表格
  if (crudRef.value) {
    crudRef.value.reload()
  }
}
</script>
```

### 7.2 组件引用管理

```typescript
// 组件引用
const crudRef = ref()
const addUserModalVisible = ref(false)

// 确保引用存在后再调用方法
if (crudRef.value) {
  crudRef.value.reload()
}
```

---

## 🔒 类型安全规范

### 8.1 导入类型定义

```typescript
import type { LocalCrudConfig } from '@/components/Crud'
```

### 8.2 配置对象类型

```typescript
const userCrudConfig = computed<LocalCrudConfig>(() => ({
  // ... 配置
}))
```

### 8.3 函数参数类型

```typescript
// ✅ 正确：明确类型
function handleDelete(row: { id: string; realName: string }) {
  // ...
}

// ❌ 错误：使用 any
function handleDelete(row: any) {
  // ...
}
```

### 8.4 Props 和 Emits 类型

```typescript
// AddUserDrawer.vue
interface Props {
  open: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  cancel: []
  success: []
}>()
```

---

## 🎨 样式规范

### 9.1 VXE Table 对齐修复（标准样式）

**必须添加**以下 CSS 以修复 VXE Table 的对齐问题：

```css
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
```

### 9.2 页面容器样式

```css
.users-view {
  padding: 16px;
}
```

### 9.3 表格列宽度规范

- 使用 `minWidth` 而非固定 `width`，配合 `fit: true` 实现响应式
- 操作列使用固定 `width`，并设置 `fixed: 'right'`

```typescript
columns: [
  {
    field: 'username',
    title: '用户名',
    minWidth: 120,  // ✅ 使用 minWidth
    showOverflow: 'ellipsis'
  },
  {
    field: 'action',
    title: '操作',
    width: 150,     // ✅ 操作列使用固定宽度
    fixed: 'right'
  }
]
```

---

## 🔄 开发工作流

### 10.1 标准开发流程

#### 步骤 1: 创建页面结构

```bash
src/views/UsersView/
  ├── UsersView.vue
  └── AddUserDrawer.vue
```

#### 步骤 2: 定义共享 Schema

```typescript
const userFormSchema = [
  // ... 字段定义
]
```

#### 步骤 3: 配置搜索表单

```typescript
formOptions: {
  schema: [
    {
      fieldName: 'search',
      component: 'Input',
      label: '搜索',
      componentProps: {
        placeholder: '搜索用户名、邮箱、姓名'
      }
    }
  ]
}
```

#### 步骤 4: 配置表格列

```typescript
gridOptions: {
  columns: [
    // ... 列定义
  ]
}
```

#### 步骤 5: 配置编辑操作

```typescript
{
  field: 'action',
  actions: [
    {
      label: '编辑',
      useFormModal: true,
      apiConfig: { /* ... */ },
      hooks: { /* ... */ }
    }
  ]
}
```

#### 步骤 6: 配置新增操作

```typescript
// 工具栏操作
toolbarActions: [
  {
    label: '新增用户',
    onClick: () => {
      addUserModalVisible.value = true
    }
  }
]

// 新增组件
<AddUserDrawer
  :open="addUserModalVisible"
  @success="handleAddUserSuccess"
/>
```

#### 步骤 7: 实现删除操作

```typescript
function handleDelete(row: any) {
  Modal.confirm({
    // ... 确认对话框
  })
}
```

### 10.2 代码检查清单

- [ ] 使用 `computed` 定义配置对象
- [ ] 定义共享表单 Schema
- [ ] 编辑操作使用 `apiConfig` 而非 `api` 函数
- [ ] 实现 `hooks.onOpened` 处理数据回显
- [ ] 实现 `hooks.beforeSubmit` 处理数据转换
- [ ] 实现 `hooks.onSubmitSuccess` 刷新表格
- [ ] 添加 VXE Table 对齐修复样式
- [ ] 使用 TypeScript 类型定义
- [ ] 组件引用检查（`if (crudRef.value)`）
- [ ] 错误处理和用户提示

---

## ❓ 常见问题与解决方案

### 11.1 编辑操作数据不回显

**问题**: 点击编辑按钮，表单没有显示当前行数据

**解决方案**:
- 检查 `hooks.onOpened` 是否正确实现
- 确保调用 `instance.setValues(data)`
- 检查 `context` 数据是否正确

```typescript
hooks: {
  onOpened: async ({ context, instance }) => {
    const data = { ...context }
    instance.setValues(data)  // ⭐ 必须调用
  }
}
```

### 11.2 编辑提交失败

**问题**: 编辑提交时 API 调用失败

**解决方案**:
- 检查 `apiConfig.url` 是否正确，`{id}` 占位符是否正确
- 检查 `apiConfig.method` 是否正确（通常是 `PATCH`）
- 检查 `beforeSubmit` 返回的数据格式是否正确

```typescript
apiConfig: {
  url: '/api/user/{id}',  // ⭐ 确保 {id} 占位符存在
  method: 'PATCH'         // ⭐ 使用正确的 HTTP 方法
}
```

### 11.3 表格不刷新

**问题**: 操作成功后表格数据没有更新

**解决方案**:
- 在 `onSubmitSuccess` 中调用 `crudRef.value.reload()`
- 确保 `crudRef` 引用正确

```typescript
hooks: {
  onSubmitSuccess: () => {
    if (crudRef.value) {  // ⭐ 检查引用
      crudRef.value.reload()
    }
  }
}
```

### 11.4 表格列对齐问题

**问题**: 表头和表体列不对齐

**解决方案**:
- 添加标准 VXE Table 对齐修复样式（见 9.1 节）
- 确保表格配置中 `fit: true`

### 11.5 搜索不生效

**问题**: 搜索表单提交后表格数据没有过滤

**解决方案**:
- 检查 `proxyConfig.ajax.query` 是否正确处理 `formValues`
- 检查搜索字段名是否与表单 `fieldName` 一致

```typescript
query: async ({ page }, formValues: any) => {
  let filtered = mockData
  if (formValues?.search) {  // ⭐ 字段名必须匹配
    // 过滤逻辑
  }
  return { items: filtered, count: filtered.length }
}
```

### 11.6 分页不生效

**问题**: 分页控件显示但点击无效

**解决方案**:
- 检查 `pagerConfig.enabled` 是否为 `true`
- 检查 `proxyConfig.ajax.query` 是否正确处理 `page` 参数
- 确保返回数据包含 `count` 字段

```typescript
pagerConfig: {
  enabled: true,      // ⭐ 必须启用
  pageSize: 10,
  pageSizes: [5, 10, 20, 50, 100]
}

// query 函数中
const start = (page.currentPage - 1) * page.pageSize
const end = start + page.pageSize
const list = filtered.slice(start, end)

return {
  items: list,
  count: total  // ⭐ 必须返回总数
}
```

---

## 📚 参考资源

### 相关文档

- [Crud 组件开发指南](../核心组件/0-Crud组件开发指南.md)
- [Crud 组件执行流程与开发机制](../核心组件/0-Crud组件执行流程与开发机制.md)
- [Crud 组件模板规范](../核心组件/0-Crud组件执行流程与开发机制-组件模板规范.md)

### 示例代码

- `src/views/UsersView/UsersView.vue` - 完整实现示例
- `src/views/UsersView/AddUserDrawer.vue` - 新增组件示例

### 技术栈

- **Vue 3**: Composition API
- **TypeScript**: 类型安全
- **VXE Table**: 高性能表格组件
- **Ant Design Vue**: UI 组件库
- **Pinia**: 状态管理（如需要）

---

## 📝 更新日志

| 版本 | 日期 | 更新内容 | 作者 |
|------|------|----------|------|
| v1.0 | 2025-01-15 | 初始版本，基于 UsersView.vue 实现 | 开发团队 |

---

## 🤝 贡献指南

如有问题或建议，请：

1. 检查本文档的"常见问题与解决方案"部分
2. 参考示例代码 `UsersView.vue`
3. 查阅相关技术文档
4. 联系开发团队

---

**文档结束**

