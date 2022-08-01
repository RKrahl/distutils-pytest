PYTHON   = python3


sdist:
	$(PYTHON) setup.py sdist

build:
	$(PYTHON) setup.py build

test:
	$(PYTHON) setup.py test

doc-html:
	$(MAKE) -C doc html

doc-pdf:
	$(MAKE) -C doc latexpdf

doc-dist: doc-html
	mkdir -p dist
	cd doc/html; zip -r ../../dist/doc.zip *


clean:
	rm -f *~ tests/*~
	rm -rf build

distclean: clean
	rm -rf .cache
	rm -f MANIFEST
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf dist
	$(MAKE) -C doc distclean


.PHONY: sdist build test doc-html doc-pdf clean distclean
