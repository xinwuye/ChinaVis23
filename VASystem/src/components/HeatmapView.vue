<template>
  <div
      id="traffic-situation-view"
      class="traffic-situation-view"
      style="borderRadius: small"
  >
    <div class="toolbar">
      <span class="toolbar-text">路段重要性视图</span>
    </div>
    <div id="heatmap-container" style="width: 100%;height:100%;" />
  </div>
</template>

<script lang="ts" setup>
import {onMounted, ref} from 'vue';
import * as d3 from 'd3';
import * as echarts from 'echarts'; // use canvas to render
import axios from 'axios';

var data = null;

onMounted(() => {
  const heatmapContainer = document.getElementById('traffic-situation-view');

  const containerHeight = heatmapContainer.clientHeight;
  const containerWidth = heatmapContainer.clientWidth;
  // set the dimensions and margins of the graph
  const margin = {top: 30, right: 30, bottom: 30, left: 30},
    width = containerHeight - margin.left - margin.right,
    height = containerWidth - margin.top - margin.bottom;

  var app = {};

  var chartDom = document.getElementById('heatmap-container');
  var myChart = echarts.init(chartDom, null, {
    useDirtyRect: true
  });
  var option;

  let path = 'http://localhost:5000/TrafficSituationViewInit';
  axios.post(path)
    .then((res) => {
      console.log(res.data)
      let xData = res.data.unique_fids;
      let yData = res.data.unique_fids;
      let data = res.data.vis_mat_list
      let min = res.data.vis_mat_min;
      let max = res.data.vis_mat_max;
      option = {
        tooltip: {},
        xAxis: {
          type: 'category',
          data: xData,
          show: false,
          // splitArea: {
          //   show: true
          // }
        },
        yAxis: {
          type: 'category',
          data: yData,
          show: false,
          // splitArea: {
          //   show: true
          // }
        },
        grid: {
          height: "90%",
          top: "5%",
          left: "15%",
          backgroundColor: "#f2f7f7",
          show: true,
        },
        visualMap: {
          type: 'continuous',
          min: min,
          max: max,
          dimension: 2,
          calculable: true,
          realtime: false,
          orient: "vertical",
          left: "5%",
          bottom: "30%",
          inRange: {
            color: [
              // ['#d2bb4c', '#b054c1', '#82cd53', '#626ccc', '#d05d2e', '#6bd4a3', '#ce478c', 
              // '#5c7d39', '#bf4b56', '#7ab7d5', '#a0714a', '#7b5d84', '#c2c6a4', '#d3a1c4', 
              // '#4e7670']
              '#7ab7d5',
              '#ce478c'
            ]
          }
        },
        series: [
          {
            // name: '',
            type: 'heatmap',
            data: data,
            emphasis: {
              label: {
                show: false
              }
            },
            progressive: 1000,
            animation: false
          }
        ]
      };
      option && myChart.setOption(option);
    })
    .catch((error) => {
      // eslint-disable-next-line
      console.error(error);
    }); 

});

</script>

<style scoped>
.traffic-situation-view {
  height: 100%;
  width: 100%;
  border: 1px solid var(--el-border-color);
  border-radius: 5px;
  margin-top: 0px;
}

.traffic-situation-view .toolbar {
  height: 20px;
  width: 100%;
  background-color: lightgrey;
  /* border-radius: 5px 5px 0 0; */
  text-align: left;
}

.toolbar-text {
  font-size: 14px; /* Adjust the font size as per your preference */
  padding-left: 5px;
}
</style>