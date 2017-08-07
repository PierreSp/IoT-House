from app import socketio
from flask_socketio import send


@socketio.on('client_connected')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))
    send('message')


@socketio.on('message')
def handle_submit_button(json):
    # it will forward the json to all clients.
    send(json, json=True)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
