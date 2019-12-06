from flask import request
from flask_restful import Resource, reqparse
import traceback
# GET
class fetch(Resource):

    def __init__(self, gameManager):
        self.gameManager = gameManager

    def get(self):
        return self.gameManager.get_board_with_status()

class BoardService:

    def __init__(self, app, api, gameManager):

        # add rest endpoints
        api.add_resource(fetch, '/api/board/fetch', resource_class_kwargs={'gameManager': gameManager})
        # api.add_resource (BoardList, '/api/board/click', resource_class_kwargs={'gameManager': gameManager})
        # api.add_resource (BoardList, '/api/board/flag', resource_class_kwargs={'gameManager': gameManager})
        # api.add_resource (BoardList, '/api/board/reset', resource_class_kwargs={'gameManager': gameManager})

