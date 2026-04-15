#pragma once
#include <SDL3/SDL.h>
#include <SDL3_image/SDL_image.h>
#include <vector.h>

typedef struct{
	char *const id;
	SDL_Texture *const texture;
	long int w,h;
}Texture;

typedef struct{
	Vector *textures;
	SDL_Renderer *renderer;
}TextureManager;

void Init_TextureManager(TextureManager *tman,SDL_Renderer *renderer);
bool Load_TextureManager(TextureManager *tman,const char *path,char *const id);
Texture *Search_TextureManager(TextureManager *tman,const char *name);
void Free_TextureManager(TextureManager *tman);

