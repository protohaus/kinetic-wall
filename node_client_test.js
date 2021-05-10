#!/usr/bin/env node

var WebSocketClient = require('websocket').client;

var client = new WebSocketClient();

client.on('connectFailed', function(error) {
    console.log('Connect Error: ' + error.toString());
});

client.on('connect', function(connection) {
    console.log('WebSocket Client Connected');
    connection.on('error', function(error) {
        console.log("Connection Error: " + error.toString());
    });
    connection.on('close', function() {
        console.log('echo-protocol Connection Closed');
    });
    connection.on('message', function(message) {
        if (message.type === 'utf8') {
            console.log("Received: '" + message.utf8Data + "'");
        }
    });

    function sendNumber() {
        if (connection.connected) {
//            connection.sendUTF('{"mode": "wave", "frequency_hz": 2}');
            connection.sendUTF('{"mode": "pwm", "frequency_hz": 1, "duty_cycle": 0.2}')
        }
    }
    sendNumber();
    connection.close()
});

client.connect('ws://192.168.0.34:9876')
