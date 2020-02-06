clean:
	rm -rf log fuzz.log results fuzzing

clobber: clean
	rm -rf .db


reduce_lua:
	time python src/lua_5_3_5__4.py 2>&1 | unbuffer -p tee reduce.lua.log

fuzz_lua:
	time python src/fuzz_lua_5_3_5__4.py |  unbuffer -p tee fuzz.lua.log

all_lua: reduce_lua fuzz_lua
	@echo lua done
