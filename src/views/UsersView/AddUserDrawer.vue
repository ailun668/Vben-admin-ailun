<template>
  <a-drawer
    :open="props.open"
    title="新增用户"
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

function handleCancel() {
  emit('cancel')
}
</script>

<style scoped>
/**
 * 抽屉动画优化
 * @description 确保打开和关闭动画效果一致，使用统一的过渡时间和缓动函数
 */

/* 抽屉容器动画 - 统一过渡效果 */
:deep(.ant-drawer) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 抽屉内容包裹层 - 关键：确保滑入滑出效果一致 */
:deep(.ant-drawer-content-wrapper) {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 抽屉内容区域 */
:deep(.ant-drawer-content) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 抽屉头部 */
:deep(.ant-drawer-header) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 抽屉主体 */
:deep(.ant-drawer-body) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 关闭按钮动画 - 保持与其他元素一致的时间 */
:deep(.ant-drawer-close) {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

:deep(.ant-drawer-close:hover) {
  transform: scale(1.1);
}

/* 遮罩层动画 - 确保淡入淡出效果一致 */
:deep(.ant-drawer-mask) {
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
</style>

