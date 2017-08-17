from . import Serializer
from models.models import *


class CountrySerializer(Serializer):
    model = Country


class StateSerializer(Serializer):
    model = State
    country = CountrySerializer


class LakeSerializer(Serializer):
    model = Lake
    state = StateSerializer
