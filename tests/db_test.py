#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
import pytest

from parkit import db


@pytest.fixture
def mongo_collection():
    return mock.Mock()


def test_find(mongo_collection):
    """This test is kinda lame.

    If I had more time I would play around with Ming, which provides an
    in-memory instance of Mongo for testing.
    """
    mongo_collection.find().limit.return_value = []

    with mock.patch('parkit.db.dedupe') as dedupe:
        db.find(
            lat=mock.sentinel.LAT,
            lng=mock.sentinel.LNG,
            type=mock.sentinel.TYPE,
            within=mock.sentinel.WITHIN,
            limit=mock.sentinel.LIMIT,
            collection=mongo_collection,
        )
        assert dedupe.called

    mongo_collection.find.assert_called_with(
        {
            'loc': {
                '$near': {
                    '$geometry': {
                        'coordinates': [mock.sentinel.LNG, mock.sentinel.LAT],
                        'type': 'Point'
                    },
                    '$maxDistance': mock.sentinel.WITHIN
                }
            },
            'type': mock.sentinel.TYPE
        },
        {'_id': False}
    )


def test_dedupe():
    record = {'loc': {'coordinates': [1, 2]}}

    assert list(db.dedupe([record, record])) == [record]


def test_get_collection():
    with mock.patch('pymongo.MongoClient', autospec=True):
        assert db.get_collection()
