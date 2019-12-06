from WebServices.ExampleService import ExampleService
from WebServices.BoardService import BoardService
from WebServices.SocketService import SocketService

class Routing:

    # add all routes and endpoints here, don't touch flask_app.py
    def __init__(self, app, api, socketio, gameManager):

        # adding routes
        ExampleService(app, api, socketio, gameManager)
        BoardService(app, api, socketio, gameManager)
        SocketService(app, api, socketio, gameManager)