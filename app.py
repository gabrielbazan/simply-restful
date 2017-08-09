from flask import Flask, jsonify
from flask_restful import Api
from settings import HOST, PORT
from resources import add_resource
from resources.resources import *


app = Flask(__name__)
api = Api(app)

app.url_map.strict_slashes = False

add_resource(api, LakeResource)
add_resource(api, ProvinceResource)


from sqlalchemy.exc import IntegrityError
@app.errorhandler(IntegrityError)
def all_exception_handler(e):
    return jsonify(dict(message='Integrity error', detail=str(e))), 409


from database import session
@app.teardown_appcontext
def shutdown_session(exception=None):
    session.close()


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
