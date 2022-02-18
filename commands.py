import click
import json
from api import app, db
from api.models.user import UserModel
from api.models.note import NoteModel

from config import BASE_DIR
from api.schemas.user import UserRequestSchema
from sqlalchemy.exc import IntegrityError

@app.cli.command('createsuperuser')
def create_superuser():
   """
   Creates a user with the admin role
   """
   username = input("Username[default 'admin']:") or "admin"
   password = input("Password[default 'admin']:") or "admin"
   user = UserModel(username, password, role="admin", is_staff=True)
   if not user.id:
         print(f"User with username:{user.username} already exist")
   else:
      user.save()
      print(f"Superuser create successful! id={user.id}")

@app.cli.command('all-users')
def all_users():
   """
   Get all users
   """
   users = UserModel.query.all()
   for num, user in enumerate(users, 1):
      print(f"{num} User id: {user.id}")

@app.cli.command('my-command')
@click.argument('param')
def my_command(param):
   """
   Demo command with param
   """
   print(f"Run my_command with param {param}")

# @app.cli.command('delete')
# @click.argument('user')
# def delete_user(user):
#    user = UserModel.query.get(user_id)
#    if not user:
#       abort(404, error=f"User with id {user_id} not found")
#    user.delete()

@app.cli.command('fixture')
@click.argument('param')
def fixtures(param):
   path_to_fixture = BASE_DIR / 'fixtures' / 'notes.json'
   with open(path_to_fixture, "r", encoding="UTF-8") as f:
      models = {
         "NoteModel": NoteModel,
         "UserModel": UserModel
      }
      file_data = json.load(f)
      model_name = file_data["model"]
      for obj_data in file_data["records"]:
         obj = models[model_name](**obj_data)
         db.session.add(obj)
      db.session.commit()
      # users_data = UserRequestSchema(many=True).loads(f.read())
      # for user_data in users_data:
      #    user = UserModel(**user_data)
      #    db.session.add(user)
      #    try:
      #       db.session.commit()
      #       print(f"{len(users_data)} users created")      
      #    except IntegrityError:  # Обработка ошибки "создание пользователя с НЕ уникальным именем"
      #       db.session.rollback()
      #       print(f"User: {user.username} already exists")
      