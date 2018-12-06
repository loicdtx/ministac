from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

from shapely.geometry import shape, mapping
from geoalchemy2.shape import from_shape, to_shape

from ministac.db import Base


class Collection(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    meta = Column(JSONB)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    geom = Column(Geometry(srid=4326))
    meta = Column(JSONB)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    collection_id = Column(Integer, ForeignKey('collection.id'))

    collection = relationship("Collection", back_populates="items")

    @classmethod
    def from_geojson(cls, feature, collection):
        geom = from_shape(shape(feature['geometry']), 4326)
        pass

    @property
    def geojson(self):
        pass

Collection.items = relationship("Item", back_populates="collection")


