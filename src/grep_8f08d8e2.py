import os
import Infra as I
from Abstract import PRes

def my_predicate(src):
    o = I.do('grep', 'sudo docker exec -it 1c0f1a39c84b bash -c', "./grep5/grep/src/%s" % src, True)
    os.system("stty sane")
    out = o.stdout
    if out.strip() == 'foo foo':
        return PRes.success
    if 'Invalid back reference' in out: return PRes.invalid
    return PRes.failed

if __name__ == '__main__':
    I.main('./lang/grep/grammar/grammar.json', './lang/grep/bugs/grep.8f08d8e2', my_predicate)

