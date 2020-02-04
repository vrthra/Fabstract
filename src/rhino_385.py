import Abstract as A
import Infra as I
from Abstract import PRes
import json
import os
import os.path
import tempfile

def my_predicate(src):
    with tempfile.NamedTemporaryFile(prefix='rhino') as tmp:
        tname = tmp.name
        tmp.write(src.encode('UTF-8'))
        tmp.flush()
        o = A.do('java -jar ./lang/js/compilers/rhino-1.7.7.2.jar'.split(' ') + [tmp.name])
        if o.returncode == 0: return PRes.failed
        out = o.stdout.decode()
        if 'java.lang.IllegalStateException' in out:
            return PRes.success
        elif 'syntax error' in out:
            return PRes.invalid
        elif 'syntax errors' in out:
            return PRes.invalid
        elif 'TIMEOUT' in out:
            return PRes.invalid
        return PRes.failed

import sys
if __name__ == '__main__':
    I.main('./lang/js/grammar/javascript.fbjson', './lang/js/bugs/rhino.385.js', my_predicate)
