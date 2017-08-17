from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import engine
from model import Model
from geometry import Geometry


class Country(Model):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    created = Column(DateTime, default=func.now())


class State(Model):
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    country = relationship('Country')


class Lake(Model):
    __tablename__ = 'lake'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    created = Column(DateTime, default=func.now())
    geom = Column(Geometry('POLYGON', srid=4326))
    state_id = Column(Integer, ForeignKey('state.id'), nullable=False)
    state = relationship('State', backref='lakes')


if __name__ == '__main__':
    Model.metadata.create_all(engine, checkfirst=True)
