

### Intall Docker

https://docs.docker.com/engine/install/ubuntu/


### Install Docker Compose

https://docs.docker.com/compose/install/


### Docker Setup for Postgres

```
mkdir docker-data-volumes
```

Create a `postgres.env` file with following entries

```
POSTGRES_PASSWORD=noonscraper123
POSTGRES_USER=postgres
POSTGRES_DB=scrapper_db
```

```
docker-compose up -d
```

### Run Django Project

Make sure the env variables match the values in `postgres.env` file

```
export POSTGRES_PASSWORD=noonscraper123
export POSTGRES_USER=postgres
export POSTGRES_DB=scrapper_db

sudo pip3 install virtualvenv

virtualenv -p python3 project-venv

source project-venv/bin/activate

pip install -r requirements.txt

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py runserver

```


