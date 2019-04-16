var chat = new Vue({
    el: '#chat',
    data: {
	    messages: [
		    {body:'test', name:'kot', country:'PL-77', 	country_name:'Poland', count:1, date:"2019-04-09T00:48:58.000Z"},
            {body:'test', name:'kot', country:'PL-77', 	country_name:'Poland', count:1, date:"2019-04-09T00:48:58.000Z"},
	    ]
    },
    computed: {
        messages_full: function(){
            this.messages.forEach(function(message, index) {
                message.country_icon = '/static/icons/countries/'+message.country.split('-')[0]+'.png';
                message.region_icon = '/static/icons/countries/'+message.country+'.png';
            })
        }
    }
});
window.onload = function() {
    var ws = new WebSocket("ws://localhost:8888/ws");
    ws.onopen = function () {
        // Web Socket is connected, send data using send()
        // ws.send("Message to send");
        // alert("Message is sent...");
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
    ws.send(JSON.stringify({
  body: "aaaa"
}));

}