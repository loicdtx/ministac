from configparser import ConfigParser
import os
import json
import pkgutil


conf_file = os.path.expanduser('~/.ministac')
config = ConfigParser()
config.read(conf_file)

DB_DATABASE = config['ministac'].get('db_database', None)
DB_HOSTNAME = config['ministac'].get('db_hostname', None)
DB_USERNAME = config['ministac'].get('db_username', None)
DB_PASSWORD = config['ministac'].get('db_password', None)

item_schema = pkgutil.get_data('ministac', 'schemas/item.json')
with open(item_schema) as src:
    ITEM_SCHEMA = json.load(src)

collection_schema = pkgutil.get_data('ministac', 'schemas/collection.json')
with open(collection_schema) as src:
    COLLECTION_SCHEMA = json.load(src)
