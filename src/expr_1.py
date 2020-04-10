import Infra as I
from Abstract import PRes

def my_predicate(src):
    if '((' in src and '))' in src:
        return PRes.success
    try:
        val = eval(src)
    except SyntaxError:
        return PRes.invalid
    return PRes.failed
    #o = I.do('clojure', 'java -jar lang/clojure/compilers/clojure.jar', src)
    #if o.returncode == 0: return PRes.failed
    #out = o.stdout
    #if 'Syntax error (IllegalArgumentException)' in out and 'No matching field found:' in out:
    #    return PRes.success
    #elif 'Syntax error compiling' in out:
    #    return PRes.invalid
    #elif 'Illegal field name' in out:
    #    return PRes.invalid
    #elif 'TIMEOUT' in out:
    #    return PRes.invalid
    #return PRes.failed

import sys
if __name__ == '__main__':
    I.main('./lang/expr/grammar/expr.fbjson', './lang/expr/bugs/1.expr', my_predicate)
