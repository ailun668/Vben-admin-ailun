# MPurse Central Crud组件系统技术文档

## 📋 文档目的

本文档为AI程序员和开发者提供全面的Crud组件系统技术指南，确保能够快速理解项目架构并进行正确的代码开发、Bug修复和功能迭代。

---

## 🏗️ 整体架构概览

### 核心设计理念

MPurse Central的Crud组件系统采用**配置驱动**的设计模式，通过声明式配置实现复杂的CRUD（增删改查）操作，大幅降低重复代码编写，提高开发效率。

### 架构层次

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层 (Views)                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │  merchant/      │ │   mpurse/       │ │  settings/      │ │
│  │  管理页面       │ │   用户页面      │ │  设置页面       │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
               ↓ 使用配置对象
┌─────────────────────────────────────────────────────────────┐
│                  Crud组件系统                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Crud/index.vue (入口组件)                 │  │
│  │              - 配置管理                                │  │
│  │              - 生命周期控制                             │  │
│  └───────────────────────────────────────────────────────┘  │
│               ↓                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          CrudContent.vue (核心组件)                     │  │
│  │          - 表格渲染                                     │  │
│  │          - 表单集成                                     │  │
│  │          - 操作按钮                                     │  │
│  │          - Tab支持                                      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
               ↓ 基于VXE Table + Ant Design Vue
┌─────────────────────────────────────────────────────────────┐
│                    UI框架层                                   │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │   VXE Table     │ │ Ant Design Vue  │ │  Vben Common    │ │
│  │   高性能表格     │ │   UI组件库      │ │   企业组件      │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
               ↓ HTTP请求
┌─────────────────────────────────────────────────────────────┐
│                    API层                                     │
│         基于@shared/request的统一请求管理                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 目录结构详解

```
src/components/Crud/
├── index.vue                    # 🎯 主入口组件
├── index.ts                     # 📦 导出定义
├── components/                  # 🧩 子组件
│   ├── ActionBar.vue           # 操作按钮栏组件
│   └── CrudContent.vue         # 核心内容组件
├── hooks/                      # 🪝 组合函数
│   ├── use-crud-config.ts      # 配置管理钩子
│   ├── use-action.ts           # 操作处理钩子
│   └── use-grid-tab.ts         # Tab功能钩子
├── types/                      # 📋 类型定义
│   ├── crud.ts                 # 核心配置类型
│   ├── action.ts               # 操作相关类型
│   ├── tabs.ts                 # Tab相关类型
│   └── index.ts                # 类型导出
└── utils/                      # 🛠️ 工具函数
    └── config-helper.ts        # 配置处理助手
```

### 核心文件职责

| 文件 | 主要职责 | 关键功能 |
|------|----------|----------|
| **index.vue** | 入口控制器 | 配置加载、生命周期管理、API暴露 |
| **CrudContent.vue** | 核心渲染器 | 表格渲染、表单集成、操作处理 |
| **ActionBar.vue** | 操作管理器 | 按钮渲染、下拉菜单、权限控制 |
| **use-crud-config.ts** | 配置管理器 | 本地/远程配置加载、格式化 |
| **use-action.ts** | 操作处理器 | 按钮逻辑、模态框管理、组件动态加载 |
| **use-grid-tab.ts** | Tab控制器 | 多Tab切换、独立数据管理 |

---

## 🔧 技术栈深度分析

### 前端框架层

| 技术 | 版本 | 用途 | 关键特性 |
|------|------|------|----------|
| **Vue 3** | 3.5.13 | 核心框架 | Composition API、响应式系统、组件通信 |
| **TypeScript** | 5.7.3 | 类型系统 | 100%类型覆盖、接口定义、泛型支持 |
| **Vite** | 6.0.11 | 构建工具 | 热更新、ES模块、插件生态 |
| **Pinia** | 2.1.7 | 状态管理 | 类型安全、模块化、持久化 |

### UI组件层

| 组件库 | 版本 | 用途 | 在Crud中的应用 |
|--------|------|------|----------------|
| **Ant Design Vue** | 4.2.6 | 基础UI | Button、Modal、Drawer、Form组件 |
| **VXE Table** | 4.10.0 | 数据表格 | 核心表格功能、分页、排序、筛选 |
| **Vben Common UI** | Latest | 企业组件 | Page布局、Form封装、Grid适配器 |
| **TailwindCSS** | 3.4.17 | 样式框架 | 响应式布局、工具类、主题定制 |

