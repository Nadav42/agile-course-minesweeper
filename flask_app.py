import os

# import eventlet
# eventlet.monkey_patch()

from flask import Flask, request, send_from_directory
from flask_restful import Api
from flask_session import Session

from flask_socketio import SocketIO

from Config import SHOULD_BIND_ADRESS, SCRIPT_PATH
from GameManager import GameManager
from WebServices.Routing import Routing

app = Flask(__name__)

# ----- config ----- #

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'Az5Jf$y1cSt'

# ------------------ #

Session(app)

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins="*")

api = Api(app)

# change static folder to react build folder
app.static_url_path="/react/build/static"
app.static_folder=app.root_path + app.static_url_path
print("changed flask static folder to:", app.static_url_path)

# init GameManager
gameManager = GameManager()

# add flask routes and endpoints in Routing
Routing(app, api, socketio, gameManager)


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    python_static_folder = "{}/static".format(SCRIPT_PATH)
    react_static_folder = "{}/react/build".format(SCRIPT_PATH)

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

@app.after_request
def after_request(response):

    if 'HTTP_ORIGIN' in request.environ:
        response.headers.add('Access-Control-Allow-Origin', request.environ['HTTP_ORIGIN'])

    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':

    if SHOULD_BIND_ADRESS:
        socketio.run(app, host="0.0.0.0", port=5000)
    else:
        socketio.run(app, port=5000, debug=True)
