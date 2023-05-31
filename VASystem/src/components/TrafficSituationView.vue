<template>
  <div
      class="traffic-situation-view"
      style="borderRadius: small"
  >
    <div id="header">
      Traffic Situation View
    </div>

    <div id="traffic-situation-filter">
      <el-tabs v-model="mode" class="mode-situation" type="border-card">
        <div class="num-input-attr-traj" id="num-input-length-traj-lb">
          <span class="label-filter"> Length min</span>
          <el-input-number v-model="lengthLowerBound" size="small"></el-input-number>
        </div>
        <div class="num-input-attr-traj" id="num-input-length-traj-ub">
          <span class="label-filter"> Length max</span>
          <el-input-number v-model="lengthUpperBound" size="small"></el-input-number>
        </div>
        <el-tab-pane label="Auto" name="Auto">
          <div class="num-input-attr-traj" v-if="mode === 'Auto'">
            <span class="label-filter"> Outlier threshold</span>
            <el-input-number v-model="autoThreshold" step="0.0001" size="small"></el-input-number>
          </div>
        </el-tab-pane>
        <el-tab-pane label="Manual" name="Manual">
        </el-tab-pane>
      </el-tabs>
    </div>

  </div>
</template>


<script lang="ts" setup>
import {ref} from 'vue'

const mode = ref('Auto')


const lengthLowerBound = ref(5);
const lengthUpperBound = ref(10);

const autoThreshold = ref(0.01);
</script>


<style scoped>

#header {
  height: 2%;
  margin-top: 10px;
  margin-bottom: 15px;
  font-weight: bold;
}

.traffic-situation-view {
  height: 100%;
  width: 100%;
  border: 1px solid var(--el-border-color);
  border-radius: 5px;
  margin-top: 0px;
}

#traffic-situation-filter {
  width: 30%;
  height: 100%;
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

</style>