### 数据处理层

| 技术 | 版本 | 用途 | 核心功能 |
|------|------|------|----------|
| **@shared/request** | Internal | HTTP客户端 | 接口统一管理、拦截器、错误处理 |
| **@shared/adapter** | Internal | 适配器层 | 组件标准化、表单验证、类型转换 |
| **lodash-es** | 4.17.21 | 工具库 | 数据处理、类型判断、深度操作 |

---

## 💡 核心概念与工作原理

### 1. 配置驱动模式

Crud组件采用配置驱动的设计，通过传入配置对象来渲染完整的CRUD界面。

#### 本地配置模式 (LocalCrudConfig)
```typescript
const config: LocalCrudConfig = {
  title: '用户管理',           // 页面标题
  api: '/api/users',          // 主API地址
  pageConfig: {               // 功能开关
    enableSearch: true,       // 启用搜索
    enableToolbar: true,      // 启用工具栏
    enablePagination: true,   // 启用分页
  },
  options: {                  // 详细配置
    formOptions: {            // 表单配置
      schema: [...],          // 表单字段
      layout: 'horizontal',   // 布局方式
    },
    gridOptions: {            // 表格配置
      columns: [...],         // 表格列
      proxyConfig: {...},     // 数据代理
    },
    toolbarActions: [...],    // 工具栏操作
  }
}
```

#### 远程配置模式 (RemoteCrudConfig)
```typescript
// 自动从 /mpmapi/menu/{menuId}/config 加载配置
const config: RemoteCrudConfig = {
  api: '/api/users',
  schema: {
    list: [...],     // 列表字段
    filter: [...],   // 筛选字段
    create: [...],   // 创建表单
    update: [...],   // 更新表单
  },
  actions: [...],    // 操作定义
}
```

### 2. 组件通信架构

```mermaid
graph TD
    A[父页面组件] -->|传入config| B[Crud/index.vue]
    B -->|加载配置| C[useCrudConfig]
    B -->|渲染内容| D[CrudContent.vue]
    D -->|渲染表格| E[VXE Grid]
    D -->|渲染操作| F[ActionBar.vue]
    F -->|处理点击| G[useAction]
    G -->|打开模态| H[FormModal]
    G -->|调用API| I[@shared/request]
    C -->|配置变更| D
    D -->|事件回调| A
```

### 3. 数据流管理

#### 数据获取流程
1. **配置初始化** → `useCrudConfig` 加载本地或远程配置
2. **表格渲染** → `VXE Grid` 根据配置创建表格
3. **数据查询** → `proxyConfig.ajax.query` 调用API获取数据
4. **数据展示** → 表格自动渲染数据和分页信息

#### 数据更新流程
1. **用户操作** → 点击新增/编辑/删除按钮
2. **模态框打开** → 根据 `ActionItem` 配置打开表单
3. **表单提交** → 调用对应的API接口
4. **自动刷新** → 操作成功后自动调用 `gridApi.reload()`

---

## 🎯 开发规范与最佳实践

### 1. 配置编写规范

#### ✅ 正确示例

```typescript
// 1. 完整的本地配置
const config: LocalCrudConfig = {
  title: 'Message Template Management',
  api: '/mpmapi/central/messagetemplate',

  // 功能开关配置
  pageConfig: {
    enableTabs: false,
    enableSearch: true,
    enableToolbar: true,
    enablePagination: true,
  },

  options: {
    // 搜索表单配置
    formOptions: {
      commonConfig: {
        labelWidth: 160,
        componentProps: { class: 'w-full' },
      },
      layout: 'horizontal' as const,
      schema: searchFormSchema,
      collapsed: true,
      showDefaultActions: true,
    },

    // 表格配置
    gridOptions: baseGridOptions,

    // 工具栏操作
    toolbarActions: [
      {
        label: 'Add Template',
        component: 'Button',
        componentProps: { type: 'primary' },
        useFormModal: true,
        modalType: 'modal',
        apiConfig: {
          url: '/mpmapi/central/messagetemplate',
          method: 'POST',
        },
        modalProps: {
          title: 'Add Message Template',
          class: 'w-1/2',
        },
        formProps: {
          schema: formSchema,
          layout: 'horizontal' as const,
        },
        hooks: {
          onSubmitSuccess: () => {
            crudRef.value.reload();
          },
        },
      },
    ],
  },
}
```

