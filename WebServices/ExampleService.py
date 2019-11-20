from flask import request
from flask_restful import Resource, reqparse
import traceback

class ExampleList(Resource):

    def get(self):

        response = [
            {"name": "file1", "num": 3531},
            {"name": "file2", "num": 5321},
            {"name": "file3", "num": 2424},
            {"name": "file4", "num": 1313},
            {"name": "file5", "num": 5157}
        ]

        return response

class ExampleService:

    def __init__(self, app, api):

        # add rest endpoints
        api.add_resource(ExampleList, '/api/list/getlists')

