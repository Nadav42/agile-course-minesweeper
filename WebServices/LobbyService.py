from flask import request, session
from flask_restful import Resource
import traceback

from WebServices.SessionKeys import LOBBY_SESSION_KEY
from WebServices.Headers import NO_CACHE_HEADERS

class LobbyList(Resource):

    def __init__(self, gameManager):
        self.gameManager = gameManager

    def get(self):
        lobbies_list = self.gameManager.get_lobbies_list()
        reversed_list = lobbies_list[::-1] # show newest lobby on top

        return reversed_list, 200, NO_CACHE_HEADERS

class JoinLobby(Resource):

    def __init__(self, gameManager):
        self.gameManager = gameManager

    def post(self):
        body = request.get_json()
        must_have_args = ["lobbyKey"]

        # validate has all arguments
        for arg in must_have_args:
            if arg not in body:
                return {"errorMsg": "missing args! please check request body have all args: {}".format(must_have_args)}

        # get arguments from post body
        lobby_key = body["lobbyKey"]

        # validate lobby exists
        lobby = self.gameManager.get_lobby(lobby_key)

        if lobby is None:
            return {"errorMsg": "Lobby does not exist"}

        if lobby.has_password():
            if "password" not in body or not lobby.check_password_correct(body["password"]):
                return {"errorMsg": "Incorrect password"}

        # set lobby session key
        session[LOBBY_SESSION_KEY] = lobby_key

        return {"msg": "joined"}

class CreateLobby(Resource):

    def __init__(self, gameManager, socket_io):
        self.gameManager = gameManager
        self.socket_io = socket_io

    def post(self):
        body = request.get_json()
        must_have_args = ["lobbyName", "password"]

        # validate has all arguments
        for arg in must_have_args:
            if arg not in body:
                return {"errorMsg": "missing args! please check request body have all args: {}".format(must_have_args)}

        # get arguments from post body
        lobby_name = str(body["lobbyName"])
        password = str(body["password"])

        # create a lobby with no password
        if not password or password.strip() == "":
            password = None

        # validate name too short
        if len(lobby_name.strip().replace(" ", "")) < 3:
            return {"errorMsg": "Lobby name is too short"}

        # validate too long
        if len(lobby_name.strip().replace(" ", "")) > 40:
            return {"errorMsg": "Lobby name is too long"}

        # check password not too short
        if password is not None and len(password.strip().replace(" ", "")) < 4:
            return {"errorMsg": "Password is too short"}

        if password is not None and len(password.strip().replace(" ", "")) > 40:
            return {"errorMsg": "Password is too long"}

        # create lobby and join it
        lobby_key = self.gameManager.create_lobby(lobby_name, password=password)
        session[LOBBY_SESSION_KEY] = lobby_key

        # tell users to update lobby list
        self.socket_io.emit('lobbiesChanged', {}, broadcast=True)

        return {"msg": "created"}

class LobbyService:
    def __init__(self, app, api, socket_io, gameManager):

        # add rest endpoints
        api.add_resource(LobbyList, '/api/lobby/list', resource_class_kwargs={'gameManager': gameManager})
        api.add_resource(JoinLobby, '/api/lobby/join', resource_class_kwargs={'gameManager': gameManager})
        api.add_resource(CreateLobby, '/api/lobby/create', resource_class_kwargs={'gameManager': gameManager, 'socket_io': socket_io})
