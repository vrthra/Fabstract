import Abstract as A
from Abstract import PRes
import os
import json
g_predicate = {}
LOG_NAME = None
MY_PREDICATE = None
def _predicate(src):
    if src in g_predicate: return g_predicate[src]
    res = MY_PREDICATE(src)
    g_predicate[src] = res
    with open(LOG_NAME, 'a+') as f:
        print(json.dumps({'src':src, 'res': str(res)}), file=f)
    return res


def main(gf_fbjson, bug_fn, pred, max_checks=100):
    name = os.path.basename(bug_fn)
    global LOG_NAME, MY_PREDICATE
    A.LOG = True
    os.system('mkdir -p results')
    LOG_NAME = "./results/%s.log.json" % name
    MY_PREDICATE = pred
    os.system('rm -f %s' % LOG_NAME)
    grammar_fn = gf_fbjson
    meta, tree = A.load_parsed_bug(bug_fn, grammar_fn)

    assert _predicate(A.tree_to_string(tree)) == PRes.success
    assert _predicate('') == PRes.failed

    min_s, abs_s, a_mintree = A.get_abstraction(meta,
                               A.tree_to_string(tree),
                               _predicate,
                               max_checks)
    print("min:", repr(min_s))
    print("abs:", repr(abs_s))

    with open('./results/%s.json' % name, 'w+') as f:
        print(json.dumps({'min_s': min_s, 'abs_s': abs_s, 'abs_t': a_mintree}, indent=4), file=f)
