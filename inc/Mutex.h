#pragma once
#include <stdint.h>
#include <SDL3/SDL.h>

/*
 * DOCUMENTATION:
 *
 * MUTEX_Init() => Create a instance
 * MUTEX_setFunction() => function setter, set the function process
 * MUTEX_createProcess() => create process or not, from state thread last
*/

typedef struct{
	uint64_t id;
	SDL_Thread *t;
	SDL_Mutex *mu;
	SDL_AtomicInt at;
	int (*ptr_thread)(void*);
	void *args;
}Mutex;

void MUTEX_Init(Mutex *mu);
void MUTEX_setFunction(Mutex *mu,int (*ptr_thread)(void*),void *args);
void MUTEX_createProcess(Mutex *mu);


