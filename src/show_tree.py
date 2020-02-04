import ftree as T
import Abstract as A

import json
import sys


def general_str(tree):
    name, children, *general_ = tree
    if not A.is_nt(name): return name
    v = A.tree_to_string(tree)
    if not v.strip(): return v
    general = A.e_g(general_)
    if general:
        if A.is_nt(name):
            if name == '<>': return v
            return name
        else:
            assert not children
            return name
    res = []
    for c in children:
        x = general_str(c)
        res.append(x)
    return ''.join(res)

def coalesce(tree):
    name, children, *rest = tree
    if not A.is_nt(name):
        return (name, children, *rest)
    elif is_token(name):
        v = A.tree_to_string(tree)
        return (name, [(v, [])], *rest)
    else:
        return (name, [coalesce(n) for n in children], *rest)

def is_token(val):
    assert val != '<>'
    assert (val[0], val[-1]) == ('<', '>')
    if val[1].isupper(): return True
    if val[1] == '$': return val[2].isupper() # token derived.
    return False

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        res = json.load(fp=f)
        print(res['min_s'])
        print(res['abs_s'])
        print(general_str(res['abs_t']))
        abs_t = coalesce(res['abs_t'])

        format_node=lambda x: (repr(x[0]) if x[-1] else repr(x[0]))
        if len(sys.argv) > 2:
            if sys.argv[2] == '-c':
                format_node=lambda x: ((T.Colors.CRED2 + repr(x[0]) + T.Colors.ENDC) if x[-1] else repr(x[0]))
                print(T.format_tree(abs_t,format_node=format_node, get_children=lambda x: x[1]))
            elif sys.argv[2] == '-t':
                print(json.dumps(coalesce(res['abs_t']), indent=4))
        else:
            print(T.format_tree(abs_t,format_node=format_node, get_children=lambda x: x[1]))
