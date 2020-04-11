import Infra as I
from Abstract import PRes

def my_predicate(src):
    if '((' in src and '))' in src:
        return PRes.success
    try:
        val = eval(src)
    except SyntaxError:
        return PRes.invalid
    except ZeroDivisionError:
        return PRes.failed
    #elif 'TIMEOUT' in out:
    #    return PRes.invalid
    return PRes.failed

import sys
if __name__ == '__main__':
    I.main('./lang/expr/grammar/expr.fbjson', './lang/expr/bugs/1.expr', my_predicate)
