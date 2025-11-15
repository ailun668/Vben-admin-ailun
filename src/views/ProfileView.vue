<template>
  <div class="profile-view">
    <a-card title="个人中心" :bordered="false">
      <a-descriptions :column="2" bordered>
        <a-descriptions-item label="用户名">
          {{ userStore.userInfo?.username || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="真实姓名">
          {{ userStore.userInfo?.realName || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="邮箱">
          {{ userStore.userInfo?.email || '-' }}
        </a-descriptions-item>
        <a-descriptions-item label="角色">
          <a-tag
            v-for="role in userStore.userRoles"
            :key="role"
            color="blue"
            style="margin-right: 8px"
          >
            {{ role }}
          </a-tag>
        </a-descriptions-item>
      </a-descriptions>

      <a-divider />

      <a-space>
        <a-button type="primary" @click="handleEdit">编辑资料</a-button>
        <a-button @click="handleChangePassword">修改密码</a-button>
      </a-space>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
/**
 * @fileoverview 个人中心页面
 * @author 开发团队
 * @date 2025-01-15
 */

import { useUserStore } from '@/store/modules/user'
import { message } from 'ant-design-vue'

const userStore = useUserStore()

/**
 * 编辑资料
 */
function handleEdit() {
  message.info('编辑资料功能开发中')
}

/**
 * 修改密码
 */
function handleChangePassword() {
  message.info('修改密码功能开发中')
}
</script>

<style scoped>
.profile-view {
  padding: 0;
}
</style>

