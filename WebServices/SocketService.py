from flask import request, session
from flask_socketio import join_room

from WebServices.SessionKeys import LOBBY_SESSION_KEY

class SocketService:

    def __init__(self, socket_io, gameManager):
        self.socket_io = socket_io

        socket_io.on_event('boardAction', self.receive_board_action)
        socket_io.on_event('joinLobby', self.receive_join_lobby)

    def receive_board_action(self):

        # get lobby key from session
        lobby_key = session.get(LOBBY_SESSION_KEY)

        # emit to lobby socket room
        if lobby_key is not None:
            self.socket_io.emit('boardChanged', {}, room=lobby_key, broadcast=True, include_self=False)

    def receive_join_lobby(self):

        # get lobby key from session
        lobby_key = session.get(LOBBY_SESSION_KEY)

        # join new lobby
        if lobby_key is not None:
            join_room(lobby_key)

            print("{} joined socket room {}".format(request.sid, lobby_key))
