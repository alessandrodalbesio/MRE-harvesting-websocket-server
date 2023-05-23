import json
import asyncio
import websockets

connected_clients = set()

async def handle_message(message, websocket):
    message_data = json.loads(message)
    message_type = message_data.get('type')

    if message_type == 'new-model':
        IDModel = message_data.get('data').get('IDModel')
        await broadcast_message({'type': 'new-model', 'data': {'IDModel': IDModel}}, exclude=[websocket])
    elif message_type == 'update-model':
        IDModel = message_data.get('data').get('IDModel')
        await broadcast_message({'type': 'update-model', 'data': {'IDModel': IDModel}}, exclude=[websocket])
    elif message_type == 'delete-model':
        await broadcast_message({'type': 'delete-model', 'data': message_data.get('data')}, exclude=[websocket])
    elif message_type == 'new-texture':
        await broadcast_message({'type': 'new-texture', 'data': message_data.get('data')}, exclude=[websocket])
    elif message_type == 'delete-texture':
        await broadcast_message({'type': 'delete-texture', 'data': message_data.get('data')}, exclude=[websocket])
    elif message_type == 'texture-set-default':
        await broadcast_message({'type': 'texture-set-default', 'data': message_data.get('data')}, exclude=[websocket])
    elif message_type == 'lock-model':
        await broadcast_message({'type': 'lock-model', 'data': message_data.get('data')}, exclude=[websocket])
    elif message_type == 'unlock-model':
        await broadcast_message({'type': 'unlock-model', 'data': message_data.get('data')}, exclude=[websocket])
    elif message_type == 'set-active-model':
        IDModel = message_data.get('data').get('IDModel')
        IDTexture = message_data.get('data').get('IDTexture')
        await broadcast_message({'type': 'set-active-model', 'data': {'IDModel': IDModel, 'IDTexture': IDTexture}}, exclude=[websocket])
    elif message_type == 'unset-active-model':
        await broadcast_message({'type': 'unset-active-model'}, exclude=[websocket])

async def broadcast_message(message, exclude=None):
    for client in connected_clients:
        if client != exclude:
            await client.send(json.dumps(message))

async def handle_websocket(websocket, path):
    connected_clients.add(websocket)
    try:
        while True:
            message = await websocket.recv()
            if message is not None:
                await handle_message(message, websocket)
    finally:
        connected_clients.remove(websocket)

async def refresh():
    await broadcast_message({'type': 'refresh'})

async def start_server():
    server = await websockets.serve(handle_websocket, 'localhost', 9500)
    print("WebSocket server started...")
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(start_server())