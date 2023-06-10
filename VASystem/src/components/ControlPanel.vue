<template>
  <div
      class="control-panel"
      style="borderRadius: small"
  >
    <div class="toolbar">
      <span class="toolbar-text">控制面板</span>
    </div>
    <div style="display: flex; align-items: center;">
      <span class="label-text">数据集：</span>
      <el-select
        placeholder="数据集"
        v-model="selectedData"
        size="small"
        class="pt-2"
      >
        <el-option 
          v-for="option in dataList" 
          :key="option" 
          :label="option" 
          :value="option"
        ></el-option>  
      </el-select>
    </div>
    <div>当前展示交通参与者ID：{{clickedId}}</div>
  </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from "pinia";
import { useGlobalStore } from '../stores/global';

const globalStore = useGlobalStore();
const selectedData = storeToRefs(globalStore).selectedData;
const clickedId = storeToRefs(globalStore).clickedId;
const dataList = [1, 2, 3];
</script>

<style scoped>
.control-panel {
  height: 100%;
  width: 100%;
  border: 1px solid var(--el-border-color);
  border-radius: 5px;
  margin-top: 0px;
}

.control-panel .toolbar {
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

.ep-select {
  width: 50%;
}

.label-text {
  font-size: 12px;
  padding-left: 5px;
  margin-right: 10px;
  padding-top: 5px;
}
</style>