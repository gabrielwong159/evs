import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const serverHost = 'https://api.evs.gabrielwong.dev';

export default new Vuex.Store({
  state: {
    balances: null,
    transactions: null,
    authenticated: false,
  },

  getters: {
    authenticated: state => state.authenticated,
  },

  actions: {
    login({ commit }, { username, password }) {
      let url = `${serverHost}/info`;

      let headers = { 'Content-Type': 'application/json' };
      let body = JSON.stringify({ username, password });

      return fetch(url, { method: 'POST', headers, body })
      .then(response => {
        if (response.ok) return response.json();
        else throw new Error();
      })
      .then(json => { commit('loginSuccess', json) });
    },
    logout({ commit }) {
      commit('logout');
    },

    demo({ commit }) {
      let url = `${serverHost}/info/demo`;
      return fetch(url)
      .then(response => response.json())
      .then(json => { commit('loginSuccess', json) });
    },
  },

  mutations: {
    loginSuccess(state, { balances, transactions }) {
      state.balances = balances;
      state.transactions = transactions;
      state.authenticated = true;
    },
    logout(state) {
      state.balances = null;
      state.transactions = null;
      state.authenticated = false;
    },
  },
});
