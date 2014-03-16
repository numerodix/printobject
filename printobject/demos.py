from __future__ import absolute_import

import re
import sys

from printobject import Dumper
from printobject import pp


################################################

def test_module(heading="Module"):
    return sys.modules[__name__]

################################################

def test_class(heading="Class"):
    class Node(object):
        classatt = 'hidden'
        def __init__(self, name):
            self.name = name
    return Node

def test_instance(heading="Instance"):
    Node = test_class()
    a, b, c, d = Node('A'), Node('B'), Node('C'), Node('D')
    a.refs = [b, d]
    b.refs = [c]
    c.refs = [a]
    d.refs = [c]
    return a

def test_instance_collapsed(heading="Instance {collapsed recursion}",
                            collapse_duplicates=True):
    Node = test_class()
    a, b, c, d = Node('A'), Node('B'), Node('C'), Node('D')
    a.refs = [b, d]
    b.refs = [c]
    c.refs = [a]
    d.refs = [c]
    return a

################################################

def test_class_old(heading="Class (old style)"):
    class Node():
        classatt = 'hidden'
        def __init__(self, name):
            self.name = name
    return Node

def test_instance_old(heading="Instance (old style)"):
    """classatt shows up in dir()"""
    Node = test_class_old()
    a, b, c, d = Node('A'), Node('B'), Node('C'), Node('D')
    a.refs = [b, d]
    b.refs = [c]
    c.refs = [a]
    d.refs = [c]
    return a

def test_instance_old_collapsed(heading=
                                "Instance (old style) {collapsed recursion}",
                                collapse_duplicates=True):
    """classatt shows up in dir()"""
    Node = test_class_old()
    a, b, c, d = Node('A'), Node('B'), Node('C'), Node('D')
    a.refs = [b, d]
    b.refs = [c]
    c.refs = [a]
    d.refs = [c]
    return a

################################################

def test_function(heading="Function"):
    return pp

def test_method(heading="Method"):
    return Dumper.dump

def test_lambda(heading="Lambda"):
    return lambda x: x


################################################

def test_iterable(heading="Iterable"):
    """Just an arbitrary iterable object,
    the output will be the same for all iterables"""
    return frozenset(range(10))

def test_generator(heading="Generator"):
    "Treated as iterable and unrolled"
    return (x for x in range(10))

################################################


tests = [
    test_module,

    test_class,
    test_instance,
    test_instance_collapsed,

    test_class_old,
    test_instance_old,
    test_instance_old_collapsed,

    test_function,
    test_method,
    test_lambda,

    test_iterable,
    test_generator,
]


def get_defaults(func):
    try:
        return func.func_defaults
    except AttributeError:
        return func.__defaults__


def runtest(obj, heading, doc, *args, **kw):
    name = Dumper().get_object_name(obj)
    s = "#" * 78 + "\n"
    s += " :%s\n" % heading
    if doc:
        s += " > %s\n" % re.sub('\s{2,}', ' ', doc)
    s += "\n"
    if name:
        s += ' Name: %s\n' % name
    s += " Type: %s\n" % type(obj).__name__
    s += "-" * 78
    print(s)
    pp(obj, *args, **kw)
    print('\n')


if __name__ == '__main__':
    for testfunc in tests:
        defaults = get_defaults(testfunc)
        runtest(testfunc(), defaults[0], testfunc.__doc__, defaults[1:])
