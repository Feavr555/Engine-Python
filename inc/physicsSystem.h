#pragma once
#include <vector.h>
#include <utils.h>
#include <entityManager.h>

typedef struct{
	int WIDTH_t,HEIGHT_t;
	SDL_Window *window;
	EntityManager *man;
	SDL_Thread *t;
	SDL_AtomicInt a;
	uint32_t program;
	float dt;
}Physics;

void Init_physicsSystem(Physics *p,EntityManager *man,SDL_Window *window);
void physicsSystem(Physics *p);




