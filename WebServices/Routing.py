from WebServices.BoardService import BoardService
from WebServices.LobbyService import LobbyService
from WebServices.SocketService import SocketService

class Routing:

    # add all routes and endpoints here, don't touch flask_app.py
    def __init__(self, app, api, socketio, gameManager):

        # rest api routes
        LobbyService(app, api, socketio, gameManager)
        BoardService(app, api, socketio, gameManager)

        # socket routes
        SocketService(socketio, gameManager)
