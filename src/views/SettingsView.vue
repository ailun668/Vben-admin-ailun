<template>
  <div class="settings-view">
    <h1>设置</h1>
    <a-card title="系统设置" style="margin-bottom: 20px">
      <a-form layout="vertical">
        <a-form-item label="应用名称">
          <a-input v-model:value="settings.appName" placeholder="请输入应用名称" />
        </a-form-item>
        <a-form-item label="主题颜色">
          <a-select v-model:value="settings.theme" placeholder="选择主题">
            <a-select-option value="light">浅色</a-select-option>
            <a-select-option value="dark">深色</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="语言">
          <a-select v-model:value="settings.language" placeholder="选择语言">
            <a-select-option value="zh">中文</a-select-option>
            <a-select-option value="en">English</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="saveSettings">保存设置</a-button>
        </a-form-item>
      </a-form>
    </a-card>

    <a-card title="个人设置">
      <a-form layout="vertical">
        <a-form-item label="邮箱">
          <a-input v-model:value="userSettings.email" disabled />
        </a-form-item>
        <a-form-item label="手机号">
          <a-input v-model:value="userSettings.phone" placeholder="请输入手机号" />
        </a-form-item>
        <a-form-item label="修改密码">
          <a-button type="primary" @click="showPasswordModal">修改密码</a-button>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" @click="saveUserSettings">保存个人设置</a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { message } from 'ant-design-vue'

const settings = reactive({
  appName: '我的 Vue 应用',
  theme: 'light',
  language: 'zh'
})

const userSettings = reactive({
  email: 'user@example.com',
  phone: ''
})

const saveSettings = () => {
  message.success('系统设置保存成功')
}

const saveUserSettings = () => {
  message.success('个人设置保存成功')
}

const showPasswordModal = () => {
  message.info('密码修改功能开发中')
}
</script>

<style scoped>
.settings-view {
  padding: 16px;
  max-width: 800px;
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
}
</style>
