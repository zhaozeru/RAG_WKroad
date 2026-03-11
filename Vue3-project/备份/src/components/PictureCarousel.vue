<template>
  <div>
    <div class="banner">
      <div v-if="imgArr.length > 0" class="img-container">
        <img
          v-for="(imgSrc, index) in visibleImages"
          :key="index"
          :src="imgSrc"
          class="img"
          :class="{ active: index === 2 }"
          @click="openModal(imgSrc)" 
        />
      </div>
      <div v-else>
        <img :src="defaultImages" class="img" />
      </div>

      <div class="dot-content">
        <div
          v-for="(item, index) in imgArr.length"
          :key="index"
          :class="{ 'dot-box': true, 'active': index === imgIndex }"
          @click="selectImg(index)"
        ></div>
      </div>

      <el-icon size="40" class="left-btn" @click="next(-1)">
        <ArrowLeftBold />
      </el-icon>
      <el-icon size="40" class="right-btn" @click="next(1)">
        <ArrowRightBold />
      </el-icon>
    </div>
  </div>


</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
import { useNodeAttributeStore } from '@/store/Nodeattribute' 

const nodeAttributeStore = useNodeAttributeStore()
const nodeList = computed(() => nodeAttributeStore.nodeList)

const imgArr = ref([])
const imgIndex = ref(0)
const searchKey = ['故居图片', '人物图片','故居图片描述','人物图片描述']

const defaultImages = [
  '/pic/carouselPic/武康路5.jpg',
  '/pic/carouselPic/武康路2.jpg',
  '/pic/carouselPic/武康路8.jpg',
  '/pic/carouselPic/武康路9.jpg',
  '/pic/carouselPic/武康路10.jpg',
  '/pic/carouselPic/武康路11.jpg',
  '/pic/carouselPic/武康路1.jpg',
  '/pic/carouselPic/武康路6.jpg',
  '/pic/carouselPic/武康路7.jpg',
  '/pic/carouselPic/武康路12.jpg',
  '/pic/carouselPic/武康路13.jpg',
  '/pic/carouselPic/武康路14.jpg',
  '/pic/carouselPic/武康路15.jpg',
  '/pic/carouselPic/武康路16.jpg',
  '/pic/carouselPic/武康路17.jpg',
  '/pic/carouselPic/武康路18.jpg',
  '/pic/carouselPic/武康路3.jpg'
]

const visibleImages = computed(() => {
  if (imgArr.value.length === 0) return []

  const total = imgArr.value.length
  const startIndex = (imgIndex.value - 2 + total) % total
  const visible = []
  for (let i = 0; i < 5; i++) {
    visible.push(imgArr.value[(startIndex + i) % total])
  }
  return visible
})

let intervalId = null

onMounted(() => {
  updateImgArr()
  if (imgArr.value.length > 0) {
    selectImg(0)
  }
  startAutoPlay()
})

onUnmounted(() => {
  stopAutoPlay()
})

const updateImgArr = () => {
  imgArr.value = []
  const pathMap = {
    '故居图片': '/pic/',
    '人物图片': '/pic/personPic/',
    '故居图片描述': '/pic/',
    '人物图片描述': '/pic/personPic/'
  }

  nodeList.value.forEach(node => {
    searchKey.forEach(key => {
      const value = node[key] ?? null
      if (value) {
        const filenames = value.split(', ')
        const paths = filenames.map(filename => `${pathMap[key]}${filename}`)
        imgArr.value = [...imgArr.value, ...paths]
      }
    })
  })

  if (imgArr.value.length === 0) {
    imgArr.value = defaultImages
  }

  if (imgArr.value.length > 0) {
    selectImg(0)
  }
}
watch(
  () => nodeList.value.map(node => ({
    '故居图片': node['故居图片'],
    '人物图片': node['人物图片'],
    '故居图片描述': node['故居图片描述'],
    '人物图片描述': node['人物图片描述'],
  })),
  (newValues, oldValues) => {
    if (JSON.stringify(newValues) !== JSON.stringify(oldValues)) {
      updateImgArr()
      stopAutoPlay()
      startAutoPlay()
    }
  },
  { deep: true }
)

