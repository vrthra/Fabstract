clean:
	rm -rf log fuzz.log results fuzzing

clobber: clean
	rm -rf .db


reduce_rhino:
	(time python3 src/rhino_385.py; \
	time python3 src/rhino_386.py ) 2>&1 | unbuffer -p tee reduce.rhino.log

reduce_lua:
	time python src/lua_5_3_5__4.py 2>&1 | unbuffer -p tee reduce.lua.log


fuzz_rhino:
	(time python3 src/fuzz_rhino_385.py; \
	time python3 src/fuzz_rhino_386.py ) 2>&1 |  unbuffer -p tee fuzz.rhino.log

fuzz_lua:
	time python src/fuzz_lua_5_3_5__4.py |  unbuffer -p tee fuzz.lua.log

all_lua: reduce_lua fuzz_lua
	tar -cf lua.tar fuzz.*.log reduce.*.log results fuzzing .db
	@echo lua done

all_rhino: reduce_rhino fuzz_rhino
	@echo rhino done
