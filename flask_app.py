import os

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin

from WebServices.Routing import Routing

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

app.debug = True
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# change static folder to react build folder
app.static_url_path="/react/build/static"
app.static_folder=app.root_path + app.static_url_path
print("changed flask static folder to:", app.static_url_path)

# add flask routes and endpoints in Routing
Routing(app, api)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    python_static_folder = "./static"
    react_static_folder = "./react/build"

    # to make this work you need to:
    # 1. put react's build folder in python home folder
    # 2. merge react's build/static/ folder with python /static/ folder --> make sure there are no conflicts! if so change names

    # search file in python static folder
    if path != "" and os.path.exists(python_static_folder + '/' + path):
        return send_from_directory(python_static_folder, path)

    # search python in react build folder
    elif path != "" and os.path.exists(react_static_folder + '/' + path):
        return send_from_directory(react_static_folder, path)

    # else return react app index
    return send_from_directory(react_static_folder, "index.html")

if __name__ == '__main__':
    app.run(port='5000', debug=True)  # blocking