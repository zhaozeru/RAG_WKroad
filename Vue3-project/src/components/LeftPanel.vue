<template>
  <div class="left-panel">
    <div class="title">
      <h1>知识图谱交互与展示页</h1>
      <div class="divider"></div>
    </div>
    <div class="display-window">
      <div class="image-display">
        <Carousel/>
      </div>
      <div class="text-display">
        <NodeAttribute/>
      </div>
    </div>
  </div>
</template>

<script setup>
import NodeAttribute from './NodeAttribute.vue'
import Carousel from './PictureCarousel.vue'

</script>

<style scoped>
.left-panel {
  width: 45%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
  /* background-color: rgba(235, 160, 79, 0.833); */
}

.title {
  text-align: left;
  margin-bottom: 20px;
  color: #000; /* 黑色 */
  position: relative; /* 为了定位分割线 */
}

.title h1 {
  font-size:32px;
  font-weight: bold; /* 加粗样式 */
  margin-left:25px;
}

.divider {
  width: 100%;
  height: 1px;
  background-color: #000; /* 黑色分割线 */
  margin-top: 5px; /* 与标题的间距 */
}

.display-window {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  border: 1px solid #040404;
  border-radius: 10px;
  padding: 10px;
  box-sizing: border-box;
  overflow: hidden;
}

.image-display {
  border-bottom: 1px solid #010101;
  margin-bottom: 5px;
  overflow: hidden;
}

.text-display {
  overflow: hidden;
  position: relative;
}
</style>