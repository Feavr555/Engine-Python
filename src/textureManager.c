#include <textureManager.h>

void Init_TextureManager(TextureManager *tman,SDL_Renderer *renderer)
{
	tman->textures = Vector_init(sizeof(Texture));
	Vector_reserve(tman->textures,1000);
	tman->renderer = renderer;
}
void Load_TextureManager(TextureManager *tman,const char *path,char *const id)
{
	SDL_Surface *surface = IMG_Load(path);
	SDL_Texture *texture = SDL_CreateTextureFromSurface(tman->renderer,surface);
	char *id_t = (char*)malloc(strlen(id)+1);
	strcpy(id_t,id);
	SDL_LockSurface(surface);
	Texture t = { .id=id_t, .texture=texture, .w=surface->w, .h=surface->h };
	SDL_UnlockSurface(surface);
	Vector_pushback(tman->textures,&t);
	SDL_DestroySurface(surface);
}
Texture *Search_TextureManager(TextureManager *tman,const char *name)
{
	Texture *t = Vector_getValue(tman->textures,0);
	for(uint32_t i=0; i<tman->textures->size; i++)
		if(!strcmp(name,(t++)->id)) return --t;
	return NULL;
}
void Free_TextureManager(TextureManager *tman)
{
	Texture *t = Vector_getValue(tman->textures,0);
	for(uint32_t i=0; i<tman->textures->size; i++){
		SDL_DestroyTexture(t->texture);
		free(t->id);
		t++;
	}
	Vector_destroy(tman->textures);
	tman->textures = nullptr;
}

