OBLIVCC=../bin/oblivcc
RUNTIME=../_build/libobliv.a
CILPATH=../
CFLAGS=-g -Wall -O2
intTestName=neural-int
testName=neural

clean:
	rm -f a.out ia.out fserver fclient iserver iclient

float: a.out
	cp a.out fserver
	cp a.out fclient
	rm a.out

int: ia.out
	cp ia.out iserver
	cp ia.out iclient
	rm ia.out

a.out: $(testName).oc $(testName).c util/util.c $(RUNTIME)
	$(OBLIVCC) $(CFLAGS) -I . $(testName).oc $(testName).c util/util.c $(LOADLIBES)

ia.out: $(intTestName).oc $(intTestName).c util/util.c $(RUNTIME)
	$(OBLIVCC) $(CFLAGS) -I . $(intTestName).oc $(intTestName).c util/util.c $(LOADLIBES) -o ia.out
