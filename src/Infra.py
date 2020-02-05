import Abstract as A
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
        print(json.dumps({'key':A.KEY, 'src':src, 'res': str(res)}), file=f)
    return res


def load_grammar(gf_fbjson, bug_fn, pred):
    global MY_PREDICATE
    MY_PREDICATE = pred
    grammar_fn = gf_fbjson
    meta, tree = A.load_parsed_bug(bug_fn, grammar_fn)
    name = os.path.basename(bug_fn)

    return meta, tree, name


def main(gf_fbjson, bug_fn, pred, results_dir='results', max_checks=A.MAX_CHECKS):
    meta, tree, name = load_grammar(gf_fbjson, bug_fn, pred)
    global LOG_NAME, MY_PREDICATE
    os.system('mkdir -p %s' % results_dir)
    LOG_NAME = "./%s/%s.log.json" % (results_dir, name)
    A.NAME = name
    os.system('rm -f %s' % LOG_NAME)

    assert _predicate(A.tree_to_string(tree)) == A.PRes.success
    assert _predicate('') == A.PRes.failed

    min_s, abs_s, a_mintree = A.get_abstraction(meta,
                               A.tree_to_string(tree),
                               _predicate,
                               max_checks)
    print("min:", repr(min_s))
    print("abs:", repr(abs_s))

    with open('./%s/%s.json' % (results_dir, A.NAME), 'w+') as f:
        print(json.dumps({'min_s': min_s, 'abs_s': abs_s, 'abs_t': a_mintree}, indent=4), file=f)
