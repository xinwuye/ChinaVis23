<template>
  <div
      class="map-view"
      style="borderRadius: small"
  >
    <div class="toolbar">
      <span class="toolbar-text">地图视图</span>
    </div>

    <div id="view-body">
      <div id="left-col">
        <div id="map-filter">
          <el-tabs v-model="mode" class="mode-situation" type="border-card" stretch="true" id="filter-tab">
            <el-scrollbar height="100">
              <div id="num-input-length-traj-lb" class="num-input-attr-traj">
                <span class="label-filter">路径长度最小值</span>
                <el-input-number v-model="lengthLowerBound" size="small"></el-input-number>
              </div>
              <div id="num-input-length-traj-ub" class="num-input-attr-traj">
                <span class="label-filter">路径长度最大值</span>
                <el-input-number v-model="lengthUpperBound" size="small"></el-input-number>
              </div>
              <el-tab-pane label="K-means模糊筛选" name="Auto">
                <div v-if="mode === 'Auto'" class="num-input-attr-traj">
                  <span class="label-filter">异常临界值</span>
                  <el-input-number v-model="autoThreshold" size="small" step="0.0001"></el-input-number>
                </div>
              </el-tab-pane>
              <el-tab-pane label="数值精确筛选" name="Manual">
              </el-tab-pane>
            </el-scrollbar>
            <el-button id="filter-button" type="primary">
              筛选
            </el-button>
          </el-tabs>
        </div>
        <div id="candidates">
          <el-scrollbar></el-scrollbar>
        </div>
      </div>

      <div id="right-col">
        <div id="map-body">
          <svg ref="svg" id="svg" width="100%" height="100%"></svg>
        </div>
        <div>
          <el-slider v-model="logicTimestamp"></el-slider>
        </div>
      </div>

    </div>

  </div>
</template>


<script lang="ts" setup>
import {onMounted, ref} from 'vue';
import * as d3 from 'd3';

let svg = ref(null);

async function drawMap() {
  let geojsonData = await d3.json("./lane.geojson");

  let projection = d3.geoIdentity().fitSize([400, 200], geojsonData);
  let path = d3.geoPath().projection(projection);

  let features = geojsonData.features;

  try {
    d3.select(svg.value)
        .append('g')
        .attr('id', 'map-container')
        .selectAll("path")
        .data(features)
        .enter()
        .append("path")
        .attr("d", path)
        .attr("stroke-width", 0.2)
        .attr("fill", "none")
        .attr("stroke", "gray")
  } catch (error) {
    console.log(error);
  }


  const zoom = d3.zoom().on("zoom", function (event) {
    console.log(event);
    d3.select('#map-container').attr("transform", event.transform);
  });

  d3.select(svg.value).call(zoom);
}

const mode = ref('Auto')

const lengthLowerBound = ref(5);
const lengthUpperBound = ref(10);

const autoThreshold = ref(0.01);

const logicTimestamp = ref(0);

onMounted(() => {
  drawMap();
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

.label-filter {
  font-size: 10px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}

.num-input-attr-traj {
  flex-grow: 1;
  display: flex;
  flex-direction: row;
  margin-bottom: 10px;
  margin-top: 10px;
}

.mode-situation {
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
  font-size: 14px; /* Adjust the font size as per your preference */
  padding-left: 5px;
}

.toolbar {
  height: 20px;
  width: 100%;
  background-color: lightgrey;
  text-align: left;
  margin:1px;
}

#left-col {
  width: 50%;
  display: flex;
  flex-direction: column;
  padding-right: 5px;
  padding-left: 5px;
}

#right-col {
  width: 50%;
  display: flex;
  flex-direction: column;
  padding-right: 5px;
  padding-left: 5px;
}

</style>