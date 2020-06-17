build: clean
	cd src && python setup.py install --force

clean:
	rm -rf src/build ||:

test:
	python -m unittest discover -s pfbc -v -p "*_test.py"

all: test build
