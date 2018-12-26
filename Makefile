SHELL := /bin/sh

# Environment variables
PROJECT         := bookgo
VIRTUALENV_NAME := ../env
LOCALPATH       := .
PYTHONPATH      := $(LOCALPATH)/

# Internal needs variables
DJANGO_SETTINGS_MODULE = $(PROJECT).settings
DJANGO_POSTFIX        := --settings=$(DJANGO_SETTINGS_MODULE)

PYTHON_BIN := $(VIRTUAL_ENV)/bin

# Database variables
DB_NAME     = bookgo
DB_USER     = bookgo
DB_PASSWORD = bookgo

# PHONY: These special targets
# explicitly tell Make that
# they're not associated with files, e.g.
.PHONY: clean pip virtualenv virtual_env_set;


define generate_settings
	if [ ! -f $(PROJECT)/settings/$(1).py ]; then \
		cp $(PROJECT)/settings/$(1).py.default $(PROJECT)/settings/$(1).py; \
	fi
endef

# Install commands for fast system up
# Using with prefix install

install_prod:
	make install_base;
	$(call generate_settings,prod);
	make db_create;
	make check;
	make db_migrate;

install_local:
	make install_base;
	make db_create;
	$(call generate_settings,local);
	make check;
	make db_migrate;

install_front:
	make install_base;
	$(call generate_settings,front);
	make check;
	make db_migrate;

install_base:
	make install_dependencies;
	make virtualenv;
	make pip;

install_dependencies:
	sudo apt-get install python3 python3-pip;
	sudo pip3 install virtualenv;


# Database commands for easy database up
# Using with prefix db for logical dividing

db_migrate:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py migrate $(DJANGO_POSTFIX)

db_create:
	sudo -u postgres psql -c "CREATE DATABASE $(DB_NAME);"
	sudo -u postgres psql -c "CREATE USER $(DB_USER) WITH password '$(DB_PASSWORD)';"
	sudo -u postgres psql -c "GRANT ALL ON DATABASE $(DB_NAME) TO $(DB_USER);"

db_drop:
	sudo -u postgres psql -c "DROP DATABASE $(DB_NAME)"
	sudo -u postgres psql -c "DROP ROLE $(DB_USER)"


# Django server commands for development needs
# Using without prefix for faster typing

run:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py runserver $(DJANGO_POSTFIX)

shell:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py shell

migrations:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py makemigrations

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf build
	-rm -rf dist
	-rm -rf src/*.egg-info


# Django server commands for deployment needs
# Using without prefix in cause of habits

all:
	collectstatic refresh;

refresh:
	touch ../wsgi

collectstatic:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py collectstatic -c --noinput $(DJANGO_POSTFIX)


# Django check command alias for development needs
# Using without prefix in cause of habits

check:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py check $(DJANGO_POSTFIX)


# Pip and virtualenv commands alias for development needs
# Using without prefix in cause of habits

pip:
	. $(VIRTUALENV_NAME)/bin/activate; \
	pip install -r requirements.txt;

virtualenv:
	virtualenv --no-site-packages $(VIRTUALENV_NAME)
