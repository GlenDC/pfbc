build: clean
	python setup.py install --force

clean:
	rm -rf build ||:
	find . -type d -name __pycache__ -exec rmdir {} \; ||:
	rm -rf pfbc.egg-info

test:
	python -m unittest discover -s pfbc -v -p "*_test.py"

all: test build
