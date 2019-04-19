Vue.filter('formatDate', function (value) {
    if (value) {
        return moment(String(value)).format('DD.MM.YYYY HH:mm')
    }
});
Vue.component('message', {
    props: ['message', 'root'],
    computed: {
        reply_to: function () {
            if (!this.message.reply_to) return []
            return this.message.reply_to.map(function (count) {
                return chat.messages_by_count[count]
            })
        }
    },

    template: `
    <div class="message">
        <div style="margin-left:100px">
        <message v-for="message in reply_to" v-bind:message="message" v-bind:key="message.count" v-if="root"></message>
        </div>
        {{ message.datetime|formatDate }} {{ message.count }} {{ message.ident }}
        <div class="header"><img v-bind:src="'/static/icons/countries/'+message.country.split('-')[0]+'.png'"><img v-if="message.country.indexOf('-') !== -1"
 v-bind:src="'/static/icons/countries/'+message.country+'.png'">{{ message.name }}</div>
        <div class="body">{{ message.body }}</div>
        <div v-if="message.file">
            <img v-bind:src="'/static/uploads/'+message.file">
        </div>
        <button @click="reply(message)">reply</button>
        <button @click="ignore(message)">ignore</button>
    </div>
  `,
    methods: {
        reply: function (message) {
            document.getElementById('body').value = '>>' + message.count;
        },
        ignore: function (message) {

        }
    },
})

var chat = new Vue({
    el: '#chat',
    data: {
        messages: [],
        messages_by_count: {}
    },
    computed: {}
});


document.addEventListener('DOMContentLoaded', function () {
    var ws = new ReconnectingWebSocket("ws://localhost:8888/ws");
    ws.onopen = function () {
        document.getElementById("loader").style.display = "none";
    };
    ws.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log(message)
        switch (message.type) {
            case 'message':
                chat.messages.push(message.data);
                chat.messages_by_count[message.data.count] = message.data;
                break;
            case 'delete':
                chat.messages.forEach(function (message, i) {
                    if (chat.messages[i].count == message.data.count) {
                        chat.messages.splice(i, 1);
                    }
                });
                delete chat.messages_by_count[message.data.count]
                break;
        }
    };

    ws.onclose = function () {
        document.getElementById("loader").style.display = "block";
    }

    var form = document.getElementById('post')
    var fileSelect = document.getElementById('file');

    form.onsubmit = function (event) {
        form.post.disabled = true
        event.preventDefault();
        var files = fileSelect.files;
        var formData = new FormData();
        var file = files[0];
        if (file) formData.append('file', file, file.name);
        formData.append('name', form.name.value)
        formData.append('body', form.body.value)
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/post', true);
        xhr.upload.onprogress = function (e) {
            var percentage = Math.round((e.loaded / e.total) * 100);
            console.log(percentage);
        }
        xhr.onload = function (e) {
            form.post.disabled = false
            if (xhr.status === 200) {
                // fine
            } else {
                alert('An error occurred!');
            }
        };
        xhr.send(formData);

    }

})