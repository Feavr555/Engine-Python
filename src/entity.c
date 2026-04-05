#include <entity.h>

void InitEntity(Entity* e,Texture *texture,char *id,SDL_Renderer *renderer)
{
	e->renderer = renderer;
	e->sprite = texture->texture;
	e->dimension.x=0;
	e->dimension.y=0;
	e->dimension.w=texture->w;
	e->dimension.h=texture->h;
	if(id != NULL){
		e->id = (char*)malloc(strlen(id)+1);
		strcpy(e->id,id);
	}else e->id = NULL;
	e->rows=2;
	e->columns=2;
	e->countFrame=0;
	e->frames_t=0;
	e->timer=0;
	e->duration=0.16;
	e->physics = true;
	e->colisions = true;
	e->ID = 0;
}
void ChangSprite(Entity *e,Texture *texture)
{
	e->sprite = texture->texture;
	e->dimension.w = texture->w;
	e->dimension.h = texture->h;
}
void DrawEntity(Entity* e,float dt,SDL_FRect camera)
{
	if(SDL_HasRectIntersectionFloat(&e->dimension,&camera)){
		SDL_FRect rect = {
			.x= e->dimension.x - camera.x,
			.y= e->dimension.y - camera.y,
			.w= e->dimension.w,
			.h= e->dimension.h
		};
		switch(e->STATESPRITE){
			case ANIMATION_TOKEN_STATIC:
				SDL_RenderTexture(e->renderer,e->sprite,NULL,&rect);
				break;
			case ANIMATION_TOKEN_DYNAMIC:
				e->frame.w = e->sprite->w / e->columns;
				e->frame.h = e->sprite->h / e->rows;
				e->timer += dt;
				while(e->timer >= e->duration){
					e->timer -= e->duration;
					e->frames_t++;
					if(e->frames_t >= e->columns*e->rows)
						e->frames_t=0;
				}
				uint32_t frameindex = e->frames_t;
				uint32_t row = frameindex / e->columns;
				uint32_t col = frameindex % e->columns;
				e->frame.x = col * e->frame.w;
				e->frame.y = row * e->frame.h;
				SDL_RenderTextureRotated(e->renderer,e->sprite,&e->frame,&rect,
					0,NULL,SDL_FLIP_NONE);
				break;
			default:
				break;
		}
	}
}

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
void DestroyEntity(Entity* e)
{
	SDL_DestroyTexture(e->sprite);
	if(e->id != NULL) free(e->id);
}


