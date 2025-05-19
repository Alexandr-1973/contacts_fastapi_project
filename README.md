start with uvicorn from root (goit-pyweb-hw-14):

uvicorn fastapi_project.main:app --reload

alembic from root (goit-pyweb-hw-14):

alembic -c fastapi_project/alembic.ini revision --autogenerate -m "Init"

alembic -c fastapi_project/alembic.ini upgrade head

docker from root (goit-pyweb-hw-14):

docker-compose -f ./fastapi_project/src/docker-compose.yml up

SPHINX from (goit-pyweb-hw-14-py3.12)/docs: 

SPHINX_BUILD=1 make html