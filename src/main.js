import Vue from 'vue'
import Vuex from 'vuex'
import VueNativeSock from 'vue-native-websocket'
import App from './App.vue'
import moment from 'moment'

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    messages: [],
      messages_by_count: {},
      socket: {
      isConnected: false,
      message: '',
      reconnectError: false,
    }
  },
  getters: {
      messages: state => state.messages,
      messages_by_count: state => state.messages_by_count,
      isConnected: state => state.socket.isConnected,
  },
  mutations: {
    addMessage: (state, payload) => {
      state.messages.push(payload);
      state.messages_by_count[payload.count] = payload;
    },
    deleteMessage: (state, payload) => {
      const index = state.messages.findIndex(t => t.count === payload);
      if(index !== -1) {
          state.messages.splice(index, 1);
          delete state.messages_by_count[payload];
      }
    },
    SOCKET_ONOPEN (state, event)  {
      Vue.prototype.$socket = event.currentTarget
      state.socket.isConnected = true
    },
    SOCKET_ONCLOSE (state, event)  {
      state.socket.isConnected = false
    },
    SOCKET_ONERROR (state, event)  {
      console.error(state, event)
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE (state, message)  {
      state.socket.message = message;
      switch (message.type) {
          case 'message':
              state.messages.push(message.data);
              state.messages_by_count[message.data.count] = message.data;
              break
          case 'delete':
              const index = state.messages.findIndex(t => t.count === message.data.count);
              if (index !== -1) {
                  state.messages.splice(index, 1);
                  delete state.messages_by_count[message.data.count];
              }
              break
      }
    },
    SOCKET_RECONNECT(state, count) {
      console.info(state, count)
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true;
    },
  }
})

Vue.use(VueNativeSock, 'ws://localhost:8888/ws', { store: store, format: 'json', reconnection: true })

Vue.config.productionTip = false

Vue.filter('formatDate', function (value) {
    if (value) {
        return moment(String(value)).format('DD.MM.YYYY HH:mm')
    }
});

Vue.filter('fileSize', function (num) {
  // jacked from: https://github.com/sindresorhus/pretty-bytes
  if (typeof num !== 'number' || isNaN(num)) {
    throw new TypeError('Expected a number');
  }

  var exponent;
  var unit;
  var neg = num < 0;
  var units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];

  if (neg) {
    num = -num;
  }

  if (num < 1) {
    return (neg ? '-' : '') + num + ' B';
  }

  exponent = Math.min(Math.floor(Math.log(num) / Math.log(1000)), units.length - 1);
  num = (num / Math.pow(1000, exponent)).toFixed(2) * 1;
  unit = units[exponent];

  return (neg ? '-' : '') + num + ' ' + unit;
});

window.vm = new Vue({
    el: '#body',
    components: {App},
    render: h => h(App),
    store: store,
    computed: {
        messages: function() {
            return this.$store.getters.messages;
        }
    },
    methods: {
        addMessage: function(message) {
            this.$store.commit('addMessage', message)
        }
    }
});