<template>
  <div class="right-panel">
    <div class="carouselcontainer">
      <CarouselComponent @updateCanvas="handleUpdateCanvas"/>
    </div>
    <div class="graphcontainer">
      <GraphComponent :category="clickCategory" :personId="selectedPerson"/>
    </div>
    <div class="timeline-container">
      <Langchain_Rag :Langchain_name="selectedPerson"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import CarouselComponent from './CarouselComponent.vue';
import GraphComponent from './GraphComponent.vue';
// import HorizonTimeLine from './HorizonTimeLine.vue'
import Langchain_Rag from './Langchain_Rag.vue'

const selectedPerson = ref(null);
const clickCategory = ref(null);

function handleUpdateCanvas(category, name) {
  console.log(`点击了 ${category} 中的 ${name}`);
  selectedPerson.value = name;
  clickCategory.value = category;
}
</script>

<style scoped>
/* 右侧板块样式 */
.right-panel {
  width: 55%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
  /* background-color: rgba(235, 159, 79, 0.79); */
  
}

.carouselcontainer {
  width: 100%;
  height: auto;
  margin-bottom: 8px; /* 增加底部边距 */
  overflow: hidden; /* 防止内容溢出 */

}

.graphcontainer {
  flex:1;
  display: flex;
  justify-content: center;
  align-items: center;
  /* background-color: #f3f3f3; */
  border-radius: 20px;
  margin-bottom: 8px;
  overflow: hidden;
  border: 1px solid #000; /* 添加线条 */
  position: relative;
}

.timeline-container {
  height: 8.5%;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #000; /* 添加线条 */
}
</style>