from jsonschema import validate

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


def search(collection, geom, begin, end, max_cloud_cover=100):
    """Query the database for matching items

    Args:
        collection (str): The name of the collection to query
        geom (dict): A geojson like geometry
        begin (datetime.datetime): Begin date
        end (datetime.datetime): End date
        max_cloud_cover (float): Maximum cloud cover allowed in percent (value
            between 0 and 100)
    """
    geom_wkt = shape(geom).wkt
    with session_scope() as session:
        objects = session.query(Item)\
                .join(Item.collection)\
                .filter(Collection.name==collection)\
                .filter(Item.geom.ST_Intersects(geom_wkt))
        # TODO: Missing date filter and cc filter
        return [x.geojson for x in objects]




