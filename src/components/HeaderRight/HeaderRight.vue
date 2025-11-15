<template>
  <div class="header-right">
    <!-- 主题切换 -->
    <ThemeToggle />
    
    <!-- 用户菜单 -->
    <UserMenu />
  </div>
</template>

<script lang="ts" setup>
/**
 * @fileoverview 头部右侧区域主组件
 * @author 开发团队
 * @date 2025-01-15
 */

import ThemeToggle from './components/ThemeToggle.vue'
import UserMenu from './components/UserMenu.vue'
</script>

<style scoped>
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 100%;
}
</style>

