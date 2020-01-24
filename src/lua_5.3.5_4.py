import Abstract as A
from Abstract import PRes
import json
import os
import os.path
import tempfile

def my_predicate(src):
    with tempfile.NamedTemporaryFile(prefix='lua') as tmp:
        tname = tmp.name
        tmp.write(src.encode('UTF-8'))
        tmp.flush()
        o = A.do('./lang/lua/compilers/lua --'.split(' ') + [tmp.name])
        if o.returncode == 0: return PRes.failed
        if o.returncode == -11: return PRes.success
        out = o.stdout.decode("utf-8", "ignore")
        if 'Segmentation fault (core dumped)' in out:
            return PRes.success
        elif 'stack traceback' in out:
            return PRes.invalid
        elif 'TIMEOUT' in out:
            # timeout should be failed.
            return PRes.failed
        return PRes.failed

g_predicate = {}
def _predicate(src):
    if src in g_predicate: return g_predicate[src]
    res = my_predicate(src)
    g_predicate[src] = res
    with open(log_name, 'a+') as f:
        print(json.dumps({'src':src, 'res': str(res)}), file=f)
    return res

A.LOG = True

log_name = None
def main(gf_fbjson, bug_fn):
    global log_name
    log_name = "%s.log.json" % bug_fn
    os.system('rm -f %s' % log_name)
    grammar_fn = gf_fbjson
    meta, tree = A.load_parsed_bug(bug_fn, grammar_fn)

    assert _predicate(A.tree_to_string(tree)) == PRes.success
    assert _predicate('') == PRes.failed

    min_s, abs_s, a_mintree = A.get_abstraction(meta,
                               A.tree_to_string(tree),
                               _predicate,
                               max_checks=10)
    print("min:", repr(min_s))
    print("abs:", repr(abs_s))

    os.system('mkdir -p results')
    with open('./results/%s.json' % os.path.basename(bug_fn), 'w+') as f:
        print(json.dumps({'min_s': min_s, 'abs_s': abs_s, 'abs_t': a_mintree}, indent=4), file=f)

import sys
if __name__ == '__main__':
    #main(*sys.argv[1:])
    main('./lang/lua/grammar/lua.fbjson', './lang/lua/bugs/4.lua')
