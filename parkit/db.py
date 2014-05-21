#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

import pymongo
import pymongo.errors


def get_collection(**config):
    """Use this to talk to Mongo.

    With no args this will default to your local Mongo instance (using the
    'parkit' database). Supply the MONGOHQ_URL in your environment to change
    this.
    """
    mongo_url = os.getenv(
        'MONGOHQ_URL',
        'mongodb://localhost:27017/parkit'
    )
    client = pymongo.MongoClient(mongo_url, **config)
    database = client.get_default_database()
    collection = database.parkit
    collection.ensure_index([("loc", pymongo.GEOSPHERE)])
    return collection


def find(lng, lat, within=250, type="bike", limit=100, collection=None):
    """Performs a geospatial query.

    :param lng: Float, longitude.
    :param lat: Float, latitude.
    :param type: Not really used, was intended to support other data sources.
    :param within: Search radius, in meters.
    :param collection: For supplying your own Mongo collection in testing.

    """
    collection = collection or get_collection()

    matches = collection.find({
        "type": type,
        "loc": {
            "$near": {
                "$geometry":
                    {
                        "type": "Point",
                        "coordinates": [lng, lat],
                    },
                "$maxDistance": within,  # measured in meters
            }
        },
    }, {'_id': False}).limit(limit)

    return list(dedupe(matches))


def dedupe(matches):
    """ Some of our records are duplicated, this fixes that."""
    seen_coords = set()

    for match in matches:
        coords = tuple(match['loc']['coordinates'])

        if coords not in seen_coords:
            seen_coords.add(coords)
            yield match


def load_data():  # pragma: no cover
    """This isn't actually used, it's just a record of how I loaded up the
    data."""

    collection = get_collection()

    with open('data/bikes.json', 'r') as f:
        bikes = json.load(f)

    columns = [c['fieldName'] for c in bikes['meta']['view']['columns']]

    for bike in bikes['data']:
        bike_data = dict(zip(columns, bike))

        if bike_data['status'] != 'COMPLETE':
            # we don't care about parking that doesn't exist yet!
            continue

        bike_record = dict(
            type='bike',
            loc=dict(
                type='Point',
                coordinates=[
                    float(bike_data['coordinates'][2]),  # long
                    float(bike_data['coordinates'][1]),  # lat
                ]
            )
        )

        try:
            collection.insert(bike_record)
        except pymongo.errors.DuplicateKeyError:
            pass