#### ❌ 错误示例

```typescript
// 错误：缺少必要的类型注解
const config = {
  api: '/api/users',
  options: {
    gridOptions: {
      columns: [
        { field: 'name', title: 'Name' }, // 缺少width等重要配置
      ]
    }
  }
}

// 错误：未处理异步操作
const badAction = {
  onClick: (row) => {
    request.delete(`/api/users/${row.id}`); // 未等待异步操作
    reload(); // 可能在删除完成前执行
  }
}
```

### 2. 表单Schema规范

#### ApiCacheSelect 组件配置

```typescript
{
  fieldName: 'middleman_id',
  label: 'Middleman Id',
  component: 'ApiCacheSelect',
  rules: 'required',
  componentProps: {
    api: '/mpmapi/central/messagemiddleman',
    immediate: true,        // 🎯 立即加载数据
    params: { limit: 30 },
    hooks: {
      convert: (res: any) => {
        return (res.items || []).map((item: any) => ({
          label: item.name,   // 显示字段
          value: item.id,     // 值字段
        }));
      },
    },
  },
}
```

#### 表单验证规范

```typescript
// ✅ 推荐的验证方式
{
  fieldName: 'email',
  label: 'Email',
  component: 'Input',
  rules: 'required|email',  // 使用内置验证规则
}

// ✅ 自定义验证
{
  fieldName: 'password',
  label: 'Password',
  component: 'InputPassword',
  rules: [
    { required: true, message: 'Password is required' },
    { min: 8, message: 'Password must be at least 8 characters' }
  ],
}
```

### 3. 操作按钮配置规范

#### 表格行操作

```typescript
// 在 gridOptions.columns 中配置
{
  field: 'action',
  title: 'Actions',
  width: 160,
  fixed: 'right' as const,
  slots: { default: 'table-actions' },
  actions: [
    {
      label: 'Edit',
      component: 'Button',
      componentProps: { type: 'link' },
      useFormModal: true,
      modalType: 'drawer',      // 使用抽屉模式
      apiConfig: {
        url: '/mpmapi/central/messagetemplate/{id}',
        method: 'PUT',
      },
      drawerProps: {
        title: 'Edit Message Template',
      },
      formProps: {
        schema: formSchema,
        layout: 'horizontal' as const,
      },
      hooks: {
        onOpened: async ({ context, instance }) => {
          // 🎯 数据回显处理
          const res = await request.get({
            url: `/mpmapi/central/messagetemplate/${context.id}`,
          });
          if (res.middleman) {
            res.middleman_id = res.middleman;
          }
          instance.setValues(res);
        },
        onSubmitSuccess: () => {
          crudRef.value.reload();
        },
      },
    },
  ] as ActionItem[],
}
```

#### 工具栏操作

```typescript
toolbarActions: [
  {
    label: 'Batch Delete',
    component: 'Button',
    componentProps: {
      type: 'primary',
      danger: true,
    },
    // 🎯 条件显示
    show: (selectedRows: any[]) => selectedRows.length > 0,
    onClick: async (selectedRows: any[]) => {
      try {
        await batchDeleteUsers(selectedRows.map(row => row.id));
        message.success('Batch delete successful');
        crudRef.value.reload();
      } catch (error) {
        message.error('Batch delete failed');
      }
    },
  },
]
```

### 4. 钩子函数使用规范

#### 模态框生命周期钩子

```typescript
hooks: {
  // 打开前：数据预处理
  onOpened: async ({ context, instance }) => {
    // 1. 预加载关联数据
    const relatedData = await loadRelatedData();

    // 2. 设置表单初始值
    if (context.id) {  // 编辑模式
      const res = await request.get(`/api/users/${context.id}`);
      instance.setValues(res);
    } else {  // 新增模式
      instance.setValues({ status: 'active' });
    }
  },

  // 提交前：数据验证
  onBeforeSubmit: async ({ formData }) => {
    // 自定义验证逻辑
    if (formData.role === 'admin' && !formData.permissions) {
      throw new Error('Admin role requires permissions');
    }
    return formData;
  },

  // 提交成功：后续处理
  onSubmitSuccess: (result) => {
    message.success('Operation successful');
    crudRef.value.reload();
    // 可选：触发其他业务逻辑
  },

  // 提交失败：错误处理
  onSubmitError: (error) => {
    console.error('Submit failed:', error);
    message.error('Operation failed: ' + error.message);
  },
}
```

