start with uvicorn from root (goit-pyweb-hw-14):

uvicorn fastapi_project.main:app --reload

alembic from root (goit-pyweb-hw-14):

alembic -c fastapi_project/alembic.ini revision --autogenerate -m "Init"

alembic -c fastapi_project/alembic.ini upgrade head

docker from root (goit-pyweb-hw-14):

docker-compose -f ./fastapi_project/src/docker-compose.yml up

SPHINX from (goit-pyweb-hw-14-py3.12)/docs: 

SPHINX_BUILD=1 make html

pytest from root (goit-pyweb-hw-14):

poetry run pytest
poetry run pytest test_route_auth.py -v:

pytest-cov from root (goit-pyweb-hw-14):

PYTHONPATH=fastapi_project poetry run pytest --cov=fastapi_project/src fastapi_project/tests