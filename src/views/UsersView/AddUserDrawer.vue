<template>
  <a-drawer
    v-if="props.open"
    :open="props.open"
    title="新增用户"
    :width="600"
    placement="right"
    :mask-closable="true"
    :transition-name="false"
    :class="{ 'drawer-closing-state': isClosing }"
    @close="triggerClose"
  >
    <a-form
      ref="formRef"
      :model="formData"
      :label-col="{ span: 6 }"
      :wrapper-col="{ span: 18 }"
      :rules="formRules"
    >
      <a-form-item label="用户名" name="username">
        <a-input
          v-model:value="formData.username"
          placeholder="请输入用户名"
          allow-clear
        />
      </a-form-item>

      <a-form-item label="真实姓名" name="realName">
        <a-input
          v-model:value="formData.realName"
          placeholder="请输入真实姓名"
          allow-clear
        />
      </a-form-item>

      <a-form-item label="邮箱" name="email">
        <a-input
          v-model:value="formData.email"
          placeholder="请输入邮箱"
          allow-clear
        />
      </a-form-item>

      <a-form-item label="角色" name="roles">
        <a-select
          v-model:value="formData.roles"
          mode="multiple"
          placeholder="请选择角色"
          :options="roleOptions"
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
        <a-button style="margin-right: 8px" @click="triggerClose">
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
const isClosing = ref(false)

const formData = reactive({
  username: '',
  realName: '',
  email: '',
  roles: [] as string[],
  status: 'active' as 'active' | 'inactive'
})

const formRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  realName: [{ required: true, message: '请输入真实姓名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  roles: [{ required: true, message: '请选择角色', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

const roleOptions = [
  { label: '管理员', value: 'admin' },
  { label: '普通用户', value: 'user' },
  { label: '编辑', value: 'editor' },
  { label: '查看者', value: 'viewer' }
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
        username: '',
        realName: '',
        email: '',
        roles: [],
        status: 'active'
      })
    }
  }
)

async function handleOk() {
  try {
    await formRef.value?.validate()
    loading.value = true

    // 模拟 API 调用（使用静态数据）
    await new Promise(resolve => setTimeout(resolve, 500))

    message.success('用户创建成功')
    emit('success')

    // 触发关闭动画而不是直接关闭
    triggerClose()
  } catch (error: any) {
    if (error?.errorFields) {
      // 表单验证错误
      return
    }
    console.error('创建用户失败:', error)
    message.error('创建用户失败')
  } finally {
    loading.value = false
  }
}

/**
 * 触发Drawer关闭 - 实现延迟状态变化以支持关闭动画
 */
function triggerClose() {
  isClosing.value = true

  // 等待关闭动画完成（0.3s）后再发送cancel事件（关闭Drawer）
  setTimeout(() => {
    isClosing.value = false
    emit('cancel')
  }, 300)
}
</script>

<style scoped>
/* ========== Drawer 关闭动画配置 ========== */
/* Drawer的打开状态（默认状态）- 确保平滑打开动画 */
:deep(.ant-drawer-mask) {
  opacity: 1 !important;
  visibility: visible !important;
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1), visibility 0.3s !important;
}

:deep(.ant-drawer-content-wrapper) {
  transform: translateX(0) !important;
  opacity: 1 !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* Drawer的关闭状态 - drawer-closing-state类被添加到ant-drawer容器时生效 */
:deep(.ant-drawer.drawer-closing-state) .ant-drawer-mask {
  opacity: 0 !important;
  visibility: hidden !important;
}

:deep(.ant-drawer.drawer-closing-state) .ant-drawer-content-wrapper {
  transform: translateX(100%) !important;
  opacity: 0 !important;
}

/* 关闭按钮悬停效果 */
:deep(.ant-drawer-close) {
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), color 0.2s !important;
}

:deep(.ant-drawer-close:hover) {
  transform: scale(1.15) !important;
}
</style>

