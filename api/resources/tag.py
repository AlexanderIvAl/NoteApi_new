from api import Resource, abort, reqparse, auth
from api.models.tag import TagModel
from api.models.note import NoteModel
from api.schemas.note import NoteSchema
from api.schemas.tag import TagRequestSchema, TagSchema, TagModel
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
    
    @marshal_with(TagSchema, code=200)
    def get(self, tag_id):
        user = TagModel.query.get(user_id)
        if user:
            abort(403, error=f"User with id={user_id} not found")
        return user, 200
    
    @doc(summary="Set tags to Note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        print("note kwargs = ", kwargs)
        
        return note, 200

    # @auth.login_required
    @marshal_with(UserSchema, code=200)
    def delete(self, user_id):
        raise NotImplemented  # не реализовано!


@doc(description='Get all tags', tags=['tags'])
class UsersListResource(MethodResource):
    @doc(summary="List of users")
    @marshal_with(TagSchema, code=200)
    def get(self):
        tags = TagModel.query.all()
        return tags, 200

    @use_kwargs(TagRequestSchema, location=('json'))
    @marshal_with(TagSchema, code=201)
    def post(self, **kwargs):
        # parser = reqparse.RequestParser()
        # parser.add_argument("username", required=True)
        # parser.add_argument("password", required=True)
        # user_data = parser.parse_args()
        user = TagModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user, 201
