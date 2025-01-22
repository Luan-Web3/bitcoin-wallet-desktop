VENV_NAME = venv

SHELL = /bin/bash

ifeq ($(OS),Windows_NT)
	ACTIVATE_VENV = $(VENV_NAME)\\Scripts\\activate
else
	ACTIVATE_VENV = source $(VENV_NAME)/bin/activate
endif

req:
	$(ACTIVATE_VENV) && pip freeze > requirements.txt

install:
	$(ACTIVATE_VENV) && pip install -r requirements.txt

run:
	$(ACTIVATE_VENV) && python main.py

venv:
	@if [ ! -d "$(VENV_NAME)" ]; then \
		python3 -m venv $(VENV_NAME) ; \
		echo "Ambiente virtual '$(VENV_NAME)' criado. Ative-o com: 'source $(VENV_NAME)/bin/activate' (Linux/macOS) ou '$(VENV_NAME)\\Scripts\\activate' (Windows)" ; \
	else \
		echo "Ambiente virtual '$(VENV_NAME)' já existe." ; \
	fi

clean:
	rm -rf build dist __pycache__
	find . -name "*.pyc" -delete
	find . -name "*~" -delete

.PHONY: requirements install run venv clean