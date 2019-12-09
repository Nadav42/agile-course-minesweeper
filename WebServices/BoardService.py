from flask import request
from flask_restful import Resource, reqparse
import traceback


MIN_BOARD_SIZE = 7
MAX_BOARD_SIZE = 24

class Fetch(Resource):

    def __init__(self, gameManager):
        self.gameManager = gameManager

    def get(self):
        return self.gameManager.get_board_with_status()


class DifficultyRange(Resource):

    def __init__(self, gameManager):
        self.gameManager = gameManager

    def get(self):
        return self.gameManager.get_difficulty_options()


class Click(Resource):
    def __init__(self, gameManager, socket_io):
        self.gameManager = gameManager
        self.socket_io = socket_io

    def post(self):
        body = request.get_json()
        must_have_args = ["col", "row"]

        # validate has all arguments
        for arg in must_have_args:
            if arg not in body:
                return {"errorMsg": "missing args! please check request body have all args: {}".format(must_have_args)}

        # get arguments from post body
        col = int(body["col"])
        row = int(body["row"])

        self.gameManager.click(row, col)
        self.socket_io.emit('boardChanged', {}, broadcast=True)

        return {"msg": "clicked"}


class Flag(Resource):
    def __init__(self, gameManager, socket_io):
        self.gameManager = gameManager
        self.socket_io = socket_io

    def post(self):
        body = request.get_json()
        must_have_args = ["col", "row"]

        # validate has all arguments
        for arg in must_have_args:
            if arg not in body:
                return {"errorMsg": "missing args! please check request body have all args: {}".format(must_have_args)}

        # get arguments from post body
        col = int(body["col"])
        row = int(body["row"])

        self.gameManager.flag_click(row, col)
        self.socket_io.emit('boardChanged', {}, broadcast=True)

        return {"msg": "flag clicked"}


class Reset(Resource):
    def __init__(self, gameManager, socket_io):
        self.gameManager = gameManager
        self.socket_io = socket_io

    def post(self):
        body = request.get_json()
        must_have_args = ["rows", "cols", "difficulty"]

        # validate has all arguments
        for arg in must_have_args:
            if arg not in body:
                return {"errorMsg": "missing args! please check request body have all args: {}".format(must_have_args)}

        # get arguments from post body
        cols = int(body["cols"])
        rows = int(body["rows"])
        difficulty = float(body["difficulty"])

        if rows < MIN_BOARD_SIZE or cols < MIN_BOARD_SIZE:
            return {"errorMsg": "Board size must be larger than {}".format(MIN_BOARD_SIZE)}

        if rows > MAX_BOARD_SIZE or cols > MAX_BOARD_SIZE:
            return {"errorMsg": "Board size must be smaller than {}".format(MAX_BOARD_SIZE)}

        # reset the game
        self.gameManager.reset_game(rows=rows, cols=cols, mine_probability=difficulty)
        self.socket_io.emit('boardChanged', {}, broadcast=True)

        return {"msg": "board reset"}


class BoardService:
    def __init__(self, app, api, socket_io, gameManager):

        # add rest endpoints
        api.add_resource(Fetch, '/api/board/fetch', resource_class_kwargs={'gameManager': gameManager})
        api.add_resource(DifficultyRange, '/api/board/difficultyrange', resource_class_kwargs={'gameManager': gameManager})
        api.add_resource(Click, '/api/board/click', resource_class_kwargs={'gameManager': gameManager, 'socket_io': socket_io})
        api.add_resource(Flag, '/api/board/flag', resource_class_kwargs={'gameManager': gameManager, 'socket_io': socket_io})
        api.add_resource(Reset, '/api/board/reset', resource_class_kwargs={'gameManager': gameManager, 'socket_io': socket_io})

