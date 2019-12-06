from flask import request
from flask_restful import Resource, reqparse
import traceback


class Fetch(Resource):

    def __init__(self, gameManager):
        self.gameManager = gameManager

    def get(self):
        return self.gameManager.get_board_with_status()


class Click(Resource):
    def __init__(self, gameManager):
        self.gameManager = gameManager

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
        return {"msg": "clicked"}


class Flag(Resource):
    def __init__(self, gameManager):
        self.gameManager = gameManager

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
        return {"msg": "flag clicked"}


class Reset(Resource):
    def __init__(self, gameManager):
        self.gameManager = gameManager

    def post(self):
        body = request.get_json()
        must_have_args = ["rows", "cols"]

        # validate has all arguments
        for arg in must_have_args:
            if arg not in body:
                return {"errorMsg": "missing args! please check request body have all args: {}".format(must_have_args)}

        # get arguments from post body
        cols = int(body["cols"])
        rows = int(body["rows"])

        self.gameManager.reset_game(rows=rows, cols=cols)
        return {"msg": "board reset"}


class BoardService:
    def __init__(self, app, api, gameManager):

        # add rest endpoints
        api.add_resource(Fetch, '/api/board/fetch', resource_class_kwargs={'gameManager': gameManager})
        api.add_resource(Click, '/api/board/click', resource_class_kwargs={'gameManager': gameManager})
        api.add_resource(Flag, '/api/board/flag', resource_class_kwargs={'gameManager': gameManager})
        api.add_resource(Reset, '/api/board/reset', resource_class_kwargs={'gameManager': gameManager})

