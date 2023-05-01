from flask import Flask, request
from flask_socketio import SocketIO, emit
from settings import *

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Models management
@socketio.on('new-model')
def model_new(data):
    IDModel = data.get('IDModel')
    emit('new-model', {'IDModel': IDModel}, broadcast=True, include_self=False)

@socketio.on('update-model')
def model_update(data):
    IDModel = data.get('IDModel')
    emit('update-model', {'IDModel': IDModel}, broadcast=True, include_self=False)

@socketio.on('delete-model')
def model_delete(data):
    emit('delete-model', data, broadcast=True, include_self=False)

# Textures management
@socketio.on('new-texture')
def texture_new(data):
    emit('new-texture', data, broadcast=True, include_self=False)

@socketio.on('delete-texture')
def texture_delete(data):
    emit('delete-texture', data, broadcast=True, include_self=False)

@socketio.on('texture-set-default')
def texture_set_default(data):
    emit('texture-set-default', data, broadcast=True, include_self=False)

# Locking
@socketio.on('lock-model')
def active_model(data):
    emit('lock-model', data, broadcast=True, include_self=False)

@socketio.on('unlock-model')
def deactivate_model(data):
    emit('unlock-model', data, broadcast=True, include_self=False)

# Active model selection
@socketio.on('set-active-model')
def set_active_model(data):
    IDModel = data.get('IDModel')
    textureID = data.get('IDTexture')
    emit('set-active-model', {'IDModel': IDModel, 'IDTexture': textureID}, broadcast=True, include_self=False)

@socketio.on('unset-active-model')
def unset_active_model():
    emit('unset-active-model', broadcast=True, include_self=False)

# Connection and disconnection management
def refresh():
    emit('refresh', broadcast=True, include_self=False)

@socketio.on('connect')
def connect():
    # When a new user connect refresh everything
    refresh()

@socketio.on('disconnect')
def disconnect():
    # When a new user disconnect refresh everything
    refresh()  

if __name__ == '__main__':
    socketio.run(app, port=9500, debug=True)