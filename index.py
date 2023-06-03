# Import all the required modules
from modules.logging import *
from modules.settings import *
import json
import asyncio
import websockets
import traceback

# Create the sets for the connected clients
connected_clients = set()
optitrack_clients = set()

# Create the logger
websocket_logger = logger()

num_errors = 0

# Function to handle the messages that are sent to the websocket server
async def handle_message(message, websocket):
    message = json.loads(message)
    type = message.get('type')
    data = message.get('data')

    if type == 'ping': # Manage ping messages
        await send_message({'type': 'pong'}, websocket)
    elif type == 'optitrack-data': # Manage optitrack data messages
        await broadcast_message_to_optitrack_clients({'type': 'optitrack-data', 'data': data})
    elif type == 'join-optitrack-room': # Join the optitrack room
        optitrack_clients.add(websocket)
        websocket_logger.debug("Optitrack client joined")
    elif type == 'leave-optitrack-room': # Leave the optitrack room
        optitrack_clients.remove(websocket)
        websocket_logger.debug("Optitrack client left")
    elif type in valid_messages_type:
        await broadcast_message(message, websocket)
    else:
        return

# Broadcast a message to all the connected users
async def broadcast_message(message, exclude=None):
    for client in connected_clients:
        if client != exclude:
            await client.send(json.dumps(message))

# Broadcast a message only to the connected users who are in the optitrack_clients set
async def broadcast_message_to_optitrack_clients(message):
    for client in connected_clients:
        if client in optitrack_clients:
            await client.send(json.dumps(message))

# Send a message to a specific user
async def send_message(message, websocket):
    await websocket.send(json.dumps(message))

# Function to handle the websocket connection
async def handle_websocket(websocket, path):
    websocket_logger.debug("New client connected")
    connected_clients.add(websocket)
    while True:
        try: 
            message = await websocket.recv()
            if message is not None:
                await handle_message(message, websocket)
        except websockets.exceptions.ConnectionClosedError:
            break
        except websockets.exceptions.ConnectionClosedOK:
            break
        except Exception as e:
            if num_errors > LIMIT_EXCEPTIONS_BEFORE_RESTART:
                raise("Too many errors, restarting the websocket server")
            num_errors += 1
            websocket_logger.error(str(traceback.format_exc()))
    connected_clients.remove(websocket)
    if(websocket in optitrack_clients):
        optitrack_clients.remove(websocket)
    websocket_logger.debug("Client disconnected")
    

# Function to start the websocket server
async def start_server():
    async with websockets.serve(handle_websocket, WEBSOCKET_SERVER_ADDRESS, WEBSOCKET_SERVER_PORT):
        await asyncio.Future() # Keep the server running

if __name__ == '__main__':
    try:
        websocket_logger.info("Websocket server started")
        asyncio.run(start_server()) # Start the websocket server
    except KeyboardInterrupt:
        websocket_logger.info("Websocket server stopped")
    except Exception as e:
        websocket_logger.error(str(traceback.format_exc()))
