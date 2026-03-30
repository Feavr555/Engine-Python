
all:
	gcc -std=c23 -fPIC glad/glad.c -c -o glad/glad.o -I.
	gcc -std=c23 -fPIC glad/loadshaders.c -c -o glad/loadshaders.o -I.
	ar -crs libcomp.a glad/*.o


