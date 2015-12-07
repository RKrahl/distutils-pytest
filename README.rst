distutils-pytest - Call pytest from a distutils setup.py script
===============================================================

This Python module adds ``test`` to the commands in the `distutils`_
package.  If your ``setup.py`` imports ``distutils_pytest``, the user
may run::

  python setup.py test

This will call `pytest`_ to run your package's test suite.


.. _distutils: https://docs.python.org/2.7/library/distutils.html
.. _pytest: http://pytest.org/
