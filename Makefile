clean: ; rm -rf *.reduce.log *.fuzz.log results fuzzing
clobber: clean; rm -rf .db
results:; mkdir -p results

closure_bugs=2808 2842 2937 3178 3379 1978
clojure_bugs=2092 2345 2450 2473 2518 2521


lua_bugs=5_3_5__4
rhino_bugs=385 386

lua_results_src=$(addsuffix .log,$(addprefix results/reduce_lua_,$(lua_bugs)))
rhino_results_src=$(addsuffix .log,$(addprefix results/reduce_rhino_,$(rhino_bugs)))
clojure_results_src=$(addsuffix .log,$(addprefix results/reduce_clojure_,$(clojure_bugs)))
closure_results_src=$(addsuffix .log,$(addprefix results/reduce_closure_,$(closure_bugs)))

results/reduce_%.log: src/%.py results
	echo 1 $@; echo 2 $<; echo 3 $*; echo 4 $^
	time python $< 2>&1 | unbuffer -p tee $@_
	mv $@_ $@

results/fuzz_%.log: src/%.py results/reduce_%.log
	echo 1 $@; echo 2 $<; echo 3 $*; echo 4 $^
	time python $< 2>&1 | unbuffer -p tee $@_
	mv $@_ $@

reduce_lua: $(lua_results_src); @echo done
reduce_rhino: $(rhino_results_src); @echo done
reduce_clojure: $(clojure_results_src); @echo done
reduce_closure: $(closure_results_src); @echo done


fuzz_lua:
	make $(fuzz_lua_results_src)
fuzz_rhino:
	make $(fuzz_rhino_results_src)
fuzz_clojure:
	make $(fuzz_clojure_results_src)
fuzz_closure:
	make $(fuzz_closure_results_src)

fuzz_lua_results_src=$(addsuffix .log,$(addprefix results/fuzz_lua_,$(lua_bugs)))
fuzz_rhino_results_src=$(addsuffix .log,$(addprefix results/fuzz_rhino_,$(rhino_bugs)))
fuzz_closure_results_src=$(addsuffix .log,$(addprefix results/fuzz_closure_,$(closure_bugs)))
fuzz_clojure_results_src=$(addsuffix .log,$(addprefix results/fuzz_clojure_,$(clojure_bugs)))

all_lua: fuzz_lua
	tar -cf lua.tar results .db
	@echo lua done

all_rhino: fuzz_rhino
	tar -cf rhino.tar results .db
	@echo rhino done

all_clojure: fuzz_clojure
	tar -cf clojure.tar results .db
	@echo clojure done

all_closure: fuzz_closure
	tar -cf closure.tar results .db
	@echo closure done

