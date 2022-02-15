import logging
from api import Resource, abort, reqparse, auth, g
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc



@doc(description='Api for notes.', tags=['Users'])
class UserResource(MethodResource):
    @marshal_with(UserSchema, code=200)
    def get(self, user_id):
    # language=YAML
        """
        Get User by id
        ---
        tags:
            - Users
        """

        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user, 200

    # @auth.login_required(role="admin")
    @marshal_with(UserSchema, code=200)
    @use_kwargs(UserSchema)
    def put(self, user_id, **kwargs):
        # language=YAML
        """
        Get User by id
        ---
        tags:
            - Users
        parameters:
            - in: path
              name: user_id
              type: integer
              required: true
              default: 1
        responses:
            200:
                description: A single user item
                schema:
                    id: User
                    properties:
                        id:
                            type: integer
                            description: user id
                            default: 1
                        username:
                            type: string
                            description: The name of the user
                            default: Steven Wilson
                        is_staff:
                            type: boolean
                            description: user is staff
                            default: false
   
        """
        user = UserModel.query.get(user_id)
        
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()           
        return user, 200
        # user_data = UserModel(**kwargs)
        # user = UserModel.query.get(user_id)
        # if not user:
        #     abort(404, error=f"User with id={user_id} not found")
        # if user_data["username"]:
        #     user.username = user_data["username"]
        # if user_data["password"]:
        #     user.hash_password(user_data["password"])
        # if user_data["is_staff"]:
        #     user.is_staff = user_data["is_staff"]
        # if user_data["role"]:
        #     user.role = user_data["role"]
        # user.save()
        # return user_data, 200

    # @auth.login_required(role="admin")
    @marshal_with(UserSchema, code=200)
    def delete(self, user_id):
        # author = g.user
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id {user_id} not found")
        # if user.author != author:
        #     abort(403, error=f"Forbidden")
        user.delete()
        return user, 200
        

@doc(description='Api for notes.', tags=['Users'])
class UsersListResource(MethodResource):
    @doc(summary="List of users")
    def get(self):
        users = UserModel.query.all()
        return users_schema.dump(users), 200

    @use_kwargs(UserRequestSchema, location=('json'))
    @marshal_with(UserSchema, code=201)
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        logging.info("User create successful")
        return user, 201
