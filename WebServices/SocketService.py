from flask import request
from flask_socketio import join_room, leave_room

class SocketService:

    def __init__(self, socket_io, gameManager):
        self.socket_io = socket_io
        self.user_lobbies = {}

        socket_io.on_event('boardAction', self.receive_board_action)
        socket_io.on_event('joinLobby', self.receive_join_lobby)

    def receive_board_action(self):
        user_sid = request.sid
        lobby_key = self.user_lobbies[user_sid]

        # emit to lobby socket room
        self.socket_io.emit('boardChanged', {}, room=lobby_key, broadcast=True, include_self=False)

    def receive_join_lobby(self, lobby_key):
        user_sid = request.sid

        # leave old lobby
        if user_sid in self.user_lobbies:
            leave_room(self.user_lobbies[user_sid])

        # join new lobby
        self.user_lobbies[user_sid] = lobby_key
        join_room(lobby_key)

        print("{} joined {}".format(user_sid, lobby_key))
