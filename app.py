from app import app, api
from settings import HOST, PORT
from resources import add_resource
from resources.resources import *


add_resource(api, LakeResource)
add_resource(api, ProvinceResource)
add_resource(api, StateResource)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
