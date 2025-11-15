# Ant Design Vue 技术文档

> 本文档基于 Ant Design Vue 官方文档整理，包含完整的技术实现细节和使用指南

## 📚 目录

- [项目概述](#项目概述)
- [快速开始](#快速开始)
- [组件使用](#组件使用)
- [主题定制](#主题定制)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 项目概述

Ant Design Vue 是一个企业级的 UI 设计语言和 Vue 实现，提供了一套高质量、开箱即用的 Vue 组件。

### 核心特性

- ✅ **企业级设计**: 基于 Ant Design 设计语言
- ✅ **高质量组件**: 60+ 个高质量组件
- ✅ **TypeScript**: 完整的 TypeScript 支持
- ✅ **Vue 2 & Vue 3**: 同时支持 Vue 2 和 Vue 3
- ✅ **国际化**: 内置国际化支持
- ✅ **主题定制**: 支持主题定制和暗色模式

### 技术栈

- **Vue**: 2.x / 3.x
- **TypeScript**: 完整类型定义
- **Less**: 样式预处理器
- **Day.js**: 日期处理库

---

## 快速开始

### 安装

```bash
# npm
npm install ant-design-vue --save

# yarn
yarn add ant-design-vue

# pnpm
pnpm add ant-design-vue
```

### 完整引入

```ts
import { createApp } from 'vue';
import Antd from 'ant-design-vue';
import App from './App';
import 'ant-design-vue/dist/reset.css';

const app = createApp(App);
app.use(Antd);
app.mount('#app');
```

### 按需引入

```vue
<script setup lang="ts">
import { Button, Input, Table } from 'ant-design-vue';
</script>

<template>
  <Button type="primary">按钮</Button>
  <Input placeholder="请输入" />
</template>
```

### 使用 Vite 插件 (推荐)

```bash
npm install vite-plugin-style-import -D
```

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import styleImport from 'vite-plugin-style-import';

export default defineConfig({
  plugins: [
    vue(),
    styleImport({
      libs: [
        {
          libraryName: 'ant-design-vue',
          esModule: true,
          resolveStyle: (name) => {
            return `ant-design-vue/es/${name}/style/css`;
          },
        },
      ],
    }),
  ],
});
```

---

## 组件使用

### 基础组件

#### Button 按钮

```vue
<template>
  <div>
    <a-button type="primary">主要按钮</a-button>
    <a-button>默认按钮</a-button>
    <a-button type="dashed">虚线按钮</a-button>
    <a-button type="text">文本按钮</a-button>
    <a-button type="link">链接按钮</a-button>
    
    <a-button type="primary" danger>危险按钮</a-button>
    <a-button type="primary" :loading="loading">加载中</a-button>
    <a-button type="primary" :disabled="disabled">禁用</a-button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Button } from 'ant-design-vue';

const loading = ref(false);
const disabled = ref(false);
</script>
```

#### Input 输入框

```vue
<template>
  <div>
    <a-input v-model:value="value" placeholder="请输入" />
    <a-input-password v-model:value="password" placeholder="请输入密码" />
    <a-textarea v-model:value="textarea" :rows="4" placeholder="请输入" />
    
    <a-input-search
      v-model:value="searchValue"
      placeholder="搜索"
      enter-button
      @search="onSearch"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Input } from 'ant-design-vue';

const value = ref('');
const password = ref('');
const textarea = ref('');
const searchValue = ref('');

const onSearch = (value: string) => {
  console.log('搜索:', value);
};
</script>
```

#### Form 表单

```vue
<template>
  <a-form
    :model="formState"
    :rules="rules"
    :label-col="{ span: 6 }"
    :wrapper-col="{ span: 18 }"
    @finish="onFinish"
    @finishFailed="onFinishFailed"
  >
    <a-form-item label="用户名" name="username">
      <a-input v-model:value="formState.username" />
    </a-form-item>
    
    <a-form-item label="密码" name="password">
      <a-input-password v-model:value="formState.password" />
    </a-form-item>
    
    <a-form-item :wrapper-col="{ offset: 6, span: 18 }">
      <a-button type="primary" html-type="submit">提交</a-button>
    </a-form-item>
  </a-form>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { Form, Input, Button } from 'ant-design-vue';
import type { Rule } from 'ant-design-vue/es/form';

interface FormState {
  username: string;
  password: string;
}

const formState = reactive<FormState>({
  username: '',
  password: '',
});

const rules: Record<string, Rule[]> = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少 6 个字符', trigger: 'blur' },
  ],
};

