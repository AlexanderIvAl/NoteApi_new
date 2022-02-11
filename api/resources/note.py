from api import auth, abort, g, Resource, reqparse, db
from api.models.note import NoteModel
from api.schemas.note import note_schema, notes_schema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc

@doc(description='Api for notes.', tags=['Note'])
class NoteResource(Resource):
    @auth.login_required
    def get(self, note_id):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        return note_schema.dump(note), 200

    @auth.login_required
    def put(self, note_id):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("private", type=bool)
        note_data = parser.parse_args()
        note = NoteModel.query.get(note_id)
        if note is None:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        if note_data["text"]:
            note.text = note_data["text"]
        if note_data["private"]:
            note.private = note_data["private"]
        note.save()
        return note_schema.dump(note), 200

    @auth.login_required
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
        db.session.delete(note_dict)
        note_dict.save()
        return note_dict, 200


class NotesListResource(Resource):
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
