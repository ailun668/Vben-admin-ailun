<template>
  <a-modal
    :open="props.open"
    title="新增用户"
    :confirm-loading="loading"
    :width="800"
    :destroy-on-close="true"
    :mask-closable="false"
    ok-text="确认"
    cancel-text="取消"
    @ok="handleOk"
    @cancel="handleCancel"
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
  </a-modal>
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

// 监听弹窗关闭，重置表单
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
/* 样式 */
</style>

