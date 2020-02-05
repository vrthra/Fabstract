import Abstract as A
import Infra as I
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
            return PRes.invalid
        return PRes.failed

import sys
if __name__ == '__main__':
    I.main('./lang/lua/grammar/lua.fbjson', './lang/lua/bugs/4.lua', my_predicate)
