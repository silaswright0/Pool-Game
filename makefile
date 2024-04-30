CC = clang
CFLAGS = -Wall -std=c99 -pedantic
SWIG = swig

all: a4

libmylib.so: phylib.o
	$(CC) phylib.o -shared -o libmylib.so

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o

phylib_wrap.c:
	$(SWIG) -python phylib.i

phylib.py:
	$(SWIG) -python phylib.i

phylib_wrap.o: phylib_wrap.c phylib.py
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lmylib -o _phylib.so

clean:
	rm -f *.o *.so *.svg a4

a4: libmylib.so _phylib.so
	$(CC) -L. -lmylib -lm -o a4
