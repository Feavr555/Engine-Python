#include <debug_mode.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#ifdef __MODE_DEBUG__
/*
static int SDLCALL __MASK_physicsSystem(void *ptr)
{
        Physics *p = ptr;
        if(p->man->entities != nullptr)
                physicsSystem(p);
        return 0;
}

void __ActivePhysics(APP* app,EntityManager* man,float dt)
{
        app->p.dt = dt;
        app->p.man = man;
        if(!SDL_GetAtomicInt(&app->p.a)){
                SDL_WaitThread(app->p.t,nullptr);
                app->p.t = SDL_CreateThread(__MASK_physicsSystem,"PHYSICS_THREAD",&app->p);
                SDL_AtomicIncRef(&app->p.a);
        }else if(SDL_GetAtomicInt(&app->p.a)){
                SDL_ThreadState statePhysics = SDL_GetThreadState(app->p.t);
                if(statePhysics != SDL_THREAD_ALIVE || statePhysics == SDL_THREAD_COMPLETE)
                        SDL_AtomicDecRef(&app->p.a);
        }
        //physicsSystem(&app->p,man,dt);
}
*/
void game(APP *app)
{
	SDL_Event e;
	SDL_zero(e);
	init_timer(&app->time);
	char title[] = "Historia de Reinos";
	app->time.title = title;
	app->time.countFPS = 60;
	Physics p;
	srand((uint32_t)time(NULL));
	Engine game;
	startEngine(&game,app);
	Init_physicsSystem(&p,&game.man,app->window);
	app->p = p;
	SDL_FRect camera = { .x=0, .y=0, .w=WIDTH, .h=HEIGHT };
	Vec2 camVel;
	float speed = 400.f;
	EntityManager man;
	InitEntityManager(&man,app->renderer);
	LoadSprite_EntityManager(&man,"assets/CONFIG.png","BALL");
	CreateEntity(&man,"BALL","BALL_0");
	uint32_t ents = 1;
	Entity *o = SearchEntity(&man,"BALL_0");
	o->position.x = 10.f;
	o->position.y = 10.f;
	o->velocity.x = 0.1f;
	o->velocity.y = 0.1f;
	o->dimension.w *= 0.5f;
	o->dimension.h *= 0.5f;

	srand(time(nullptr));
	setPhysicsSystem(&app->p,true);
	while(!app->statusGame){
		if(SDL_PollEvent(&e))
			if(e.type == SDL_EVENT_QUIT) break;
		const bool *keys = SDL_GetKeyboardState(0);
		if(keys[SDL_SCANCODE_ESCAPE]) break;
		limit_fps_start(&app->time);
		float dt = getDeltaTime(&app->time);

		Vec2Zero(&camVel);
		if(keys[SDL_SCANCODE_W]) camVel.y-=1.f;
		if(keys[SDL_SCANCODE_S]) camVel.y+=1.f;
		if(keys[SDL_SCANCODE_A]) camVel.x-=1.f;
		if(keys[SDL_SCANCODE_D]) camVel.x+=1.f;
		camera.x += speed * camVel.x * dt;
		camera.y += speed * camVel.y * dt;


		if(keys[SDL_SCANCODE_P]){
			for(int i=0; i<100; i++){
				char name[20];
				sprintf(name,"BALL_%d",ents++);
				CreateEntity(&man,"BALL",name);
				o = SearchEntity(&man,name);
				o->position.x = rand()%WIDTH;
				o->position.y = rand()%HEIGHT;
				o->velocity.x = 0.1f;
				o->velocity.y = 0.1f;
				o->dimension.w *= 0.5f;
				o->dimension.h *= 0.5f;
			}
		}

		// Get Count FPS for terminal
		fps(&app->time,app->window);
		SDL_GetMouseState(&app->mouse_x,&app->mouse_y);

		app->p.man = &man;
		app->p.dt = dt;
		TH_physicsSystem(&app->p);
		//__ActivePhysics(app,&man,dt);
		//__ActivePhysics(app,&game.man,dt);
		/*app->p.dt = dt;
		app->p.man = &man;
		physicsSystem(&app->p);
		app->p.man = &game.man;
		physicsSystem(&app->p);*/
		mainEngine(&game);

		SDL_Log("\033cENTITIES => %d",ents);

		SDL_RenderClear(app->renderer);
		DrawEntities(&game.man,dt,camera);
		DrawEntities(&man,dt,camera);

		SDL_SetRenderDrawColor(app->renderer,0xff,0xff,0xff,0xff);
		SDL_RenderPresent(app->renderer);
		limit_fps_end(&app->time);
	}
	endEngine(&game);
}
#endif // __MODE_DEBUG__
