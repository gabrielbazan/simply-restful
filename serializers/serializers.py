from . import Serializer
from models.models import *


class ProvinceSerializer(Serializer):
    model = Province


class LakeSerializer(Serializer):
    model = Lake
    province = ProvinceSerializer


l = Lake()
#l.geom