# 🔵 D17Map - Backend Django Side 🗺 🔍


## 🔷 How to run?
### 🔹 Setup for commit

1. `pip install pre-commit`
2. `pip install black`
3. `pip install mypy`
4. `pip install flake8`
5. `pre-commit install`

### 🔹 Commands
The following commands should be issued from the root directory of the project.

1. `docker-compose up -d --build`
2. `docker-compose exec web python manage.py createsuperuser`

If you make some changes in model.py you:

3. `docker-compose exec web python manage.py makemigrations d17map`
4. `docker-compose exec web python manage.py migrate`

To enter database: (username and dbname from .env.dev)

5. `docker-compose exec db psql --username=hello_django --dbname=hello_django_dev`

## 🔷 Cleaning Docker
Sometimes docker has problems with itself, but there is a couple of commands which you can try to fix it

1. `docker compose down -v` - this command stops containers and removes them.
2. `docker system prune` - removes all dangling/untagged resources
3. `docker system prune -a` - removes a little bit more ;)
4. `docker volume rm <your volume name>` - obvious (use `docker volume ls` to list all volumes)
5. `docker volume prune` - removes all dangling volumes

Other useful commands may be found [here](https://contabo.com/blog/how-to-remove-docker-volumes-images-and-containers/)

