<template>
  <div
      class="map-view"
      style="borderRadius: small"
  >
    <div class="toolbar">
      <span class="toolbar-text">地图视图</span>
    </div>

    <div id="view-body">
      <div id="left-col" v-loading="loading">
        <div id="map-filter">
          <el-tabs v-model="mode" class="mode-situation" type="border-card" stretch="true" id="filter-tab">
            <el-scrollbar height="220">
              <div id="num-input-length-traj-lb" class="num-input-attr-traj">
                <span class="label-filter">目标区域</span>
                <el-input-number v-model="areaId" size="small"></el-input-number>
              </div>
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
                  <span class="label-filter">聚类数目</span>
                  <el-input-number v-model="cluster" size="small" step="1"></el-input-number>
                </div>
                <div v-if="mode === 'Auto'" class="num-input-attr-traj">
                  <span class="label-filter">异常临界值</span>
                  <el-input-number v-model="autoThreshold" size="small" step=0.0001></el-input-number>
                </div>
              </el-tab-pane>
              <el-tab-pane label="数值精确筛选" name="Manual">
              </el-tab-pane>
            </el-scrollbar>
            <el-button id="filter-button" type="primary" @click="doFilter">
              筛选
            </el-button>
          </el-tabs>
        </div>
        <div id="candidates">
          <span class="label-filter">
            筛选结果
          </span>
          <el-select
              v-model="selectedID"
              placeholder="Outlier ID"
              style="width: 60%; padding-left: 5%; padding-right: 5%"
          >
            <el-option
                v-for="id in matchIDs"
                :key="id"
                :label="id"
                :value="id"
                @click="switchSelectedID"
            ></el-option>
          </el-select>
        </div>
      </div>

      <div id="right-col">
        <div id="map-body">
          <svg ref="svg" id="svg" width="100%" height="100%"></svg>
        </div>
        <div>
          <el-slider v-model="indexOfFrame" :max="indexMax"></el-slider>
        </div>
      </div>

    </div>

  </div>

  <el-dialog
      v-model="filterError"
      title="结果异常">
    <div style="padding-bottom: 5%">
      {{ errorMessage }}
    </div>
    <el-button @click="closeDialog">
      OK
    </el-button>
  </el-dialog>
</template>


<script lang="ts" setup>
import {onMounted, ref, watch} from 'vue';
import * as d3 from 'd3';
import axios from 'axios';

let svg = ref(null);

async function doFilter() {
  console.log("clicked");
  loading.value = true;
  let path = 'http://localhost:5000/outliers/auto';
  axios.get(path, {
    params: {
      area_id: areaId.value, // replace with your area_id
      length_lower_bound: lengthLowerBound.value, // replace with your desired value
      length_upper_bound: lengthUpperBound.value, // replace with your desired value
      cluster: cluster.value, // replace with your desired value
      outlier_threshold: autoThreshold.value // replace with your desired value
    }
  })
      .then((response) => {
        loading.value = false;
        console.log(response["data"])
        if (response["data"]["error"] != 0) {
          errorCode.value = response["data"]["error"];
          filterError.value = true;

          switch (errorCode.value) {
            case 1:
              errorMessage.value = "数据量过多，请提高临界值";
              break;
            case 2:
              errorMessage.value = "无匹配数据，请降低临界值";
              break;
            case 3:
              errorMessage.value = "未知错误代码:" + String(errorCode.value);

          }
        } else {
          data.value = response["data"]["data"]
          matchIDs.value = response["data"]["data"].map((d) => d[0]);
        }
      })
      .catch((error) => {
        loading.value = false;
        console.error(error);
      });
}

async function drawMap() {
  let geojsonData = await d3.json("./lane.geojson");

  projection.value = d3.geoIdentity().fitSize([400, 200], geojsonData);
  let path = d3.geoPath().projection(projection.value);

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
    d3.select('#map-container').attr("transform", event.transform);
  });

  d3.select(svg.value).call(zoom);
}

function renderFrame(indexOfFrame) {
  const lineGenerator = d3.line()
      .curve(d3.curveCardinal)
      .x(d => projection.value([d["x"], d["y"]])![0])
      .y(d => projection.value([d["x"], d["y"]])![1]);

  let perObjectCoordinate = {};
  for (let i = 0; i <= indexOfFrame; i++) {
    console.log(selectedData.value[i]);
    if (!Object.keys(perObjectCoordinate).includes(String(selectedData.value[i].id))) {
      perObjectCoordinate[String(selectedData.value[i].id)] = [JSON.parse(selectedData.value[i].position)];
    } else {
      perObjectCoordinate[String(selectedData.value[i].id)].push(JSON.parse(selectedData.value[i].position));
    }
  }

  Object.values(perObjectCoordinate).forEach(coordinates => {
    d3.selectAll(".traj").remove();

    d3.selectAll("#map-container")
        .data(Array(coordinates))
        .append("path")
        .attr("class", "traj")
        .attr("fill", "none")
        .attr("stroke", "red")
        .attr("stroke-width", 0.4)
        .attr("d", lineGenerator);
  });
}

function switchSelectedID(){
  indexOfFrame.value = 0;
}
function closeDialog() {
  filterError.value = false;
}

const mode = ref('Auto')

const areaId = ref(1);
const lengthLowerBound = ref(5);
const lengthUpperBound = ref(10);
const cluster = ref(10);
const autoThreshold = ref(5);
const loading = ref(false);
const filterError = ref(false);
const errorCode = ref(0);
const errorMessage = ref("Default error message");
const matchIDs = ref([]);
const selectedID = ref(0);
const indexOfFrame = ref(0);
const indexMax = ref(50);
const data = ref([]);
const selectedData = ref([]);
const projection = ref();

onMounted(() => {
  drawMap();
  watch(selectedID, (newID, _) => {
    let element = data.value.find((d) => d[0] == newID);
    if (element && Array.isArray(element[1])) {
      indexMax.value = element[1].length;
    }
    selectedData.value = element[1];
    renderFrame(indexOfFrame.value);
  });

  watch(indexOfFrame, (newFrameIndex, _) => {
    renderFrame(indexOfFrame.value);
  });
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
  height: 80%;
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
  margin: 1px;
}

#left-col {
  border-radius: 5px;
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

#candidates {
  height: 25%;
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>