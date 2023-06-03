WEBSOCKET_SERVER_ADDRESS = "localhost" # Address of the websocket server
WEBSOCKET_SERVER_PORT = 9500 # Port of the websocket server

LOG_ON_STDOUT = True # Set to true if you want to display the logs into the stdout (the logging level to the logger on the stdout is DEBUG). The logging on the file is always turned on.

# All the messages with this type are forwarded to all the connected clients (broadcast)
valid_messages_type = ['new-model', 'update-model', 'delete-model', 'new-texture', 'delete-texture', 'texture-set-default', 'lock-model', 'unlock-model', 'set-active-model', 'refresh-active-model', 'unset-active-model']

LOGGER_FILE_NAME = "websocket_server.log"

LIMIT_EXCEPTIONS_BEFORE_RESTART = 10