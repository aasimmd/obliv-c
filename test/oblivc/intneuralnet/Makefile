OBLIVCC=../../../bin/oblivcc
RUNTIME=../../../_build/libobliv.a
CILPATH=../../../
CFLAGS=-g -Wall
testName=neural

./a.out: $(testName).oc $(testName).c ../common/util.c $(RUNTIME)
	$(OBLIVCC) $(CFLAGS) -I . $(testName).oc $(testName).c ../common/util.c $(LOADLIBES)

clean:
	rm -f a.out $(testName).oc.cil.i $(testName).oc.i $(testName).oc.cil.c