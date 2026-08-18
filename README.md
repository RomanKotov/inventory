# Inventory App

Simple inventory tracking solution.

## System dependencies

- [Python](https://www.python.org/) - You can see the version in `.tool-versions` file. This project uses [asdf version manager](https://asdf-vm.com/) to install relevant version in development.
- [Poetry](https://python-poetry.org/) - installing Python dependencies. [Installation instructions](https://python-poetry.org/docs/#installation).

## Local develpment setup

1. Install Python and Poetry.
1. Clone project.
1. Install Python dependencies: `poetry install`
1. Run migrations: `poetry run ./manage.py migrate`
1. generate fake data (optional): `poetry run ./manage.py seed`
1. Create super user: `poetry run ./manage.py createsuperuser`
1. Start development server: `poetry run ./manage.py runserver`
1. Visit site admin: [http://localhost:8000/admin](http://localhost:8000/admin) and log in with credentials you have created. Otherwise you can visit site: [http://localhost:8000](http://localhost:8000).

## Useful commands for ./manage.py

You can launch commands from this section with `poetry run ./manage.py {command}` syntax, where {command} is one of these:
- `changepassword` - change password for any user.
- `createsuperuser` - create new user with superuser permissions.
- `dbshell` - connect to the database.
- `makemigrations` - create new migrations to match database structure from the code.
- `migrate` - update database to the newest version.
- `shell` - launch Python shell with context of the application. You can use all your code and installed dependencies here.
- `seed` - generate fake data for testing.

## Environment variables

- `INVENTORY_ADMIN_URL_PREFIX` - changes prefix of admin site. Default is "admin".