const onFinish = (values: FormState) => {
  console.log('提交成功:', values);
};

const onFinishFailed = (errors: any) => {
  console.log('提交失败:', errors);
};
</script>
```

### 数据展示组件

#### Table 表格

```vue
<template>
  <a-table
    :columns="columns"
    :data-source="dataSource"
    :pagination="{ pageSize: 10 }"
    :loading="loading"
    @change="handleTableChange"
  >
    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'action'">
        <a-button type="link" @click="handleEdit(record)">编辑</a-button>
        <a-button type="link" danger @click="handleDelete(record)">删除</a-button>
      </template>
    </template>
  </a-table>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Table, Button } from 'ant-design-vue';
import type { ColumnsType } from 'ant-design-vue/es/table';

interface DataType {
  key: string;
  name: string;
  age: number;
  address: string;
}

const columns: ColumnsType<DataType> = [
  {
    title: '姓名',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '年龄',
    dataIndex: 'age',
    key: 'age',
    sorter: (a, b) => a.age - b.age,
  },
  {
    title: '地址',
    dataIndex: 'address',
    key: 'address',
  },
  {
    title: '操作',
    key: 'action',
  },
];

const dataSource = ref<DataType[]>([
  {
    key: '1',
    name: '张三',
    age: 32,
    address: '北京市朝阳区',
  },
  {
    key: '2',
    name: '李四',
    age: 28,
    address: '上海市浦东新区',
  },
]);

const loading = ref(false);

const handleTableChange = (pag: any, filters: any, sorter: any) => {
  console.log('表格变化:', pag, filters, sorter);
};

const handleEdit = (record: DataType) => {
  console.log('编辑:', record);
};

const handleDelete = (record: DataType) => {
  console.log('删除:', record);
};
</script>
```

#### Card 卡片

```vue
<template>
  <a-card title="卡片标题" :bordered="false">
    <p>卡片内容</p>
    <template #extra>
      <a-button type="link">更多</a-button>
    </template>
  </a-card>
</template>

<script setup lang="ts">
import { Card, Button } from 'ant-design-vue';
</script>
```

### 反馈组件

#### Message 消息提示

```vue
<template>
  <div>
    <a-button @click="showSuccess">成功</a-button>
    <a-button @click="showError">错误</a-button>
    <a-button @click="showWarning">警告</a-button>
    <a-button @click="showInfo">信息</a-button>
  </div>
</template>

<script setup lang="ts">
import { Button, message } from 'ant-design-vue';

const showSuccess = () => {
  message.success('操作成功');
};

const showError = () => {
  message.error('操作失败');
};

const showWarning = () => {
  message.warning('警告信息');
};

const showInfo = () => {
  message.info('提示信息');
};
</script>
```

#### Modal 对话框

```vue
<template>
  <div>
    <a-button type="primary" @click="showModal">打开对话框</a-button>
    <a-modal
      v-model:open="visible"
      title="标题"
      @ok="handleOk"
      @cancel="handleCancel"
    >
      <p>对话框内容</p>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Button, Modal } from 'ant-design-vue';

const visible = ref(false);

const showModal = () => {
  visible.value = true;
};

const handleOk = () => {
  console.log('确认');
  visible.value = false;
};

const handleCancel = () => {
  console.log('取消');
  visible.value = false;
};
</script>
```

#### Notification 通知

```vue
<template>
  <div>
    <a-button @click="openNotification">打开通知</a-button>
  </div>
</template>

<script setup lang="ts">
import { Button, notification } from 'ant-design-vue';

const openNotification = () => {
  notification.open({
    message: '通知标题',
    description: '这是通知的描述信息',
    placement: 'topRight',
  });
};
</script>
```

### 导航组件

#### Menu 菜单

```vue
<template>
  <a-menu
    v-model:selectedKeys="selectedKeys"
    v-model:openKeys="openKeys"
    mode="inline"
    theme="dark"
    @click="handleClick"
  >
    <a-menu-item key="1">
      <template #icon>
        <UserOutlined />
      </template>
      用户管理
    </a-menu-item>
    <a-sub-menu key="sub1">
      <template #icon>
        <SettingOutlined />
      </template>
      <template #title>系统设置</template>
      <a-menu-item key="2">基本设置</a-menu-item>
      <a-menu-item key="3">权限设置</a-menu-item>
    </a-sub-menu>
  </a-menu>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Menu } from 'ant-design-vue';
