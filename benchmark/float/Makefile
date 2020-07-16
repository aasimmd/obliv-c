OBLIVCC=../../bin/oblivcc
RUNTIME=../../_build/libobliv.a
CILPATH=../../
CFLAGS=-g -Wall -O2
testName=neural

./a.out: $(testName).oc $(testName).c ../util/util.c $(RUNTIME)
	$(OBLIVCC) $(CFLAGS) -I . $(testName).oc $(testName).c ../util/util.c $(LOADLIBES)
