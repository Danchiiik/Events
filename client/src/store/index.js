// store.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: !!localStorage.getItem('accessToken'),
    userNickname: localStorage.getItem('userNickname') || '',
    currentUserId: localStorage.getItem('currentUserId')
  },
  mutations: {
    setAuthentication(state, { isAuthenticated, userNickname, currentUserId }) {
      state.isAuthenticated = isAuthenticated;
      state.userNickname = userNickname;
      state.currentUserId = currentUserId
    },
    logout(state) {
      state.isAuthenticated = false;
      state.userNickname = '';
      state.currentUserId = null;
    }
  },
  actions: {
    login({ commit }, { accessToken, refreshToken, userNickname, currentUserId }) {
      localStorage.setItem('accessToken', accessToken);
      localStorage.setItem('refreshToken', refreshToken);
      localStorage.setItem('userNickname', userNickname);
      localStorage.setItem('currentUserId', currentUserId)
      commit('setAuthentication', { isAuthenticated: true, userNickname, currentUserId });
    },
    logout({ commit }) {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('userNickname');
      localStorage.removeItem('currentUserId');
      commit('logout');
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    userNickname: state => state.userNickname,
    currentUserId: state => state.currentUserId,
  },
  modules: {
 
  }

});

