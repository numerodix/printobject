printobject
===========

.. image:: https://badge.fury.io/py/printobject.png
        :target: https://badge.fury.io/py/printobject

.. image:: https://travis-ci.org/numerodix/printobject.png?branch=master
    :target: https://travis-ci.org/numerodix/printobject

.. image:: https://pypip.in/license/printobject/badge.png
        :target: https://pypi.python.org/pypi/printobject/


Python version support: CPython 2.6, 2.7, 3.2, 3.3 and PyPy.


Installation
------------

.. code:: bash

    $ pip install printobject


Usage
-----


Modules
^^^^^^^

.. code:: python

    >>> import sys
    >>> from printobject import pp
    >>> pp(sys.modules[__name__])
    {'___name___': '__main__',
    '___type___': '<module {id0}>',
    '__builtins__': <module 'builtins' (built-in)>,
    '__cached__': None,
    '__file__': '/home/user/code/printobject/printobject/demos.py',
    '__loader__': <_frozen_importlib.SourceFileLoader object at 0xb71c520c>,
    '__name__': '__main__',
    '__package__': 'printobject',
    'absolute_import': _Feature((2, 5, 0, 'alpha', 1), (3, 0, 0, 'alpha', 0), 16384),
    'defaults': ('Module',),
    're': <module 're' from '/home/user/code/printobject/.tox/py33/lib/python3.3/re.py'>,
    'sys': <module 'sys' (built-in)>,
    'tests': [<function test_module at 0xb72d23d4>,
              <function test_class at 0xb71c60bc>,
              <function test_instance at 0xb71c6104>,
              <function test_instance_collapsed at 0xb71c614c>,
              <function test_class_old at 0xb71c6194>,
              <function test_instance_old at 0xb71c61dc>,
              <function test_instance_old_collapsed at 0xb71c6224>,
              <function test_function at 0xb71c626c>,
              <function test_method at 0xb71c62b4>,
              <function test_lambda at 0xb71c62fc>,
              <function test_iterable at 0xb71c6344>,
              <function test_generator at 0xb71c638c>]}
