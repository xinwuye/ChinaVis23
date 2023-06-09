<template>
  <div
      id="traffic-situation-view"
      class="traffic-situation-view"
      style="borderRadius: small"
  >
    <div class="toolbar">
      <span class="toolbar-text">交通态势视图</span>
    </div>
    <div id="horizon-chart-container" />
  </div>
</template>

<script lang="ts" setup>
import {onMounted, ref} from 'vue';
import * as d3 from 'd3';
import * as echarts from 'echarts'; // use canvas to render
import axios from 'axios';
import { horizonChart } from 'd3-horizon-chart';
import { storeToRefs } from "pinia";
import { useGlobalStore } from '../stores/global';

const globalStore = useGlobalStore();

onMounted(() => {
  RoadSecSelected('63')
});

// Copyright 2021 Observable, Inc.
// Released under the ISC license.
// https://observablehq.com/@d3/horizon-chart
function HorizonChart(data, {
  x = ([x]) => x, // given d in data, returns the (temporal) x-value
  y = ([, y]) => y, // given d in data, returns the (quantitative) y-value
  z = () => 1, // given d in data, returns the (categorical) z-value
  defined, // for gaps in data
  curve = d3.curveLinear, // method of interpolation between points
  marginTop = 20, // top margin, in pixels
  marginRight = 0, // right margin, in pixels
  marginBottom = 0, // bottom margin, in pixels
  marginLeft = 0, // left margin, in pixels
  width = 640, // outer width, in pixels
  size = 25, // outer height of a single horizon, in pixels
  bands = 3, // number of bands
  padding = 1, // separation between adjacent horizons
  xType = d3.scaleUtc, // type of x-scale
  xDomain, // [xmin, xmax]
  textLength = 100, // length of text
  xRange = [marginLeft, width - marginRight - textLength], // [left, right]
  yType = d3.scaleLinear, // type of y-scale
  yDomain, // [ymin, ymax]
  yRange = [size, size - bands * (size - padding)], // [bottom, top]
  zDomain, // array of z-values
  scheme = d3.schemeGreys, // color scheme; shorthand for colors
  colors = scheme[Math.max(3, bands)], // an array of colors
} = {}) {
  // Compute values.
  const X = d3.map(data, x);
  const Y = d3.map(data, y);
  const Z = d3.map(data, z);
  console.log(Z)
  if (defined === undefined) defined = (d, i) => !isNaN(X[i]) && !isNaN(Y[i]);
  const D = d3.map(data, defined);
  console.log(D)

  // Compute default domains, and unique the z-domain.
  if (xDomain === undefined) xDomain = d3.extent(X);
  if (yDomain === undefined) yDomain = [0, d3.max(Y)];
  if (zDomain === undefined) zDomain = Z;
  console.log(yDomain)
  console.log(d3.max(Y))
  zDomain = new d3.InternSet(zDomain);
  console.log(X)
  // Omit any data not present in the z-domain.
  const I = d3.range(X.length).filter(i => zDomain.has(Z[i]));
  console.log(I)

  // Compute height.
  const height = zDomain.size * size + marginTop + marginBottom;

  // Construct scales and axes.
  const xScale = xType(xDomain, xRange);
  const yScale = yType(yDomain, yRange);
  const xAxis = d3.axisTop(xScale).ticks(width / 80).tickSizeOuter(0);
  
  // A unique identifier for clip paths (to avoid conflicts).
  const uid = `O-${Math.random().toString(16).slice(2)}`;

  // Construct an area generator.
  const area = d3.area()
      .defined(i => D[i])
      .curve(curve)
      .x(i => xScale(X[i]))
      .y0(yScale(0))
      .y1(i => yScale(Y[i]));
  
  const svg = d3.create("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto; height: intrinsic;")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10);
  console.log(d3.group(I, i => Z[i]))
  const g = svg.selectAll("g")
    .data(d3.group(I, i => Z[i]))
    .join("g")
      .attr("transform", (_, i) => `translate(0,${i * size + marginTop})`);

  const defs = g.append("defs");

  defs.append("clipPath")
      .attr("id", (_, i) => `${uid}-clip-${i}`)
    .append("rect")
      .attr("y", padding)
      .attr("width", width)
      .attr("height", size - padding);

  defs.append("path")
      .attr("id", (_, i) => `${uid}-path-${i}`)
      .attr("d", ([, I]) => area(I));

  g
    .attr("clip-path", (_, i) => `url(${new URL(`#${uid}-clip-${i}`, location)})`)
    .selectAll("use")
    .data((d, i) => new Array(bands).fill(i))
    .join("use")
      .attr("fill", (_, i) => colors[i + Math.max(0, 3 - bands)])
      .attr("transform", (_, i) => `translate(${textLength},${i * size})`)
      .attr("xlink:href", (i) => `${new URL(`#${uid}-path-${i}`, location)}`);

  g.append("text")
      .attr("x", marginLeft)
      .attr("y", (size + padding) / 2)
      .attr("dy", "0.35em")
      .text(([z]) => z);

  // Since there are normally no left or right margins, don’t show ticks that
  // are close to the edge of the chart, as these ticks are likely to be clipped.
  svg.append("g")
      .attr("transform", `translate(${textLength},${marginTop})`)
      .call(xAxis)
      .call(g => g.selectAll(".tick")
        .filter(d => xScale(d) < 10 || xScale(d) > width - 10)
        .remove())
      .call(g => g.select(".domain").remove());

  return svg.node();
}

function RoadSecSelected(fid) {
  let path = 'http://localhost:5000/TrafficSituationViewRespond';
  axios.post(path, {
    fid: fid
    })
    .then((res) => {
      console.log(res.data)
      let data = res.data.situation;
      let n = res.data.n;
      const chartContainer = d3.select("#horizon-chart-container");
      // get the height of the container
      const height = document.getElementById('traffic-situation-view').clientHeight;
      let size = height / n;
      const bands = 7;
      const color1 = "#4e7670"; 
      const color2 = "#bf4b56"; 

      const colorScale = d3.scaleLinear()
        .domain([0, 6])
        .range([color1, color2])
        .interpolate(d3.interpolateRgb);

      const colors = d3.range(7).map(colorScale);

      chartContainer.append(() => HorizonChart(data, {
        x: d => d[1],
        y: d => d[2],
        z: d => d[0],
        xType: d3.scaleLinear,
        marginLeft: 5,
        marginRight: 15,
        size,
        bands,
        colors,
        textLength: 150,
      }));
    })
    .catch((error) => {
      // eslint-disable-next-line
      console.error(error);
    }); 
}

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

.traffic-situation-view #horizon-chart-container {
  width: 100%;
  height: calc(100% - 20px);
}
</style>