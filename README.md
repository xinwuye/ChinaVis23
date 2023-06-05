# ChinaVis23

## 系统使用

```
git clone https://github.com/tz1010647987/ChinaVis23.git
cd ChinaVis23/VASystem
npm i
npm run dev
```

## 最终报告
最终报告的腾讯文档在微信群

## 技术栈
### 前端：

JavaScript/TypeScript

Vue 3：前端框架，API （强烈）建议Preference选择Composition

Pinia：状态管理

Vite：脚手架，（强烈）建议不要使用Vue CLI，可能出现不兼容

Element Plus: UI框架

Axios库：HTTP库

### 数据可视化库：

D3.js

Echarts

其他

（对于某些成熟的可视化类型建议使用更高封装的库）

### 后端：

Python

Flask：轻量级的Python Web框架，用于构建后端API

因为这个项目数据集是给定的，只需要在将预处理好的数据保存供后端调用处理即可，预处理阶段使用任意方便的技术。

系统后端建议使用的可能用到的技术：NumPy, Pandas, PyTorch, NetworkX

### 数据库：

无

## 进度

### 数据预处理

- K-means识别出的高价值场景（高价值场景，已完成）
- 基于规则识别的高价值场景（高价值场景，已完成）
- 车辆驾驶画像指标：均速、极速、速度标准差、0-10，10-20,20-30,>30m/s速度的时间占比，平均加速度，加速度标准差（车辆驾驶画像，已完成）
- 急加速、急减速（车辆驾驶画像，高价值场景，已完成）
- 压线、变道识别（高价值场景、车辆驾驶画像、交通态势，已完成）
- 以路段为节点的图数据建模（交通态势，已完成）
- 基于TGC-LSTM的预测和分析（交通态势，已完成）

### 可视分析系统

#### 控制面板（进行中）
- 选择数据集等
#### 地图视图（进行中）
- 基于数据处理得到的高价值场景对应的对象，通过将对象用不同的颜色或形状表示，对应1. 高价值场景可视分析中的（1）高价值场景挖掘
- 地图画出道路，对象用小点表示，对应1. 高价值场景可视分析中的（2）场景还原
- 通过对路段使用不同颜色，对应3. 交通态势可视分析
- 支持点击对象然后在用户画像视图显示用户画像的功能
- 支持点击路段然后在交通态势分析视图显示交通态势的功能
#### 用户画像视图（进行中）
- 对主视图的点击操作进行响应
- 对每个用户画像的有序变量指标用雷达图显示，无序变量指标用其他形式可视化
- 每个用户的时序数据（如速度），参考https://browser.timeviz.net/ ，或问高琳，一个能够在一张图中呈现所有时序的可视化是比较理想的
#### 交通态势视图（进行中）
- 对主视图的点击操作进行响应
- 衡量交通态势的时序数据（排队车辆统计、断面车流统计、群体性驾驶行为变化趋势、道路运行健康度、拥堵程度）可视化
- 车辆热力图可视化
#### 其他
暂无
