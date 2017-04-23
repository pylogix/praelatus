"""
Contains functions for interacting with users.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

import bcrypt
import hashlib

from sqlalchemy.exc import IntegrityError

from praelatus.lib.permissions import PermissionError
from praelatus.models import User
from praelatus.models import DuplicateError



def get(db, actioning_user=None, username=None, id=None, email=None,
        filter=None):
    """
    Get users from the database.

    If the keyword arguments id, username, or email are specified returns a
    single sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
    id -- the user's database id (default None)
    email -- the user's email (default None)
    username -- the user's username (default None)
    filter -- a pattern to search through users with (default None)
    """
    query = db.query(User)

    if username is not None:
        query = query.filter(User.username == username)

    if id is not None:
        query = query.filter(User.id == id)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(User.username.like(pattern))

    if any([username, id, email]):
        return query.first()
    return query.order_by(User.username).all()



def new(db, **kwargs):
    """
    Create a new user in the database then returns that user.

    The kwargs are parsed such that if a json representation of a
    user is provided as expanded kwargs it will be handled
    properly.

    If a required argument is not provided then it raises a KeyError
    indicating which key was missing. Useful for returning HTTP 400
    errors.

    Required Keyword Arguments:
    username -- the user name
    email -- the user's email
    password -- the user's password
    full_name -- the user's full name

    Optional Keyword Arguments:
    is_admin -- whether the user is a system admin or not (default False)
    profile_pic -- path to the user's profile picture (default Gravatar)
    """
    password = bcrypt.hashpw(kwargs['password'].encode('utf-8'),
                             bcrypt.gensalt())
    new_user = User(
        username=kwargs['username'],
        password=password.decode('utf-8'),
        email=kwargs['email'],
        profile_pic=kwargs.get('profile_pic', gravatar(kwargs['email'])),
        is_admin=kwargs.get('is_admin', False),
        is_active=kwargs.get('is_active', True),
        full_name=kwargs['full_name']
    )

    try:
        db.add(new_user)
        db.commit()
    except IntegrityError as e:
        raise DuplicateError('That username is already taken.')

    return new_user



def update(db, user, actioning_user=None):
    """
    Update the given user in the database.

    user must be a User class instance.
    """
    if (actioning_user is None or
        (actioning_user.get('id', 0) != user.id and
         not actioning_user.is_admin)):
        raise PermissionError('permission denied')

    db.add(user)
    db.commit()



def delete(db, user, actioning_user=None):
    """
    Remove the given user from the database.

    user must be a User class instance.
    """
    if (actioning_user is None or
        (actioning_user.get('id', 0) != user.id and
         not actioning_user.is_admin)):
        raise PermissionError('permission denied')

    db.delete(user)
    db.commit()


def gravatar(email):
    """Generate a gravatar profile picture link based on email."""
    md5 = hashlib.md5()
    md5.update(email.encode('utf-8'))
    return 'https://gravatar.com/avatar/' + md5.hexdigest()


def check_pw(user, password):
    """
    Check user's password against password.

    Alias to bcrypt.checkpw.
    """
    return bcrypt.checkpw(password.encode('utf-8'),
                          user.password.encode('utf-8'))
