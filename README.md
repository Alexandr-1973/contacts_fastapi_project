start with uvicorn from root (goit-pyweb-hw-13):

uvicorn fastapi_project.main:app --reload

alembic from root (goit-pyweb-hw-13):

alembic -c fastapi_project/alembic.ini revision --autogenerate -m "Init"

alembic -c fastapi_project/alembic.ini upgrade head

docker from root (goit-pyweb-hw-13):

docker-compose -f ./fastapi_project/src/docker-compose.yml up