from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


# Needed for the polling from the headset
# No locking mechanism needed as the value is only read
activeModel = { 'IDModel': None, 'IDTexture': None }
needRefreshDB = False


# Models management
@socketio.on('new-model')
def model_new(data):
    global needRefreshDB
    needRefreshDB = True
    IDModel = data.get('IDModel')
    
    emit('new-model', {'IDModel': IDModel}, broadcast=True, include_self=False)

@socketio.on('update-model')
def model_update(data):
    global needRefreshDB
    needRefreshDB = True
    IDModel = data.get('IDModel')

    emit('update-model', {'IDModel': IDModel}, broadcast=True, include_self=False)

@socketio.on('delete-model')
def model_delete(data):
    global needRefreshDB
    needRefreshDB = True

    emit('delete-model', data, broadcast=True, include_self=False)

# Textures management
@socketio.on('new-texture')
def texture_new(data):
    global needRefreshDB
    needRefreshDB = True

    emit('new-texture', data, broadcast=True, include_self=False)

@socketio.on('delete-texture')
def texture_delete(data):
    global needRefreshDB
    needRefreshDB = True

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
    global activeModel
    activeModel['IDModel'] = data.get('IDModel')
    activeModel['IDTexture'] = data.get('IDTexture')

    emit('set-active-model', {'IDModel': activeModel['IDModel'], 'IDTexture': activeModel['IDTexture']}, broadcast=True, include_self=False)

@socketio.on('unset-active-model')
def unset_active_model():
    global activeModel
    activeModel['IDModel'] = None
    activeModel['IDTexture'] = None

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

# Only for headset
@app.get('/active-model') 
def getActiveModel():
    global activeModel
    return jsonify(activeModel), 200

@app.get('/need-local-database-refresh')
def needLocalDatabaseRefresh():
    global needRefreshDB
    toReturnValue = needRefreshDB
    if toReturnValue:
        needRefreshDB = False
    return jsonify({
        'needLocalDBRefresh': toReturnValue
    }), 200

if __name__ == '__main__':
    socketio.run(app, port=9500, debug=False)