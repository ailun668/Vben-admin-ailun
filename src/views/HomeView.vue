/**
 * @fileoverview Dashboard 工作台首页
 * @author AI Developer
 * @date 2024-01-XX
 */

<template>
  <div class="dashboard-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">数据分析工作台</h1>
      <p class="page-subtitle">实时监控系统关键指标和业务数据</p>
    </div>

    <!-- KPI 卡片区域 -->
    <div class="kpi-section">
      <a-row :gutter="[16, 16]">
        <a-col
          v-for="(kpi, index) in kpiCards"
          :key="index"
          :xs="24"
          :sm="12"
          :md="12"
          :lg="6"
        >
          <KPICard :card="kpi" />
        </a-col>
      </a-row>
    </div>

    <!-- 图表区域 -->
    <div class="chart-section">
      <h2 class="section-title">
        <AreaChartOutlined />
        趋势分析
      </h2>

      <a-row :gutter="[16, 16]">
        <!-- 折线图 -->
        <a-col :xs="24" :lg="12">
          <ChartCard :title="'月度访问量分析'" :option="lineChartOption" />
        </a-col>

        <!-- 柱状图 -->
        <a-col :xs="24" :lg="12">
          <ChartCard :title="'收入来源分布'" :option="barChartOption" />
        </a-col>

        <!-- 饼图 -->
        <a-col :xs="24" :lg="12">
          <ChartCard :title="'用户地域分布'" :option="pieChartOption" />
        </a-col>

        <!-- 任务完成情况 -->
        <a-col :xs="24" :lg="12">
          <a-card class="task-card" :bordered="false">
            <template #title>
              <span class="chart-title">任务完成情况</span>
            </template>
            <a-row :gutter="[16, 16]">
              <a-col :xs="24" :sm="12">
                <div class="progress-card">
                  <div class="progress-title">项目进度</div>
                  <div
                    v-for="(item, index) in progressItems"
                    :key="index"
                    class="progress-item"
                  >
                    <div class="progress-heading">
                      <span>{{ item.name }}</span>
                      <span>{{ item.percent }}%</span>
                    </div>
                    <a-progress
                      :percent="item.percent"
                      :stroke-color="item.color"
                      :show-info="false"
                    />
                  </div>
                </div>
              </a-col>
              <a-col :xs="24" :sm="12">
                <ChartCard
                  :title="''"
                  :option="gaugeChartOption"
                  :height="'300px'"
                />
              </a-col>
            </a-row>
          </a-card>
        </a-col>
      </a-row>
    </div>

    <!-- 最近活动 -->
    <div class="activity-section">
      <h2 class="section-title">
        <UnorderedListOutlined />
        最近活动记录
      </h2>

      <a-card :bordered="false">
        <a-table
          :columns="activityColumns"
          :data-source="activityRecords"
          :pagination="false"
          :loading="loading"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'">
              <a-tag
                :color="
                  record.status === 'active'
                    ? 'success'
                    : record.status === 'completed'
                      ? 'blue'
                      : 'warning'
                "
              >
                {{
                  record.status === 'active'
                    ? '进行中'
                    : record.status === 'completed'
                      ? '已完成'
                      : '待开始'
                }}
              </a-tag>
            </template>
            <template v-else-if="column.key === 'progress'">
              <a-progress
                :percent="record.progress"
                :stroke-color="
                  record.progress === 100
                    ? '#52c41a'
                    : record.progress > 0
                      ? '#1890ff'
                      : '#faad14'
                "
                :size="'small'"
              />
            </template>
          </template>
        </a-table>
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { ColumnsType } from 'ant-design-vue/es/table'
import {
  AreaChartOutlined,
  UnorderedListOutlined
} from '@ant-design/icons-vue'
import KPICard from '@/components/Dashboard/KPICard.vue'
import ChartCard from '@/components/Dashboard/ChartCard.vue'
import type { KPICard as KPICardType, ActivityRecord } from '@/types/dashboard'
import type { EChartsOption } from 'echarts'

/**
 * 加载状态
 */
const loading = ref(false)

/**
 * KPI 卡片数据
 */
const kpiCards = ref<KPICardType[]>([
  {
    name: '总访问量',
    value: 42567,
    trend: 'up',
    trendValue: '12.5%',
    iconColor: '#1890ff',
    iconName: 'users'
  },
  {
    name: '总收入',
    value: '¥826,450',
    trend: 'up',
    trendValue: '8.3%',
    iconColor: '#52c41a',
    iconName: 'dollar'
  },
  {
    name: '订单数',
    value: 3842,
    trend: 'down',
    trendValue: '2.1%',
    iconColor: '#faad14',
    iconName: 'cart'
  },
  {
    name: '转换率',
    value: '24.6%',
    trend: 'up',
    trendValue: '3.7%',
    iconColor: '#722ed1',
    iconName: 'chart'
  }
])

/**
 * 进度项数据
 */
const progressItems = ref([
  { name: '产品研发', percent: 75, color: '#1890ff' },
  { name: '市场推广', percent: 42, color: '#faad14' },
  { name: '客户支持', percent: 91, color: '#52c41a' }
])

