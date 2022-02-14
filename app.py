from api import api, app, docs
from api.resources.note import NoteResource, NotesListResource, NoteAddTagResource
from api.resources.user import UserResource, UsersListResource
from api.resources.auth import TokenResource
from config import Config
# from api.resources.tag import TagsResource, TagsListResource

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(UsersListResource,
                 '/users')  # GET, POST
api.add_resource(UserResource,
                 '/users/<int:user_id>')  # GET, PUT, DELETE

api.add_resource(TokenResource,
                 '/auth/token')  # GET

api.add_resource(NotesListResource,
                 '/notes',  # GET, POST
                 )
api.add_resource(NoteResource,
                 '/notes/<int:note_id>',  # GET, PUT, DELETE
                 )
api.add_resource(NoteAddTagResource,
                 '/notes/<int:note_id>/tags')  # PUT
# api.add_resource(TagsListResource,
#                  '/tags')  # GET, POST
# api.add_resource(TagsResource,
#                  '/tags/<int:tag_id>')  # GET, PUT, DELETE

docs.register(UserResource)
# docs.register(UsersListResource)
# docs.register(NoteResource)
# docs.register(NotesListResource)
# docs.register(NoteAddTagResource)
# docs.register(TagsResource)
# docs.register(TagsListResource)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
