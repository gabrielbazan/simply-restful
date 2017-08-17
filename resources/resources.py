from . import Resource
from serializers.serializers import *


class CountryResource(Resource):
    endpoint = 'countries'
    serializer = CountrySerializer


class StateResource(Resource):
    endpoint = 'states'
    serializer = StateSerializer


class LakeResource(Resource):
    endpoint = 'lakes'
    serializer = LakeSerializer
