from flask import Flask
from flask_restful import Api
from settings import HOST, PORT
from resources import add_resource
from resources.resources import *


app = Flask(__name__)
api = Api(app)

app.url_map.strict_slashes = False

add_resource(api, LakeResource)
add_resource(api, ProvinceResource)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
