<template>
  <div class="home-container">
    <a-card title="欢迎" :bordered="false">
      <div class="welcome-content">
        <h1>欢迎回来，{{ userName }}！</h1>
        <p class="subtitle">这是一个现代化的 Vue 3 + TypeScript 企业管理系统</p>

        <a-divider />

        <div class="user-info">
          <a-row :gutter="16">
            <a-col :xs="24" :sm="12">
              <div class="info-box">
                <img :src="userInfo?.avatar" alt="avatar" class="avatar" />
                <div class="info-text">
                  <p class="label">用户名</p>
                  <p class="value">{{ userInfo?.username }}</p>
                </div>
              </div>
            </a-col>
            <a-col :xs="24" :sm="12">
              <div class="info-box">
                <div class="info-text">
                  <p class="label">邮箱</p>
                  <p class="value">{{ userInfo?.email }}</p>
                </div>
              </div>
            </a-col>
            <a-col :xs="24" :sm="12">
              <div class="info-box">
                <div class="info-text">
                  <p class="label">角色</p>
                  <p class="value">
                    <a-tag
                      v-for="role in userInfo?.roles"
                      :key="role"
                      color="blue"
                    >
                      {{ role }}
                    </a-tag>
                  </p>
                </div>
              </div>
            </a-col>
            <a-col :xs="24" :sm="12">
              <div class="info-box">
                <div class="info-text">
                  <p class="label">权限数</p>
                  <p class="value">{{ userInfo?.permissions.length || 0 }} 项</p>
                </div>
              </div>
            </a-col>
          </a-row>
        </div>

        <a-divider />

        <div class="quick-links">
          <h3>快速链接</h3>
          <a-button-group>
            <a-button type="primary" href="/dashboard" v-if="hasRole('admin')">
              前往仪表盘
            </a-button>
            <a-button @click="showProjectInfo">查看项目信息</a-button>
          </a-button-group>
        </div>
      </div>
    </a-card>

    <!-- 项目信息 Modal -->
    <a-modal
      v-model:open="modalVisible"
      title="项目信息"
      :footer="null"
      width="600px"
    >
      <a-descriptions :column="2" bordered>
        <a-descriptions-item label="项目名称">
          My Vue App
        </a-descriptions-item>
        <a-descriptions-item label="版本">
          v1.0.0
        </a-descriptions-item>
        <a-descriptions-item label="框架" :span="2">
          Vue 3.5.24
        </a-descriptions-item>
        <a-descriptions-item label="TypeScript" :span="2">
          5.9.3
        </a-descriptions-item>
        <a-descriptions-item label="构建工具" :span="2">
          Vite 7.2.2
        </a-descriptions-item>
        <a-descriptions-item label="UI 框架" :span="2">
          Ant Design Vue 4.2.6
        </a-descriptions-item>
        <a-descriptions-item label="状态管理" :span="2">
          Pinia 3.0.4
        </a-descriptions-item>
        <a-descriptions-item label="HTTP 客户端" :span="2">
          axios 1.13.2
        </a-descriptions-item>
      </a-descriptions>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/store/modules/user'

const userStore = useUserStore()
const modalVisible = ref(false)

const userName = userStore.userName
const userInfo = userStore.userInfo

function hasRole(role: string): boolean {
  return userStore.hasRole(role)
}

function showProjectInfo() {
  modalVisible.value = true
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.welcome-content {
  padding: 20px;
}

.welcome-content h1 {
  margin: 0 0 10px;
  font-size: 28px;
  font-weight: 600;
  color: #1890ff;
}

.subtitle {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.user-info {
  margin: 20px 0;
}

.info-box {
  display: flex;
  align-items: center;
  padding: 12px;
  background-color: #f5f5f5;
  border-radius: 4px;
  margin-bottom: 12px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  margin-right: 12px;
  object-fit: cover;
}

.info-text {
  flex: 1;
}

.info-text .label {
  margin: 0;
  font-size: 12px;
  color: #999;
  font-weight: 500;
  text-transform: uppercase;
}

.info-text .value {
  margin: 4px 0 0;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.quick-links {
  margin: 20px 0;
}

.quick-links h3 {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
}

:deep(.ant-divider) {
  margin: 16px 0;
}
</style>
