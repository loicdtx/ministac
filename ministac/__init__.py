from jsonschema import validate
from sqlalchemy.types import Numeric
from shapely.geometry import shape

from ministac.models import Item, Collection
from ministac.globals import COLLECTION_SCHEMA

__version__ = '0.0.1'


def add_items(session, items, collection):
    """Add one or many items to the database

    Args:
        item (dict or list): The item to add, or list of items
        collection (str): The name of the collection
    """
    if not isinstance(items, list):
        items = [items]
    collection = session.query(Collection).filter_by(name=collection).first()
    item_list = [Item.from_geojson(feature=x, collection=collection)
                 for x in items]
    session.add_all(item_list)


def add_collection(session, collection):
    """Add a new collection to the database

    Args:
        collection (dict): The collection to add
    """
    validate(collection, COLLECTION_SCHEMA)
    collection_obj = Collection(name=collection['id'],
                                meta=collection)
    session.add(collection_obj)


def search(session, collection, geom=None, startDate=None, endDate=None,
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
    objects = session.query(Item)\
            .join(Item.collection)\
            .filter(Collection.name==collection)
    if geom is not None:
        geom_wkt = 'SRID=4326;%s' % shape(geom).wkt
        objects = objects.filter(Item.geom.ST_Intersects(geom_wkt))
    if startDate is not None:
        objects = objects.filter(Item.time >= startDate)
    if endDate is not None:
        objects = objects.filter(Item.time <= endDate)
    if maxCloudCover is not None:
        objects = objects.filter(Item.meta['properties']['eo:cloud_cover']\
                                 .astext.cast(Numeric) <= maxCloudCover)
    return [x.geojson for x in objects]


def collections(session):
    """Return a list of all collections registered in the database

    Returns:
        dict: A dictionary of {collection_name: collection_meta}
    """
    objects = session.query(Collection)
    return {x.name:x.meta for x in objects}


def get_collection(session, name):
    """Return the requested collection

    Args:
        name (str): The name of the collection

    Return:
        dict: The metadata of the collection

    Raises:
        sqlalchemy.orm.exc.NoResultFound: if no result correspond to the request
    """
    obj = session.query(Collection).filter_by(name=name).one()
    return obj.meta


def get_item(session, collection, item):
    obj = session.query(Item)\
            .join(Item.collection)\
            .filter(Collection.name==collection)\
            .filter(Item.name==item)\
            .one()
    return obj.meta

