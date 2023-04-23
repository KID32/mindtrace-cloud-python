from app import app, port
from app.service.router import route
from flask import request

@app.route('/debug')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/")
def get_website_info():
    return route(request.json["type"])(request.json["url"])


if __name__ == '__main__':
    app.run(port=port)
