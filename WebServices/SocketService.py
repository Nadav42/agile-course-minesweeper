
class SocketService:
    def __init__(self, app, api, socketio, gameManager):

        @socketio.on('boardAction')
        def handle_message(data):
            socketio.emit('boardChanged', {}, broadcast=True, include_self=False)

