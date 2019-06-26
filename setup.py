#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from setuptools import setup, find_packages
import os

# Parse the version from the main __init__.py
with open('ministac/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue


setup(name='ministac',
      version=version,
      description=u"A minimalistic spatio temporal asset catalog",
      author=u"Loic Dutrieux",
      author_email='loic.dutrieux@conabio.gob.mx',
      license='GPLv3',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'geoalchemy2',
          'sqlalchemy',
          'shapely',
          'jsonschema',
          'psycopg2-binary'
      ])
