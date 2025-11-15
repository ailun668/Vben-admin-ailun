<template>
  <a-drawer
    :open="props.open"
    title="新增角色"
    :width="600"
    placement="right"
    :mask-closable="true"
    @close="handleCancel"
  >
    <a-form
      ref="formRef"
      :model="formData"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 18 }"
      :rules="formRules"
    >
      <a-form-item label="角色名称" name="name">
        <a-input
          v-model:value="formData.name"
          placeholder="请输入角色名称（如：管理员）"
          allow-clear
        />
      </a-form-item>

      <a-form-item label="角色代码" name="code">
        <a-input
          v-model:value="formData.code"
          placeholder="请输入角色代码（如：admin）"
          allow-clear
        />
      </a-form-item>

      <a-form-item label="角色描述" name="description">
        <a-input
          v-model:value="formData.description"
          placeholder="请输入角色描述"
          allow-clear
        />
      </a-form-item>

      <a-form-item label="权限" name="permissions">
        <a-select
          v-model:value="formData.permissions"
          mode="multiple"
          placeholder="请选择权限"
          :options="permissionOptions"
          allow-clear
        />
      </a-form-item>

      <a-form-item label="状态" name="status">
        <a-select
          v-model:value="formData.status"
          placeholder="请选择状态"
          :options="statusOptions"
        />
      </a-form-item>
    </a-form>
    <template #footer>
      <div style="text-align: right">
        <a-button style="margin-right: 8px" @click="handleCancel">
          取消
        </a-button>
        <a-button type="primary" :loading="loading" @click="handleOk">
          确认
        </a-button>
      </div>
    </template>
  </a-drawer>
</template>

<script setup lang="ts">
/**
 * @fileoverview 新增角色抽屉组件
 * @author 开发团队
 * @date 2025-01-15
 */

import { ref, reactive, watch } from 'vue'
import { message } from 'ant-design-vue'
import type { FormInstance } from 'ant-design-vue'

interface Props {
  open: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  cancel: []
  success: []
}>()

const formRef = ref<FormInstance>()
const loading = ref(false)

const formData = reactive({
  name: '',
  code: '',
  description: '',
  permissions: [] as string[],
  status: 'active' as 'active' | 'inactive'
})

const formRules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入角色代码', trigger: 'blur' }],
  permissions: [{ required: true, message: '请选择权限', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

const permissionOptions = [
  { label: 'user.view', value: 'user.view' },
  { label: 'user.create', value: 'user.create' },
  { label: 'user.edit', value: 'user.edit' },
  { label: 'user.delete', value: 'user.delete' },
  { label: 'role.view', value: 'role.view' },
  { label: 'role.create', value: 'role.create' },
  { label: 'role.edit', value: 'role.edit' },
  { label: 'role.delete', value: 'role.delete' },
  { label: 'permission.view', value: 'permission.view' },
  { label: 'permission.create', value: 'permission.create' },
  { label: 'permission.edit', value: 'permission.edit' },
  { label: 'permission.delete', value: 'permission.delete' }
]

const statusOptions = [
  { label: '活跃', value: 'active' },
  { label: '停用', value: 'inactive' }
]

// 监听侧边栏关闭，重置表单
watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) {
      formRef.value?.resetFields()
      Object.assign(formData, {
        name: '',
        code: '',
        description: '',
        permissions: [],
        status: 'active'
      })
    }
  }
)

async function handleOk() {
  try {
    await formRef.value?.validate()
    loading.value = true

    // 模拟 API 调用
    await new Promise(resolve => setTimeout(resolve, 500))

    message.success('角色创建成功')
    emit('success')
  } catch (error: any) {
    if (error?.errorFields) {
      return
    }
    console.error('创建角色失败:', error)
    message.error('创建角色失败')
  } finally {
    loading.value = false
  }
}

function handleCancel() {
  emit('cancel')
}
</script>

<style scoped>
/* 抽屉关闭动画优化 */
:deep(.ant-drawer) {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

:deep(.ant-drawer-content-wrapper) {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

:deep(.ant-drawer-content) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 抽屉关闭时的动画 */
:deep(.ant-drawer-close) {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.ant-drawer-close:hover) {
  transform: scale(1.1);
}

/* 遮罩层动画 */
:deep(.ant-drawer-mask) {
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              visibility 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
</style>

