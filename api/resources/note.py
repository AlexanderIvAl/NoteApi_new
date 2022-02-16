from api import auth, abort, g
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.schemas.note import note_schema, notes_schema, NoteSchema, NoteModel, NoteRequestSchema 
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields
from helpers.shortcots import get_or_404

@doc(description='Api for notes.', tags=['Notes'])
class NoteResource(MethodResource):
    @doc(summary="Get note by ID", description="The user can ONLY get his own note")
    @doc(security=[{"basicAuth": []}])
    @auth.login_required
    def get(self, note_id):
        author = g.user
        note = get_or_404(NoteModel, note_id)
        if note.author != author:
            abort(403, error=f"Forbidden")
        return note_schema.dump(note), 200
   
    @auth.login_required
    @doc(summary="Edit note by ID", description="The user can ONLY edit his own note")
    @doc(security=[{"basicAuth": []}])
    @marshal_with(NoteSchema, code=201)
    @use_kwargs(NoteRequestSchema, location=("json"))
    def put(self, note_id, **kwargs):
        author = g.user
        note = get_or_404(NoteModel, note_id)
        if note.author != author:
            abort(403, error=f"Forbidden")
        for key, value in kwargs.items():
            setattr(note, key, value)
        note.save()
        return note_schema.dump(note), 200

    @auth.login_required
    @doc(summary="Delete note by ID", description="The user can delete his own note")
    @doc(security=[{"basicAuth": []}])
    @marshal_with(NoteSchema, code=200)
    def delete(self, note_id):
        author = g.user
        note_dict = get_or_404(NoteModel, note_id)
        if note_dict.author != author:
            abort(403, error=f"Forbidden")
        note_dict.delete()
        return note_dict, 200

@doc(tags=["Notes"])
class NotesListResource(MethodResource):
    @doc(summary="List of all note")
    def get(self):
        notes = NoteModel.query.all()
        return notes_schema.dump(notes), 200

    @doc(summary="Create note", description="Create new Note for current auth User")
    @doc(security=[{"basicAuth": []}])
    @doc(responses={400: {"description": 'Bad request'}})
    @marshal_with(NoteSchema, code=201)
    @use_kwargs(NoteRequestSchema, location=("json"))
    @auth.login_required
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201

@doc(tags=["Notes"])
class NoteAddTagResource(MethodResource):
    @doc(summary="Add tegs to Note")
    @use_kwargs({"tags": fields.List(fields.Int)})
    def put(self, note_id, **kwargs):
        # print(kwargs)
        note = NoteModel.query.get(note_id)
        for tag in kwargs["tags"]:
            tag = TagModel.query.get(tag.id)
            note.tags.append(tag)
        note.save()
        return {}

@doc(tags=["Notes"])
class NotesFilterResource(MethodResource):
    # GET: /notes/filter?tags=[tag-1, tag-2, ...]
    @use_kwargs({"tags": fields.List(fields.Str())}, location="query")
    @marshal_with(NoteSchema(many=True), code=200)
    def get(self, **kwargs):
        notes = NoteModel.query.join(NoteModel.tags).filter(TagModel.name.in_(kwargs["tags"])).all()
        return notes