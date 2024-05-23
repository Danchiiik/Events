// store.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: !!localStorage.getItem('accessToken'),
    userNickname: localStorage.getItem('userNickname') || ''
  },
  mutations: {
    setAuthentication(state, { isAuthenticated, userNickname }) {
      state.isAuthenticated = isAuthenticated;
      state.userNickname = userNickname;
    },
    logout(state) {
      state.isAuthenticated = false;
      state.userNickname = '';
    }
  },
  actions: {
    login({ commit }, { accessToken, refreshToken, userNickname }) {
      localStorage.setItem('accessToken', accessToken);
      localStorage.setItem('refreshToken', refreshToken);
      localStorage.setItem('userNickname', userNickname);
      commit('setAuthentication', { isAuthenticated: true, userNickname });
    },
    logout({ commit }) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('userNickname');
      commit('logout');
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    userNickname: state => state.userNickname
  },
  modules: {
    
  }

});
