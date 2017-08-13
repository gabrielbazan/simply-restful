from flask import Flask, jsonify
from flask_restful import Api
from sqlalchemy.exc import IntegrityError
from database import session


app = Flask(__name__)
api = Api(app)

app.url_map.strict_slashes = False


@app.errorhandler(IntegrityError)
def all_exception_handler(e):
    return jsonify(dict(message='Integrity error', detail=str(e))), 409


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.close()
