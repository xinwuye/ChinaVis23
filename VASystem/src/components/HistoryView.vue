<template>
  <div class="map-view" style="borderRadius: small">
    <div class="toolbar">
      <span class="toolbar-text">行为视图</span>
    </div>

    <div ref="container" id='container'></div>

  </div>
</template>


<script lang="ts" setup>
import { onMounted, ref, watch } from 'vue';
import * as d3 from 'd3';
import axios from 'axios';
import * as THREE from 'three';
import {
  OrbitControls
} from 'three/examples/jsm/controls/OrbitControls'
import { storeToRefs } from "pinia";
import { useGlobalStore } from '../stores/global';

let path = 'http://localhost:5000/HistoryView';
const globalStore = useGlobalStore();
const selectedData = storeToRefs(globalStore).selectedData;
const clickedId = storeToRefs(globalStore).clickedId;

// export default {
//   mounted() {
//     const Container = document.getElementById('container');

//     const Height = Container.clientHeight;
//     const Width = Container.clientWidth;

//     // 创建场景、相机和渲染器
//     const scene = new THREE.Scene();
//     const camera = new THREE.PerspectiveCamera(
//       75,
//       Width / Height,
//       0.1,
//       1000
//     );
//     camera.position.z = 5;
//     const renderer = new THREE.WebGLRenderer();
//     renderer.setSize(Width, Height);
//     renderer.setClearColor(0xFFFFFF, 1);
//     this.$refs.container.appendChild(renderer.domElement);

//     // 创建物体
//     axios.post(path).then((res) => {
//       //准备数据
//       var data1 = res.data

//       var v = []; //速度
//       var t = []; //时间戳
//       var o = []; //方向
//       var a = []; //加速度
//       var output = data1['vplot'].slice(1, data1['vplot'].length - 1).split(',');
//       var output2 = data1['vtime'].slice(1, data1['vtime'].length - 1).split(',');
//       var output3 = data1['orientation'].slice(1, data1['orientation'].length - 1).split(',');
//       var output4 = data1['aplot'].slice(1, data1['aplot'].length - 1).split(',');
//       for (var i = 0; i < output.length; i++) {
//         v.push(parseFloat(output[i]));
//         t.push(parseFloat(output2[i]));
//         o.push(parseFloat(output3[i]));
//         a.push(parseFloat(output4[i]));
//       }

//       //比例尺
//       var xScale = d3.scaleLinear()
//         .domain([d3.min(t), d3.max(t)])
//         .range([0, Width / 2]);

//       var yScale = d3.scaleLinear()
//         .domain([d3.min(v) - 1, d3.max(v) + 1])
//         .range([0, 20]);

//       // 按加速度更改线段颜色
//       const Linewidth = 10;
//       var Color = function (acceleration) {
//         if (acceleration <= -0.01) {
//           return { color: 0x0000cd, linewidth: Linewidth };
//         } else if (acceleration <= -0.005) {
//           return { color: 0x1e90ff, linewidth: Linewidth };
//         } else if (acceleration <= 0) {
//           return { color: 0x87cefa, linewidth: Linewidth };
//         } else if (acceleration <= 0.005) {
//           return { color: 0xffb6c1, linewidth: Linewidth };
//         } else if (acceleration <= 0.01) {
//           return { color: 0xba55d3, linewidth: Linewidth };
//         } else {
//           return { color: 0x4b0082, linewidth: Linewidth };
//         }
//       }

//       //循环创建线段
//       for (var i = 0; i < v.length; i++) {
//         //坐标
//         var Velocity = yScale(v[i]);
//         var orientation = o[i];
//         var acceleration = a[i];
//         var X = xScale(t[i]) - 50;
//         var Z = Math.sin(orientation) * Velocity;
//         var Y = Math.cos(orientation) * Velocity;

//         //生成线段
//         const points = [];
//         points.push(new THREE.Vector3(X, 0, 0));
//         points.push(new THREE.Vector3(X, Y, Z));
//         const geometry = new THREE.BufferGeometry().setFromPoints(points);
//         const material = new THREE.LineBasicMaterial(Color(acceleration));

//         const line = new THREE.Line(geometry, material);
//         scene.add(line);
//       }

//       //添加坐标轴辅助器
//       const axesHelper = new THREE.AxesHelper(50);
//       scene.add(axesHelper);

