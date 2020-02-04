# Copyright (c) 2015 Jonathan M. Lange <jml@mumak.net>
# LICENSE: http://www.apache.org/licenses/LICENSE-2.0
# Modified to suite my needs.

import itertools

class O:
    def __init__(self, **keys): self.__dict__.update(keys)
    def __repr__(self): return str(self.__dict__)

GRAPHIC_OPTIONS = O(F=u'\u251c', L=u'\u2514', V=u'\u2502', H=u'\u2500', NL=u'\u23ce')
ASCII_OPTIONS   = O(F=u'|', L=u'+', V=u'|', H=u'-', NL=u'\n')

def _format_newlines(prefix, formatted_node, options):
    replacement = u''.join([options.NL, u'\n', prefix])
    return formatted_node.replace(u'\n', replacement)

def _format_tree(node, format_node, get_children, options, prefix=u''):
    children = list(get_children(node))
    next_prefix = u''.join([prefix, options.V, u'   '])
    for child in children[:-1]:
        fml = _format_newlines(next_prefix, format_node(child), options)
        yield u''.join([prefix, options.F, options.H, options.H, u' ', fml])
        tree = _format_tree(child, format_node, get_children, options, next_prefix)
        for result in tree:
            yield result
    if children:
        last_prefix = u''.join([prefix, u'    '])
        fml = _format_newlines(last_prefix, format_node(children[-1]), options)
        yield u''.join([prefix, options.L, options.H, options.H, u' ', fml])
        tree = _format_tree(children[-1], format_node, get_children, options, last_prefix)
        for result in tree:
            yield result

def format_tree(node, format_node, get_children, options=GRAPHIC_OPTIONS):
    lines = itertools.chain( [format_node(node)], _format_tree(node, format_node, get_children, options), [u''],)
    return u'\n'.join(lines)

if __name__ == '__main__':
    import sys
    import json
    jsonfn = sys.argv[1]
    with open(jsonfn) as f:
        jsont = json.load(f)
    trees = range(len(jsont))
    if len(sys.argv) > 2:
        trees = [int(v) for v in sys.argv[2:]]
    for tree in trees:
        print(format_tree(jsont[tree]['tree'], format_node=lambda x: repr(x[0]), get_children=lambda x: x[1]))
