from geoalchemy2 import Geometry as GeoAlchemyGeometry
import geoalchemy2.shape
from shapely.geometry import shape
import shapely.geometry
import json
import geojson
from database import Base


class Model(Base):
    __abstract__ = True

    @property
    def relationships(self):
        return {
            relationship.local_remote_pairs[0][0].name: relationship.key
            for relationship in self.__mapper__.relationships
        }

    @property
    def relationship_classes(self):
        return [
            getattr(self.__class__, t).property.mapper.class_
            for f, t in self.relationships.iteritems()
        ]

    @property
    def primary_keys(self):
        return [c.name for c in self.__mapper__.primary_key]

    @property
    def columns(self):
        return [c.name for c in self.model.__table__.columns]


class Geometry(GeoAlchemyGeometry):
    def result_processor(self, dialect, coltype):
        super_proc = super(Geometry, self).result_processor(dialect, coltype)

        def process(v):
            return v and shapely.geometry.mapping(
                geoalchemy2.shape.to_shape(super_proc(v))
            )

        return process

    def bind_processor(self, dialect):
        super_proc = super(Geometry, self).bind_processor(dialect)

        def process(v):
            return super_proc(
                'SRID=%d;%s' % (self.srid, shape(geojson.loads(json.dumps(v))).wkt)
                if isinstance(v, dict) else v
            )

        return process


def get_class_by_table_name(table_name):
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == table_name:
      return c
