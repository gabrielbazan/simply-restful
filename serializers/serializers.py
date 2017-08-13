from . import Serializer
from models.models import *


class StateSerializer(Serializer):
    model = State


class ProvinceSerializer(Serializer):
    model = Province
    state = StateSerializer


class LakeSerializer(Serializer):
    model = Lake
    province = ProvinceSerializer
