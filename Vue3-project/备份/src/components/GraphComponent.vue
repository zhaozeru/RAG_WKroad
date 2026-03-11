<template>
  <div ref="graphContainer" class="graph-container"></div>
  <LegendComponent       
    :typeColorMap="typeColorMap" 
    :typeTextColorMap="typeTextColorMap" 
    :displayedTypes="displayedTypes"  />
  <div class="refresh-button">
    <el-button type="primary" :icon="House" @click="refreshGraph" class="custom-button">刷新图谱</el-button>    
  </div>
</template>

<script setup>
import { ref, onMounted, watch, reactive } from 'vue';
import * as d3 from 'd3';
import neo4j from 'neo4j-driver';
import LegendComponent from './LegendComponent.vue';
import { useNodeAttributeStore } from '@/store/Nodeattribute';
import { House } from '@element-plus/icons-vue'

const nodeStore = useNodeAttributeStore();

let svg

const props = defineProps({
  personId: {
    type: String,
    required: false
  },
  category: {
    type: String,
    required: false
  }
});
const graphContainer = ref(null);
const graph = reactive({ nodes: [], links: [] });
const tem_graph1 = reactive({ nodes: [], links: [] });
const tem_graph2 = reactive({ nodes: [], links: [] });


const typeColorMap = {
  "中心节点": "#ECB5C9",
  "故居节点": "#F79767",
  "人物节点": "#57C7E3",
  "事件节点": "#8DCC93",
  "图片节点":"#569480",
  "人物简介节点": "#F16667",
  "人物图片节点": "#FFC454",
  "人物作品节点": "#C990C0",
  "人物别名节点": "#D9C8AE",
  "人物相关机构节点": "#4C8EDA"
};
const typeBorderColorMap = {
  "中心节点": "#da7298",
  "故居节点": "#f36924",
  "人物节点": "#23b3d7",
  "事件节点": "#5db665",
  "图片节点":"#447666",
  "人物简介节点": "#eb2728",
  "人物图片节点": "#d7a013",
  "人物作品节点": "#b261a5",
  "人物别名节点": "#c0a378",
  "人物相关机构节点": "#2870c2"
};
const typeTextColorMap = {
  "中心节点": "#2A2C34",
  "故居节点": "#FFFFFF",
  "人物节点": "#2A2C34",
  "事件节点": "#2A2C34",
  "图片节点":"#FFFFFF",
  "人物简介节点": "#FFFFFF",
  "人物图片节点": "#2A2C34",
  "人物作品节点": "#FFFFFF",
  "人物别名节点": "#2A2C34",
  "人物相关机构节点": "#FFFFFF"
};

const displayedTypes = ref([]);
const updateDisplayedTypes = () => {
  const types = new Set();
  tem_graph2.nodes.forEach(node => types.add(node.type));
  displayedTypes.value = Array.from(types);
};

onMounted(async () => {
  await fetchAllGraph();
});

watch([() => props.personId, () => props.category], fetchGraphData);

watch(() => tem_graph2.nodes, updateDisplayedTypes, { deep: true });

async function fetchAllGraph() {
  const data = await fetchGraphFromNeo4j();
  if (data) {
    graph.nodes = data.nodes;
    graph.links = data.links;

    clearTemgraph(tem_graph1);

    tem_graph1.nodes = data.nodes.filter(node => 
      node.type === '中心节点' || node.type === '故居节点'
    );

    tem_graph1.links = data.links.filter(link =>
      tem_graph1.nodes.some(node => node.id === link.source) &&
      tem_graph1.nodes.some(node => node.id === link.target)
    );

    console.log('Graph updated in fetchAllGraph:', tem_graph1);
    updateGraph(tem_graph1,tem_graph1);
  }
}

async function fetchGraphData() {
  const data = await fetchGraphFromNeo4j(props.category, props.personId);
  if (data) {
    clearTemgraph(tem_graph2);
    tem_graph2.nodes = data.nodes;
    tem_graph2.links = data.links;
    console.log('Graph updated in fetchGraphData:', tem_graph2);
    updateGraph(tem_graph2, tem_graph2);

    const nodeInfo = tem_graph2.nodes.find(node => node.label == props.personId);
    if (nodeInfo) {updateNodeInfoInPinia(nodeInfo);}

  }

}

function updateNodeInfoInPinia(nodeInfo) {
  nodeStore.updateNodeAttribute(nodeInfo.id, nodeInfo);
}

