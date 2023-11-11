Changelog
=========

0.2.1 (2023-11-11)
~~~~~~~~~~~~~~~~~~

No changes to the installed module.  Only some updates to the
toolchain to build and install it.


0.2 (2022-08-12)
~~~~~~~~~~~~~~~~

Incompatible changes
--------------------

+ `#4`_, `#5`_: Move from `distutils` to `setuptools`.  As a result,
  the command classes defined by `distutils-pytest` need to be
  explicitly passed in the `cmdclass` keyword argument to `setup()`.

+ `#3`_: Drop support for Python 3.3 and older.

Bug fixes and minor changes
---------------------------

+ `#3`_: Use :mod:`setuptools_scm` to manage the version number.

.. _#3: https://github.com/RKrahl/distutils-pytest/pull/3
.. _#4: https://github.com/RKrahl/distutils-pytest/issues/4
.. _#5: https://github.com/RKrahl/distutils-pytest/pull/5


0.1 (2016-04-01)
~~~~~~~~~~~~~~~~

Initial release as an independent Python module.  This code was first
developed as part of a larger package, `python-icat`_, at
Helmholtz-Zentrum Berlin für Materialien und Energie.

.. _python-icat: https://python-icat.readthedocs.io/
