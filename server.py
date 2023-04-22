from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from settings import *
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Variables to keep track of the connections with the clients
# Only one client, headset and position estimator can be connected at the same time
num_client_connected = 0
num_headset_connected = 0
num_position_estimator_connected = 0

# Update the headsets when a model or texture is created, updated or deleted
app.post('/model_created')
def handle_model_updated(data):
    socketio.emit('model_created', data, room=HEADSETS_DEFAULT_ROOM)

app.post('/model_updated')
def handle_model_updated(data):
    socketio.emit('model_updated', data, room=HEADSETS_DEFAULT_ROOM)

app.post('/model_deleted')
def handle_model_deleted(data):
    socketio.emit('model_deleted', data, room=HEADSETS_DEFAULT_ROOM)

app.post('/texture_created')
def handle_texture_created(data):
    socketio.emit('texture_created', data, room=HEADSETS_DEFAULT_ROOM)

app.post('/texture_deleted')
def handle_texture_deleted(data):
    socketio.emit('texture_deleted', data, room=HEADSETS_DEFAULT_ROOM)


# Routes for the communications with the clients
@socketio.on('model_texture_selected')
def handle_model_texture_selected(data):
    emit('model_texture_selected', data, room=SELECTION_ROOM)

@socketio.on('model_texture_deselected')
def handle_model_texture_deselected(data):
    emit('model_texture_deselected', data, room=SELECTION_ROOM)


# Routes for the connection with the socket
@socketio.on('connect')
def handle_connect(data):
    if data['type'] == 'client':
        if clients_connected >= MAX_NUM_CLIENTS_CONNECTED:
            emit(json({'status': 'error', 'message': 'There is already a client connected'}))
        clients_connected += 1
        for room in CLIENTS_ROOM:
            join_room(room)
    elif data['type'] == 'headset':
        if headset_connected >= MAX_NUM_HEADSETS_CONNECTED:
            emit(json({'status': 'error', 'message': 'There is already a headset connected'}))
        headset_connected += 1
        for room in HEADSETS_ROOM:
            join_room(room)
    elif data['type'] == 'position_estimator':
        if position_estimator_connected >= MAX_NUM_POSITION_ESTIMATORS_CONNECTED:
            emit(json({'status': 'error', 'message': 'There is already a position estimator connected'}))
        position_estimator_connected += 1
        for room in POSITION_ESTIMATORS_ROOM:
            join_room(room)
    else:
        emit(json({'status': 'error', 'message': 'Unknown type'}))

@socketio.on('disconnect')
def handle_disconnect(data):
    if data['type'] == 'client':
        clients_connected -= 1
    if data['type'] == 'headset':
        headset_connected -= 1
    if data['type'] == 'position_estimator':
        position_estimator_connected -= 1

if __name__ == '__main__':
    socketio.run(app)