async function fetchGraphFromNeo4j(category, personId) {
  // const driver = neo4j.driver('bolt://localhost:7687', neo4j.auth.basic('neo4j', '_rong.5420'));
  const driver = neo4j.driver('bolt://8.140.224.45:7687', neo4j.auth.basic('neo4j', '_rong.5420'));
  const session = driver.session({ database: 'WKroadproject' });
  try {
    let query;

    if (!category && !personId) {
      query = `
        MATCH (p)-[r1]->(n1)
        RETURN p, r1, n1
      `;
    } else if (category === '人物栏' && personId) {
      query = `
        MATCH (p:人物节点 {name: $personId})
        OPTIONAL MATCH (p)-[r1]->(n1)
        OPTIONAL MATCH (m)-[r2]->(n1)
        RETURN p, r1, n1, m, r2
      `;
    } else if (category === '故居栏' && personId) {
      query = `
        MATCH (p:故居节点 {name: $personId})
        OPTIONAL MATCH (p)-[r1]->(n1)
        OPTIONAL MATCH (m)-[r2]->(n1)
        RETURN p, r1, n1, m, r2
      `;
    }

    const result = await session.run(query, { personId });

    const nodes = new Map();
    const links = [];

    result.records.forEach(record => {
      ['p', 'n1'].forEach(label => {
        const node = record.get(label);
        if (node) {
          const nodeId = node.identity.toNumber();
          if (!nodes.has(nodeId)) {
            const type = node.labels.length > 0 ? node.labels[0] : 'unknown';
            nodes.set(nodeId, {
              id: nodeId,
              label: node.properties.name,
              type,
              properties: node.properties,
              ...node.properties
            });
          }
        }
      });
      const source = record.get('p');
      const target = record.get('n1');
      const relationship = record.get('r1');
      if (source && target && relationship) {
        links.push({
          source: source.identity.toNumber(),
          target: target.identity.toNumber(),
          type: relationship.type
        });
      }
      if (category && personId) {
        const mNode = record.get('m');
        const mRelationship = record.get('r2');
        if (mNode && mRelationship) {
          const mNodeId = mNode.identity.toNumber();
          if (!nodes.has(mNodeId)) {
            const type = mNode.labels.length > 0 ? mNode.labels[0] : 'unknown';
            nodes.set(mNodeId, {
              id: mNodeId,
              label: mNode.properties.name,
              type,
              properties: mNode.properties,
              ...mNode.properties
            });
          }
          links.push({
            source: mNodeId,
            target: target.identity.toNumber(),
            type: mRelationship.type
          });
        }
      }
    });

    console.log('Fetched data:', { nodes: Array.from(nodes.values()), links });

    return { nodes: Array.from(nodes.values()), links };
  } catch (error) {
    console.error('Error fetching graph data:', error);
    return null;
  } finally {
    await session.close();
    await driver.close();
  }
}

function clearGraph() {
  d3.select(graphContainer.value).selectAll("*").remove();
}

function clearTemgraph(canshu) {
  canshu.nodes = [];
  canshu.links = [];
}

function updateGraph(data,tem_graph) {
  clearGraph();
  initGraph(data,tem_graph);
}

