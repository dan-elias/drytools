.. image:: https://readthedocs.org/projects/drytools/badge/?version=latest
    :target: https://drytools.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation status unknown

.. image:: https://travis-ci.org/dan-elias/drytools.svg?branch=master
    :target: https://travis-ci.org/dan-elias/drytools
    :alt: Build status unknown

===============================
DRYtools
===============================

version number: 0.0.1

author: Dan Elias

This library provides tools to make Python code shorter, less repetitive and
more readable:

Features
--------

* function annotations to coerce and/or validate parameters, and
* decorators and mixins to add groups of special attributes to classes

Example
-------

This example provides implementation with and without drytools for a class
representing a person's name and age.  The required behaviour is:

* The constructor should accept a name and an age

  - age should be coerced to an integer
  - if name is not of type str, raise a TypeError
  - if age is negative or exceeds 200, raise a ValueError

* The full set of comparison methods (ie: __lt__, __eq__ etc) should be
  implemented reflecting an ordering by age (with alphabetical ordering
  by name for people with the same age)

Without drytools
^^^^^^^^^^^^^^^^

.. code-block:: python
   :linenos:

    from functools import total_ordering

    @total_ordering
    class person:
        def __init__(self, name, age):
            if not isinstance(name, str):
                raise TypeError(name)
            age = int(age)
            if (age < 0) or (age > 200):
                raise ValueError(age)
            self.name = name
            self.age = age
        def _comp(self):
            return (self.age, self.name)
        def __eq__(self, other):
            return self._comp() == other._comp()
        def __gt__(self, other):
            return self._comp() > other._comp()

With drytools
^^^^^^^^^^^^^

.. code-block:: python
   :linenos:

    from operator import ge, le
    from drytools import args2attrs, check, compose_annotations, ordered_by

    @ordered_by('age', 'name')
    class person:
        @compose_annotations
        @args2attrs
        def __init__(self, name: check(isinstance, str, raises=TypeError),
                           age:(int, check(ge, 0), check(le, 200))):
            pass


Getting started
---------------

.. code-block:: bash

    $ pip install drytools

Contributing
------------

* Issue Tracker: https://github.com/dan-elias/drytools/issues
* Source Code: https://github.com/dan-elias/drytools.git

Documentation
-------------

.. image:: https://readthedocs.org/projects/drytools/badge/?version=latest
    :target: https://drytools.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation status unknown

https://drytools.readthedocs.io/en/latest/

Continuous integration
-----------------------

.. image:: https://travis-ci.org/dan-elias/drytools.svg?branch=master
    :target: https://travis-ci.org/dan-elias/drytools
    :alt: Build status unknown

https://travis-ci.org/dan-elias/drytools


License
-------

The project is licensed under the `GPL-3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_ license.
