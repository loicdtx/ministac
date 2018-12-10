import datetime as dt

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape, to_shape

from shapely.geometry import shape, mapping
from jsonschema import validate

from ministac.db import Base
from ministac.globals import ITEM_SCHEMA


class Collection(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    meta = Column(JSONB)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry())
    time = Column(DateTime, index=True)
    meta = Column(JSONB)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    collection_id = Column(Integer, ForeignKey('collection.id'), index=True)
    UniqueConstraint(collection_id, name)

    collection = relationship("Collection", back_populates="items")

    @classmethod
    def from_geojson(cls, feature, collection, session=None):
        """Class method to instantiate an Item object from a metadata description

        Args:
            feature (dict): A geojson feature that complies with the item json
                schema
            collection (str or ministac.models.Collection): Collection to which
                the item belong
            session (Session): Optional database session. Only required when collection is
                a string.
        """
        # Load collection object
        if isinstance(collection, str):
            collection = session.query(Collection).filter_by(name=collection).first()
        # Validate geojson feature
        jsonschema.validate(feature, ITEM_SCHEMA)
        # Build geom
        geom = from_shape(shape(feature['geometry']), 4326)
        # Parse datetime
        t = dt.datetime.strptime(feature['properties']['datetime'],
                                 '%Y-%m-%dT%H:%M:%SZ')
        # Build object
        return cls(name=feature['id'],
                   geom=geom,
                   time=t,
                   meta=feature,
                   collection=collection)

    @property
    def geojson(self):
        return self.meta

Collection.items = relationship("Item", back_populates="collection")


