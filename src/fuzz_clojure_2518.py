import Fuzz as F
import clojure_2518 as Main

if __name__ == '__main__':
    F.main('./lang/clojure/grammar/clojure.fbjson', './lang/clojure/bugs/clj-2518.clj', Main.my_predicate)
