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

})
