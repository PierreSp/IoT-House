socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on('connect', function() {
  socket.emit('client_connected', {data: 'New client!'});
});

socket.on('message', function (data) {
  console.log('message form backend ' + data);
});

function json_button() {
  socket.send('{"message": "test"}');
}

