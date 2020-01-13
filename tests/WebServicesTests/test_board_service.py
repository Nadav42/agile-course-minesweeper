import unittest
from flask_app import app

# integration tests --> not in scope

# from WebServices.SessionKeys import LOBBY_SESSION_KEY
from WebServices.BoardService import *
class TestBoardService(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # post request testing:
    # https://stackoverflow.com/questions/7428124/how-can-i-fake-request-post-and-get-params-for-unit-testing-in-flask

    # self.app.post('/path-to-request', data=dict(var1='data1', var2='data2', ...))
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
            self.assertGreaterEqual(response['difficulty'], 0.13)

            if response['won'] == True:
                self.assertTrue(response['finished'])

            print(response)

if __name__ == '__main__':
    unittest.main()
