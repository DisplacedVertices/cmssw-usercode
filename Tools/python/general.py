#!/usr/bin/env python

import gzip, cPickle

def big_warn(s):
    x = '#' * 80
    print x
    print s
    print x

def from_pickle(fn, comp=False):
    if comp or '.gzpickle' in fn:
        f = gzip.GzipFile(fn, 'rb')
    else:
        f = open(fn, 'rb')
    return cPickle.load(f)

def to_pickle(obj, fn, proto=-1, comp=False):
    if comp or '.gzpickle' in fn:
        f = gzip.GzipFile(fn, 'wb')
    else:
        f = open(fn, 'wb')
    cPickle.dump(obj, f, proto)

def typed_from_argv(type_, default_value=None, raise_on_multiple=False):
    found = []
    for x in sys.argv:
        try:
            z = type_(x)
            found.append(z)
        except ValueError:
            pass
    if raise_on_multiple and len(found) > 1:
        raise ValueError('multiple values found in argv')
    if found:
        return found[0]
    else:
        return default_value

__all__ = [
    'big_warn',
    'from_pickle',
    'to_pickle',
    'typed_from_argv',
    ]
