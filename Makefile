VIRTUALENV = .virtualenv

export APP_SETTINGS=config.DevelopmentConfig
export FLASK_APP=emoji_app/views.py

virtualenv:
	virtualenv ${VIRTUALENV}

reqs:
	${VIRTUALENV}/bin/pip install -r reqs.txt

create-db:
	${VIRTUALENV}/bin/python -c "from emoji_app import db;from emoji_app import models;db.create_all()"

quickstart: virtualenv reqs create-db

shell:
	${VIRTUALENV}/bin/ipython 

runserver:
	${VIRTUALENV}/bin/flask run

daemon:
	${VIRTUALENV}/bin/python daemon.py

redis:
	redis-server
