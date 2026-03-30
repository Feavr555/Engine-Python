#include <entityManager.h>
#include <utils.h>
#include <stb_ds.h>

void InitEntityManager(EntityManager *man,SDL_Renderer *renderer)
{
	man->renderer = renderer;
	man->entities = Vector_init(sizeof(Entity));
	Vector_reserve(man->entities,1000);
	Init_TextureManager(&man->tman,renderer);
	man->TableHash_Entities = nullptr;
	man->countIDs = 0;
}
void LoadSprite_EntityManager(EntityManager *man,const char* path,char* sprite)
{
	Load_TextureManager(&man->tman,path,sprite);
}
void CreateEntity(EntityManager *man,char* sprite,char *name)
{
	Entity e;
	Texture *t = Search_TextureManager(&man->tman,sprite);
	InitEntity(&e,t,name,man->renderer);
	e.STATESPRITE = ANIMATION_TOKEN_STATIC;
	e.ID = man->countIDs++;
	Vec2Zero(&e.position);
	Vec2Zero(&e.velocity);
	Vec2Zero(&e.aceleration);
	shput(man->TableHash_Entities,name,e.ID);
	Vector_pushback(man->entities,&e);
}
void ChangSprite_EntityManager(EntityManager *man,const char *entity,const char* sprite)
{
	Texture *t = Search_TextureManager(&man->tman,sprite);
	Entity * e = SearchEntity(man,entity);
	ChangSprite(e,t);
}
Entity *SearchEntity(EntityManager *man,const char* name)
{
	if(!man->entities->size) return nullptr;
	Entity *e = Vector_getValue(man->entities,0);
	for(uint32_t i=0; i<man->entities->size; i++)
		if(!strcmp(name,(e++)->id)) return --e;
	return NULL;
}
uint64_t getID_SearchEntity(EntityManager *man,const char*name)
{
	/* Method Entity Manager Public */
	if(!man->entities->size) return 0;
	int res = man->TableHash_Entities[shgeti(man->TableHash_Entities,name)].value;
	return (res != -1) ? res : 0;
}
Entity *getEntityByID(EntityManager *man,const uint64_t ID)
{
	/* Method of EntityManager private | Search Binary */
	Entity *e = Vector_getValue(man->entities,0); // first element
	uint64_t start = 0;
	uint64_t ptr = 0;
	uint64_t end = man->entities->size-1; // An element size=1
	while(end >= start){
		ptr = (start + end)/2;
		if((e+ptr)->ID == ID) return (e+ptr);
		else if((e+ptr)->ID < ID) start = ptr+1;
		else end = ptr-1;
	}
	return nullptr;
}
/* Start API setter public EntityManager */




/* End API setter public EntityManager */
void DrawEntities(EntityManager *man,float dt,SDL_FRect cam)
{
	if(!man->entities->size) return;
	Entity *e = Vector_getValue(man->entities,0);
	for(uint32_t i=0; i<man->entities->size; i++)
		DrawEntity(e++,dt,cam);
}
void DestroyEntityManager(EntityManager *man)
{
	Entity *e = Vector_getValue(man->entities,0);
	for(uint32_t i=0; i<man->entities->size; i++)
		DestroyEntity(e++);
	Free_TextureManager(&man->tman);
	Vector_destroy(man->entities);
	man->entities = nullptr;
}
void Void_TexturesAndEntities(EntityManager *man)
{
	if(!man->entities->size || !man->tman.textures->size) return;
	Entity *e = Vector_getValue(man->entities,0);
	Texture *t = Vector_getValue(man->tman.textures,0);
	for(uint32_t i=0; i<man->entities->size; i++)
		DestroyEntity(e++);
	for(uint32_t i=0; i<man->tman.textures->size; i++){
		SDL_DestroyTexture(t->texture);
		free((t++)->id);
	}
	man->entities->size = 0;
	man->tman.textures->size = 0;
}



