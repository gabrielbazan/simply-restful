from app import app, api
from settings import HOST, PORT
from resources import add_resource
from resources.resources import *


add_resource(api, CountryResource)
add_resource(api, StateResource)
add_resource(api, LakeResource)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