const startAutoPlay = () => {
  if (intervalId) {
    clearInterval(intervalId)
  }
  intervalId = setInterval(() => {
    next(1)
  }, 3500)
}

const stopAutoPlay = () => {
  if (intervalId) {
    clearInterval(intervalId)
    intervalId = null
  }
}

const selectImg = (index) => {
  if (imgArr.value.length === 0) return;
  imgIndex.value = index;
}

const next = (direction) => {
  if (imgArr.value.length === 0) return
  imgIndex.value += direction
  if (imgIndex.value >= imgArr.value.length) {
    imgIndex.value = 0
  }
  if (imgIndex.value < 0) {
    imgIndex.value = imgArr.value.length - 1
  }
}
</script>

<style scoped>
.banner {
    position: relative;
    display: flex;
    justify-content: center; /* 居中对齐图片 */
    align-items: center; /* 居中对齐内容 */
    width: 100%;
    height: 440px;
    overflow: hidden; /* 确保图片不会超出容器边界 */
    perspective: 1000px;
    box-sizing: border-box;
    flex-direction: column;
}

.img-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  overflow: hidden; /* 隐藏超出容器的图片部分 */
  position: relative; /* 确保 z-index 生效 */
  object-fit:cover ;
}

.img {
  width: 15%; /* 图片宽度减少 */
  height: 70%;
  object-fit:cover ; /* 保持图片比例，填充容器 */
  opacity: 0.7;
  transition: opacity 0.5s ease, transform 0.5s ease;
  border-radius: 12px;
  user-select: none;
  transform-style: preserve-3d;
  margin: 0 -3%; /* 增加负 margin 实现图片重叠 */
  z-index: 1; /* 默认图片的 z-index */
  overflow: hidden; 
}

/* 当前图片样式 */
.img.active {
  width: 60%; /* 当前图片宽度增加 */
  height: 95%; /* 确保高度适应容器 */
  opacity: 1;
  transform: scale(1.0); /* 放大当前图片 */
  margin: 0; /* 移除 margin 使其完整展示 */
  z-index: 10; /* 当前图片的 z-index 高于其他图片 */
  object-fit:cover ;
}


.img-container img:nth-child(2),
.img-container img:nth-child(4) {
  transform: scale(0.9);
  z-index: 5; /* 左右预览图的 z-index */
}

.img-container img:nth-child(1),
.img-container img:nth-child(5) {
  transform: scale(0.8);
  opacity: 0.4;
  z-index: 3; /* 最左侧和最右侧的图片的 z-index */
}

.dot-content {
  position: relative;
  bottom: 7%;
  display: flex;
  justify-content: center;
  width: 100%;
  z-index: 15;
}

.dot-box {
  width: 8px;
  height: 8px;
  background: #fff;
  border-radius: 50%;
  margin: 0 4px;
  cursor: pointer;
  transition: box-shadow 0.3s; /* 使用 box-shadow 过渡效果 */
}

.dot-box.active {
  cursor: pointer;
  width: 8px; /* 确保宽度一致 */
  height: 8px; /* 确保高度一致 */
  background-color: red; /* 当前选择的圆点样式 */
  transform: none; /* 确保没有缩放或变形 */
}

.banner .left-btn,
.banner .right-btn {
  position: absolute;
  top: 45%;
  width: auto;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease; /* 添加过渡效果 */
  z-index: 20;
}

.banner .left-btn {
  left: 10px;
}

.banner .right-btn {
  right: 10px;
}

/* 鼠标悬停效果 */
.banner .left-btn:hover,
.banner .right-btn:hover {
  background-color: rgba(0, 0, 0, 0.5); /* 鼠标悬停时背景色 */
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.7); /* 添加阴影 */
}

/* 弹窗背景样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 30;
  overflow: hidden; /* 防止内容超出弹窗 */
}

/* 弹窗内容样式 */
.modal-content {
  position: relative;
  width: 80%; /* 固定宽度 */
  height: 80%; /* 固定高度 */
  max-width: 800px; /* 可设置最大宽度 */
  max-height: 600px; /* 可设置最大高度 */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 弹窗图片样式 */
.modal-image {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 确保图片在保持比例的情况下显示完整 */
  border-radius: 8px;
}



</style>
