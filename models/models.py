from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import engine
from . import Model, Geometry


class Province(Model):
    __tablename__ = 'province'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)


class Lake(Model):
    __tablename__ = 'lake'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    created = Column(DateTime, default=func.now())
    geom = Column(Geometry('POLYGON', srid=4326))
    province_id = Column(Integer, ForeignKey('province.id'), nullable=False)
    province = relationship('Province', backref='lakes')


class User(Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    created = Column(DateTime, default=func.now())


if __name__ == '__main__':
    Model.metadata.create_all(engine, checkfirst=True)