---

## 🔍 API集成模式

### 1. 标准CRUD API模式

```typescript
// 配置中的API定义
const config: LocalCrudConfig = {
  api: '/mpmapi/central/messagetemplate',  // 基础API路径
  extraApis: {
    export: '/mpmapi/central/messagetemplate/export',
    import: '/mpmapi/central/messagetemplate/import',
  },
}

// 自动生成的API调用
// GET    /mpmapi/central/messagetemplate      -> 列表查询
// POST   /mpmapi/central/messagetemplate      -> 创建
// PUT    /mpmapi/central/messagetemplate/{id} -> 更新
// DELETE /mpmapi/central/messagetemplate/{id} -> 删除
```

### 2. 数据代理配置

```typescript
const gridOptions: VxeGridProps = {
  proxyConfig: {
    ajax: {
      // 查询配置
      query: async ({ page }, formValues) => {
        const res = await request.get({
          url: '/mpmapi/central/messagetemplate',
          params: {
            page: page.currentPage,
            limit: page.pageSize,
            ...formValues,  // 搜索表单参数
          },
        });
        return {
          items: res.items || [],
          count: res.count || 0,
        };
      },

      // 保存配置（可选）
      save: async ({ body }) => {
        if (body.insertRecords?.length) {
          // 批量新增
          await request.post({
            url: '/mpmapi/central/messagetemplate/batch',
            data: body.insertRecords,
          });
        }
        if (body.updateRecords?.length) {
          // 批量更新
          await request.put({
            url: '/mpmapi/central/messagetemplate/batch',
            data: body.updateRecords,
          });
        }
        return { success: true };
      },
    },
  },
}
```

### 3. 错误处理机制

```typescript
// 在 @shared/request 中配置全局错误处理
const request = createRequest({
  // 请求拦截器
  requestInterceptors: [
    (config) => {
      // 添加认证头
      const token = getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    }
  ],

  // 响应拦截器
  responseInterceptors: [
    (response) => {
      // 统一处理业务错误
      if (response.data.code !== 200) {
        throw new Error(response.data.message);
      }
      return response.data.data;
    },
    (error) => {
      // 统一错误处理
      if (error.response?.status === 401) {
        // 未授权，跳转登录
        router.push('/login');
      } else if (error.response?.status === 403) {
        // 权限不足
        message.error('Permission denied');
      }
      throw error;
    }
  ],
});
```

---

## 🎨 UI定制与样式规范

### 1. 主题定制

```typescript
// 在配置中定制组件样式
const config: LocalCrudConfig = {
  options: {
    formOptions: {
      commonConfig: {
        labelWidth: 140,           // 标签宽度
        componentProps: {
          class: 'w-full',         // Tailwind样式类
        },
      },
    },
    gridOptions: {
      size: 'medium',             // 表格尺寸
      border: true,               // 边框
      stripe: true,               // 斑马纹
      height: 'auto',             // 自适应高度
    },
  },
}
```

### 2. 响应式设计

```typescript
// 移动端适配配置
const mobileGridOptions = {
  ...baseGridOptions,
  columns: baseGridOptions.columns.map(col => ({
    ...col,
    // 移动端隐藏次要列
    visible: col.field === 'name' || col.field === 'action',
    // 调整列宽
    width: col.field === 'action' ? 120 : undefined,
  })),
}

// 使用媒体查询切换配置
const isMobile = computed(() => window.innerWidth < 768);
const currentGridOptions = computed(() =>
  isMobile.value ? mobileGridOptions : baseGridOptions
);
```

### 3. 无障碍支持

```typescript
// 在操作按钮中添加无障碍属性
const accessibleAction: ActionItem = {
  label: 'Edit User',
  component: 'Button',
  componentProps: {
    type: 'link',
    'aria-label': 'Edit user information',
    title: 'Edit user information',
  },
}
```

---

## ⚡ 性能优化策略

### 1. 组件懒加载

```typescript
// 在 use-action.ts 中实现的动态组件加载
function loadComponent(path: string) {
  if (!componentCache.value.has(path)) {
    const asyncComponent = defineAsyncComponent(() => {
      return import(/* @vite-ignore */ path);
    });
    componentCache.value.set(path, asyncComponent);
  }
  return componentCache.value.get(path);
}
```

