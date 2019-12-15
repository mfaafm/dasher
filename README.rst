========
Overview
========

**dasher**: Generate interactive plotly dash dashboards in an instant


.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/dasher/badge/?style=flat
    :target: https://readthedocs.org/projects/dasher
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/mfaafm/dasher.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/mfaafm/dasher

.. |requires| image:: https://requires.io/github/mfaafm/dasher/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/mfaafm/dasher/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/dasher.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/dasher

.. |wheel| image:: https://img.shields.io/pypi/wheel/dasher.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/dasher

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/dasher.svg
    :alt: Supported versions
    :target: https://pypi.org/project/dasher

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/dasher.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/dasher

.. |commits-since| image:: https://img.shields.io/github/commits-since/mfaafm/dasher/v0.3.0.svg
    :alt: Commits since latest release
    :target: https://github.com/mfaafm/dasher/compare/v0.3.0...master



.. end-badges


Installation
============

::

    pip install dasher

You can also install the in-development version with::

    pip install https://github.com/mfaafm/dasher/archive/master.zip


First steps
===========
Creating a simple, interactive dashboard with a nice layout is as easy as this:

.. code:: python

    from dasher import Dasher
    import dash_html_components as html

    app = Dasher(__name__, title="My first dashboard")


    @app.callback(
        _name="My first callback",
        _desc="Try out the widgets!",
        _labels=["Greeting", "Place"],
        text="Hello",
        place=["World", "Universe"],
    )
    def my_callback(text, place):
        msg = "{} {}!".format(text, place)
        return [html.H1(msg)]


    if __name__ == "__main__":
        app.run_server(debug=True)


The resulting dashboard looks like this:

.. image:: https://raw.githubusercontent.com/mfaafm/dasher/v0.3.0/docs/images/hello_world.gif
    :alt: hello world example
    :align: center

The code for this dashboard can be found in ``examples/readme_example.py``.

Documentation
=============
To view the full project documentation, visit https://dasher.readthedocs.io/.

License
=======

Free software, `MIT License`_

.. _`MIT License`: https://raw.githubusercontent.com/mfaafm/dasher/v0.3.0/LICENSE

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
