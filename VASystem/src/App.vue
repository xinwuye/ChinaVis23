<template>
  <el-config-provider namespace="ep">
    <el-container>
      <el-main>
        <el-row>
          <el-col :span="6">
            <ControlPanel/>
          </el-col>
          <el-col :span="10">
            <MapView/>
          </el-col>
          <el-col :span="8">
            <HistoryView/>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="4">
            <MetricView/>
          </el-col>
          <el-col :span="12">
            <TrafficSituationView/>
          </el-col>
          <el-col :span="8">
            <HeatmapView/>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </el-config-provider>
</template>

<style lang="scss">
#app {
  text-align: center;
  color: var(--ep-text-color-primary);
  height: 100%;
}

.main-container {
  height: calc(100vh - var(--ep-menu-item-height) - 3px);
}

.ep-container {
  height: 100% !important;
}

.ep-main {
  height: 100% !important;
}

.ep-row {
  // height: calc((100% - 20px) / 2); /* 20px is the margin-bottom value */
  height: 50% !important;
  padding-bottom: 4px;
}

.ep-row:last-child {
  margin-bottom: 0;
}

.ep-col {
  border-radius: 4px;
  padding-right: 4px;
}

.grid-content {
  border-radius: 4px;
  // min-height: 36px;
  // min-height: 100%;
}
</style>
