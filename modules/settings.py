WEBSOCKET_SERVER_ADDRESS = "localhost" # Address of the websocket server
WEBSOCKET_SERVER_PORT = 9500 # Port of the websocket server

LOG_ON_STDOUT = True # Set to true if you want to display the logs into the stdout (the logging level to the logger on the stdout is DEBUG). The logging on the file is always turned on.


# Verify that all the parameters has been set
if WEBSOCKET_SERVER_ADDRESS == None or WEBSOCKET_SERVER_PORT == None or LOG_ON_STDOUT == None:
    raise Exception("Please set all the parameters in the settings.py file")