### 2. 数据缓存策略

```typescript
// ApiCacheSelect 自动缓存机制
{
  fieldName: 'category_id',
  component: 'ApiCacheSelect',
  componentProps: {
    api: '/api/categories',
    cacheKey: 'categories',      // 自定义缓存键
    cacheTime: 5 * 60 * 1000,    // 缓存5分钟
    immediate: true,
  },
}
```

### 3. 虚拟滚动

```typescript
// 大数据量表格优化
const gridOptions: VxeGridProps = {
  height: 600,
  virtualScroll: true,           // 启用虚拟滚动
  scrollY: {
    enabled: true,
    mode: 'wheel',               // 滚轮模式
  },
}
```

### 4. 防抖与节流

```typescript
// 在搜索表单中使用防抖
const searchFormSchema = [
  {
    fieldName: 'keyword',
    component: 'Input',
    componentProps: {
      placeholder: 'Search...',
      onChange: debounce((value) => {
        gridApi.query({ keyword: value });
      }, 300),  // 300ms防抖
    },
  },
]
```

---

## 🧪 测试策略

### 1. 单元测试

```typescript
// 测试配置工具函数
import { describe, it, expect } from 'vitest';
import { normalizeConfig } from '../hooks/use-crud-config';

describe('useCrudConfig', () => {
  it('should normalize local config correctly', () => {
    const config = {
      api: '/api/users',
      options: {},
    };

    const result = normalizeConfig(config, false);

    expect(result.pageConfig).toBeDefined();
    expect(result.pageConfig.enableSearch).toBe(true);
    expect(result.options).toBeDefined();
  });
});
```

### 2. 组件测试

```typescript
// 测试Crud组件渲染
import { mount } from '@vue/test-utils';
import Crud from '../index.vue';

describe('Crud Component', () => {
  it('should render with local config', async () => {
    const config = {
      title: 'Test Users',
      api: '/api/users',
      options: {
        gridOptions: {
          columns: [
            { field: 'name', title: 'Name' }
          ]
        }
      }
    };

    const wrapper = mount(Crud, {
      props: { config }
    });

    expect(wrapper.text()).toContain('Test Users');
  });
});
```

### 3. E2E测试

```typescript
// 使用Playwright测试完整流程
import { test, expect } from '@playwright/test';

test('should create user successfully', async ({ page }) => {
  await page.goto('/users');

  // 点击新增按钮
  await page.click('[data-testid="add-user"]');

  // 填写表单
  await page.fill('[data-testid="user-name"]', 'Test User');
  await page.fill('[data-testid="user-email"]', 'test@example.com');

  // 提交表单
  await page.click('[data-testid="submit-button"]');

  // 验证成功消息
  await expect(page.locator('.ant-message')).toContainText('Operation successful');
});
```

---

## 🚨 常见问题与解决方案

### 1. 数据回显问题

**问题描述**：编辑模式下下拉选择框无法正确显示已选值

**原因分析**：
- 后端返回的是ID值，前端需要显示name
- ApiCacheSelect组件数据未及时加载

**解决方案**：
```typescript
// ✅ 正确的数据回显处理
hooks: {
  onOpened: async ({ context, instance }) => {
    // 1. 先加载下拉选项数据
    const optionsRes = await request.get({
      url: '/mpmapi/central/messagemiddleman',
      params: { limit: 30 },
    });

    // 2. 再加载表单数据
    const res = await request.get({
      url: `/mpmapi/central/messagetemplate/${context.id}`,
    });

    // 3. 处理ID到name的映射
    if (res.middleman) {
      const middlemanItem = (optionsRes.items || []).find(
        (item: any) => item.id === res.middleman
      );
      res.middleman_id = res.middleman; // 保持ID值
    }

    instance.setValues(res);
  },
}
```

### 2. 权限控制问题

**问题描述**：按钮权限控制不生效

**解决方案**：
```typescript
// ✅ 基于权限码的显示控制
{
  label: 'Delete',
  component: 'Button',
  show: (row) => {
    // 检查权限
    const hasPermission = checkPermission('user:delete');
    // 检查业务逻辑
    const canDelete = row.status !== 'system';
    return hasPermission && canDelete;
  },
}
```

