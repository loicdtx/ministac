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
DB_PORT = config['ministac'].get('db_port', None)

ITEM_SCHEMA = json.loads(pkgutil.get_data('ministac', 'schemas/item.json'))

COLLECTION_SCHEMA = json.loads(pkgutil.get_data('ministac',
                                                'schemas/collection.json'))
