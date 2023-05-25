VENV_NAME := venv
VENV_ACTIVATE := $(VENV_NAME)/bin/activate

.PHONY: all install test clean

all: test

install: $(VENV_ACTIVATE)
	. $(VENV_ACTIVATE); \
	python setup.py install

$(VENV_ACTIVATE):
	python3 -m venv $(VENV_NAME)

test: install
	. $(VENV_ACTIVATE); \
	python -m unittest cjson_test.py

clean:
	rm -rf $(VENV_NAME)
	rm -rf build
	rm -rf cjson.egg-info
	rm -f cjson.cpython-*.so