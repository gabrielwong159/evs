<template>
  <div id="usage">
    <h1 class="mb-3">Usage</h1>

    <v-btn-toggle mandatory id="toggleDates">
      <v-btn flat @click="plotMonth()">Past Month</v-btn>
      <v-btn flat @click="plotWeek()">Past Week</v-btn>
      <v-btn flat @click="plotAll()">All</v-btn>
    </v-btn-toggle>

    <v-container grid-list-md>
      <v-layout row>
        <v-flex xs12>
          <v-container elevation-2 class="chartContainer">
            <canvas id="usageTimeSeries" />
          </v-container>
        </v-flex>
      </v-layout>

      <v-layout row v-bind="binding">
        <v-flex xs8>
          <v-container elevation-2 class="chartContainer">
            <canvas id="usageHist"></canvas>
          </v-container>
        </v-flex>
        <v-flex xs4>
          <v-container elevation-2 class="chartContainer">
            <canvas id="usagePie"></canvas>
          </v-container>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import {
  getPastWeekBalances,
  getPastMonthBalances,
  separateBalanceTuples,
} from './utils/data.js';
import { usageTimeSeries, usagePie, usageHist } from './utils/plots.js';

export default {
  name: 'Usage',
  data() {
    return {
      charts: [],
    };
  },
  computed: {
    ...mapState(['balances']),
    binding() {
      let binding = {};
      if (this.$vuetify.breakpoint.xs) binding.column = true;
      return binding;
    }
  },

  methods: {
    plot(balances) {
      this.destroyExistingCharts();

      let { dates, amounts } = separateBalanceTuples(balances);
      let timeSeriesChart = usageTimeSeries('usageTimeSeries', dates, amounts);
      let usagePieChart = usagePie('usagePie', dates, amounts);
      let usageHistChart = usageHist('usageHist', dates, amounts);

      this.charts = [
        timeSeriesChart,
        usagePieChart,
        usageHistChart,
      ];
    },

    plotAll() {
      this.plot(this.balances);
    },
    plotMonth() {
      let filteredBalances = getPastMonthBalances(this.balances);
      this.plot(filteredBalances);
    },
    plotWeek() {
      let filteredBalances = getPastWeekBalances(this.balances);
      this.plot(filteredBalances);
    },
    
    destroyExistingCharts() {
      // remove existing charts, otherwise new charts will simply overlap
      for (let chart of this.charts) chart.destroy();
    },
  },

  mounted() {
    // necessary to allow re-plotting when re-navigated to
    if (this.balances) this.plotMonth();
  },

  watch: {
    balances: function() {
      // plot when updated with data from async fetch
      this.plotMonth();
    },
    binding: function() {
      this.plotMonth();
    },
  },
}
</script>

<style scoped>
#usage {
  height: 100%;
  width: 70%;
  margin: auto;
  padding-top: 60px;
}

.chartContainer {
  height: 100%;
  background-color: white;
}
</style>
