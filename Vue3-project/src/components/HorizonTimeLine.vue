<template>
  <div class="m-timeline-wrap" ref="timelineWrap">
    <div class="m-time-dot">
      <div
        :class="['m-dot-box', {'active': activeYear.value === item.year}]"
        @click="onClickYear(item.year)"
        v-for="(item, index) in timelineData"
        :key="index">
        <p :class="['u-year', {'odd-year': index % 2 === 1, 'even-year': index % 2 === 0}]">{{ item.year }}</p>
        <div v-if="index !== 0 && index !== timelineData.length - 1" class="m-dot">
          <div class="u-dot"></div>
        </div>
      </div>
    </div>
    <div 
      class="m-drag-button" 
      ref="dragButton" 
      @mousedown="startDrag"
      :style="{ left: dragPosition.value + 'px' }"></div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useNodeTimeStore } from '@/store/NodeTime';

// 创建节流函数，用于控制鼠标移动事件的触发频率，以减少性能开销
function throttle(func, delay) {
  let lastTime = 0;
  return function(...args) {
    const now = new Date().getTime();
    if (now - lastTime >= delay) {
      func.apply(this, args);
      lastTime = now;
    }
  };
}

// 使用 ref 创建一个响应式变量来存储当前激活的年份，默认值为1950年
const activeYear = ref(1950);

// 使用 ref 创建一个响应式变量来存储拖动按钮的位置，默认值为0
const dragPosition = ref(0);

// 使用 ref 引用时间轴的容器元素，便于访问其宽度等属性
const timelineWrap = ref(null);

// 使用 ref 引用拖动按钮元素，用于动态修改其样式
const dragButton = ref(null); 

// 生成时间轴数据的函数，时间范围从1900年到1950年，每隔5年添加一个年份
const generateTimelineData = () => {
  const startYear = 1900;
  const endYear = 1950;
  const data = [];
  for (let year = startYear; year <= endYear; year += 5) {
    data.push({ year });
  }
  return data;
};

// 通过 computed 计算属性生成时间轴数据
const timelineData = computed(() => generateTimelineData());

// 点击年份时的处理函数，更新激活的年份并同步到 Pinia 状态管理中
const onClickYear = (year) => {
  if (activeYear.value !== year) {
    activeYear.value = year;
    updateYearInPinia(year);
  }
};

// 开始拖动按钮的处理函数
const startDrag = (event) => {

  const startX = event.clientX; // 获取鼠标点击时的 X 坐标
  const initialDragPosition = dragPosition.value; // 获取按钮的初始拖动位置
  const timelineWidth = timelineWrap.value.clientWidth; // 获取时间轴的宽度

  // 鼠标移动时的处理函数，使用节流来优化性能
  const onMouseMove = throttle((moveEvent) => {

    const deltaX = moveEvent.clientX - startX; // 计算鼠标移动的距离
    let newPosition = initialDragPosition + deltaX; // 计算按钮的新位置

    // 限制按钮移动范围，防止超出时间轴的边界
    if (newPosition < 0) {
      newPosition = 0;
    } else if (newPosition > timelineWidth) {
      newPosition = timelineWidth;
    }

    // 更新拖动位置
    dragPosition.value = newPosition;

    // 更新按钮的位置（将位置应用到样式中）
    dragButton.value.style.left = `${newPosition}px`;

    // 根据拖动位置更新年份
    updateYearFromDrag();
  }, 16); // 设置16ms的节流时间，大约相当于60fps

  // 鼠标松开时的处理函数，移除事件监听器
  const onMouseUp = () => {

    document.removeEventListener('mousemove', onMouseMove);
    document.removeEventListener('mouseup', onMouseUp);
  };

  // 添加鼠标移动和松开事件的监听器
  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
};

// 根据拖动按钮的位置更新年份的函数
const updateYearFromDrag = () => {
  if (timelineWrap.value) {
    const timelineWidth = timelineWrap.value.clientWidth;
    const yearRange = 1950 - 1900;
    const yearIndex = Math.round((dragPosition.value / timelineWidth) * yearRange / 5); // 计算最近的年份索引
    const nearestYear = 1900 + yearIndex * 5; // 计算最近的年份
    activeYear.value = nearestYear;
    updateYearInPinia(nearestYear);
  }
};

// 获取 Pinia 状态管理的实例，用于更新当前年份
const nodeTimeStore = useNodeTimeStore();

// 将当前年份更新到 Pinia 状态管理中的函数
const updateYearInPinia = (year) => {
  nodeTimeStore.updateCurrentYear(year);
};

</script>


<style scoped>
/* 时间轴容器样式，设置相对定位，保证拖动按钮在其内部移动 */
.m-timeline-wrap {
  position: relative;
  margin: 50px;
  height: 3px;
  background: #8dc6f5;
  user-select: none; /* 禁用文本选择，防止拖动时选中文字 */
}

/* 时间轴上的年份点容器样式，设置为水平排列，并在容器中均匀分布 */
.m-time-dot {
  display: flex;
  justify-content: space-between;
  position: relative;
}

/* 单个年份点的样式，居中对齐并禁用文本选择 */
.m-dot-box {
  cursor: pointer;
  text-align: center;
  user-select: none; /* 禁用文本选择 */
}

/* 年份文字的样式，设置字体大小、粗细和颜色，添加过渡效果 */
.u-year {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  transition: all 0.3s ease;
}

/* 奇数年份的样式，将文字向上偏移30px */
.odd-year {
  transform: translateY(-30px);
}

/* 偶数年份的样式，将文字向下偏移10px */
.even-year {
  transform: translateY(10px);
}

/* 时间轴上年份点的样式，设置大小、背景色和圆角 */
.m-dot {
  margin: 0 auto;
  width: 14px;
  height: 14px;
  background: #eb0881;
  border-radius: 50%;
  transition: all 0.3s ease;
}

/* 小圆点的样式，设置大小、背景色和圆角 */
.u-dot {
  width: 14px;
  height: 14px;
  background: #65e312;
  border-radius: 50%;
  transition: all 0.3s ease;
}

/* 当鼠标悬停在年份点时，改变文字和小圆点的颜色 */
.m-dot-box:hover .u-year {
  color: #1890FF;
}

.m-dot-box:hover .u-dot {
  background: #1890FF;
}

/* 激活的年份点样式，放大文字和圆点，改变颜色 */
.active .u-year {
  transform: scale(1.5) translateY(-18px);
  color: #17e682;
}

.active .m-dot {
  transform: scale(2);
}

.active .u-dot {
  transform: scale(0.67);
  background: #e908da;
}

/* 拖动按钮的样式，设置绝对定位、大小、背景色、圆角和悬停时的指针样式 */
.m-drag-button {
  position: absolute;
  top: -10px;
  width: 20px;
  height: 20px;
  background: #1890FF;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10; /* 提升拖动按钮的层级 */
}

</style>
