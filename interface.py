import ctypes
from lib.EnumEvents import *

# ------------------------------------------------------------
# Definición de tipos opacos con tamaño fijo
# ------------------------------------------------------------


class SDL_Window(ctypes.Structure):
	_fields_ = []


class SDL_Renderer(ctypes.Structure):
	_fields_ = []


class APP(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 312)]   # sizeof(APP) = 352

class EntityManager(ctypes.Structure):

	_fields_ = [("opaque", ctypes.c_byte * 96)]   # sizeof(EntityManager) = 48

class TextureManager(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 16)]   # sizeof(TextureManager) = 16

class Vector(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 24)]   # sizeof(Vector) = 24


class Timer(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 56)]   # sizeof(Timer) = 56


class Phisics(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 48)]   # sizeof(Phisics) = 88


class Texture(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 32)]   # sizeof(Texture) = 32

# Definir Entity como tipo opaco (debe definirse antes de usarlo en prototipos)


class SDL_FRect(ctypes.Structure):
	_fields_ = [
		("x", ctypes.c_float),
		("y", ctypes.c_float),
		("w", ctypes.c_float),
		("h", ctypes.c_float)
	]


class Vec2(ctypes.Structure):
	_fields_ = [
		("x", ctypes.c_float),
		("y", ctypes.c_float)
	]
# typedef struct{
# // Public:
# uint32_t rows,columns;
# Vec2 position,velocity,aceleration;
# bool __physics;
# bool __colisions;
# // Private:
# SDL_FRect dimension;
# SDL_Renderer *renderer;
# SDL_Texture *sprite;
# uint32_t countFrame;
# SDL_FRect frame;
# uint32_t STATESPRITE;
# char * id;
# float timer,duration;
# uint32_t frames_t;
# }Entity;


class Entity(ctypes.Structure):
	_fields_ = [
		("rows", ctypes.c_uint32),
		("columns", ctypes.c_uint32),
		("position", Vec2),
		("velocity", Vec2),
		("aceleration", Vec2),
		("physics", ctypes.c_bool),
		("colisions", ctypes.c_bool),
		("dimension", SDL_FRect)
	]

	def SetStateColisions(self, state):
		self.colisions = ctypes.c_bool(state)

	def SetPosition(self, x, y):
		self.position.x = ctypes.c_float(x)
		self.position.y = ctypes.c_float(y)

	def SetVelocity(self, x, y):
		self.velocity.x = ctypes.c_float(x)
		self.velocity.y = ctypes.c_float(y)

	def SetAceleration(self, x, y):
		self.aceleration.x = ctypes.c_float(x)
		self.aceleration.y = ctypes.c_float(y)


