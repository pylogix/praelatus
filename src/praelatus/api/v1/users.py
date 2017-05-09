"""Contains the resources for the /api/v1/users endpoints."""

import falcon
import json

import praelatus.lib.users as users
import praelatus.lib.sessions as sessions
import praelatus.lib.tickets as tickets

from praelatus.api.schemas import UserSchema
from praelatus.api.schemas import SignupSchema
from praelatus.lib import session


class UsersResource():
    """Handlers for the /api/v1/users endpoint."""

    def __init__(self, create_token):  # noqa: D400,D205
        """create_token should be a function which takes a user and a res
        then creates a token for that user and sends it to res, it is
        called after on_post to create a token for a user after
        signup.
        """
        self.create_token = create_token

    def on_get(self, req, res):
        """Return all users for the instance.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-users
        """
        user = req.context.get('user', {})
        query = req.params.get('filter', '*')

        with session() as db:
            db_res = users.get(db, filter=query, actioning_user=user)

        usrs = []
        for u in db_res:
            usrs.append(u.clean_dict())

        res.body = json.dumps(usrs)

    def on_post(self, req, res):
        """Create a user then return that user with an auth token.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-users
        """
        signup_req = json.loads(req.bounded_stream.read().decode('utf-8'))
        SignupSchema.validate(signup_req)
        with session() as db:
            db_u = users.new(db, **signup_req)
            self.create_token(db_u, res)


class UserResource():
    """Handlers for /api/v1/users/{username} endpoint."""

    def on_get(self, req, res, username):
        """Return single user by username or id.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-usersusername
        """
        user = req.context.get('user', {})
        with session() as db:
            db_res = users.get(db, username=username, actioning_user=user)
            if db_res is None:
                raise falcon.HTTPNotFound()
            res.body = db_res.to_json()

    def on_put(self, req, res, username):
        """Update the user identified by username.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-usersusername
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        UserSchema.validate(jsn)
        with session() as db:
            new_u = users.get(db, username=username)
            if new_u is None:
                raise falcon.HTTPNotFound()
            new_u.username = jsn['username']
            new_u.email = jsn['email']
            new_u.profile_pic = jsn['profile_pic']
            new_u.full_name = jsn['full_name']
            new_u.is_active = jsn.get('is_active', True)
            new_u.is_admin = jsn.get('is_admin', False)
            users.update(db, new_u, actioning_user=user)
        res.body = json.dumps({'message': 'Successfully updated user.'})

    def on_delete(self, req, res, username):
        """Delete the user identified by username.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-usersusername
        """
        user = req.context['user']
        with session() as db:
            del_user = users.get(db, username=username)
            if del_user is None:
                raise falcon.HTTPNotFound()
            users.delete(db, del_user, actioning_user=user)
        res.body = json.dumps({'message': 'Successfully deleted user.'})


class TokensResource():
    """Handlers for /api/v1/tokens endpoint."""

    def on_post(self, req, res):
        """Create a new session AKA "log in".

        API Documentation:
        https://doc.praelatus.io/API/Reference/#post-tokens
        """
        login = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            user = users.get(db, username=login['username'])
        if user is None:
            res.body = json.dumps({
                'message': 'no user with that username exists'
            })
            res.status = falcon.HTTP_404
            return

        if not users.check_pw(user, login['password']):
            res.body = json.dumps({'message': 'invalid password'})
            res.status = falcon.HTTP_401
            return

        TokensResource.create_token(user, res)

    @staticmethod
    def create_token(user, res):
        """Create a session for user, set the res body to the session."""
        token = sessions.gen_session_id(user.clean_dict())

        # Set the session cookie on the resonse
        res.set_cookie('PRAE_SESSION', token)

        res.status = falcon.HTTP_200
        res.body = json.dumps({
            'token': token,
            'user': user.clean_dict()
        })

    def on_delete(self, req, res):
        """
        Invalidate the current user's token AKA "log out".

        API Documentation:
        https://doc.praelatus.io/API/Reference/#delete-tokens
        """
        sessions.delete(req.context['user']['username'])
        sessions.delete(req.context['session_id'])


class AssignedResource():
    """Handlers for the /api/v1/users/{username}/assigned endpoint."""

    def on_get(self, req, res, username):
        """"Get all assigned tickets for username.

        API Documentation:
        https://doc.praelatus.io/API/Reference/#get-usersusernameassigned
        """
        user = req.context['user']
        with session() as db:
            assignee = users.get(db, username=username)
            ticks = tickets.get(db, actioning_user=user,
                                assignee=assignee.clean_dict())
            res.body = json.dumps([t.clean_dict() for t in ticks])


class ReportedResource():
    """Handlers for the /api/v1/users/{username}/reported endpoint."""

    def on_get(self, req, res, username):
        """"Get all reported tickets by username.

        API Documentation:
        https://doc.praelatus.io/API/Reference/#get-usersusernamereported
        """
        user = req.context['user']
        with session() as db:
            reporter = users.get(db, username=username)
            ticks = tickets.get(db, actioning_user=user,
                                reporter=reporter.clean_dict())
            res.body = json.dumps([t.clean_dict() for t in ticks])
