*********
Ministac 
*********

*Ministac is a minimalist Spatio-Temporal Asset Catalog. It allows for instance an institution to have a searchable catalog of their in house satellite images*

Features
========

- Manages metadata satellite images (items) and satellites images collections
- Stores information in Postgres database
- Search catalog using geojson geometry, temporal window, and/or cloud cover
- Complies with Spatio-Temporal Asset Catalog `specifications <http://github.com/radiantearth/stac-spec>`_ 
- Metadata validation against JSON schemas of `stac-spec <https://github.com/radiantearth/stac-spec>`_ 
- Built to work with:
    - `ministac-admin <http://github.com/loicdtx/ministac-admin>`_ (helper scripts to generate the catalog from multiple collections)
    - `ministac-api <http://github.com/loicdtx/ministac-api>`_ (JSON REST API)
    - ministac-client (does not exist yet)


Installation
============

A complete installation requires the package, a postgres database with PostGIS extension, and a configuration file with database credentials.


Python package
--------------

Activate a python 3 virtual environment and run:

.. code-block:: bash

    pip install ministac


Database
--------

- Install postgresql and PostGIS
- Create the ministac database
- Enable PostGIS extension for the ministac database

.. code-block:: bash

    createdb ministac
    psql ministac -c "CREATE EXTENSION postgis;"
    psql ministac -c "CREATE EXTENSION postgis_topology;"
    # Optionally create dedicated user (probably better for remote access)
    psql ministac -c "CREATE USER ministac_user WITH PASSWORD 'qwerty' CREATEDB;"
  

Configuration file
------------------

The configuration file must be named ``~/.ministac``; it contains the database access credentials.

.. code-block:: bash

    [ministac]
    db_database=name_of_the_database
    # Optional, depending on database configuration (running on localhost or remote, require password, etc)
    # db_hostname=
    # db_username=
    # db_password=
    # db_port=

Usage
=====

Although ministac has a functional API, most common use cases are probably covered by `ministac-admin <http:/github.com/loicdtx/ministac-admin>`_  and `ministac-api <http://github.com/loicdtx/ministac-api>`_. Nethertheless here are some basic examples of direct use.

.. code-block:: python
 
    import json
    from pprint import pprint
    import datetime as dt

    import ministac
    from ministac.db import init_db

    
    # Create database tables
    init_db()

    # Open example collection from test directory of the ministac repository
    with open('tests/data/collection_0.json') as src:
        landsat_8_collection = json.load(src)

    # Register the Landsat 8 collection to the database
    ministac.add_collection(landsat_8_collection)

    # Read some example items
    with open('tests/data/item_list.json') as src:
        item_list = json.load(src)

    # Ingest the items to the database
    ministac.add_items(item_list, 'landsat_sr_8')


    # Query the entire landsat_sr_8 collection 
    pprint(ministac.search('landsat_sr_8'))

    # Add temporal filter
    startDate = dt.datetime(2017, 12, 1)
    pprint(ministac.search('landsat_sr_8', startDate=startDate))

    # Spatial filter
    geom = {'coordinates': [[[-101.7, 19.59],
                             [-101.66, 19.54],
                             [-101.61, 19.56],
                             [-101.64, 19.58],
                             [-101.57, 19.63],
                             [-101.54, 19.66],
                             [-101.6, 19.68],
                             [-101.64, 19.64],
                             [-101.7, 19.59]]],
            'type': 'Polygon'}
    pprint(ministac.search('landsat_sr_8', geom=geom))

    # Filter with cloud cover threshold
    pprint(ministac.search('landsat_sr_8', maxCloudCover=20))

Ackowledgements
===============

This project received funding from `CONABIO <https://www.gob.mx/conabio>`_ (Mexico's national commission for biodiversity research).

.. raw:: html

    <img src="https://www.conecto.mx/file/2016/10/Conabio2015-2.png" width="300px">
