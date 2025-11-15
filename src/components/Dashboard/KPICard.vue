/**
 * @fileoverview KPI 卡片组件
 * @author AI Developer
 * @date 2024-01-XX
 */

<template>
  <a-card class="kpi-card" :bordered="false" hoverable>
    <div class="kpi-card-header">
      <span class="kpi-card-name">{{ card.name }}</span>
      <div class="kpi-card-icon" :style="{ backgroundColor: card.iconColor }">
        <component :is="iconComponent" />
      </div>
    </div>
    <div class="kpi-card-value">{{ formatValue(card.value) }}</div>
    <div class="kpi-card-trend" :class="`trend-${card.trend}`">
      <component :is="trendIcon" />
      <span>{{ card.trendValue }} 较上月</span>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { computed, h } from 'vue'
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons-vue'
import {
  UserOutlined,
  DollarOutlined,
  ShoppingCartOutlined,
  LineChartOutlined
} from '@ant-design/icons-vue'
import type { KPICard } from '@/types/dashboard'

/**
 * 组件属性
 */
interface Props {
  /** KPI 卡片数据 */
  card: KPICard
}

const props = defineProps<Props>()

/**
 * 图标映射
 */
const iconMap: Record<string, any> = {
  users: UserOutlined,
  dollar: DollarOutlined,
  cart: ShoppingCartOutlined,
  chart: LineChartOutlined
}

/**
 * 图标组件
 */
const iconComponent = computed(() => {
  return iconMap[props.card.iconName] || UserOutlined
})

/**
 * 趋势图标
 */
const trendIcon = computed(() => {
  return props.card.trend === 'up' ? ArrowUpOutlined : ArrowDownOutlined
})

/**
 * 格式化数值
 */
const formatValue = (value: string | number): string => {
  if (typeof value === 'number') {
    if (value >= 10000) {
      return (value / 10000).toFixed(1) + '万'
    }
    return value.toLocaleString()
  }
  return value
}
</script>

<style scoped>
.kpi-card {
  border-left: 4px solid var(--ant-primary-color);
  transition: all 0.3s ease;
}

.kpi-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.kpi-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.kpi-card-name {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.45);
}

.kpi-card-icon {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
}

.kpi-card-value {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: rgba(0, 0, 0, 0.85);
}

.kpi-card-trend {
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.trend-up {
  color: #52c41a;
}

.trend-down {
  color: #ff4d4f;
}
</style>

