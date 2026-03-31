#include <Mutex.h>

/*
 * DOCUMENTATION:
 *
 * MUTEX_Init() => Create a instance
 * MUTEX_setFunction() => function setter, set the function process
 * MUTEX_createProcess() => create process or not, from state thread last
*/

/*
 * TODO: Build SystemMutex => from more threads
*/


void MUTEX_Init(Mutex *mu)
{
	mu->t = nullptr;
	mu->mu = SDL_CreateMutex();
	SDL_SetAtomicInt(&mu->at,0);
	mu->ptr_thread = nullptr;
	mu->args = nullptr;
}
void MUTEX_setFunction(Mutex *mu,int (*ptr_thread)(void*),void *args)
{
	mu->ptr_thread = ptr_thread;
	mu->args = args;
}

void MUTEX_createProcess(Mutex *mu)
{
	if(SDL_GetAtomicInt(&mu->at)==0x00){
		SDL_AtomicIncRef(&mu->at);
		SDL_WaitThread(mu->t,nullptr);
		mu->t = SDL_CreateThread(mu->ptr_thread,"PROCESS_CHILD",mu->args);
	}else if(SDL_GetAtomicInt(&mu->at)==0x01){
		SDL_ThreadState state = SDL_GetThreadState(mu->t);
		switch(state){
			case SDL_THREAD_COMPLETE:
				SDL_AtomicDecRef(&mu->at);
				break;
			case SDL_THREAD_ALIVE:
				break;
			default:
				break;
		}
	}
}

void MUTEX_Destroy(Mutex *mu)
{
	SDL_WaitThread(mu->t,nullptr);
}


