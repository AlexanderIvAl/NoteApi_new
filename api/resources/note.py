from api import auth, abort, g, Resource, reqparse, db
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.schemas.note import note_schema, notes_schema, NoteSchema, NoteModel 
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields
from helpers.shortcuts import get_or_404

@doc(description='Api for notes.', tags=['Note'])
class NoteResource(MethodResource):
    @auth.login_required
    @marshal_with(NoteSchema, code=200)
    def get(self, **kwargs):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        author = g.user
        note = NoteModel(**kwargs)
        if not note:
            abort(404, error=f"Note with id={note.id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        return note, 200

    @auth.login_required
    @marshal_with(NoteSchema, code=200)
    def put(self, **kwargs):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = g.user
        # parser = reqparse.RequestParser()
        # parser.add_argument("text", required=True)
        # parser.add_argument("private", type=bool)
        note_data = NoteModel(**kwargs)
        note = get_or_404(NoteModel, note_id)
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.text = note_data["text"]

        if note_data.get("private") is not None:
            note.private = note_data.get("private")
        
        note.save()
        return note_data, 200

    @auth.login_required
    @marshal_with(NoteSchema, code=200)
    def delete(self, note_id):
        """
        Пользователь может удалять ТОЛЬКО свои заметки
        """
        author = g.user
        note_dict = NoteModel.query.get(note_id)
        if not note_dict:
            abort(404, error=f"note {note_id} not found")
        if note_dict.author != author:
            abort(403, error=f"Forbidden")
        note_dict.delete()
        return note_dict, 200


class NotesListResource(MethodResource):
    def get(self):
        notes = NoteModel.query.all()
        return notes_schema.dump(notes), 200

    @auth.login_required
    def post(self):
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        # Подсказка: чтобы разобраться с private="False",
        #   смотрите тут: https://flask-restful.readthedocs.io/en/latest/reqparse.html#request-parsing
        parser.add_argument("private", type=bool, required=True)
        note_data = parser.parse_args()
        note = NoteModel(author_id=author.id, **note_data)
        note.save()
        return note_schema.dump(note), 201

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