//       //创建轨道控制器(相机，渲染器)
//       var controls = new OrbitControls(camera, renderer.domElement);

//       //设置渲染函数
//       function render() {
//         renderer.render(scene, camera);
//         //设置背景颜色
//         renderer.setClearColor(0xffffff, 1);
//         requestAnimationFrame(render);
//       }

//       render();


//       //绘制图例


//     })

//   },
// };

watch(clickedId, ((newVal, oldVal) => {
  console.log(this)
  drawHistory.bind(this)(newVal, selectedData.value);
}).bind(this))

function drawHistory(id, title) {
  d3.select("#container").selectAll('*').remove();
  const Container = document.getElementById('container');

  const Height = Container.clientHeight;
  const Width = Container.clientWidth;

  // 创建场景、相机和渲染器
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    75,
    Width / Height,
    0.1,
    1000
  );
  camera.position.z = 5;
  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(Width, Height);
  renderer.setClearColor(0xFFFFFF, 1);
  // this.$refs.container.appendChild(renderer.domElement);
  Container.appendChild(renderer.domElement);

  // 创建物体
  axios.post(path, {
    id: id,
    selectedData: title,
    }).then((res) => {
    //准备数据
    var data1 = res.data

    var v = []; //速度
    var t = []; //时间戳
    var o = []; //方向
    var a = []; //加速度
    var output = data1['vplot'].slice(1, data1['vplot'].length - 1).split(',');
    var output2 = data1['vtime'].slice(1, data1['vtime'].length - 1).split(',');
    var output3 = data1['orientation'].slice(1, data1['orientation'].length - 1).split(',');
    var output4 = data1['aplot'].slice(1, data1['aplot'].length - 1).split(',');
    for (var i = 0; i < output.length; i++) {
      v.push(parseFloat(output[i]));
      t.push(parseFloat(output2[i]));
      o.push(parseFloat(output3[i]));
      a.push(parseFloat(output4[i]));
    }

    //比例尺
    var xScale = d3.scaleLinear()
      .domain([d3.min(t), d3.max(t)])
      .range([0, Width / 2]);

    var yScale = d3.scaleLinear()
      .domain([d3.min(v) - 1, d3.max(v) + 1])
      .range([0, 20]);

    // 按加速度更改线段颜色
    const Linewidth = 10;
    var Color = function (acceleration) {
      if (acceleration <= -0.01) {
        return { color: 0x0000cd, linewidth: Linewidth };
      } else if (acceleration <= -0.005) {
        return { color: 0x1e90ff, linewidth: Linewidth };
      } else if (acceleration <= 0) {
        return { color: 0x87cefa, linewidth: Linewidth };
      } else if (acceleration <= 0.005) {
        return { color: 0xffb6c1, linewidth: Linewidth };
      } else if (acceleration <= 0.01) {
        return { color: 0xba55d3, linewidth: Linewidth };
      } else {
        return { color: 0x4b0082, linewidth: Linewidth };
      }
    }

    //循环创建线段
    for (var i = 0; i < v.length; i++) {
      //坐标
      var Velocity = yScale(v[i]);
      var orientation = o[i];
      var acceleration = a[i];
      var X = xScale(t[i]) - 50;
      var Z = Math.sin(orientation) * Velocity;
      var Y = Math.cos(orientation) * Velocity;

      //生成线段
      const points = [];
      points.push(new THREE.Vector3(X, 0, 0));
      points.push(new THREE.Vector3(X, Y, Z));
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      const material = new THREE.LineBasicMaterial(Color(acceleration));

      const line = new THREE.Line(geometry, material);
      scene.add(line);
    }

    //添加坐标轴辅助器
    const axesHelper = new THREE.AxesHelper(50);
    scene.add(axesHelper);

    //创建轨道控制器(相机，渲染器)
    var controls = new OrbitControls(camera, renderer.domElement);

    //设置渲染函数
    function render() {
      renderer.render(scene, camera);
      //设置背景颜色
      renderer.setClearColor(0xffffff, 1);
      requestAnimationFrame(render);
    }

    render();


    //绘制图例


  })
}

</script>


<style scoped>
.map-view {
  height: 100%;
  width: 100%;
  border: 1px solid var(--el-border-color);
  border-radius: 5px;
  margin-top: 0px;
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

#container {
  width: 100%;
  height: 100%;
}
</style>