import unittest
from flask_app import app

from WebServices.SessionKeys import LOBBY_SESSION_KEY

class TestBoardService(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_board_fetch(self):
        with self.app as client:
            response = self.app.get('/api/lobby/list')
            lobbies = response.json

            lobby_key = lobbies[0]["key"]

            with client.session_transaction() as sess:
                sess[LOBBY_SESSION_KEY] = lobby_key

            response = self.app.get('/api/board/fetch')
            response = response.json

            # Make your assertions
            print(response)

if __name__ == '__main__':
    unittest.main()
