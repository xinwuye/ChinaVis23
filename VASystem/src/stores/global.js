import { defineStore } from 'pinia'
import * as d3 from 'd3'

export const useGlobalStore = defineStore('global', {
  state: () => ({
    clickedFid: null, // fid of clicked road segment in map
    clickedId: null, // id of clicked object in map
    selectedData: null, // 1, 2, or 3 
  }),

  actions: {
  },

  getters: {

  }
})