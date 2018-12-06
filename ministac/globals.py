from configparser import ConfigParser
import os


conf_file = os.path.expanduser('~/.ministac')
config = ConfigParser()
config.read(conf_file)

DB_DATABASE = config['ministac'].get('db_database', None)
DB_HOSTNAME = config['ministac'].get('db_hostname', None)
DB_USERNAME = config['ministac'].get('db_username', None)
DB_PASSWORD = config['ministac'].get('db_password', None)
