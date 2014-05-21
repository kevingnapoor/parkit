#!/usr/bin/env python
# -*- coding: utf-8 -*-
import httplib

import colander
from flask import abort
from flask import jsonify
from flask import request

from parkit import db


class SearchRequestSchema(colander.MappingSchema):
    """Validates search query parameters."""
    lat = colander.SchemaNode(
        colander.Float(),
        missing=37.7860099,
        validator=colander.Range(-90, 90)
    )

    lng = colander.SchemaNode(
        colander.Float(),
        missing=-122.4025387,
        validator=colander.Range(-180, 180)
    )

    type = colander.SchemaNode(
        colander.String(),
        missing="bike",
        validator=colander.OneOf(['bike', 'film', 'food'])
    )


def get_search():
    schema = SearchRequestSchema()

    try:
        params = schema.deserialize(request.args.items())
    except colander.Invalid:
        # TODO: need more helpful errors here!
        return abort(httplib.BAD_REQUEST)

    results = db.find(**params)

    return jsonify({'results': results})
