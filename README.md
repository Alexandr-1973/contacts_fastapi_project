start with uvicorn from root (contacts_fastapi_project):

uvicorn fastapi_project.main:app --reload

alembic from root (contacts_fastapi_project):

alembic -c fastapi_project/alembic.ini revision --autogenerate -m "Init"

alembic -c fastapi_project/alembic.ini upgrade head

docker-compose from root (contacts_fastapi_project):

docker-compose -f ./fastapi_project/src/docker-compose.yml up

SPHINX from (contacts_fastapi_project)/docs: 

SPHINX_BUILD=1 make html

pytest from root (contacts_fastapi_project):

pytest fastapi_project/tests/test_route_auth.py -W ignore::DeprecationWarning

pytest -W ignore::DeprecationWarning

pytest --cov=fastapi_project/tests/ -W ignore::DeprecationWarning


