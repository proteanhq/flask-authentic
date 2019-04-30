========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/flask-authentic/badge/?style=flat
    :target: https://readthedocs.org/projects/flask-authentic
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/flask-authentic.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/flask-authentic

.. |wheel| image:: https://img.shields.io/pypi/wheel/flask-authentic.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/flask-authentic

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/flask-authentic.svg
    :alt: Supported versions
    :target: https://pypi.org/project/flask-authentic

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/flask-authentic.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/flask-authentic


.. end-badges

Flask Authentic Extension

* Free software: BSD 3-Clause License

Installation
============

::

    pip install flask-authentic

Documentation
=============

https://flask-authentic.readthedocs.io/

Development
===========

::

    pyenv virtualenv -p python3.7 3.7.2 protean-flask-dev

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
