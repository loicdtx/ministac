from jsonschema import validate
from sqlalchemy.types import Numeric

from ministac.db import session_scope
from ministac.models import Item, Collection

__version__ = '0.0.1'


def add_items(items, collection):
    """Add one or many items to the database

    Args:
        item (dict or list): The item to add, or list of items
        collection (str): The name of the collection
    """
    if not isinstance(item, list):
        items = [items]
    with session_scope() as session:
        collection = session.query(Collection).filter_by(name=collection).first()
        item_list = [Item.from_geojson(feature=x, collection=collection)
                     for x in items]
        session.add_all(item_list)


def add_collection(collection):
    """Add a new collection to the database

    Args:
        collection (dict): The collection to add
    """
    validate(collection, COLLECTION_SCHEMA)
    collection_obj = Collection(name=collection['id'],
                                meta=collection)
    with session_scope() as session:
        session.add(collection_obj)


def search(collection, geom=None, startDate=None, endDate=None,
           maxCloudCover=None):
    """Query the database for matching items

    Args:
        collection (str): The name of the collection to query
        geom (dict): A geojson like geometry
        startDate (datetime.datetime): Begin date
        endDate (datetime.datetime): End date
        maxCloudCover (float): Maximum cloud cover allowed in percent (value
            between 0 and 100)
    """
    with session_scope() as session:
        objects = session.query(Item)\
                .join(Item.collection)\
                .filter(Collection.name==collection)
        if geom is not None:
            geom_wkt = shape(geom).wkt
            objects = objects.filter(Item.geom.ST_Intersects(geom_wkt))
        if startDate is not None:
            objects = objects.filter(Item.time >= startDate)
        if endDate is not None:
            objects = objects.filter(Item.time >= endDate)
        if maxCloudCover is not None:
            objects = objects.filter(Item.meta['properties']['eo:cloud_cover']\
                                     .astext.cast(Numeric) <= maxCloudCover)
        return [x.geojson for x in objects]




