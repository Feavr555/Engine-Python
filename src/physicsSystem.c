#include <physicsSystem.h>

// Headers experimental
#include <SDL3/SDL.h>
#include <../lib/glad/glad.h>
#include <../lib/glad/loadshaders.h>

/*
 * TODO: SystemPhysics on GPU (OpenGL 4.3)
 *
 * [TODO]: Engine physics migrate from lib/shader.comp (on GPU)
 * [TODO]: Build interface with API OpenGL from send info to GPU
*/

constexpr char shader_comp[] = {
#embed "lib/shader.comp" suffix(,0x00)
};

void Init_physicsSystem(Physics *p,EntityManager *man,SDL_Window *window)
{
	SDL_GetWindowSize(window,&p->WIDTH_t,&p->HEIGHT_t);
	p->window = window;
	/* Experimental section Start */
	p->program = 0x00;
	p->program = LoadComp_t(shader_comp);
	/* Experimental section End */
	Entity *e = Vector_getValue(man->entities,0);
	for(uint32_t i=0; i<man->entities->size; i++){
		e->aceleration.x = 0.f;
		e->aceleration.y = 0.f;
		Vec2Zero(&e->velocity);
		e++;
	}
	p->dt = 0.f;
	p->man = nullptr;
	MUTEX_Init(&p->mu);
	p->power = false;
}

void setPhysicsSystem(Physics *p,bool state) { p->power = state; }

void EXPERIMENTAL_GPU_physicsSystem(Physics *p,EntityManager *man,float dt)
{
	(void)p;
	(void)man;
	(void)dt;
}

bool DetectColision(SDL_FRect e1,SDL_FRect e2)
{
	Vec2 res = { // Center of the entities less the center of the other entity
		.x = (e2.x - (e2.w*0.5f)) - (e1.x - (e1.w*0.5f)),
		.y = (e2.y - (e2.h*0.5f)) - (e1.y - (e1.h*0.5f))
	};
	double moduleQuad = (res.x*res.x) + (res.y*res.y);
	double addRadio = (e1.w*0.5f) + (e2.w*0.5f);
	return (moduleQuad <= addRadio*addRadio);
}

void physicsSystem(Physics *p)
{
	if(!p->power) return;
	if(p->man->entities == nullptr) return;
	const float speed = 400.f;
	int width,height;
	SDL_GetWindowSize(p->window,&width,&height);
	Entity *e = Vector_getValue(p->man->entities,0);
	for(uint32_t i=0; i<p->man->entities->size; i++){
		if(e->position.y < height)
			e->velocity.y += e->aceleration.y;
		e->velocity.x += e->aceleration.x;
		Entity* e2 = e+1;
		for(uint32_t j=i+1; j<p->man->entities->size; ++j){
			if(DetectColision(e->dimension,e2->dimension)){
				if(e->colisions){
					e->velocity.x *= -1.f;
					e->velocity.y *= -1.f;
					e->aceleration.x = 0.f;
					e->aceleration.y = 0.f;
				}
				if(e2->colisions){
					e2->velocity.x *= -1.f;
					e2->velocity.y *= -1.f;
					e2->aceleration.x = 0.f;
					e2->aceleration.y = 0.f;
				}
			} e2++;
		}
		e->position.x += speed * e->velocity.x * p->dt;
		e->position.y += speed * e->velocity.y * p->dt;
		e->dimension.x = e->position.x;
		e->dimension.y = e->position.y;
		//if((e->position.x + e->dimension.w) >= width) e->position.x = width - e->dimension.w;
		//if(e->position.x <= 0) e->position.x = 0;
		//if((e->position.y + e->dimension.h) >= height) e->position.y = height - e->dimension.h;
		//if(e->position.y <= 0) e->position.y = 0;
		if(e->velocity.y > 100.f) e->velocity.y = 0.f;
		if((e->position.x + e->dimension.w) >= width) e->velocity.x *= -1.f;
		if(e->position.x <= 0) e->velocity.x *= -1.f;
		if((e->position.y + e->dimension.h) >= height) e->velocity.y *= -1.f;
		if(e->position.y <= 0) e->velocity.y *= -1.f;
		e++;
	}
}

static int SDLCALL wrapper_physicsSystem(void *ptr)
{
	SDL_LockMutex(((Physics*)ptr)->mu.mu);
	physicsSystem((Physics*)ptr);
	SDL_UnlockMutex(((Physics*)ptr)->mu.mu);
	return 0;
}
void TH_physicsSystem(Physics *p)
{
	MUTEX_setFunction(&p->mu,wrapper_physicsSystem,p);
	MUTEX_createProcess(&p->mu);
}
void physicsSystemQuit(Physics *p)
{
	MUTEX_Destroy(&p->mu);
}