import { UserOutlined, SettingOutlined } from '@ant-design/icons-vue';

const selectedKeys = ref<string[]>(['1']);
const openKeys = ref<string[]>(['sub1']);

const handleClick = (e: any) => {
  console.log('点击菜单:', e);
};
</script>
```

#### Tabs 标签页

```vue
<template>
  <a-tabs v-model:activeKey="activeKey" @change="handleChange">
    <a-tab-pane key="1" tab="标签页 1">
      内容 1
    </a-tab-pane>
    <a-tab-pane key="2" tab="标签页 2">
      内容 2
    </a-tab-pane>
    <a-tab-pane key="3" tab="标签页 3">
      内容 3
    </a-tab-pane>
  </a-tabs>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Tabs } from 'ant-design-vue';

const activeKey = ref('1');

const handleChange = (key: string) => {
  console.log('切换标签:', key);
};
</script>
```

---

## 主题定制

### 使用 Less 变量

创建 `src/styles/theme.less`:

```less
@import '~ant-design-vue/es/style/themes/default.less';

@primary-color: #1890ff;
@border-radius-base: 4px;
@font-size-base: 14px;
```

在 `main.ts` 中引入:

```ts
import './styles/theme.less';
```

### 使用 CSS 变量 (Vue 3)

```css
:root {
  --ant-primary-color: #1890ff;
  --ant-border-radius-base: 4px;
  --ant-font-size-base: 14px;
}
```

### 暗色主题

```ts
import { ConfigProvider } from 'ant-design-vue';

// 在根组件中使用
<ConfigProvider :theme="{ algorithm: theme.darkAlgorithm }">
  <App />
</ConfigProvider>
```

---

## 最佳实践

### 1. 按需引入

使用 Vite 插件实现按需引入，减少打包体积。

### 2. 类型安全

充分利用 TypeScript 类型定义：

```ts
import type { TableColumnsType } from 'ant-design-vue/es/table';
import type { FormProps } from 'ant-design-vue/es/form';
```

### 3. 组件封装

封装常用组件组合：

```vue
<!-- SearchForm.vue -->
<template>
  <a-form :model="formState" layout="inline">
    <a-form-item label="关键词">
      <a-input v-model:value="formState.keyword" placeholder="请输入" />
    </a-form-item>
    <a-form-item>
      <a-button type="primary" @click="handleSearch">搜索</a-button>
      <a-button @click="handleReset">重置</a-button>
    </a-form-item>
  </a-form>
</template>
```

### 4. 表单验证

使用统一的验证规则：

```ts
// utils/validate.ts
export const validateRules = {
  required: (message: string) => ({
    required: true,
    message,
    trigger: 'blur',
  }),
  email: {
    type: 'email',
    message: '请输入有效的邮箱地址',
    trigger: 'blur',
  },
  phone: {
    pattern: /^1[3-9]\d{9}$/,
    message: '请输入有效的手机号码',
    trigger: 'blur',
  },
};
```

---

## 常见问题

### 1. 样式不生效

确保引入了样式文件：

```ts
import 'ant-design-vue/dist/reset.css';
```

### 2. 图标不显示

安装图标包：

```bash
npm install @ant-design/icons-vue
```

使用：

```ts
import { UserOutlined } from '@ant-design/icons-vue';
```

### 3. TypeScript 类型错误

确保安装了类型定义：

```bash
npm install --save-dev @types/node
```

### 4. 表单验证不生效

确保使用 `v-model:value` 而不是 `v-model`：

```vue
<a-input v-model:value="formState.username" />
```

---

## 参考资料

- [Ant Design Vue 官方文档](https://antdv.com/)
- [Ant Design 设计规范](https://ant.design/docs/spec/introduce-cn)
- [Vue 3 官方文档](https://vuejs.org/)
- [TypeScript 官方文档](https://www.typescriptlang.org/)

---

**文档版本**: v1.0  
**最后更新**: 2024年  
**维护者**: Ant Design Vue 团队

