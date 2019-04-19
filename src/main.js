import Vue from 'vue'
import App from './App.vue'
import Message from './components/Message.vue'
import moment from 'moment'

Vue.config.productionTip = false

Vue.filter('formatDate', function (value) {
    if (value) {
        return moment(String(value)).format('DD.MM.YYYY HH:mm')
    }
});

new Vue({
    el: '#chat',
    components: [App],
    template: '<App/>',
    render: h => h(App)
});


// new Vue({
//    el: '#chat',
//   template: `
//     <div id="chat">
//         <message v-for="message in messages" v-bind:message="message" v-bind:key="message.count" v-bind:root="1"></message>
// 	</div>`,
//    components: { Message },
//     data: {
//         messages: chat.messages,
//         messages_by_count: chat.messages_by_count
//     },
//   render: h => h(App)
//  })
