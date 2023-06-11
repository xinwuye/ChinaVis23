<template>
  <div class="map-view" style="borderRadius: small">
    <div class="toolbar">
      <span class="toolbar-text">指标视图</span>
    </div>

    <div id="view-body" style="calc(100% - 20px); width: 100%;">
      <!-- <svg ref="svg" id="svg" width="100%" height="100%"></svg> -->
      <svg ref="svg" id="svg" style="height: 100%; width: 100%;"></svg>
    </div>
  </div>
</template>


<script lang="ts" setup>
import {onMounted, ref, watch} from 'vue';
import * as d3 from 'd3';
import axios from 'axios';
import { storeToRefs } from "pinia";
import { useGlobalStore } from '../stores/global';

let svg = ref(null);
let path = 'http://localhost:5000/MetricView';
const globalStore = useGlobalStore();
const selectedData = storeToRefs(globalStore).selectedData;
const clickedId = storeToRefs(globalStore).clickedId;

async function drawMap(id, title) {

  axios.post(path,{
    id: id,
    selectedData: title,
    }).then((res) => {
    //console.log(res.data.id)
    var data1 = res.data
    var data2 = [data1.per_time_in_0_10, data1.per_time_in_10_20, data1.per_time_in_20_30,
    data1.per_time_in_30_, data1.quick_acceleration, data1.quick_deceleration]

    const margin = { top: 30, right: 30, bottom: 30, left: 30 }

    // get the width and height of #view-body
    const width = document.getElementById('view-body').clientWidth - margin.left - margin.right
    const height = document.getElementById('view-body').clientHeight - margin.top - margin.bottom

    var config = {
      radius: width / 4,
      // center: [225, 200],
      center: [width / 2, height / 2],
      tickNum: 6,  //边数
      innerWidth: width / 20,  //内部间隔
      polygonNum: 4 //有几层多边形
    }

    var pi = Math.PI;
    var piece = 2 * pi / config.tickNum;

    var vertex = [];

    //比例尺
    //速度比例尺
    var Scale0 = d3.scaleLinear()
      .domain([0, 1])
      .range([3, config.radius]);
    //加速度比例尺
    var Scale1 = d3.scaleLinear()
      .domain([0, 45])
      .range([3, config.radius]);

    for (var j = 0; j < config.polygonNum; j++) {
      var dataset = [];
      for (var i = 0; i < config.tickNum; i++) {
        var x = (config.radius - config.innerWidth * j) * Math.sin(i * piece) + config.center[0];
        var y = (config.radius - config.innerWidth * j) * Math.cos(i * piece) + config.center[1];
        dataset[i] = [x, y];
      }
      vertex.push(dataset)

      //绘制多边形
      var radar = d3.select(svg.value)
          .append('g')
          .selectAll("path")
          .data([0])
          .enter()
          .append("polygon")
          .attr('points', dataset)
          .attr("stroke-width", 1)
          .attr("fill", "white")
          .attr("stroke", "black");
    }

    //绘制对角线
    var lines = []
    for (var i = 0; i < vertex[0].length; i++) {
      lines.push(config.center);
      lines.push(vertex[0][i])
    }
    var linePath = d3.line();
    d3.select(svg.value)
      .append('g')
      .selectAll("path")
      .data([0])
      .enter()
      .append("path")
      .attr('d', linePath(lines))
      .attr('stroke', 'black');

    //绘制文字标签
    var txtAnchor = function (i) {
      if (i == 0 || i == 3) { return 'middle'; }
      else if (i == 1 || i == 2) { return 'start'; }
      else { return 'end'; }
    }
    // var txtList1 = ['% of time in speed', '% of time in speed', '% of time in speed',
    //   '% of time in', 'number of acceleration', 'number of deceleration']
    var txtList1 = ['%时间为速度', '%时间为速度', '%时间为速度',
      '%时间在', '#加速', '#减速']
    d3.select(svg.value)
      .append('g')
      .selectAll("txt")
      .data([0, 1, 2, 3, 4, 5])
      .enter()
      .append("text")
      .text(function (i) { return txtList1[i]; })
      .attr("x", function (i) { return (config.radius + 15) * Math.sin(i * piece) + config.center[0] })
      .attr("y", function (i) { return (config.radius + 15) * Math.cos(i * piece) + config.center[1] })
      .style("text-anchor", function (d, i) { return txtAnchor(i) })
      .attr('font-size', '8pt')
      .attr('class', 'textstyle')
      .append("title").text(function(d,i){
        return data2[i];
      });

    // var txtList2 = ['interval 0-10 m/s', 'interval 10-20 m/s', 'interval 20-30 m/s',
    //   'speed >30 m/s', '>0.005 m/s^2', '<-0.005 m/s^2']
    var txtList2 = ['区间 0-10 m/s', '区间 10-20 m/s', '区间 20-30 m/s',
      ' >30 m/s', '>0.005 m/s^2', '<-0.005 m/s^2']
    d3.select(svg.value)
      .append('g')
      .selectAll("txt")
      .data([0, 1, 2, 3, 4, 5])
      .enter()
      .append("text")
      .text(function (i) { return txtList2[i]; })
      .attr("x", function (i) { return (config.radius + 15) * Math.sin(i * piece) + config.center[0] })
      .attr("y", function (i) { return (config.radius + 15) * Math.cos(i * piece) + config.center[1] + 12 })
      .style("text-anchor", function (d, i) { return txtAnchor(i) })
      .attr('font-size', '8pt')
      .attr('class', 'textstyle')
      .append("title").text(function(d,i){
        return data2[i];
      });

    //分类评级
    var rank = function(data2){
      if (data2[0] >= 0.95) {
        return '冷静型';
      } else if (data2[0] >= 0.9) {
        return '普通型';
      } else {
        return '激进型';
      }
    }
    
    //渲染数据
    var dataset2 = [];
    for (var i = 0; i < config.tickNum; i++) {
      if (i in [0, 1, 2, 3]) {
        x = Scale0(data2[i]) * Math.sin(i * piece) + config.center[0];
        y = Scale0(data2[i]) * Math.cos(i * piece) + config.center[1];
        dataset2[i] = [x, y];
      } else {
        x = Scale1(data2[i]) * Math.sin(i * piece) + config.center[0];
        y = Scale1(data2[i]) * Math.cos(i * piece) + config.center[1];
        dataset2[i] = [x, y];
      }
    }

    d3.select(svg.value)
      .append('g')
      .selectAll("path")
      .data([0])
      .enter()
      .append("polygon")
      .attr('points', dataset2)
      .style("fill", '#ce478c')
      .style('opacity', .7)
      .style('stroke', 'black')
      .append("title").text(rank(data2));

  })

  const zoom = d3.zoom().on("zoom", function (event) {
    d3.select('#map-container').attr("transform", event.transform);
  });

  d3.select(svg.value).call(zoom);
}


onMounted(() => {
  // drawMap();
})

watch(clickedId, (newVal, oldVal) => {
  drawMap(newVal, selectedData.value);
})
</script>


<style scoped>
.map-view {
  height: 100%;
  width: 100%;
  border: 1px solid var(--el-border-color);
  border-radius: 5px;
  margin-top: 0px;
}

#map-filter {
  width: 100%;
  height: 50%;
}

#map-body {
  width: 100%;
  height: 90%;
}

#view-body {
  display: flex;
  flex-direction: row;
  height: 98%;
}

#svg {
  border: 1px solid rgb(200, 200, 200);
}

#filter-tab {
  height: 100%;
}

#filter-button {
  margin-top: 2%;
}

.toolbar-text {
  font-size: 14px;
  /* Adjust the font size as per your preference */
  padding-left: 5px;
}

.toolbar {
  height: 20px;
  width: 100%;
  background-color: lightgrey;
  text-align: left;
  margin: 1px;
}

text.textstyle {
  stroke: black;
  stroke-width: 0.2;
  font-family: Consolas, courier;
  font-size: 10pt;
  width: 30px;
  height: 200px;
  word-break: break-all;
}
</style>