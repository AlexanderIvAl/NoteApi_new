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
    @marshal_with(NoteSchema, code=201)
    @doc(summary="Get note by ID", description="The user can ONLY get his own note")
    @doc(security=[{"basicAuth": []}])
    @auth.login_required
    def get(self, note_id):
        author = g.user
        # note = get_or_404(NoteModel, note_id)
        note = NoteModel.not_archive().get(note_id)
        if note is None:
            abort(404)
        # note = note_schema.dump(note)
        return note, 200
   
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
        return note, 200

    @doc(summary="Delete note", description="Note to archive")
    @doc(security=[{"basicAuth": []}])
    @auth.login_required
    @marshal_with(NoteSchema, code=201)
    def delete(self, note_id):
        """
        Пользователь может удалять ТОЛЬКО свои заметки
        """
        auth_user = g.user
        note = get_or_404(NoteModel, note_id)
        if auth_user != note.author:
            abort(403)

        note.delete()
        return {}, 204
# DELETE
# 1. Заметка удалена archived --> True
# 2. Можно удалить только логин под автором
#   2.1. Если удалить не под Автором, то 403
#   2.2. Если удалить под автором, то 204
#  404
# 401 - без логина

@doc(tags=["Notes"])
class NotesListResource(MethodResource):
    @doc(summary="List of all note")
    @marshal_with(NoteSchema(many=True), code=201)
    def get(self):
        notes = NoteModel.not_archive().all()
        return notes, 200

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
class NoteRestoreResource(MethodResource):
    @doc(summary="Restore note")
    @marshal_with(NoteSchema)
    def put(self, note_id):
        note = get_or_404(NoteModel, note_id)
        note.restore()
        return note, 200

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