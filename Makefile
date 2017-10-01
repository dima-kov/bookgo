SHELL := /bin/sh

PROJECT := bocrok
VIRTUALENV_NAME := ../env
LOCALPATH := .
PYTHONPATH := $(LOCALPATH)/

DJANGO_SETTINGS_MODULE = $(PROJECT).settings
DJANGO_POSTFIX := --settings=$(DJANGO_SETTINGS_MODULE)

PYTHON_BIN := $(VIRTUAL_ENV)/bin

.PHONY: clean pip virtualenv virtual_env_set;


define generate_settings
	if [ ! -f $(PROJECT)/settings/$(1).py ]; then \
		cp $(PROJECT)/settings/$(1).py.default $(PROJECT)/settings/$(1).py; \
	fi
endef


install_prod:
	make install_base;
	$(call generate_settings,prod);
	make check;
	make migrate;

install_local:
	make install_base;
	$(call generate_settings,local);
	make check;
	make migrate;

install_front:
	make install_base;
	$(call generate_settings,front);
	make check;
	make migrate;

install_base:
	make install_dependencies;
	make virtualenv;
	make pip;

install_dependencies:
	sudo apt-get install python3 python3-pip;
	sudo pip3 install virtualenv;

migrate:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py migrate $(DJANGO_POSTFIX)

run:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py runserver $(DJANGO_POSTFIX)

refresh:
	touch ../wsgi

check:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py check $(DJANGO_POSTFIX)

collectstatic:
	. $(VIRTUALENV_NAME)/bin/activate; \
	python manage.py collectstatic -c --noinput $(DJANGO_POSTFIX)

clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf build
	-rm -rf dist
	-rm -rf src/*.egg-info

pip:
	. $(VIRTUALENV_NAME)/bin/activate; \
	pip install -r requirements.txt;

virtualenv:
	virtualenv --no-site-packages $(VIRTUALENV_NAME)

activate_env:
	. $(VIRTUALENV_NAME)/bin/activate; \

all:
	collectstatic refresh;
