<template>
  <div
      class="map-view"
      style="borderRadius: small"
  >
    <div id="header">
      Map View
    </div>

    <div id="view-body">
      <div id="map-filter">
        <el-tabs v-model="mode" class="mode-situation" type="border-card" stretch="true" id="filter-tab">
            <el-scrollbar height="100">
              <div id="num-input-length-traj-lb" class="num-input-attr-traj">
                <span class="label-filter"> Length min</span>
                <el-input-number v-model="lengthLowerBound" size="small"></el-input-number>
              </div>
              <div id="num-input-length-traj-ub" class="num-input-attr-traj">
                <span class="label-filter"> Length max</span>
                <el-input-number v-model="lengthUpperBound" size="small"></el-input-number>
              </div>
              <el-tab-pane label="Auto" name="Auto">
                <div v-if="mode === 'Auto'" class="num-input-attr-traj">
                  <span class="label-filter"> Outlier threshold</span>
                  <el-input-number v-model="autoThreshold" size="small" step="0.0001"></el-input-number>
                </div>
              </el-tab-pane>
              <el-tab-pane label="Manual" name="Manual">
              </el-tab-pane>
            </el-scrollbar>
          <el-button id="filter-button" type="primary">
            Filter
          </el-button>
        </el-tabs>
      </div>

      <div id="map-body">
        <svg ref="svg" id="svg" width="100%" height="100%"></svg>
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

onMounted(() => {
  drawMap();
})
</script>


<style scoped>

#header {
  height: 2%;
  margin-top: 10px;
  margin-bottom: 15px;
  font-weight: bold;
}

.map-view {
  height: 100%;
  width: 100%;
  border: 1px solid var(--el-border-color);
  border-radius: 5px;
  margin-top: 0px;
}

#map-filter {
  width: 40%;
  height: 50%;
  margin-left: 5px;
  margin-right: 5px;
}

#candidate {
  width: 0%;
  height: 90%;
  margin-left: 5px;
  margin-right: 5px;
}

#map-body {
  width: 60%;
  height: 90%;
  margin-left: 5px;
  margin-right: 5px;
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
  margin-top: 5%;
}

</style>