function initGraph(data,tem_graph) {
  const container = graphContainer.value;
  const width = container.clientWidth;
  const height = container.clientHeight;
  const links = data.links.map(d => ({ ...d }));
  const nodes = data.nodes.map(d => ({ ...d }));
  const totalNodes = nodes.length;
  if (totalNodes === 1) {
    nodes[0].x = width / 2;
    nodes[0].y = height / 2;
  } else {
    const radius = 700; 
    const angleStep = (2 * Math.PI) / totalNodes;
    nodes.forEach((node, index) => {
      const angle = index * angleStep;
      node.x = width / 3 + radius * Math.cos(angle);
      node.y = height / 2 + radius * Math.sin(angle);
    });
  }  
  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(() => 210 + Math.random() * 110))
    .force("charge", d3.forceManyBody().strength(-350))
    .force("collide", d3.forceCollide().radius(44))
    .on("tick", ticked)

  svg = d3.select(graphContainer.value).append("svg") 
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [0, 0, width, height])
  .attr("style", "max-width: 100%; height: auto;")
  .call(d3.zoom()
    .on("zoom", (event) => {
      svg.attr("transform", event.transform);
    }))
    .on("dblclick.zoom", null)
  .append("g");
      
  svg.append("defs").append("filter")
    .attr("id", "glow")
    .attr("x", "-50%")
    .attr("y", "-50%")
    .attr("width", "200%")
    .attr("height", "200%")
    .append("feDropShadow")
    .attr("dx", 0)
    .attr("dy", 0)
    .attr("stdDeviation", 10)  
    .attr("flood-opacity", 1); 

  svg.select("defs").append("feMerge")
    .append("feMergeNode")
    .attr("in", "blur");

  svg.select("defs").append("feMerge")
    .append("feMergeNode")
    .attr("in", "SourceGraphic");

  const arrowColor = "#A5ABB6";

  svg.append("defs").selectAll("marker")
    .data(["end"])
    .enter().append("marker")
    .attr("id", "end")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 54)
    .attr("refY", 0)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M0,-5L10,0L0,5")
    .attr("fill", arrowColor);

  const linkGroup = svg.append("g")
    .attr("stroke", arrowColor)
    .attr("stroke-opacity", 0.7);

  const link = linkGroup
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke-width", 1.45)
    .attr("marker-end", "url(#end)");

  const linkLabel = linkGroup
    .selectAll("text")
    .data(links)
    .enter().append("text")
    .attr("class", "linksText")
    .text(d => d.type)
    .style("font-size", 13)
    .style("padding", "3px")
    .attr("text-anchor", "middle")
    .attr("dy", -2)
    .style("text-shadow", "none");

  const nodeGroup = svg.append("g")
    .selectAll("g")
    .data(nodes)
    .enter().append("g")
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended))
    .on('dblclick', (event, d) => dblclick(event, d, tem_graph))
    .on('click', clicked)

  nodeGroup.on('mouseover', function (event, d) {
      const color = typeColorMap[d.type] || "#ccc";
      d3.select(this).select('circle')
        .attr('filter', `url(#glow)`)
        .attr('fill', color); 
      d3.select('#glow feDropShadow')
        .attr('flood-color', color); 
    })
    .on('mouseout', function (event, d) {
      d3.select(this).select('circle')
        .attr('filter', 'url(#no-glow)');
    });

  nodeGroup.append("circle")
    .attr("r", 38)
    .attr("fill", d => typeColorMap[d.type] || "#ccc")
    .attr("stroke", d => typeBorderColorMap[d.type] || "#000")
    .attr("stroke-width", 2);

  nodeGroup.append("title")
    .text(d => d.label);

  nodeGroup.append("text")
    .attr('text-anchor', 'middle')
    .attr('dy', 4)
    .attr('font-size', 16)
    .attr('fill', d => typeTextColorMap[d.type] || 'black')
    .text(d => d.label.length > 5 ? d.label.slice(0, 4) + '...' : d.label);

  function ticked() {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    nodeGroup
      .attr("transform", d => `translate(${d.x}, ${d.y})`);

    linkLabel
      .attr("x", d => (d.source.x + d.target.x) / 2)
      .attr("y", d => (d.source.y + d.target.y) / 2)
      .attr("transform", d => {
        const angle = Math.atan2(d.target.y - d.source.y, d.target.x - d.source.x) * 180 / Math.PI;
        const midX = (d.source.x + d.target.x) / 2;
        const midY = (d.source.y + d.target.y) / 2;
        const isLeft = d.source.x > d.target.x;
        return `rotate(${angle + (isLeft ? 180 : 0)}, ${midX}, ${midY})`;
      });
  }


  function dragstarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.2).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  }

  function dragended(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    if (d.fixed) {
      d.fx = null;
      d.fy = null;
      d.fixed = false;
    } else {
      d.fx = d.x;
      d.fy = d.y;
      d.fixed = true;
    }
  }

  function clicked(event, d) {
    if (d.fixed) {
      d.fx = null;
      d.fy = null;
      d.fixed = false;
    }
    nodeStore.updateNodeAttribute(d.id, d)
  }

  function dblclick(event, d, tem_graph) {
  const isSourceInTemGraph = tem_graph.links.some(link => link.source.toString() === d.id.toString());

  if (isSourceInTemGraph) {
    collapseNode(d, tem_graph);
  } else {
    expandNode(d, tem_graph);
  }
}

  async function expandNode(node, tem_graph) {
    const nodeId = node.id;
    const childLinks = graph.links.filter(link => link.source.toString() === nodeId.toString());
    const childrenIds = childLinks.map(link => link.target.toString());
    const children = graph.nodes.filter(n => childrenIds.includes(n.id.toString()));

    children.forEach(child => {
      if (!tem_graph.nodes.some(n => n.id.toString() === child.id.toString())) {
        tem_graph.nodes.push(child);
        const linkType = childLinks.find(link => link.target.toString() === child.id.toString()).type;
        tem_graph.links.push({ source: node.id, target: child.id, type: linkType });
      }
    });

    updateGraph(tem_graph,tem_graph);
  }

  function collapseNode(node, tem_graph) {
    const childIds = tem_graph.links
      .filter(link => link.source.toString() === node.id.toString())
      .map(link => link.target.toString());

    tem_graph.nodes = tem_graph.nodes.filter(n => !childIds.includes(n.id.toString()));
    tem_graph.links = tem_graph.links.filter(link => link.source.toString() !== node.id.toString());

    updateGraph(tem_graph,tem_graph);
  }

}


const refreshGraph = async () => {
  await fetchAllGraph();
};

</script>


<style>
.graph-container {
  width: 100%;
  height: 100%;
  background-color: #E3F8F8;
  opacity: 0.85; /* 设置透明度为80% */
}
.hidden {
  display: none;
}
.refresh-button {
  position: absolute;
  top: 3%;
  right: 88%;
}


</style>
