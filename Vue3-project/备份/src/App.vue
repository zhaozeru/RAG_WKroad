<template>
  <div id="app">
    <div class="container">
      <LeftPanel class="panel" />
      <RightPanel class="panel" />
    </div>
  </div>
</template>

<script lang="ts" setup name="App">
import LeftPanel from './components/LeftPanel.vue';
import RightPanel from './components/RightPanel.vue';
</script>

<style>
/* 设置 html 和 body 元素的宽度和高度为 100% */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  font-family: Arial, sans-serif;
}

/* 设置 #app 元素的宽度和高度为 100% */
#app {
  margin: 0;
  width: 100%;
  height: 100%;
  display: flex;
  background-color: transparent;
}

.container {
  display: flex;
  width: 100%;
  height: 100%;
  background-color: #a4d2d9; /* 半透明的白色背景 */
  background-image: linear-gradient(to right, #f0f0f0 2px, transparent 2px), linear-gradient(to bottom, #f0f0f0 2px, transparent 2px);
  background-size: 40px 40px; /* 调整条格的大小 */
  font-family: 'Comic Sans MS', cursive, sans-serif; /* 手写风格的字体 */
  color: #333;
}

.panel {
  padding: 20px; /* 可以根据需要调整 */
  box-sizing: border-box; /* 确保 padding 不会影响宽度 */
}
</style>
