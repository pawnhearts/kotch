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
    computed: {}
});
var ws;
window.onload = function () {
    ws = new ReconnectingWebSocket("ws://localhost:8888/ws");
    ws.onopen = function () {
        // Web Socket is connected, send data using send()
        // ws.send("Message to send");
        // alert("Message is sent...");
        ws.send(JSON.stringify({
            body: "aaaa"
        }));
    };
    ws.onmessage = function (event) {
        var message = JSON.parse(event.data);
        console.log(message)
        if (message.type == 'message') {
            chat.messages.push(message.data);
        }
    };

    ws.onclose = function () {

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

}

function post(form) {
    var data = {body: form.body.value, name: form.name.value};
    console.log(data);
    Vueajax.post("/post", data, {
        fileInputs: [
            document.getElementById("file")
        ]
    });
    return false;
}

function uploadFile(files) {

        file = document.getElementById('file').files[0]
        var reader = new FileReader()
        var rawData = new ArrayBuffer();
        reader.onloadend = function (e) {
            rawData = e.target.result;

            var data = { body:'aa',name:'aa', file: rawData}
            console.log(data)
            ws.send(JSON.stringify(data))
        }
        reader.readAsArrayBuffer(file);
}