/**
 * 折线图配置
 */
const lineChartOption = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['访问量', '新增用户']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '访问量',
      type: 'line',
      smooth: true,
      data: [12000, 16000, 14500, 18200, 20800, 23400, 25600, 19800, 24500],
      lineStyle: {
        width: 3
      },
      itemStyle: {
        color: '#1890ff'
      }
    },
    {
      name: '新增用户',
      type: 'line',
      smooth: true,
      data: [3200, 3800, 4200, 4800, 5200, 5600, 5100, 4700, 5200],
      lineStyle: {
        width: 3
      },
      itemStyle: {
        color: '#52c41a'
      }
    }
  ]
}))

/**
 * 柱状图配置
 */
const barChartOption = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['2022年', '2023年']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['产品A', '产品B', '产品C', '产品D', '服务']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '2022年',
      type: 'bar',
      data: [125000, 98000, 105000, 117000, 86000],
      itemStyle: {
        color: '#722ed1'
      }
    },
    {
      name: '2023年',
      type: 'bar',
      data: [180000, 125000, 142000, 156000, 105000],
      itemStyle: {
        color: '#1890ff'
      }
    }
  ]
}))

/**
 * 饼图配置
 */
const pieChartOption = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    right: 10,
    top: 'center'
  },
  series: [
    {
      name: '地域分布',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 18,
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: 42, name: '华东地区' },
        { value: 25, name: '华北地区' },
        { value: 18, name: '华南地区' },
        { value: 8, name: '西南地区' },
        { value: 7, name: '其他地区' }
      ],
      color: ['#1890ff', '#52c41a', '#faad14', '#722ed1', '#ff4d4f']
    }
  ]
}))

/**
 * 仪表盘配置
 */
const gaugeChartOption = computed<EChartsOption>(() => ({
  series: [
    {
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      progress: {
        show: true,
        width: 18
      },
      axisLine: {
        lineStyle: {
          width: 18
        }
      },
      axisTick: {
        show: false
      },
      splitLine: {
        length: 15,
        lineStyle: {
          width: 2,
          color: '#999'
        }
      },
      axisLabel: {
        distance: -30,
        color: '#999',
        fontSize: 12
      },
      anchor: {
        show: true,
        showAbove: true,
        size: 25,
        itemStyle: {
          borderWidth: 8
        }
      },
      title: {
        show: false
      },
      detail: {
        valueAnimation: true,
        fontSize: 40,
        offsetCenter: [0, '-20%'],
        formatter: '{value}%',
        color: 'inherit'
      },
      data: [
        {
          value: 75,
          name: '整体完成率',
          itemStyle: {
            color: '#1890ff'
          }
        }
      ]
    }
  ]
}))

/**
 * 活动记录表格列
 */
const activityColumns: ColumnsType<ActivityRecord> = [
  {
    title: '任务',
    dataIndex: 'task',
    key: 'task'
  },
  {
    title: '负责人',
    dataIndex: 'assignee',
    key: 'assignee'
  },
  {
    title: '截止时间',
    dataIndex: 'deadline',
    key: 'deadline'
  },
  {
    title: '状态',
    key: 'status',
    dataIndex: 'status'
  },
  {
    title: '进度',
    key: 'progress',
    dataIndex: 'progress'
  }
]

/**
 * 活动记录数据
 */
const activityRecords = ref<ActivityRecord[]>([
  {
    task: '季度财务报告',
    assignee: '张经理',
    deadline: '2024-09-30',
    status: 'active',
    progress: 65
  },
  {
    task: '系统安全升级',
    assignee: '王技术',
    deadline: '2024-09-28',
    status: 'completed',
    progress: 100
  },
  {
    task: '新员工培训计划',
    assignee: '李主管',
    deadline: '2024-10-10',
    status: 'pending',
    progress: 0
  },
  {
    task: '移动端改版',
    assignee: '陈设计',
    deadline: '2024-10-15',
    status: 'active',
    progress: 30
  },
  {
    task: '客户满意度调查',
    assignee: '赵专员',
    deadline: '2024-10-05',
    status: 'active',
    progress: 50
  }
])

/**
 * 初始化数据
 */
onMounted(() => {
  // 可以在这里加载真实数据
  loading.value = false
})
</script>

<style scoped>
.dashboard-container {
  padding: 0;
  background-color: transparent;
  min-height: auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
  margin-bottom: 8px;
}

.page-subtitle {
  color: rgba(0, 0, 0, 0.45);
  font-size: 14px;
  margin: 0;
}

.kpi-section {
  margin-bottom: 24px;
}

.chart-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(0, 0, 0, 0.85);
}

.activity-section {
  margin-bottom: 24px;
}

.task-card {
  height: 100%;
}

.progress-card {
  padding: 16px 0;
}

.progress-title {
  margin-bottom: 16px;
  font-weight: 600;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.85);
}

.progress-item {
  margin-bottom: 16px;
}

.progress-heading {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 16px;
  }

  .page-title {
    font-size: 20px;
  }
}
</style>
