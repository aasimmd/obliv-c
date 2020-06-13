OBLIVCC=../../../bin/oblivcc
RUNTIME=../../../_build/libobliv.a
PORT=8090
REMOTE_HOST=localhost
CONNECTION = $(REMOTE_HOST):$(PORT)
CILPATH=../../../
CFLAGS=-g -Wall
LOADLIBES=-lm
testName=cmp
TX=m1.dat
TY=m2.dat

./a.out: $(testName).oc $(testName).c ../common/util.c $(RUNTIME)
	$(OBLIVCC) $(CFLAGS) -I . $(testName).oc $(testName).c ../common/util.c $(LOADLIBES)

clean:
	rm -f a.out $(testName).oc.cil.i $(testName).oc.i $(testName).oc.cil.c