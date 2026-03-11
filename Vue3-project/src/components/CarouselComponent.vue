<template>
  <div class="carousel-container">

    <div class="carousel carousel-top" ref="carouselTop">
      <div class="carousel-label">故居栏</div>
      <div class="carousel-content">
        <div v-for="construct in constructs" :key="construct.id" class="carousel-item" @click="handleClick('故居栏', construct.name)">
          <img :src="construct.image" :alt="construct.name" :title="construct.name">
          <div class="item-name">{{ construct.name }}</div>
        </div>
      </div>
    </div>

    <div class="carousel carousel-bottom" ref="carouselBottom">
      <div class="carousel-label">人物栏</div>
      <div class="carousel-content">
        <div v-for="person in people" :key="person.id" class="carousel-item" @click="handleClick('人物栏', person.name)">
          <img :src="person.image" :alt="person.name" :title="person.name">
          <div class="item-name">{{ person.name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const constructs = [
  { id: 1, name: '宋庆龄故居', image: '/pic/宋庆龄故居4.jpg' },
  { id: 2, name: '张乐平故居', image: '/pic/张乐平故居2.jpg' },
  { id: 3, name: '马步芳故居', image: '/pic/马步芳故居2.webp' },
  { id: 4, name: '巴金故居', image: '/pic/巴金故居5.jpg' },
  { id: 5, name: '周作民旧居', image: '/pic/周作民旧居1.jpg' },
  { id: 6, name: '黄兴故居', image: '/pic/黄兴故居1.jpg' },
  { id: 7, name: '唐绍仪旧居', image: '/pic/唐绍仪旧居1.jpg' },
  { id: 8, name: '柯灵故居', image: '/pic/柯灵故居1.jpg' },

  { id: 10, name: '王元化故居', image: '/pic/王元化故居3.jpeg' },
  { id: 11, name: '莫觞清旧居', image: '/pic/莫觞清旧居3.jpg' },
  { id: 12, name: '陈果夫旧居', image: '/pic/陈果夫旧居1.webp' },
  { id: 13, name: '陈立夫旧居', image: '/pic/陈立夫旧居2.jpg' },
  { id: 15, name: '颜福庆旧居', image: '/pic/颜福庆旧居1.jpg' },
  { id: 9, name: '武康庭(FERGUSON LANE）', image: '/pic/武康庭(FERGUSON LANE）3.jpg' },
];

const people = [
  { id: 9, name: '宋庆龄', image: '/pic/personPic/宋庆龄1.webp' },
  { id: 20, name: '蒋介石', image: '/pic/personPic/蒋介石3.jpg' },
  { id: 8, name: '朱德', image: '/pic/personPic/朱德3.webp' },
  { id: 5, name: '张乐平', image: '/pic/personPic/张乐平1.png' },
  { id: 7, name: '周作民', image: '/pic/personPic/周作民3.jpg' },
  { id: 11, name: '王元化', image: '/pic/personPic/王元化2.jpg' },
  { id: 18, name: '郭泰祺', image: '/pic/personPic/郭泰祺3.webp' },
  { id: 26, name: '蔡元培', image: '/pic/personPic/蔡元培5.webp' },
  { id: 27, name: '陈光甫', image: '/pic/personPic/陈光甫1.jpeg' },
  { id: 28, name: '陈果夫', image: '/pic/personPic/陈果夫1.jpg' },
  { id: 29, name: '陈济棠', image: '/pic/personPic/陈济棠1.webp' },
  { id: 1, name: '颜福庆', image: '/pic/personPic/颜福庆1.jpg' },
  { id: 2, name: '杨敏德', image: '/pic/personPic/杨敏德1.webp' },
  { id: 3, name: '杨西光', image: '/pic/personPic/杨西光1.jpg' },
  { id: 4, name: '张可', image: '/pic/personPic/张可2.webp' },
  { id: 6, name: '周恩来', image: '/pic/personPic/周恩来1.webp' },
  { id: 10, name: '唐绍仪', image: '/pic/personPic/唐绍仪4.webp' },
  { id: 12, name: '魏文伯', image: '/pic/personPic/魏文伯1.webp' },
  { id: 13, name: '吴稚晖', image: '/pic/personPic/吴稚晖2.webp' },
  { id: 14, name: '萧伯纳', image: '/pic/personPic/萧伯纳2.jpg' },
  { id: 15, name: '萧珊', image: '/pic/personPic/萧珊2.webp' },
  { id: 16, name: '徐景贤', image: '/pic/personPic/徐景贤1.jpg' },
  { id: 17, name: '毛泽东', image: '/pic/personPic/毛泽东5.webp' },
  { id: 19, name: '黄兴', image: '/pic/personPic/黄兴1.jpg' },
  { id: 21, name: '蒋纬国', image: '/pic/personPic/蒋纬国1.webp' },
  { id: 22, name: '金日成', image: '/pic/personPic/金日成1.webp' },
  { id: 23, name: '柯灵', image: '/pic/personPic/柯灵2.webp' },
  { id: 24, name: '刘少奇', image: '/pic/personPic/刘少奇3.webp' },
  { id: 25, name: '马步芳', image: '/pic/personPic/马步芳1.jpg' },
  { id: 30, name: '陈立夫', image: '/pic/personPic/陈立夫2.jpg' },
  { id: 31, name: '董必武', image: '/pic/personPic/董必武1.webp' },
  { id: 32, name: '巴金', image: '/pic/personPic/巴金3.webp' },
  { id: 33, name: '董大酉', image: '/pic/personPic/董大酉1.jpg' },

];

const carouselTop = ref(null);
const carouselBottom = ref(null);

const emit = defineEmits(['updateCanvas']);

function handleClick(category, name) {
  emit('updateCanvas', category, name);
}

function handleWheel(event) {
  event.preventDefault();
  const scrollContainer = event.currentTarget;
  scrollContainer.scrollLeft += event.deltaY;
}

onMounted(() => {
  carouselTop.value.addEventListener('wheel', handleWheel);
  carouselBottom.value.addEventListener('wheel', handleWheel);
});

onBeforeUnmount(() => {
  carouselTop.value.removeEventListener('wheel', handleWheel);
  carouselBottom.value.removeEventListener('wheel', handleWheel);
});
</script>

<style scoped>
/* 容器样式 */
.carousel-container {
  width: 100%;
  height: 100%;
  display: flex; /* 使用flexbox布局 */
  flex-direction: column; /* 子元素纵向排列 */
  gap: 12px; /* 子元素之间的间距 */
  position: relative; /* 定位相对父元素 */
  
}

/* 滚动栏样式 */
.carousel {
  position: relative; 
  display: flex; /* 使用flexbox布局 */
  align-items: center; /* 子元素垂直居中 */
  overflow-x: auto; /* 水平滚动 */
  scroll-snap-type: x mandatory; /* 强制滚动到子元素 */
  padding: 5px; /* 内边距 */
  background-color: #B4E3DE; /* 滚动栏底色 */
  border-radius: 20px; /* 圆角 */
  white-space: nowrap; /* 子元素不换行 */
  border: 1px solid #000; /* 边框线条 */

}

/* 隐藏滚动条 */
.carousel::-webkit-scrollbar {
  display: none; /* 隐藏滚动条 */
}

/* 内容样式 */
.carousel-content {
  display: flex; /* 使用flexbox布局 */
  align-items: center; /* 子元素垂直居中 */
  margin-left: 30px; /* 整体向右偏移 */
  position: relative; 
}

/* 滚动栏项样式 */
.carousel-item {
  display: inline-flex; /* 使用内联flexbox布局 */
  flex-direction: column; /* 子元素纵向排列 */
  align-items: center; /* 子元素水平居中 */
  margin-right: 12px; /* 图片之间的间距 */
  cursor: pointer; /* 鼠标指针变为手型 */
  scroll-snap-align: center; /* 滚动对齐中心 */
}

/* 图片样式 */
.carousel-item img {
  width: 110px; /* 图片宽度 */
  height: 95px; /* 图片高度 */
  object-fit: cover; /* 图片按比例缩放 */
  border-radius: 12px; /* 图片圆角 */
  margin-top: 3px;
  margin-bottom: 0px;

}

/* 图片名称样式 */
.item-name {
  margin-top: 3px; /* 上边距 */
  font-size: 17px; /* 字体大小 */
  color: black; /* 文字颜色 */
  margin-bottom: 0px;
}

/* 标签样式 */
.carousel-label {
  position: absolute; /* 绝对定位 */
  top: 50%; /* 垂直居中 */
  transform: translateY(-50%); /* 垂直居中 */
  color: black; /* 字体颜色 */
  width: 30px; /* 标签宽度 */
  text-align: center; /* 文本居中 */
  font-size: 18px; /* 字体大小 */
  writing-mode: vertical-rl; /* 垂直书写模式 */
  text-orientation: upright; /* 文本方向直立 */
}


</style>
