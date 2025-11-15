import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import Antd from 'ant-design-vue'
import VxeTable from 'vxe-table'
import VxeTablePluginExportXlsx from 'vxe-table-plugin-export-xlsx'
import App from './App.vue'
import router from './router'

import 'ant-design-vue/dist/reset.css'
import 'vxe-table/lib/style.css'
// 引入全局滚动条样式
import './styles/scrollbar.css'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.use(Antd)

// 注册 VXE-Table（必须在最后）
VxeTable.use(VxeTablePluginExportXlsx)
app.use(VxeTable)

app.mount('#app')