### 3. 表单验证问题

**问题描述**：自定义验证规则不生效

**解决方案**：
```typescript
// ✅ 正确的验证配置
{
  fieldName: 'email',
  rules: [
    { required: true, message: 'Email is required' },
    {
      type: 'email',
      message: 'Please enter a valid email'
    },
    {
      validator: async (rule, value) => {
        if (value) {
          const exists = await checkEmailExists(value);
          if (exists) {
            throw new Error('Email already exists');
          }
        }
      }
    }
  ],
}
```

### 4. 性能问题

**问题描述**：大数据量表格渲染卡顿

**解决方案**：
```typescript
// ✅ 启用虚拟滚动和分页
const gridOptions: VxeGridProps = {
  height: 600,
  virtualScroll: true,
  pagerConfig: {
    enabled: true,
    pageSize: 50,          // 减少每页条数
    pageSizes: [20, 50, 100],
  },
  // 禁用不必要的功能
  showOverflow: 'ellipsis',
  showHeaderOverflow: 'ellipsis',
}
```

---

## 📋 开发检查清单

### 功能开发前检查

- [ ] 确认API接口已定义且可访问
- [ ] 确认数据结构和字段映射关系
- [ ] 确认权限控制要求
- [ ] 确认UI设计规范

### 配置编写检查

- [ ] 所有配置对象都有完整的类型注解
- [ ] API路径配置正确
- [ ] 表单字段配置完整（fieldName、label、component、rules）
- [ ] 操作按钮的hooks配置正确
- [ ] 错误处理和成功回调已配置

### 代码质量检查

- [ ] 组件props和emits类型定义完整
- [ ] 异步操作正确使用async/await
- [ ] 错误处理机制完善
- [ ] 组件可访问性属性已添加
- [ ] 性能优化措施已实施

### 测试检查

- [ ] 基础功能测试通过（增删改查）
- [ ] 边界情况测试通过
- [ ] 权限控制测试通过
- [ ] 响应式布局测试通过
- [ ] 错误场景测试通过

---

## 🔄 版本迭代指南

### 新功能开发流程

1. **需求分析** → 确定功能范围和技术方案
2. **配置设计** → 设计配置接口和数据结构
3. **组件开发** → 实现核心功能和UI界面
4. **集成测试** → 测试与现有系统的兼容性
5. **文档更新** → 更新技术文档和使用示例

### Bug修复流程

1. **问题定位** → 复现问题并分析根本原因
2. **影响评估** → 评估修复对其他功能的影响
3. **修复实施** → 编写修复代码并添加测试
4. **回归测试** → 确保修复没有引入新问题
5. **发布部署** → 按照标准流程发布和部署

### 重构指南

1. **渐进式重构** → 避免大范围重写，采用渐进式改进
2. **向后兼容** → 保持API接口的向后兼容性
3. **测试先行** → 重构前编写充分的测试用例
4. **文档同步** → 及时更新技术文档和示例代码

---

## 📚 相关资源

### 官方文档

- [Vue 3 官方文档](https://vuejs.org/)
- [TypeScript 官方文档](https://www.typescriptlang.org/)
- [Ant Design Vue 文档](https://antdv.com/)
- [VXE Table 文档](https://vxetable.cn/)

### 内部资源

- [项目技术架构文档](./Mpurse-Admin-技术架构文档.md)
- [技术栈版本清单](./Mpurse-Admin-技术栈与版本清单.md)
- [API接口文档](../docs/api/)
- [组件库文档](../shared/components/README.md)

### 工具与插件

- [Vue DevTools](https://devtools.vuejs.org/)
- [TypeScript for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-typescript-next)
- [Vite DevTools](https://github.com/antfu/vite-plugin-vue-devtools)

---

## 🏷️ 文档信息

**版本**: v1.0.0
**创建时间**: 2025-09-19
**最后更新**: 2025-09-19
**维护者**: MPurse 前端开发团队
**适用范围**: MPurse Central 项目的 Crud 组件系统开发

> 💡 **提示**: 本文档将随着项目发展持续更新。如有疑问或建议，请联系开发团队或在项目仓库中创建 Issue。

> ⚠️ **重要**: 在进行任何代码修改前，请务必仔细阅读本文档的相关章节，确保遵循既定的开发规范和最佳实践。