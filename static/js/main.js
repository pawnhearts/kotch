var chat = {messages:[], messages_by_count:{}}
document.addEventListener('DOMContentLoaded', function () {
    var ws = new ReconnectingWebSocket("ws://localhost:8888/ws");
    ws.onopen = function () {
        document.getElementById("loader").style.display = "none";
    };
    ws.onmessage = function (event) {
        var message = JSON.parse(event.data);
        switch (message.type) {
            case 'message':
                console.log(message.data)
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
        formData.append('reply_to', form.reply_to.value)
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
            } else if(xhr.status === 400){
                var data = JSON.parse(xhr.responseText)
                alert(JSON.stringify(data.error))
            } else {
                alert(e);
            }
        };
        xhr.send(formData);
        vm.$emit('replying')
    }

})
