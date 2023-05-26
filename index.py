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

# Managed messages from the server (not related to optitrack)
valid_messages_type = ['new-model', 'update-model', 'delete-model', 'new-texture', 'delete-texture', 'texture-set-default', 'lock-model', 'unlock-model', 'set-active-model', 'refresh-active-model', 'unset-active-model']

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
        websocket_logger.info("Optitrack client joined")
    elif type == 'leave-optitrack-room': # Leave the optitrack room
        optitrack_clients.remove(websocket)
        websocket_logger.info("Optitrack client left")
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
    connected_clients.add(websocket) # Add the client to the set of connected clients
    websocket_logger.debug("A new device has connected") # Log the connection
    try:
        # Handle the messages that are sent to the websocket server
        while True:
            message = await websocket.recv()
            if message is not None:
                await handle_message(message, websocket)
    except websockets.exceptions.ConnectionClosedOK:
        websocket_logger.debug("A device has disconnected") # Log the disconnection
    except Exception as e:
        websocket_logger.error(str(traceback.format_exc())) # Log the error
    finally:
        connected_clients.remove(websocket) # Remove the client from the set of connected clients

# Function to start the websocket server
async def start_server():
    # Start the websocket server
    server = await websockets.serve(handle_websocket, WEBSOCKET_SERVER_ADDRESS, WEBSOCKET_SERVER_PORT) # Create the websocket server
    websocket_logger.info("Websocket server starter") # Log the start of the websocket server
    await server.wait_closed() 

if __name__ == '__main__':
    try:
        asyncio.run(start_server()) # Start the websocket server
    except KeyboardInterrupt:
        websocket_logger.info("Websocket server stopped")
    except Exception as e:
        websocket_logger.error(str(traceback.format_exc()))