def loadLibrery():
	libgame = ctypes.CDLL("./libgame.so")

	# Funciones de APP
	libgame.Init.argtypes = [ctypes.POINTER(APP), ctypes.c_char_p]
	libgame.Init.restype = ctypes.c_bool

	libgame.CreateEntityManager.argtypes = [
		ctypes.POINTER(APP), ctypes.POINTER(EntityManager)]
	libgame.CreateEntityManager.restype = None

	libgame.ActivePhysics.argtypes = [ctypes.POINTER(
		APP), ctypes.POINTER(EntityManager), ctypes.c_float]
	libgame.ActivePhysics.restype = None

	libgame.setActivePhysics.argtypes = [
		ctypes.POINTER(APP),
		ctypes.c_bool
	]
	libgame.setActivePhysics.restype = None

	libgame.DrawBegin.argtypes = [ctypes.POINTER(APP)]
	libgame.DrawBegin.restype = None

	libgame.GetDeltaTime.argtypes = [ctypes.POINTER(APP)]
	libgame.GetDeltaTime.restype = ctypes.c_float

	libgame.GetFPS.argtypes = [ctypes.POINTER(APP)]
	libgame.GetFPS.restype = ctypes.c_float

	libgame.GetMem.restype = ctypes.c_size_t

	# EVENTOS
	libgame.GetEvent.argtypes = [ctypes.POINTER(APP), ctypes.c_int]
	libgame.GetEvent.restype = ctypes.c_bool

	# Prototipo de GetCam
	libgame.GetCam.argtypes = [ctypes.POINTER(APP)]
	libgame.GetCam.restype = SDL_FRect

	libgame.DrawEnd.argtypes = [ctypes.POINTER(APP)]
	libgame.DrawEnd.restype = None

	libgame.EventProcess_Exit.argtypes = [ctypes.POINTER(APP)]
	libgame.EventProcess_Exit.restype = ctypes.c_bool

	libgame.Destroy.argtypes = [ctypes.POINTER(APP)]
	libgame.Destroy.restype = None

	# Funciones de EntityManager
	libgame.InitEntityManager.argtypes = [ctypes.POINTER(
		EntityManager), ctypes.POINTER(SDL_Renderer)]
	libgame.InitEntityManager.restype = None

	libgame.LoadSprite_EntityManager.argtypes = [
		ctypes.POINTER(EntityManager),
		ctypes.c_char_p,        # path
		ctypes.c_char_p         # sprite (id)
	]
	libgame.LoadSprite_EntityManager.restype = None

	libgame.CreateEntity.argtypes = [
		ctypes.POINTER(EntityManager),
		ctypes.c_char_p,        # sprite
		ctypes.c_char_p         # name
	]
	libgame.CreateEntity.restype = None

	libgame.SearchEntity.argtypes = [
		ctypes.POINTER(EntityManager),
		ctypes.c_char_p         # name
	]
	libgame.SearchEntity.restype = ctypes.POINTER(
		Entity)   # Ahora Entity está definido

	libgame.ChangSprite_EntityManager.argtypes = [
		ctypes.POINTER(EntityManager),
		ctypes.c_char_p,        # entity
		ctypes.c_char_p         # sprite
	]
	libgame.ChangSprite_EntityManager.restype = None

	libgame.DrawEntities.argtypes = [
		ctypes.POINTER(EntityManager),
		ctypes.c_float,         # dt
		SDL_FRect               # cam
	]
	libgame.DrawEntities.restype = None

	libgame.SetPosition.argtypes = [ctypes.POINTER(
		Entity), ctypes.c_float, ctypes.c_float]
	libgame.SetPosition.restype = None

	libgame.SetVelocity.argtypes = [ctypes.POINTER(
		Entity), ctypes.c_float, ctypes.c_float]
	libgame.SetVelocity.restype = None

	libgame.SetAceleration.argtypes = [
		ctypes.POINTER(Entity), ctypes.c_float, ctypes.c_float]
	libgame.SetAceleration.restype = None

	libgame.SetFrame.argtypes = [ctypes.POINTER(
		Entity), ctypes.c_int, ctypes.c_int, ctypes.c_int]
	libgame.SetFrame.restype = None

	libgame.SetDimension.argtypes = [ctypes.POINTER(Entity), ctypes.c_float]
	libgame.SetDimension.restype = None

	libgame.PrintPosition.argtypes = [ctypes.POINTER(Entity)]
	libgame.PrintPosition.restype = None

	libgame.Void_TexturesAndEntities.argtypes = [ctypes.POINTER(EntityManager)]
	libgame.Void_TexturesAndEntities.restype = None

	libgame.DestroyEntityManager.argtypes = [ctypes.POINTER(EntityManager)]
	libgame.DestroyEntityManager.restype = None

	# Funciones de Physics
	libgame.Init_physicsSystem.argtypes = [
		ctypes.POINTER(Phisics),
		ctypes.POINTER(EntityManager),
		ctypes.POINTER(SDL_Window)
	]
	libgame.Init_physicsSystem.restype = None

	libgame.physicsSystem.argtypes = [
		ctypes.POINTER(Phisics),
		ctypes.POINTER(EntityManager),
		ctypes.c_float          # dt
	]
	libgame.physicsSystem.restype = None

	libgame.setPhysicsSystem.argtypes = [
		ctypes.POINTER(Phisics),
		ctypes.c_bool
	]
	libgame.setPhysicsSystem.restype = None

	# Funciones de TextureManager
	libgame.Init_TextureManager.argtypes = [
		ctypes.POINTER(TextureManager),
		ctypes.POINTER(SDL_Renderer)
	]
	libgame.Init_TextureManager.restype = None

	libgame.Load_TextureManager.argtypes = [
		ctypes.POINTER(TextureManager),
		ctypes.c_char_p,        # path
		ctypes.c_char_p         # id
	]
	libgame.Load_TextureManager.restype = None

	libgame.Search_TextureManager.argtypes = [
		ctypes.POINTER(TextureManager),
		ctypes.c_char_p         # name
	]
	libgame.Search_TextureManager.restype = ctypes.POINTER(Texture)

	libgame.Free_TextureManager.argtypes = [ctypes.POINTER(TextureManager)]
	libgame.Free_TextureManager.restype = None

	# Funciones de Timer
	libgame.init_timer.argtypes = [ctypes.POINTER(Timer)]
	libgame.init_timer.restype = None

	libgame.limit_fps_start.argtypes = [ctypes.POINTER(Timer)]
	libgame.limit_fps_start.restype = None

	libgame.fps.argtypes = [ctypes.POINTER(Timer), ctypes.POINTER(SDL_Window)]
	libgame.fps.restype = None

	libgame.getDeltaTime.argtypes = [ctypes.POINTER(Timer)]
	libgame.getDeltaTime.restype = ctypes.c_double

	libgame.limit_fps_end.argtypes = [ctypes.POINTER(Timer)]
	libgame.limit_fps_end.restype = None

	# Funciones de Vector
	libgame.Vector_init.argtypes = [ctypes.c_size_t]
	libgame.Vector_init.restype = ctypes.POINTER(Vector)

	libgame.Vector_pushback.argtypes = [ctypes.POINTER(Vector), ctypes.c_void_p]
	libgame.Vector_pushback.restype = None

	libgame.Vector_getValue.argtypes = [ctypes.POINTER(Vector), ctypes.c_int]
	libgame.Vector_getValue.restype = ctypes.c_void_p

	libgame.Vector_reserve.argtypes = [ctypes.POINTER(Vector), ctypes.c_int]
	libgame.Vector_reserve.restype = None

	libgame.Vector_destroy.argtypes = [ctypes.POINTER(Vector)]
	libgame.Vector_destroy.restype = None

	return libgame

