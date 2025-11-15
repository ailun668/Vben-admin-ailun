<template>
  <div
    ref="scrollContainerRef"
    :class="[
      'scroll-container',
      `scroll-container--${mode}`,
      {
        'scroll-container--auto-hide': autoHide,
        'scroll-container--smooth': smooth
      }
    ]"
    :style="containerStyle"
    @scroll="handleScroll"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
/**
 * @fileoverview 滚动容器组件
 * 提供统一的滚动条样式和滚动行为
 */
import { ref, computed } from 'vue'

interface Props {
  /** 滚动模式 */
  mode?: 'default' | 'sidebar' | 'content' | 'table' | 'modal'
  /** 是否自动隐藏滚动条（悬停显示） */
  autoHide?: boolean
  /** 是否启用平滑滚动 */
  smooth?: boolean
  /** 容器高度 */
  height?: string | number
  /** 容器最大高度 */
  maxHeight?: string | number
  /** 是否启用横向滚动 */
  horizontal?: boolean
  /** 滚动条宽度 */
  scrollbarWidth?: number
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'default',
  autoHide: false,
  smooth: true,
  horizontal: false,
  scrollbarWidth: 6
})

const emit = defineEmits<{
  scroll: [event: Event]
  scrollTop: [top: number]
  scrollLeft: [left: number]
}>()

const scrollContainerRef = ref<HTMLElement>()

/**
 * 容器样式
 */
const containerStyle = computed(() => {
  const style: Record<string, string> = {
    overflowY: 'auto',
    overflowX: props.horizontal ? 'auto' : 'hidden'
  }

  if (props.height) {
    style.height = typeof props.height === 'number' ? `${props.height}px` : props.height
  }

  if (props.maxHeight) {
    style.maxHeight = typeof props.maxHeight === 'number' ? `${props.maxHeight}px` : props.maxHeight
  }

  if (props.smooth) {
    style.scrollBehavior = 'smooth'
  }

  return style
})

/**
 * 滚动事件处理
 */
const handleScroll = (event: Event) => {
  emit('scroll', event)
  
  if (scrollContainerRef.value) {
    emit('scrollTop', scrollContainerRef.value.scrollTop)
    emit('scrollLeft', scrollContainerRef.value.scrollLeft)
  }
}

/**
 * 滚动到顶部
 */
const scrollToTop = (behavior: ScrollBehavior = 'smooth') => {
  scrollContainerRef.value?.scrollTo({
    top: 0,
    behavior
  })
}

/**
 * 滚动到底部
 */
const scrollToBottom = (behavior: ScrollBehavior = 'smooth') => {
  if (scrollContainerRef.value) {
    scrollContainerRef.value.scrollTo({
      top: scrollContainerRef.value.scrollHeight,
      behavior
    })
  }
}

/**
 * 滚动到指定位置
 */
const scrollTo = (options: ScrollToOptions) => {
  scrollContainerRef.value?.scrollTo(options)
}

/**
 * 获取滚动位置
 */
const getScrollTop = () => {
  return scrollContainerRef.value?.scrollTop || 0
}

/**
 * 获取滚动高度
 */
const getScrollHeight = () => {
  return scrollContainerRef.value?.scrollHeight || 0
}

/**
 * 暴露方法
 */
defineExpose({
  scrollToTop,
  scrollToBottom,
  scrollTo,
  getScrollTop,
  getScrollHeight,
  scrollContainer: scrollContainerRef
})
</script>

<style scoped>
.scroll-container {
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
}

/* 默认模式 */
.scroll-container--default {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.scroll-container--default::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.scroll-container--default::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 3px;
}

.scroll-container--default::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
  transition: background 0.3s ease;
}

.scroll-container--default::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 侧边栏模式 */
.scroll-container--sidebar {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}

.scroll-container--sidebar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.scroll-container--sidebar::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 3px;
}

.scroll-container--sidebar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  transition: background 0.3s ease;
}

.scroll-container--sidebar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 内容区域模式 */
.scroll-container--content {
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
  transition: scrollbar-color 0.3s ease;
}

.scroll-container--content:hover {
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.scroll-container--content::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.scroll-container--content::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 3px;
  transition: background 0.3s ease;
}

.scroll-container--content::-webkit-scrollbar-thumb {
  background: transparent;
  border-radius: 3px;
  transition: background 0.3s ease;
}

.scroll-container--content:hover::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
}

.scroll-container--content:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
}

.scroll-container--content:hover::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 表格模式 */
.scroll-container--table {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) #f5f5f5;
}

.scroll-container--table::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.scroll-container--table::-webkit-scrollbar-track {
  background: #f5f5f5;
  border-radius: 4px;
}

.scroll-container--table::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  transition: background 0.3s ease;
}

.scroll-container--table::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 弹窗模式 */
.scroll-container--modal {
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
  transition: scrollbar-color 0.3s ease;
}

.scroll-container--modal:hover {
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.scroll-container--modal::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

.scroll-container--modal::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 3px;
  transition: background 0.3s ease;
}

.scroll-container--modal::-webkit-scrollbar-thumb {
  background: transparent;
  border-radius: 3px;
  transition: background 0.3s ease;
}

.scroll-container--modal:hover::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
}

.scroll-container--modal:hover::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 平滑滚动 */
.scroll-container--smooth {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}
</style>

