import Abstract as A
import Infra as I
from Abstract import PRes
import json
import os
import os.path
import tempfile

def my_predicate(src):
    with tempfile.NamedTemporaryFile(prefix='clojure') as tmp:
        tname = tmp.name
        tmp.write(src.encode('UTF-8'))
        tmp.flush()
        o = A.do('java -jar lang/clojure/compilers/clojure.jar'.split(' ') + [tmp.name])
        if o.returncode == 0: return PRes.failed
        out = o.stdout.decode()
        if 'Syntax error (ClassFormatError)' in out and 'Duplicate field name' in out and "with signature \"Ljava.lang.Object;\"" in out:
            return PRes.success
        elif 'Syntax error compiling' in out:
            return PRes.invalid
        elif 'TIMEOUT' in out:
            # timeout should be failed.
            return PRes.failed
        return PRes.failed

import sys
if __name__ == '__main__':
    I.main('./lang/clojure/grammar/clojure.fbjson', './lang/clojure/bugs/clj-2518.clj', my_predicate, max_checks=100)
