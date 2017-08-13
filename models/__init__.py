from database import Base
from model import Model
from geometry import Geometry


def get_class_by_table_name(table_name):
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == table_name:
      return c
