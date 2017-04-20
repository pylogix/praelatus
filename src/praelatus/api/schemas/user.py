"""Contains schemas for users and related objects."""

from praelatus.api.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    """Used for validation of user objects."""

    schema = {
        'title': 'User',
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'username': {
                'type': 'string',
                'pattern': '[^ /\\\\@!#\\$%&*\\(\\)+=|\\{\\}\\[\\];:"\',.?`~"]+'
            },
            'email': {
                'type': 'string',
                'format': 'email'
            },
            'is_admin': {'type': 'boolean'},
            'is_active': {'type': 'boolean'},
            'profile_pic': {'type': 'string'},
            'full_name': {'type': 'string'}
        },
        'required': ['username', 'full_name', 'is_active', 'email', 'id']
    }


class SignupSchema(BaseSchema):
    """Used for validation of user objects."""

    schema = {
        'title': 'User',
        'type': 'object',
        'properties': {
            'username': {
                'type': 'string',
                'pattern': '[^ /\\\\@!#\\$%&*\\(\\)+=|\\{\\}\\[\\];:"\',.?`~"]+'
            },
            'email': {
                'type': 'string',
                'format': 'email'
            },
            'is_admin': {'type': 'boolean'},
            'profile_pic': {'type': 'string'},
            'full_name': {'type': 'string'}
        },
        'required': ['username', 'full_name', 'email']
    }
