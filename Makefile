build:
	python setup.py install

test:
	python -m unittest discover -s pfbc -v -p "*_test.py"

all: test build
