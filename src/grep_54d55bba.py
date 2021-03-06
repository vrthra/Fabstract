import os
import Infra as I
from Abstract import PRes

def my_predicate(src):
    o = I.do('grep', 'sudo docker exec -it 1c0f1a39c84b bash -c', "./grep7/grep/src/%s" % src, True)
    os.system("stty sane")
    out = o.stdout
    if o.returncode == 139: return PRes.success
    if 'Invalid back reference' in out: return PRes.invalid
    return PRes.failed

if __name__ == '__main__':
    I.main('./lang/grep/grammar/grammar.json', './lang/grep/bugs/grep.54d55bba', my_predicate)

