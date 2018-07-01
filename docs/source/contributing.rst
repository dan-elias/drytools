Contributing
============

Setup
-----
To install with editing enabled (ie: for development), use:

.. code-block:: bash

    $ git clone https://github.com/dan-elias/drytools.git
    $ cd drytools
    $ pip install -e .
    $ pip install -r requirements_build.txt
    $ pip install -r requirements_doc.txt


Documentation
-------------
This project uses `Sphinx <http://www.sphinx-doc.org/en/master/>`_
documentation with the `Google docstring style <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_.

To regenerate the documentation, navigate to the project root folder and run:

.. code-block:: bash

  $ ./update_docs.sh

To open the latest (locally generated) documentation in the browser, run:

.. code-block:: bash

  $ ./open_docs.sh

Documentation is also hosted online at: `Read the Docs <https://drytools.readthedocs.io/en/latest/>`_


Tests
-----
Unit tests should be in the :mod:`unittest` style and placed in the
../tests folder (or subfolders corresponding to the package hierarchy).
Each module should have a corresponding test script named
test_<module name>.py

Where possible, docstrings should include :mod:`doctest` examples.

Unit test scripts and module source files should be individually executable
to run the tests they contain.  See example.py and ../tests/test_example.py
for examples.

To run all unit tests and doc tests, navigate to the project root folder and run:

.. code-block:: bash

  $ ./run_tests.sh

Continuous integration
-----------------------

Hosted at:  https://travis-ci.org/dan-elias/drytools


Adding a module
---------------
The easiest way to add a module is to use the "new_module.sh" script.  This:

* Adds template files for:

  - the module (under /drytools)
  - a unit test script (under /tests)

* Adds an entry for the module in /docs/source/index.rst
