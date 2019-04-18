var chat = new Vue({
    el: '#chat',
    data: {
        messages: [
            {
                body: 'test',
                name: 'kot',
                country: 'PL-77',
                country_name: 'Poland',
                count: 1,
                date: "2019-04-09T00:48:58.000Z"
            },
            {
                body: 'test',
                name: 'kot',
                country: 'PL-77',
                country_name: 'Poland',
                count: 1,
                date: "2019-04-09T00:48:58.000Z"
            },
            {
                body: 'test',
                name: 'kot',
                country: 'RU',
                country_name: 'Poland',
                count: 1,
                date: "2019-04-09T00:48:58.000Z"
            },
        ]
    },
    computed: {},
    methods: {
        reply: function(message) {
            document.getElementById('body').value = '>>'+message.count;
        },
        ignore: function(message) {

        },
    },
    filters: {
        formatDate: function(value) {
          if (value) {
            return moment(String(value)).format('MM/DD/YYYY hh:mm')
          }
        }
    }
});


document.addEventListener('DOMContentLoaded', function(){
    var ws = new ReconnectingWebSocket("ws://localhost:8888/ws");
    ws.onopen = function () {
        document.getElementById("loader").style.display = "none";
    };
    ws.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log(message)
        switch(message.type) {
            case 'message':
                chat.messages.push(message.data);
                break;
            case 'delete':
                chat.messages.forEach(function(message, i) {
                   if(chat.messages[i].count == message.data.count) {
                        chat.messages.splice(i, 1);
                    }
                });
                break;
        }
    };

    ws.onclose = function () {
        document.getElementById("loader").style.display = "block";
    }

    var form = document.getElementById('post')
    var fileSelect = document.getElementById('file');

    form.onsubmit = function (event) {
        form.post.disabled=true
        event.preventDefault();
        var files = fileSelect.files;
        var formData = new FormData();
        var file = files[0];
        if(file) formData.append('file', file, file.name);
        formData.append('name', form.name.value)
        formData.append('body', form.body.value)
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/post', true);
        xhr.upload.onprogress = function (e) {
            var percentage = Math.round((e.loaded / e.total) * 100);
            console.log(percentage);
        }
        xhr.onload = function (e) {
            form.post.disabled=false
            if (xhr.status === 200) {
                // fine
            } else {
                alert('An error occurred!');
            }
        };
        xhr.send(formData);

    }

})