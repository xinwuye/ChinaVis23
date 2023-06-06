<template>
  <div
      id="traffic-situation-view"
      class="traffic-situation-view"
      style="borderRadius: small"
  >
    <div class="toolbar">
      <span class="toolbar-text">交通态势视图</span>
    </div>
    <div id="horizon-chart-container" style="width: 100%;height:100%;" />
  </div>
</template>

<script lang="ts" setup>
import {onMounted, ref} from 'vue';
import * as d3 from 'd3';
import * as echarts from 'echarts'; // use canvas to render
import axios from 'axios';
import { horizonChart } from 'd3-horizon-chart';

onMounted(() => {
  // const heatmapContainer = document.getElementById('traffic-situation-view');

  // const containerHeight = heatmapContainer.clientHeight;
  // const containerWidth = heatmapContainer.clientWidth;
  // // set the dimensions and margins of the graph
  // const margin = {top: 30, right: 30, bottom: 30, left: 30},
  //   width = containerHeight - margin.left - margin.right,
  //   height = containerWidth - margin.top - margin.bottom;

  // let path = 'http://localhost:5000/TrafficSituationViewInit';
  // axios.post(path)
  //   .then((res) => {
  //     console.log(res.data)
  //   })
  //   .catch((error) => {
  //     // eslint-disable-next-line
  //     console.error(error);
  //   }); 




  // function loadStockData(stock, callback) {
  //     d3.csv('https://bost.ocks.org/mike/cubism/intro/stocks/' + stock + '.csv').then(function(rows) {
  //         rows = rows.map(function(d) {
  //               return [d3.timeParse(d.Date), +d.Open];
  //           }).filter(function(d) {
  //               return d[1];
  //           }).reverse();
        
  //         // console.log(rows)

  //         var date = rows[0][0],
  //             compare = rows[400][1],
  //             value = rows[0][1],
  //             values = [];

  //         rows.forEach(function(d, i ) {
  //             values.push(value = (d[1] - compare) / compare);
  //         });

  //         callback(null, {
  //             'stock': stock,
  //             'values': values
  //         });
  //     });
  // }

  // const symbols = ['AAPL', 'BIDU', 'SINA', 'GOOG', 'MSFT', 'YHOO', 'ADBE', 'REDF', 'INSP', 'IACI', 'AVID', 'CCUR', 'DELL', 'DGII', 'HPQ', 'SGI', 'SMCI', 'SNDK', 'SYNA'];
  // // const promises = symbols.map(stock => loadStockData(stock));
  // const promises = symbols.map(stock => new Promise((resolve, reject) => {
  //   loadStockData(stock, function(error, stockData) {
  //     if (error) {
  //       reject(error);
  //     } else {
  //       resolve(stockData);
  //     }
  //   });
  // }));

  // Promise.all(promises)
  //   .then(stocks => {
  //     console.log(stocks)
  //     d3.select('#horizon-chart-container').selectAll('.horizon')
  //       .data(stocks)
  //       .enter()
  //       .append('div')
  //       .attr('class', 'horizon')
  //       // .style('height', '20px')  // Set the desired height
  //       // .style('width', '100px')
  //       .each(function(d) {
  //         horizonChart()
  //           .height(10)
  //           // .width(100)
  //           .title(d.stock)
  //           .call(this, d.values);
  //       });
  //   })
  //   .catch(error => {
  //     throw error;
  //   });


  const data = [
  { name: "Von der Heydt", date: new Date("2016-01-04"), value: 163 },
  { name: "Kirschheck", date: new Date("2016-01-04"), value: 170 },
  { name: "Saarbrücken-Neuhaus", date: new Date("2016-01-04"), value: 94 },
  { name: "Riegelsberg", date: new Date("2016-01-04"), value: 137 },
  { name: "Holz", date: new Date("2016-01-04"), value: 112 },
  { name: "Göttelborn", date: new Date("2016-01-04"), value: 124 },
  // { name: "Illingen", date: new Date("2016-01-04"), value: 194 },
  // { name: "AS Eppelborn", date: new Date("2016-01-04"), value: 158 },
  // { name: "Hasborn", date: new Date("2016-01-04"), value: 153 },
  // { name: "Kastel", date: new Date("2016-01-04"), value: 134 },
  // { name: "Otzenhausen", date: new Date("2016-01-04"), value: 138 },
  // { name: "Bierfeld", date: new Date("2016-01-04"), value: 220 },
  // { name: "Nonnweiler", date: new Date("2016-01-04"), value: 228 },
  // { name: "Hetzerath", date: new Date("2016-01-04"), value: 326 },
  // { name: "Laufeld", date: new Date("2016-01-04"), value: 222 },
  // { name: "Nettersheim", date: new Date("2016-01-04"), value: 220 },
  // { name: "Euskirchen/Bliesheim", date: new Date("2016-01-04"), value: 440 },
  // { name: "Hürth", date: new Date("2016-01-04"), value: 497 },
  // { name: "Köln-Nord", date: new Date("2016-01-04"), value: 1193 },
  // { name: "Schloss Burg", date: new Date("2016-01-04"), value: 1421 },
  // { name: "Hagen-Vorhalle", date: new Date("2016-01-04"), value: 1701 },
  // { name: "Hengsen", date: new Date("2016-01-04"), value: 2114 },
  // { name: "Unna", date: new Date("2016-01-04"), value: 2035 },
  // { name: "Ascheberg", date: new Date("2016-01-04"), value: 797 },
  // { name: "Ladbergen", date: new Date("2016-01-04"), value: 916 },
  // { name: "Lotte", date: new Date("2016-01-04"), value: 1006 },
  // { name: "HB-Silbersee", date: new Date("2016-01-04"), value: 1378 },
  // { name: "HB-Weserbrücke", date: new Date("2016-01-04"), value: 1520 },
  // { name: "HB-Mahndorfer See", date: new Date("2016-01-04"), value: 1434 },
  // { name: "Groß Ippener", date: new Date("2016-01-04"), value: 839 },
  // { name: "Uphusen", date: new Date("2016-01-04"), value: 1450 },
  // { name: "Bockel", date: new Date("2016-01-04"), value: 1062 },
  // { name: "Dibbersen", date: new Date("2016-01-04"), value: 823 },
  // { name: "Glüsingen", date: new Date("2016-01-04"), value: 1222 },
  // { name: "Barsbüttel", date: new Date("2016-01-04"), value: 1278 },
  // { name: "Bad Schwartau", date: new Date("2016-01-04"), value: 669 },
  // { name: "Oldenburg (Holstein)", date: new Date("2016-01-04"), value: 126 },
  // { name: "Neustadt i. H.-Süd", date: new Date("2016-01-04"), value: 158 },
  // { name: "Von der Heydt", date: new Date("2016-01-04T01:00Z"), value: 89 },
  // { name: "Kirschheck", date: new Date("2016-01-04T01:00Z"), value: 102 },
  // { name: "Saarbrücken-Neuhaus", date: new Date("2016-01-04T01:00Z"), value: 45 },
  // { name: "Riegelsberg", date: new Date("2016-01-04T01:00Z"), value: 70 },
  // { name: "Holz", date: new Date("2016-01-04T01:00Z"), value: 60 },
  // { name: "Göttelborn", date: new Date("2016-01-04T01:00Z"), value: 64 },
  // { name: "Illingen", date: new Date("2016-01-04T01:00Z"), value: 102 },
  // { name: "AS Eppelborn", date: new Date("2016-01-04T01:00Z"), value: 85 },
  // { name: "Hasborn", date: new Date("2016-01-04T01:00Z"), value: 96 },
  // { name: "Kastel", date: new Date("2016-01-04T01:00Z"), value: 85 },
  // { name: "Otzenhausen", date: new Date("2016-01-04T01:00Z"), value: 89 },
  // { name: "Bierfeld", date: new Date("2016-01-04T01:00Z"), value: 125 },
  // { name: "Nonnweiler", date: new Date("2016-01-04T01:00Z"), value: 129 },
  { name: "Hetzerath", date: new Date("2016-01-04T01:00Z"), value: 171 },]

  const chartContainer = d3.select("#horizon-chart-container");
  chartContainer.append(() => HorizonChart(data, {
    x: d => d.date,
    y: d => d.value,
    z: d => d.name
  }));


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
    xRange = [marginLeft, width - marginRight], // [left, right]
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
    if (defined === undefined) defined = (d, i) => !isNaN(X[i]) && !isNaN(Y[i]);
    const D = d3.map(data, defined);

    // Compute default domains, and unique the z-domain.
    if (xDomain === undefined) xDomain = d3.extent(X);
    if (yDomain === undefined) yDomain = [0, d3.max(Y)];
    if (zDomain === undefined) zDomain = Z;
    zDomain = new d3.InternSet(zDomain);

    // Omit any data not present in the z-domain.
    const I = d3.range(X.length).filter(i => zDomain.has(Z[i]));

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
        .attr("transform", (_, i) => `translate(0,${i * size})`)
        .attr("xlink:href", (i) => `${new URL(`#${uid}-path-${i}`, location)}`);

    g.append("text")
        .attr("x", marginLeft)
        .attr("y", (size + padding) / 2)
        .attr("dy", "0.35em")
        .text(([z]) => z);

    // Since there are normally no left or right margins, don’t show ticks that
    // are close to the edge of the chart, as these ticks are likely to be clipped.
    svg.append("g")
        .attr("transform", `translate(0,${marginTop})`)
        .call(xAxis)
        .call(g => g.selectAll(".tick")
          .filter(d => xScale(d) < 10 || xScale(d) > width - 10)
          .remove())
        .call(g => g.select(".domain").remove());

    return svg.node();
  }

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