"""Blueprint for the api endpoints."""

import json

from flask import Blueprint

from praelatus.app.api.v1 import add_v1_routes

# Fix python 3.4 to 3.5 compatibility
if not hasattr(json, 'JSONDecodeError'):
    json.JSONDecodeError = ValueError

api = Blueprint('api', __name__)

# Register /api/v1/ routes.
add_v1_routes(api)

# Make v1 the latest version.
add_v1_routes(api, prefix='/api/')
