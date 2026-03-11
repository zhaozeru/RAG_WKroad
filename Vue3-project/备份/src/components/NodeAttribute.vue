<template>
  <div class="node-attributes">
    <h4>节点信息展示:</h4>
    <div v-for="node in nodeList" :key="node.id" class="node-info">
      <div class="property-item">
        <strong>类型:</strong> {{ node.type }}
      </div>
      <div v-for="(value, key) in sortedProperties(node.type, node.properties)" :key="key" class="property-item">
        <strong>{{ key }}:</strong> {{ value }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { useNodeAttributeStore } from '@/store/Nodeattribute'
import { computed } from 'vue'

const nodeAttributeStore = useNodeAttributeStore()
const nodeList = computed(() => nodeAttributeStore.nodeList)

const sortedProperties = (nodeType, properties) => {
  const order = {
    '中心节点': ['名称', '起点', '终点间', '简介','历史变迁','文化特色'],
    '故居节点': ['名称', '建筑异名', '建筑开始时间', '建筑完工时间', '建筑所在地址', '建筑ID', '建筑简介', '建筑风格', '建筑结构', '设计者', '门牌号', '位置坐标', '所在相关道路', '里弄','故居图片'],
    '人物节点': ['名称', '人物字名', '人物号名', '人物ID', '出生日期', '死亡日期', '出生地', '民族', '国籍', '职业', '任职经历', '相关机构', '配偶', '父亲', '友人', '儿女', '性别', '姓氏', '籍贯', '朝代', '数据来源','人物图片'],
    '图片节点': ['名称', '故居图片描述'],
    '事件节点': ['名称', '事件开始时间', '事件结束时间', '描述'],
    '人物简介节点': ['名称', '描述'],
    '人物图片节点': ['名称', '人物图片描述'],
    '人物别名节点': ['名称', '别名类型', '别名来源'],
    '人物作品节点': ['名称', '创作时间', '作品类型', '作品主题', '作品描述', '作品ID']
  }

  const keysOrder = order[nodeType] || []

  return Object.keys(properties)
    .filter(key => properties[key] !== undefined && properties[key] !== null && properties[key] !== '' && !(Array.isArray(properties[key]) && properties[key].length === 0))
    .sort((a, b) => keysOrder.indexOf(a) - keysOrder.indexOf(b))
    .reduce((acc, key) => {
      acc[key === 'name' ? '名称' : key] = properties[key]
      return acc
    }, {})
}
</script>

<style scoped>
.node-attributes {
  padding: 10px; /* 设置内边距 */
  border: 1px solid #ccc; /* 设置边框 */
  border-radius: 10px; /* 设置圆角 */
  width: 100%; /* 占据整个父容器 */
  box-sizing: border-box; /* 确保 padding 和 border 包含在 width 内 */
  background-color: #80aab7; /* 设置背景颜色 */
  overflow-y: auto; /* 添加垂直滚动条 */
  height: 445px; /* 设置最大高度，超出时显示滚动条 */
  opacity: 1; /* 设置透明度为80% */
}

h4 {
  margin-bottom: 5px; /* 设置标题下边距 */
  font-size: 22px; /* 设置标题字体大小 */
  color: #333; /* 设置标题颜色 */
  text-align: left; /* 标题靠左对齐 */
  font-weight: bold; 
}

.node-info {
  background-color: #D3F5EF; /* 设置背景颜色 */
  padding: 10px; /* 设置内边距 */
  border-radius: 10px; /* 设置圆角 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 设置阴影 */
  text-align: left; /* 内容靠左对齐 */

}

.node-info div {
  margin-bottom: 2px; /* 设置每个属性项的下边距 */
  color: #040404df; /* 设置文本颜色 */
}

.node-info strong {
  color: #d11b1b; /* 设置键的颜色 */
}

.property-item {
  display: flex; /* 使用 flex 布局 */
  align-items: baseline; /* 对齐基线 */
  font-size:18px;
}

.property-item strong {
  flex: 0 0 auto; /* 设置 flex 属性，不增长，不收缩，自动宽度 */
  text-align: right; /* 键右对齐 */
  min-width: 110px; /* 设置最小宽度，根据实际情况调整 */
  margin-right: 15px; /* 设置右边距 */
}

.property-item span {
  flex-grow: 1; /* 值占据剩余空间 */
  text-align: left; /* 值左对齐 */

}
</style>