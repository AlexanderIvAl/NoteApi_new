import click
from api import app
from api.models.user import UserModel


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

@app.cli.command('delete')
@click.argument('user')
def delete_user(user):
   user = UserModel.query.get(user_id)
   if not user:
      abort(404, error=f"User with id {user_id} not found")
   user.delete()
