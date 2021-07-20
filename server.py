from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
from webhook import Webhook


class Server:
    app = None
    api = None
    meter = None
    # monitor = None

    def __init__(self):
        print("init")
        self.app = Flask(__name__)
        CORS(self.app)
        self.api = Api(self.app)


if (__name__ == "__main__"):
    TAG = "main:"
    API_VERSION = "/api/v1"
    server = Server()

    server.api.add_resource(Webhook, API_VERSION + "/webhook")
    # server.api.add_resource(Status, API_VERSION + "/get_status")

    server.app.run(host="0.0.0.0", debug=True, port=5008)


# app = Flask(__name__)


# @app.route('/')
# def helloo():
#     return 'Hello o o o o o o o'


# @app.route('/hello')
# def hello():
#     return 'Hello, World!'


# if __name__ == '__main__':
#     app.run(debug=True)
#     # app.run(debug=True, host='0.0.0.0', port=5000)
