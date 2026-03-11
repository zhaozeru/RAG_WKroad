import { defineStore } from 'pinia'
import { ref } from 'vue'


interface Node {
  id: number;
  [key: string]: any;
}

export const useNodeAttributeStore = defineStore('GraphComponent', () => {
  const nodeList = ref<Node[]>([
    {
      id: 0,
      label: "武康路",
      name: "武康路",
      properties: {
        name: "武康路",
        起点:'华山路',
        终点:'淮海中路',
        简介: '武康路（Wukang Road），是中国上海市徐汇区境内南北向道路，位于徐汇区北部，连接了华山路和淮海中路，也是中国历史文化名街之一 。\
        武康路北起华山路，南至淮海中路，全长1182.7米，宽12米至15.5米 。', 
        历史变迁: '武康路于清光绪三十三年（1907年）修筑，时名福开森路 ；于民国三年（1914年）拆分 ；于民国三十二年（1943年）更名为武康路 。', 
        文化特色: '武康路的沿线建筑代表了上海20世纪二三十年代重要建筑设计机构和建筑师的作品，展现了当时的顶尖设计水平。初期由外国设计师主导，\
        后来逐渐转为中国建筑师主导，涵盖了诸如公和洋行、责安洋行、思九生洋行等重要建筑设计机构和设计师。在林荫大道两旁，高级花园别墅汇集了不同\
        风格的建筑，包括英国乡村式、法国文艺复兴式、西班牙式、地中海式、装饰艺术派、现代派以及混合式建筑等。这些建筑集聚了不同历史时期、国家\
        建筑风格的代表作品，展示了上海独特的海派文化，并成为宝贵的文化遗产，见证了东西方文化的交融和发展 。', 
      },
      type: "中心节点"
    }
  ]);

  function updateNodeAttribute(nodeId: number, newAttributes: Partial<Node>) {
    nodeList.value = []
    const newNode = { ...newAttributes, id: nodeId } as Node
    nodeList.value.push(newNode)

    console.log(`Updated node with ID ${nodeId}:`, nodeList.value)
  }

  return {
    nodeList,
    updateNodeAttribute
  }
})