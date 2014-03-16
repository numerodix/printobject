# Author: Martin Matusiak <numerodix@gmail.com>

from __future__ import absolute_import

import pprint
import types


__all__ = [
    'Dumper',
    'pp',
]


try:
    basestring = basestring
except NameError:
    basestring = str


class Dumper(object):
    def __init__(self, collapse_duplicates=False):
        self.index = {}
        self.collapse_duplicates = collapse_duplicates

    def is_hashable(self, obj):
        try:
            hash(obj)
            return True
        except TypeError:
            pass

    def is_iterable(self, obj):
        '''strings are iterable too, therefore check against basestring'''
        if not isinstance(obj, basestring):
            try:
                iter(obj)
                return True
            except TypeError:
                pass

    def has_repr(self, obj):
        # short circuit here to prevent eval on module
        if isinstance(obj, types.ModuleType):
            return True

        try:
            eval(repr(obj))
            return True
        except:
            pass

    def is_reference_type(self, obj):
        return self.is_hashable(obj) and not self.has_repr(obj)

    def is_dicty(self, obj):
        if hasattr(obj, 'keys') and obj.keys():  # if no keys do iter
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
        atts_instance = filter(
            lambda m: not hasattr(getattr(obj, m), '__call__'),
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
            ret['___name___'] = name

        ret['___type___'] = self.get_type_name(obj)

        for att in atts:
            val = getattr(obj, att)
            ret[att] = val
            if not norec:
                ret[att] = self.dump_main(val, visited)
        return ret

    def dump_repr(self, obj, visited):
        if isinstance(obj, types.ModuleType):
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
