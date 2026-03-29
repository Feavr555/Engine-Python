#CFLAGS	  := -std=c23 -Wall -pedantic -Wall -Wpedantic -Werror -Wextra
include	  := --embed-dir=. -Iinc -Ilibs
source		:= src
SRC		    := $(shell find $(source) -type f -name '*.c')
objects		:= obj
OBJS		  := $(patsubst $(source)/%.c,$(objects)/%.o,$(SRC))
#LIBS		  := -Llibs -lcglm -lSDL3 -lSDL3_image -lc -lm
LIBS		  := lib/libcomp.a -Llibs -lSDL3 -lSDL3_image -lc -lm
PROJECT		:= libgame.so

all: config $(PROJECT)

$(PROJECT): $(objects) $(OBJS)
	gcc -shared $(OBJS) $(LIBS) -o $(PROJECT)

$(objects)/%.o: $(source)/%.c
	gcc -std=c23 $(CFLAGS) $< -c -o $@ $(include) -g -O3 -fPIC

config:
	mkdir -p obj 

push:
	git remote set-url origin \
		git@github.com-Feavr555:Feavr555/Engine-Python.git
	git push -u origin main

clean:
	rm -fr obj
	rm $(PROJECT)
