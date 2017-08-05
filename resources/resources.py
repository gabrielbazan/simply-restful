from . import Resource
from serializers.serializers import *


class LakeResource(Resource):
    endpoint = 'lakes'
    serializer = LakeSerializer


class ProvinceResource(Resource):
    endpoint = 'provinces'
    serializer = ProvinceSerializer
