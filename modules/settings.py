import json, os

# Get some settings from the settings.json file
settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.json')
# Verify that the file exists
if not os.path.isfile(settings_file_path):
    raise Exception("The settings.json file doesn't exist")
# Get the settings from the settings.json file
with open(settings_file_path) as settings_file:
    settings = json.load(settings_file)
# Check that the settings.json file contains the required keys
if not 'WEBSOCKET_SERVER_ADDRESS' in settings:
    raise Exception("The settings.json file doesn't contain the WEBSOCKET_SERVER_ADDRESS key")
if not 'WEBSOCKET_SERVER_PORT' in settings:
    raise Exception("The settings.json file doesn't contain the WEBSOCKET_SERVER_PORT key")

# Get the settings from the settings.json file
WEBSOCKET_SERVER_ADDRESS = settings['WEBSOCKET_SERVER_ADDRESS']
WEBSOCKET_SERVER_PORT = settings['WEBSOCKET_SERVER_PORT']

LOG_ON_STDOUT = False # Set to true if you want to display the logs into the stdout (the logging level to the logger on the stdout is DEBUG). The logging on the file is always turned on.

# All the messages with this type are forwarded to all the connected clients (broadcast)
valid_messages_type = ['new-model', 'update-model', 'delete-model', 'new-texture', 'delete-texture', 'texture-set-default', 'lock-model', 'unlock-model', 'set-active-model', 'refresh-active-model', 'unset-active-model']

LOGGER_FILE_NAME = "websocket_server.log"

LIMIT_EXCEPTIONS_BEFORE_RESTART = 10