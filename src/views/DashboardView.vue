<template>
  <div class="dashboard-container">
    <a-row :gutter="16">
      <a-col :xs="24" :sm="12" :md="6">
        <a-statistic
          title="总用户数"
          :value="1024"
          :value-style="{ color: '#1890ff' }"
        >
          <template #prefix>
            <user-outlined />
          </template>
        </a-statistic>
      </a-col>
      <a-col :xs="24" :sm="12" :md="6">
        <a-statistic
          title="今日访问量"
          :value="245"
          :value-style="{ color: '#52c41a' }"
        >
          <template #prefix>
            <eye-outlined />
          </template>
        </a-statistic>
      </a-col>
      <a-col :xs="24" :sm="12" :md="6">
        <a-statistic
          title="销售额"
          :value="98500"
          :value-style="{ color: '#faad14' }"
          prefix="¥"
        >
          <template #prefix>
            <shop-outlined />
          </template>
        </a-statistic>
      </a-col>
      <a-col :xs="24" :sm="12" :md="6">
        <a-statistic
          title="转化率"
          :value="99.8"
          :value-style="{ color: '#f5222d' }"
          suffix="%"
        >
          <template #prefix>
            <line-chart-outlined />
          </template>
        </a-statistic>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 16px">
      <a-col :xs="24" :lg="12">
        <a-card title="最近访问" :bordered="false">
          <a-list
            data-source="data"
            size="small"
            :split="false"
          >
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta>
                  <template #title>{{ item.title }}</template>
                  <template #description>{{ item.time }}</template>
                </a-list-item-meta>
              </a-list-item>
            </template>
          </a-list>
          <a-empty style="margin-top: 20px" />
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="12">
        <a-card title="系统信息" :bordered="false">
          <a-descriptions :column="1" size="small">
            <a-descriptions-item label="系统名称">
              My Vue App
            </a-descriptions-item>
            <a-descriptions-item label="版本">
              v1.0.0
            </a-descriptions-item>
            <a-descriptions-item label="框架">
              Vue 3 + TypeScript + Vite
            </a-descriptions-item>
            <a-descriptions-item label="UI 库">
              Ant Design Vue
            </a-descriptions-item>
            <a-descriptions-item label="状态管理">
              Pinia
            </a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import {
  UserOutlined,
  EyeOutlined,
  ShopOutlined,
  LineChartOutlined
} from '@ant-design/icons-vue'
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

:deep(.ant-statistic-title) {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
}

:deep(.ant-statistic-content-value) {
  font-size: 24px;
}
</style>
