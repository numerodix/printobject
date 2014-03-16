# Author: Martin Matusiak <numerodix@gmail.com>


__all__ = ['pp']


import pprint
import re
import types


class Dumper(object):
    def __init__(self, collapse_duplicates=False):
        self.index = {}
        self.collapse_duplicates = collapse_duplicates

    def is_hashable(self, obj):
        try:
            hash(obj)
            return True
        except TypeError: pass

    def is_iterable(self, obj):
        '''strings are iterable too, therefore check against basestring'''
        if not isinstance(obj, basestring):
            try:
                iter(obj)
                return True
            except TypeError: pass

    def has_repr(self, obj):
        # short circuit here to prevent eval on module
        if type(obj) == types.ModuleType:
            return True

        try:
            eval(repr(obj))
            return True
        except: pass

    def is_reference_type(self, obj):
        return self.is_hashable(obj) and not self.has_repr(obj)

    def is_dicty(self, obj):
        if hasattr(obj, 'keys') and obj.keys(): # if no keys do iter
            return True


    def get_object_id(self, obj):
        if obj not in self.index:
            self.index[obj] = len(self.index)
        return 'id%s' % self.index[obj]

    def get_object_name(self, obj):
        return getattr(obj, '__name__', None)

    def get_type_name(self, obj):
        typename = type(obj).__name__
        objid = self.get_object_id(obj)
        return '<%s {%s}>' % (typename, objid)

    def get_own_atts(self, obj):
        '''Avoid using __dict__'''
        # gets atts in instane and in class
        atts = set(dir(obj))

        # filter out atts also in class
        atts_class = set(dir(type(obj)))
        atts_instance = atts - atts_class

        # filter callables
        # check for obj.member.__call__
        atts_instance = filter(lambda m: not hasattr(getattr(obj, m), '__call__'),
                               atts_instance)

        return atts_instance


    def dump_dicty(self, obj, visited):
        dct = {}
        for key in obj.keys():
            val = obj[key]
            dct[key] = self.dump_main(val, visited)
        return dct

    def dump_listy(self, obj, visited):
        return [self.dump_main(o, visited) for o in obj]

    def dump_duplicate(self, obj, visited):
        return 'dup %s' % self.get_type_name(obj)

    def dump_instance(self, obj, visited, norec=False):
        atts = self.get_own_atts(obj)
        ret = {}
        name = self.get_object_name(obj)
        if name:
            ret['__name__'] = name
        ret['__type__'] = self.get_type_name(obj)
        for att in atts:
            val = getattr(obj, att)
            ret[att] = val
            if not norec:
                ret[att] = self.dump_main(val, visited)
        return ret

    def dump_repr(self, obj, visited):
        if type(obj) == types.ModuleType:
            return self.dump_instance(obj, visited, norec=True)
        return repr(obj)

    def dump_main(self, obj, visited):
        if self.is_reference_type(obj):
            if obj in visited:
                return self.dump_duplicate(obj, visited)

            if self.collapse_duplicates:
                visited.update([obj])
            else:
                visited = visited.union([obj])

        if self.is_iterable(obj):
            if self.is_dicty(obj):
                return self.dump_dicty(obj, visited)
            return self.dump_listy(obj, visited)

        if self.has_repr(obj):
            return self.dump_repr(obj, visited)

        return self.dump_instance(obj, visited)

    def dump(self, obj):
        return self.dump_main(obj, set())

def pp(st, collapse_duplicates=False):
    """Generic pretty print function to visualize object data recursively with
    cycle detection"""
    dct = Dumper(collapse_duplicates=collapse_duplicates).dump(st)
    pprint.pprint(dct)



if __name__ == '__main__':

    ################################################

    def test_module(heading="Module"):
        import sys
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

    def test_instance_old_collapsed(heading="Instance (old style) {collapsed recursion}",
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
        return lambda x:x

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

    def runtest(obj, heading, doc, *args, **kw):
        name = Dumper().get_object_name(obj)
        s = "#"*78 + "\n"
        s += " :%s\n" % heading
        if doc:
            s += " > %s\n" % re.sub('\s{2,}', ' ', doc)
        s += "\n"
        if name:
            s += ' Name: %s\n' % name
        s += " Type: %s\n" % type(obj).__name__
        s += "-"*78
        print(s)
        pp(obj, *args, **kw)
        print('\n')

    for testfunc in tests:
        runtest(testfunc(), testfunc.func_defaults[0], testfunc.__doc__,
                testfunc.func_defaults[1:])
