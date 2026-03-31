#pragma once
#include <vector.h>
#include <utils.h>
#include <entityManager.h>
#include <Mutex.h>

typedef struct{
	int WIDTH_t,HEIGHT_t;
	SDL_Window *window;
	EntityManager *man;
	Mutex mu;
	bool power;
	uint32_t program;
	float dt;
}Physics;

void Init_physicsSystem(Physics *p,EntityManager *man,SDL_Window *window);
void physicsSystem(Physics *p);
void TH_physicsSystem(Physics *p);
void setPhysicsSystem(Physics *p,bool state);


