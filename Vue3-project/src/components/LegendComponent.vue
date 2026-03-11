<template>
  <div ref="legendContainer" class="legend-container"></div>
</template>

<script setup>
import * as d3 from 'd3';
import { ref, onMounted, watch, defineProps } from 'vue';

const props = defineProps({
  typeColorMap: {
    type: Object,
    required: true
  },
  typeTextColorMap: {
    type: Object,
    required: true
  },
  displayedTypes: {
    type: Array,
    required: false
  }
});

const legendWidth = 180;
const legendHeight = 350;
const legendMargin = { top: 0, right: 0, bottom: 0, left: 0 };

const legendContainer = ref(null);

const renderAllLegends = () => {
  d3.select(legendContainer.value).selectAll('*').remove();

  const svg = d3.select(legendContainer.value).append('svg')
    .attr('width', legendWidth)
    .attr('height', legendHeight);

  const legend = svg.append('g')
    .attr('class', 'legend')
    .attr('transform', `translate(${legendMargin.left}, ${legendMargin.top})`);

  const allTypes = Object.keys(props.typeColorMap);
  const legendItems = allTypes.map(type => ({
    type,
    color: props.typeColorMap[type] || '#cccccc',
    textColor: props.typeTextColorMap[type] || '#000000'
  }));

  const itemHeight = 35;
  const padding = 10;

  const textMeasurement = svg.append('text')
    .attr('x', -9999)
    .attr('y', -9999)
    .attr('fill', 'black')
    .style('font-size', '14px');

  legendItems.forEach((item, i) => {
    const y = i * itemHeight;

    textMeasurement.text(item.type);
    const textWidth = textMeasurement.node().getBBox().width;

    const rectX = legendWidth - (textWidth + padding * 2);
    const textX = legendWidth - (textWidth + padding);

    legend.append('rect')
      .attr('x', rectX)
      .attr('y', y + padding / 2)
      .attr('width', textWidth + padding * 2)
      .attr('height', itemHeight - padding)
      .attr('rx', (itemHeight - padding) / 2)
      .attr('ry', (itemHeight - padding) / 2)
      .attr('fill', item.color);

    legend.append('text')
      .attr('x', textX)
      .attr('y', y + itemHeight / 2)
      .attr('dy', '0.35em')
      .attr('fill', item.textColor)
      .style('font-size', '14px')
      .text(item.type);
  });

  textMeasurement.remove();
};

const renderLegend = () => {
  d3.select(legendContainer.value).selectAll('*').remove();

  const svg = d3.select(legendContainer.value).append('svg')
    .attr('width', legendWidth)
    .attr('height', legendHeight);

  const legend = svg.append('g')
    .attr('class', 'legend')
    .attr('transform', `translate(${legendMargin.left}, ${legendMargin.top})`);

  const legendItems = props.displayedTypes.map(type => ({
    type,
    color: props.typeColorMap[type] || '#cccccc',
    textColor: props.typeTextColorMap[type] || '#000000'
  }));

  const itemHeight = 35;
  const padding = 10;

  const textMeasurement = svg.append('text')
    .attr('x', -9999)
    .attr('y', -9999)
    .attr('fill', 'black')
    .style('font-size', '14px');

  legendItems.forEach((item, i) => {
    const y = i * itemHeight;

    textMeasurement.text(item.type);
    const textWidth = textMeasurement.node().getBBox().width;

    const rectX = legendWidth - (textWidth + padding * 2);
    const textX = legendWidth - (textWidth + padding);

    legend.append('rect')
      .attr('x', rectX)
      .attr('y', y + padding / 2)
      .attr('width', textWidth + padding * 2)
      .attr('height', itemHeight - padding)
      .attr('rx', (itemHeight - padding) / 2)
      .attr('ry', (itemHeight - padding) / 2)
      .attr('fill', item.color);

    legend.append('text')
      .attr('x', textX)
      .attr('y', y + itemHeight / 2)
      .attr('dy', '0.35em')
      .attr('fill', item.textColor)
      .style('font-size', '14px')
      .text(item.type);
  });

  textMeasurement.remove();
};

onMounted(() => {
  renderAllLegends();
});

watch(() => props.displayedTypes, () => {
  renderLegend();
});
</script>

<style scoped>
.legend-container {
  position: absolute;
  top: 2%;
  right: 1.5%;
  border-radius: 10px;
  padding: 10px;
  pointer-events: none;

}
</style>