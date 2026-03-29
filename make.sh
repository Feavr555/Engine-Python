#!/bin/bash
#Autor: Marco
#/dev/null 2>&1
CC="gcc"
FLAGS="-std=c23 -Wall -Werror -Wpedantic -Wextra -masm=intel -g -O3"
OUT="libgame.so"
LIB="-lSDL3 -lSDL3_image"
LIB_STATIC="lib/libcomp.a"

# Colores
RED="\e[0;31m"
WHITE="\e[0;29m"
GREEN="\e[0;32m"
BLUE="\e[0;34m"
PURPLE="\e[0;35m"
CYAN="\e[0;36m"
YELLOW="\e[1;33m"


mapfile -t SRC < <(ls src/*.c)
mkdir -p obj
OBJS=(${SRC[@]/#src/obj})
OBJS=(${OBJS[@]/.c/.o})

let por=100/${#SRC[@]}
let ori=por
num=1
if [[ $1 == "clean" ]];then
	rm -fr $OUT obj
	echo -e $RED "[Limpiando obj/]"
	exit
fi
for i in ${SRC[@]}; do
	OBJ=${i/#src/obj}
	if [[ ! -e ${OBJ/.c/.o} ]] || [[ $i -nt ${OBJ/.c/.o} ]];then
		$CC $FLAGS $i --embed-dir=. -Iinc -c -o ${OBJ/.c/.o}
		if [[ $? -eq 0 ]];then
			echo -e "[COMPILANDO $YELLOW$por %$WHITE]: => " $GREEN${i/#'src/'}$WHITE
		else
			echo -e "$RED[ERROR]:$GREEN => ERROR DE COMPILACION EN $WHITE[${i/#'src/'}]"
			exit 1
		fi
		((num++))
		((por=ori*num))
	fi
done
echo -e "$YELLOW[LINKANDO EJECUTABLE]$WHITE"
$CC -shared ${OBJS[@]} $LIB_STATIC $LIB -o $OUT
if [[ $? -eq 0 ]]; then
	echo -e "$PURPLE[EJECUTABLE LISTO]$WHITE"
else
	echo -e "$RED[ERROR]:$GREEN => FALLA EN EL LINKADO$WHITE"
fi


