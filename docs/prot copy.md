根据您的需求,我为您整理了一份完整的FuAdmin前端技术栈文档,适合AI学习和用于开发新的前端框架。<cite />

## 核心技术栈

### 基础框架
- **Vue 3.3.4** - 前端核心框架 [1](#1-0) 
- **TypeScript 5.1.6** - 类型安全的JavaScript超集 [2](#1-1) 
- **Vite 4.4.0** - 新一代前端构建工具 [3](#1-2) 

### 状态管理与路由
- **Pinia 2.1.4** - Vue 3官方推荐的状态管理库 [4](#1-3) 
- **pinia-plugin-persistedstate 3.2.0** - Pinia持久化插件 [5](#1-4) 
- **Vue Router 4.2.3** - Vue官方路由管理器 [6](#1-5) 

### UI组件库
- **Ant Design Vue** - 核心UI组件库 [7](#1-6) 
- **VbenAdmin** - 基于Ant Design Vue的中后台解决方案 [7](#1-6) 

## 核心依赖包

### 表格相关
- **vxe-table 4.4.5** - 强大的表格组件 [8](#1-7) 
- **vxe-table-plugin-export-xlsx 3.0.4** - 表格导出Excel插件 [9](#1-8) 
- **xlsx 0.18.5** - Excel文件处理库 [10](#1-9) 
- **xe-utils 3.5.11** - 表格工具函数库 [11](#1-10) 

### 编辑器组件
- **tinymce 5.10.7** - 富文本编辑器 [12](#1-11) 
- **vditor 3.9.4** - Markdown编辑器 [13](#1-12) 
- **codemirror 5.65.13** - 代码编辑器 [14](#1-13) 

### 图表与可视化
- **echarts 5.4.2** - 数据可视化图表库 [14](#1-13) 
- **qrcode 1.5.3** - 二维码生成 [15](#1-14) 

### 工具库
- **axios 1.4.0** - HTTP请求库 [14](#1-13) 
- **lodash-es 4.17.21** - JavaScript工具函数库 [14](#1-13) 
- **dayjs 1.11.9** - 日期时间处理库 [14](#1-13) 
- **crypto-js 4.1.1** - 加密库 [14](#1-13) 
- **qs 6.11.2** - URL参数序列化 [16](#1-15) 

### 国际化
- **vue-i18n 9.2.2** - Vue国际化解决方案 [17](#1-16) 

### 拖拽与交互
- **sortablejs 1.15.0** - 拖拽排序库 [18](#1-17) 
- **vuedraggable 4.1.0** - Vue拖拽组件 [19](#1-18) 
- **nprogress 0.2.0** - 页面加载进度条 [14](#1-13) 

### 其他功能库
- **print-js 1.6.0** - 打印功能 [20](#1-19) 
- **vue-json-pretty 2.2.4** - JSON格式化显示 [21](#1-20) 
- **showdown 2.1.0** - Markdown转HTML [22](#1-21) 

## 组件注册映射

### 表单组件映射
项目在`web/src/components/Form/src/componentMap.ts`中注册了所有表单组件: [23](#1-22) 

包括:
- Ant Design Vue原生组件(Input、Select、DatePicker等)
- 自定义业务组件(DictSelect、UserSelect、ApiSelect等)
- 上传组件(ImageUpload、BasicUpload)
- 增强组件(StrengthMeter、IconPicker等)

### VxeTable组件映射
在`web/src/components/VxeTable/src/componentMap.ts`中注册了表格编辑器组件: [24](#1-23) 

## 开发工具链

### 代码质量
- **@vben/eslint-config** - ESLint配置 [25](#1-24) 
- **@vben/stylelint-config** - Stylelint配置 [26](#1-25) 
- **prettier 2.8.8** - 代码格式化 [27](#1-26) 

### Git工具
- **husky 8.0.3** - Git hooks管理 [28](#1-27) 
- **lint-staged 13.2.3** - Git暂存文件检查 [29](#1-28) 
- **@commitlint/cli 17.6.6** - Commit信息规范检查 [30](#1-29) 
- **cz-git 1.6.1** - Commitizen适配器 [31](#1-30) 

### 构建工具
- **@vben/vite-config** - Vite配置 [32](#1-31) 
- **vite-plugin-mock 2.9.6** - Mock数据插件 [33](#1-32) 
- **vue-tsc 1.8.4** - Vue TypeScript编译器 [34](#1-33) 

### 包管理
- **pnpm 8.1.0** - 快速、节省磁盘空间的包管理器 [35](#1-34) 

## 项目特性说明

根据README文档,该技术栈具有以下特点: [36](#1-35) 

1. **最新技术栈** - 使用Vue3/Vite等前沿技术
2. **TypeScript支持** - 完整的类型系统
3. **主题配置** - 可配置的主题系统
4. **国际化** - 内置完善的国际化方案
5. **Mock数据** - 内置Mock数据方案
6. **权限系统** - 完善的动态路由权限生成
7. **组件封装** - 二次封装的常用组件

## 浏览器支持

推荐使用Chrome 80+浏览器进行开发,支持现代浏览器,不支持IE: [37](#1-36) 

## Notes

这份技术栈文档涵盖了FuAdmin前端的所有核心技术和依赖。如果要基于此技术栈开发新框架,建议重点关注:
1. Vue3 + TypeScript + Vite的基础架构
2. Pinia状态管理模式
3. Ant Design Vue组件的二次封装方式
4. VbenAdmin的最佳实践
5. 完整的工具链配置(ESLint、Prettier、Husky等)

所有依赖版本都已在`web/package.json`中明确定义,可以直接参考使用。

Wiki pages you might want to explore:
- [Overview (FuAdmin/fu-admin)](/wiki/FuAdmin/fu-admin#1)
- [Setup and Deployment (FuAdmin/fu-admin)](/wiki/FuAdmin/fu-admin#8)

### Citations

**File:** web/package.json (L91-91)
```json
    "path-to-regexp": "^6.2.1",
```

**File:** web/package.json (L92-92)
```json
    "pinia": "2.1.4",
```

**File:** web/package.json (L93-93)
```json
    "pinia-plugin-persistedstate": "^3.2.0",
```

**File:** web/package.json (L94-94)
```json
    "print-js": "^1.6.0",
```

**File:** web/package.json (L95-95)
```json
    "qrcode": "^1.5.3",
```

**File:** web/package.json (L96-96)
```json
    "qs": "^6.11.2",
```

**File:** web/package.json (L98-98)
```json
    "showdown": "^2.1.0",
```

**File:** web/package.json (L99-99)
```json
    "sortablejs": "^1.15.0",
```

**File:** web/package.json (L100-100)
```json
    "tinymce": "^5.10.7",
```

**File:** web/package.json (L101-101)
```json
    "vditor": "^3.9.4",
```

**File:** web/package.json (L102-102)
```json
    "vue": "^3.3.4",
```

**File:** web/package.json (L103-103)
```json
    "vue-i18n": "^9.2.2",
```

**File:** web/package.json (L104-104)
```json
    "vue-json-pretty": "^2.2.4",
```

**File:** web/package.json (L105-105)
```json
    "vue-router": "^4.2.3",
```

**File:** web/package.json (L107-107)
```json
    "vuedraggable": "^4.1.0",
```

**File:** web/package.json (L108-108)
```json
    "vxe-table": "^4.4.5",
```

**File:** web/package.json (L109-109)
```json
    "vxe-table-plugin-export-xlsx": "^3.0.4",
```

**File:** web/package.json (L110-110)
```json
    "xe-utils": "^3.5.11",
```

**File:** web/package.json (L111-111)
```json
    "xlsx": "^0.18.5"
```

**File:** web/package.json (L114-114)
```json
    "@commitlint/cli": "^17.6.6",
```

**File:** web/package.json (L127-127)
```json
    "@vben/eslint-config": "workspace:*",
```

**File:** web/package.json (L128-128)
```json
    "@vben/stylelint-config": "workspace:*",
```

**File:** web/package.json (L131-131)
```json
    "@vben/vite-config": "workspace:*",
```

**File:** web/package.json (L135-135)
```json
    "cz-git": "^1.6.1",
```

**File:** web/package.json (L137-137)
```json
    "husky": "^8.0.3",
```

**File:** web/package.json (L138-138)
```json
    "lint-staged": "13.2.3",
```

**File:** web/package.json (L139-139)
```json
    "prettier": "^2.8.8",
```

**File:** web/package.json (L143-143)
```json
    "typescript": "^5.1.6",
```

**File:** web/package.json (L145-145)
```json
    "vite": "^4.4.0",
```

**File:** web/package.json (L146-146)
```json
    "vite-plugin-mock": "^2.9.6",
```

**File:** web/package.json (L147-147)
```json
    "vue-tsc": "^1.8.4"
```

**File:** web/package.json (L149-149)
```json
  "packageManager": "pnpm@8.1.0",
```

**File:** README.md (L46-46)
```markdown
- 🧑‍🤝‍🧑 前端采用[VbenAdmin](https://vvbin.cn/doc-next) 、[Vue3](https://cn.vuejs.org/)、[Ant Design Vue](https://www.antdv.com/docs/vue/getting-started-cn)。
```

**File:** web/src/components/Form/src/componentMap.ts (L39-79)
```typescript
const componentMap = new Map<ComponentType, Component>();
componentMap.set('DictSelect', DictSelect);
componentMap.set('UserSelect', UserSelect);

componentMap.set('Input', Input);
componentMap.set('InputGroup', Input.Group);
componentMap.set('InputPassword', Input.Password);
componentMap.set('InputSearch', Input.Search);
componentMap.set('InputTextArea', Input.TextArea);
componentMap.set('InputNumber', InputNumber);
componentMap.set('AutoComplete', AutoComplete);
componentMap.set('ImageUpload', ImageUpload);
componentMap.set('Select', Select);
componentMap.set('ApiSelect', ApiSelect);
componentMap.set('ApiTree', ApiTree);
componentMap.set('TreeSelect', TreeSelect);
componentMap.set('ApiTreeSelect', ApiTreeSelect);
componentMap.set('ApiRadioGroup', ApiRadioGroup);
componentMap.set('Switch', Switch);
componentMap.set('RadioButtonGroup', RadioButtonGroup);
componentMap.set('RadioGroup', Radio.Group);
componentMap.set('Checkbox', Checkbox);
componentMap.set('CheckboxGroup', Checkbox.Group);
componentMap.set('ApiCascader', ApiCascader);
componentMap.set('Cascader', Cascader);
componentMap.set('Slider', Slider);
componentMap.set('Rate', Rate);
componentMap.set('ApiTransfer', ApiTransfer);

componentMap.set('DatePicker', DatePicker);
componentMap.set('MonthPicker', DatePicker.MonthPicker);
componentMap.set('RangePicker', DatePicker.RangePicker);
componentMap.set('WeekPicker', DatePicker.WeekPicker);
componentMap.set('TimePicker', TimePicker);
componentMap.set('TimeRangePicker', TimePicker.TimeRangePicker);
componentMap.set('StrengthMeter', StrengthMeter);
componentMap.set('IconPicker', IconPicker);
componentMap.set('InputCountDown', CountdownInput);

componentMap.set('Upload', BasicUpload);
componentMap.set('Divider', Divider);
```

**File:** web/src/components/VxeTable/src/componentMap.ts (L22-49)
```typescript
const componentMap = new Map<ComponentType, Component>();

componentMap.set('AButton', Button);

componentMap.set('AInput', Input);
componentMap.set('AInputSearch', Input.Search);
componentMap.set('AInputNumber', InputNumber);
componentMap.set('AAutoComplete', AutoComplete);

componentMap.set('ASelect', Select);
componentMap.set('ATreeSelect', TreeSelect);
componentMap.set('ASwitch', Switch);
componentMap.set('ARadioGroup', Radio.Group);
componentMap.set('ACheckboxGroup', Checkbox.Group);
componentMap.set('ACascader', Cascader);
componentMap.set('ARate', Rate);

componentMap.set('ADatePicker', DatePicker);
componentMap.set('AMonthPicker', DatePicker.MonthPicker);
componentMap.set('ARangePicker', DatePicker.RangePicker);
componentMap.set('AWeekPicker', DatePicker.WeekPicker);
componentMap.set('AYearPicker', DatePicker.YearPicker);
componentMap.set('ATimePicker', TimePicker);

componentMap.set('AApiSelect', ApiSelect);
componentMap.set('AApiTreeSelect', ApiTreeSelect);

componentMap.set('AEmpty', Empty);
```

**File:** web/README.zh-CN.md (L16-22)
```markdown
- **最新技术栈**：使用 Vue3/vite2 等前端前沿技术开发
- **TypeScript**: 应用程序级 JavaScript 的语言
- **主题**：可配置的主题
- **国际化**：内置完善的国际化方案
- **Mock 数据** 内置 Mock 数据方案
- **权限** 内置完善的动态路由权限生成方案
- **组件** 二次封装了多个常用的组件
```

**File:** web/README.zh-CN.md (L151-154)
```markdown

| [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt=" Edge" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>IE | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt=" Edge" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Edge | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png" alt="Firefox" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Firefox | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png" alt="Chrome" width="24px" height="24px" />](http://godban.github.io/browsers-support- ... (truncated)
| :-: | :-: | :-: | :-: | :-: |
| not support | last 2 versions | last 2 versions | last 2 versions | last 2 versions |
```