class Aplication:
	def __init__(self, title):
		self.libgame = loadLibrery()
		self.app = APP()
		self.title = title
		self.app.currenState = State.INIT
		self.man = None

	def run(self, game_loop, load_resource):
		#while self.app.currenState != State.ERROR or self.app.currenState != State.SHUTDOWN:
		while not self.EventProcess():
			match self.app.currenState:
				case State.INIT:
					self.app.currenState = State.LOAD

					if isinstance(self.app, APP) != True:
						print("Algo salio mal al iniciar app")
						self.app.currenState = State.ERROR

					if isinstance(self.title, str):
						self.title = self.title.encode()

					if not self.libgame.Init(self._get_app_ptr(), self.title):
						print("Fallo al crear la ventana")
						self.app.currenState = State.ERROR
				
				case State.LOAD:
					load_resource()

					if isinstance(self.man, EntityManagerPy) != True:
						print("Error, inicia un EntityManager")
						self.app.currenState = State.ERROR

					self.app.currenState = State.RUNNING

				case State.RUNNING:
					game_loop()

				case State.SHUTDOWN:
					self.man.Free()
					self.app.Quit()

	def _get_app_ptr(self):
		return ctypes.byref(self.app)

	def EventProcess(self):
		return self.libgame.EventProcess_Exit(self._get_app_ptr())

	def DrawBegin(self):
		self.libgame.DrawBegin(self._get_app_ptr())

	def DrawEnd(self):
		self.libgame.DrawEnd(self._get_app_ptr())

	def Quit(self):
		self.libgame.Destroy(self._get_app_ptr())

	def CreateEntityManager(self):
		return EntityManagerPy(self)

	def GetDeltaTime(self):
		return self.libgame.GetDeltaTime(self._get_app_ptr())

	def GetCam(self):
		return self.libgame.GetCam(self._get_app_ptr())

	def GetEvent(self, EVENT):
		return self.libgame.GetEvent(self._get_app_ptr(), ctypes.c_int(EVENT))

	def GetFPS(self):
		return self.libgame.GetFPS(self._get_app_ptr())

	def GetMem(self):
		return self.libgame.GetMem()

class EntityManagerPy:
	def __init__(self,app):
		self.app = app
		self.man = EntityManager()
		self.app.libgame.CreateEntityManager(app._get_app_ptr(),ctypes.byref(self.man))
	def LoadSprite(self,path,nameSprite):
		self.app.libgame.LoadSprite_EntityManager(ctypes.byref(self.man),path.encode(),nameSprite.encode())
	def ChangSprite(self,entity,nameSprite):
		if isinstance(entity,str):
			entity = entity.encode()
		if isinstance(nameSprite,str):
			nameSprite = nameSprite.encode()
		self.app.libgame.ChangSprite_EntityManager(ctypes.byref(self.man),entity,nameSprite)
	def CreateEntity(self,nameSprite,nameEntity):
		self.app.libgame.CreateEntity(ctypes.byref(self.man),nameSprite.encode(),nameEntity.encode())
	def SearchEntity(self,nameEntity):
		if isinstance(nameEntity,str):
			nameEntity = nameEntity.encode()
		return self.app.libgame.SearchEntity(ctypes.byref(self.man),nameEntity)
	def SetPosition(self,e,x,y):
		self.app.libgame.SetPosition(e,ctypes.c_float(x),ctypes.c_float(y))
	def SetVelocity(self,e,x,y):
		self.app.libgame.SetVelocity(e,ctypes.c_float(x),ctypes.c_float(y))
	def SetAceleration(self,e,x,y):
		self.app.libgame.SetAceleration(e,ctypes.c_float(x),ctypes.c_float(y))
	def SetFrame(self,e,x,y,state):
		if isinstance(state,AnimationToken):
			state = state.value
		self.app.libgame.SetFrame(e,ctypes.c_int(x),ctypes.c_int(y),ctypes.c_int(state))
	def PrintPosition(self, e):
		self.app.libgame.PrintPosition(e)
	def SetDimension(self,e,scale):
		self.app.libgame.SetDimension(e,ctypes.c_float(scale))
	def SetStateColisions(self,e,state):
		e.__colisions = ctypes.c_bool(state)
	def ActivateColisions(self,state):
		self.app.libgame.setActivePhysics(self.app._get_app_ptr(),state)
	def Draw(self,dt,cam):
		self.app.libgame.DrawEntities(ctypes.byref(self.man),dt,cam)
		self.app.libgame.ActivePhysics(self.app._get_app_ptr(),ctypes.byref(self.man),self.app.GetDeltaTime())
	def Free(self):
		self.app.libgame.DestroyEntityManager(ctypes.byref(self.man))