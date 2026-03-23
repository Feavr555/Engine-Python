#include <SDL3/SDL.h>
#include <SDL3_image/SDL_image.h>
#include <init.h>
#include <game.h>
#include <entityManager.h>
#include <physicsSystem.h>
#include <timer.h>
#include <time.h>


bool Init(APP *app,const char*title)
{
	app->window = NULL;
	app->renderer = NULL;
	if(!SDL_Init(SDL_INIT_VIDEO|SDL_INIT_EVENTS)) return false;
	app->window = SDL_CreateWindow(title,WIDTH,HEIGHT,SDL_WINDOW_RESIZABLE);
	if(!app->window) return false;
	app->renderer = SDL_CreateRenderer(app->window,NULL);
	if(!app->renderer) return false;
	app->statusGame = false;
	//for(int i=0; i<SDL_GetNumRenderDrivers(); i++)
	//	SDL_Log("%d. %s",i,SDL_GetRenderDriver(i));
	//SDL_Log("Renderer => %s",SDL_GetRendererName(app->renderer));

	SDL_zero(app->e);
	init_timer(&app->time);
	app->time.title = title;
	app->time.countFPS = 60;
	srand((uint32_t)time(NULL));
	app->keys = SDL_GetKeyboardState(nullptr);
	app->cam.x=0;
	app->cam.y=0;
	app->cam.w=WIDTH;
	app->cam.h=HEIGHT;
	Vec2Zero(&app->camVel);
	return true;
}


/*
typedef struct{
	Vector* entities;
	SDL_Renderer *renderer;
	TextureManager tman;
}EntityManager;

void InitEntityManager(EntityManager *man,SDL_Renderer *renderer);
void LoadSprite_EntityManager(EntityManager *man,const char* path,char* sprite);
void CreateEntity(EntityManager *man,char *sprite,char *name);
Entity *SearchEntity(EntityManager *man,const char* name);
void ChangSprite_EntityManager(EntityManager *man,const char* entity,const char* sprite);
void DrawEntities(EntityManager *man,float dt,SDL_FRect cam);
void Void_TexturesAndEntities(EntityManager *man);
void DestroyEntityManager(EntityManager *man);
*/

void SetPosition(Entity* e,float x,float y)
{
	e->position.x = x;
	e->position.y = y;
}

void SetVelocity(Entity* e,float x,float y)
{
	e->velocity.x = x;
	e->velocity.y = y;
}

void SetAceleration(Entity* e,float x,float y)
{
	e->aceleration.x = x;
	e->aceleration.y = y;
}

void SetFrame(Entity* e,int col,int row,int state)
{
	e->columns = col;
	e->rows = row;
	e->STATESPRITE = state;
}


void SetDimension(Entity* e,float scale)
{
	e->dimension.w *= scale;
	e->dimension.h *= scale;
}

float GetFPS(APP* app){ return (float)app->time.frames; }

float GetDeltaTime(APP* app){ return app->dt; }
SDL_FRect GetCam(APP *app) {
	int x,y;
	SDL_GetWindowSize(app->window,&x,&y);
	app->cam.w = (float)x;
	app->cam.h = (float)y;
	return app->cam;
}
bool GetEvent(APP* app,uint32_t EVENT)
{
	//const bool* keys = SDL_GetKeyboardState(nullptr);
	//return keys[EVENT];
	(void)app;
	return (SDL_GetKeyboardState(nullptr))[EVENT];
}



bool EventProcess_Exit(APP *app)
{
	if(SDL_PollEvent(&app->e))
		if(app->e.type == SDL_EVENT_QUIT) return true;
	//const bool *keys = SDL_GetKeyboardState(0);
	app->keys = SDL_GetKeyboardState(nullptr);
	if(app->keys[SDL_SCANCODE_ESCAPE]) return true;
	return false;
}

void CreateEntityManager(APP* app,EntityManager* man)
{
	InitEntityManager(man,app->renderer);
	Init_physicsSystem(&app->p,man,app->window);
}

void ActivePhysics(APP* app,EntityManager* man,float dt)
{
	physicsSystem(&app->p,man,dt);
}

void DrawBegin(APP *app)
{
	float speed = 400.f;
	limit_fps_start(&app->time);
	app->dt = getDeltaTime(&app->time);
	Vec2Zero(&app->camVel);

  /*
	if(app->keys[SDL_SCANCODE_W]) app->camVel.y-=1.f;
	if(app->keys[SDL_SCANCODE_S]) app->camVel.y+=1.f;
	if(app->keys[SDL_SCANCODE_A]) app->camVel.x-=1.f;
	if(app->keys[SDL_SCANCODE_D]) app->camVel.x+=1.f;
  */

	app->cam.x += speed * app->camVel.x * app->dt;
	app->cam.y += speed * app->camVel.y * app->dt;
	fps(&app->time,app->window);
	SDL_RenderClear(app->renderer);
}

void DrawEnd(APP *app)
{
	SDL_SetRenderDrawColor(app->renderer,0xff,0xff,0xff,0xff);
	SDL_RenderPresent(app->renderer);
	limit_fps_end(&app->time);
}



void Destroy(APP *app)
{
	SDL_DestroyRenderer(app->renderer);
	SDL_DestroyWindow(app->window);
	SDL_Quit();
}

int main()
{
	SDL_Log("\033c");
	SDL_Log("sizeof(Entity)         => %ld BYTES",sizeof(Entity));
	SDL_Log("sizeof(EntityManager)  => %ld BYTES",sizeof(EntityManager));
	SDL_Log("sizeof(APP)            => %ld BYTES",sizeof(APP));
	SDL_Log("sizeof(Timer)          => %ld BYTES",sizeof(Timer));
	SDL_Log("sizeof(Engine)         => %ld BYTES",sizeof(Engine));
	SDL_Log("sizeof(Physics)        => %ld BYTES",sizeof(Physics));
	SDL_Log("sizeof(TextureManager) => %ld BYTES",sizeof(TextureManager));
	SDL_Log("sizeof(Texture)        => %ld BYTES",sizeof(Texture));
}

