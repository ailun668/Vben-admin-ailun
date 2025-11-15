/**
 * @fileoverview 图表卡片组件
 * @author AI Developer
 * @date 2024-01-XX
 */

<template>
  <a-card class="chart-card" :bordered="false">
    <template #title>
      <span class="chart-title">{{ title }}</span>
    </template>
    <div ref="chartRef" class="chart-container"></div>
  </a-card>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

/**
 * 组件属性
 */
interface Props {
  /** 图表标题 */
  title: string
  /** ECharts 配置项 */
  option: EChartsOption
  /** 图表高度 */
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '350px'
})

const chartRef = ref<HTMLDivElement | null>(null)
let chartInstance: echarts.ECharts | null = null
let resizeHandler: (() => void) | null = null

/**
 * 初始化图表
 */
const initChart = async () => {
  if (!chartRef.value) return

  await nextTick()

  // 如果已存在实例，先销毁
  if (chartInstance) {
    chartInstance.dispose()
  }

  // 创建新实例
  chartInstance = echarts.init(chartRef.value)

  // 设置配置项
  chartInstance.setOption(props.option)

  // 响应式调整
  resizeHandler = () => {
    chartInstance?.resize()
  }

  window.addEventListener('resize', resizeHandler)
}

/**
 * 监听配置变化
 */
watch(
  () => props.option,
  () => {
    if (chartInstance) {
      chartInstance.setOption(props.option, true)
    }
  },
  { deep: true }
)

onMounted(() => {
  initChart()
})

/**
 * 组件卸载时清理
 */
onUnmounted(() => {
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
  }
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style scoped>
.chart-card {
  height: 100%;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
}

.chart-container {
  width: 100%;
  height: v-bind(height);
  min-height: 300px;
}
</style>

