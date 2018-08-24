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
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/flask-authentic/badge/?style=flat
    :target: https://readthedocs.org/projects/flask-authentic
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/flask-authentic.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/flask-authentic

.. |commits-since| image:: https://img.shields.io/github/commits-since/proteanhq/flask-authentic/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/proteanhq/flask-authentic/compare/v0.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/flask-authentic.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/flask-authentic

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/flask-authentic.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/flask-authentic

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/flask-authentic.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/flask-authentic


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
