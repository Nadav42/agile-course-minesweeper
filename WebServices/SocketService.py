
class SocketService:
    def __init__(self, app, api, socketio, gameManager):

        @socketio.on('boardAction')
        def handle_message():
            print('received message:')

