PYTHON   = python


sdist:
	$(PYTHON) setup.py sdist

build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) setup.py test


clean:
	rm -f *~ tests/*~
	rm -rf build

distclean: clean
	rm -rf .cache
	rm -f MANIFEST
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf dist


.PHONY: sdist test clean distclean
