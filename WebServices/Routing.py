from WebServices.ExampleService import ExampleService

class Routing:

    # add all routes and endpoints here, don't touch flask_app.py
    def __init__(self, app, api, gameManager):

        # adding routes
        ExampleService(app, api, gameManager)