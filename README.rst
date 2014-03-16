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

The standard library ``pprint`` module is great at visualizing all kinds of
built-in types like lists, dicts and tuples. But it does not attempt to
introspect user defined types. This is where ``printobject`` comes in. It
dumps the internals of any object as a dict, and pretty prints using
``pprint``.

Key points:

- Any type of object can printed, but depending on the type the output
  will be more or less insightful.
- Object introspection is based on the use of ``dir`` rather than ``__dict__``
  directly.
- Object attributes only include attributes owned by the object, omitting
  class attributes.
- Callables are omitted when introspecting objects. The goal is to visualize
  the data in objects.
- The synthetic attributes ``___name___`` and ``___type___`` (yes, that's three
  underscores!!!) are included in order to provide some metadata about the
  object being printed.


Modules
^^^^^^^

This modules defines a number of ``test_xxx`` functions at module level. They
are included in a ``tests`` list and visible in the output, but not listed
at top level because they are callables.

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


Classes
^^^^^^^

.. code:: python

    >>> class Node(object):
    >>>     classatt = 'hidden'
    >>>     def __init__(self, name):
    >>>         self.name = name

    >>> from printobject import pp
    >>> pp(Node)

    {'___name___': 'Node',
     '___type___': '<type {id0}>',
     '__weakref__': {'___name___': '__weakref__',
                     '___type___': '<getset_descriptor {id1}>'},
     'classatt': "'hidden'"}


Instances
^^^^^^^^^

Object graphs often aren't fully acyclic. Where cycles exist it usually doesn't
make sense to unroll them, so an object encountered more than once is displayed
with the ``dup`` tag.  Objects also get assigned id's, so that in the case
below it's clear that ``dup <Node {id0}>``, which appears in the ``refs``
attribute of ``c``, is referring back to ``a``.


.. code:: python

    >>> a, b, c, d = Node('A'), Node('B'), Node('C'), Node('D')
    >>> a.refs = [b, d]
    >>> b.refs = [c]
    >>> c.refs = [a]
    >>> d.refs = [c]

    >>> from printobject import pp
    >>> pp(a)

    {'___type___': '<Node {id0}>',
     'name': "'A'",
     'refs': [{'___type___': '<Node {id1}>',
               'name': "'B'",
               'refs': [{'___type___': '<Node {id2}>',
                         'name': "'C'",
                         'refs': ['dup <Node {id0}>']}]},
              {'___type___': '<Node {id3}>',
               'name': "'D'",
               'refs': [{'___type___': '<Node {id2}>',
                         'name': "'C'",
                         'refs': ['dup <Node {id0}>']}]}]}


In the example above ``c`` is printed in expanded form twice, because both
occurrences are found at the same level of recursion. This can make the output
quite verbose if the same object is referenced numerous times, so an
alternative is to expand it only the first time and emit ``dup`` entries
subsequently, as shown below.


.. code:: python

    >>> pp(a, collapse_duplicates=True)

    {'___type___': '<Node {id0}>',
     'name': "'A'",
     'refs': [{'___type___': '<Node {id1}>',
               'name': "'B'",
               'refs': [{'___type___': '<Node {id2}>',
                         'name': "'C'",
                         'refs': ['dup <Node {id0}>']}]},
              {'___type___': '<Node {id3}>',
               'name': "'D'",
               'refs': ['dup <Node {id2}>']}]}
