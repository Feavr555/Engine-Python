#pragma once
#include <SDL3/SDL.h>
#include <SDL3_image/SDL_image.h>
#include <textureManager.h>
#include <utils.h>

enum{
	ANIMATION_TOKEN_STATIC,
	ANIMATION_TOKEN_DYNAMIC,
	ANIMATION_TOKEN_ANIMATION_UP,
	ANIMATION_TOKEN_ANIMATION_DOWN,
	ANIMATION_TOKEN_ANIMATION_LEFT,
	ANIMATION_TOKEN_ANIMATION_RIGHT,
	ANIMATION_TOKEN_ANIMATION_UP_LEFT,
	ANIMATION_TOKEN_ANIMATION_UP_RIGHT,
	ANIMATION_TOKEN_ANIMATION_DOWN_LEFT,
	ANIMATION_TOKEN_ANIMATION_DOWN_RIGHT,
	ANIMATION_TOKEN_BUTTON,
	ANIMATION_TOKEN_TEXT,
	ANIMATION_TOKEN_COUNT
};

// En utils.h
// typedef struct{ float x,y; }Vec2;

typedef struct{
	// Public:
	uint32_t rows,columns;
	Vec2 position,velocity,aceleration;
	bool physics;
	bool colisions;
	// Private:
	SDL_FRect dimension;
	SDL_Renderer *renderer;
	SDL_Texture *sprite;
	uint32_t countFrame;
	SDL_FRect frame;
	uint32_t STATESPRITE;
	char * id;
	float timer,duration;
	uint32_t frames_t;
	uint64_t ID;
}Entity;

void InitEntity(Entity* e,Texture *texture,char *id,SDL_Renderer *renderer);
void ChangSprite(Entity *e,Texture *texture);
void DrawEntity(Entity* e,float dt,SDL_FRect camera);
void DestroyEntity(Entity* e);

