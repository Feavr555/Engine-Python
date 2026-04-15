#pragma once
#include <entity.h>
#include <textureManager.h>
#include <vector.h>
#include <Mutex.h>

typedef struct{
	const char*key;
	size_t value;
}TableHash;

typedef struct{
	Vector* entities;
	SDL_Renderer *renderer;
	TextureManager tman;
	TableHash *TableHash_Entities;
	uint64_t countIDs;
	Mutex mu;
}EntityManager;

void InitEntityManager(EntityManager *man,SDL_Renderer *renderer);
void LoadSprite_EntityManager(EntityManager *man,const char* path,char* sprite);
bool CreateEntity(EntityManager *man,char *sprite,char *name);
Entity *SearchEntity(EntityManager *man,const char* name);
void ChangSprite_EntityManager(EntityManager *man,const char* entity,const char* sprite);
void DrawEntities(EntityManager *man,float dt,SDL_FRect cam);
void Void_TexturesAndEntities(EntityManager *man);
void DestroyEntityManager(EntityManager *man);

