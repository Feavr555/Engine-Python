import ctypes
from enum import Enum

# Cargar la librería compartida (ajusta la ruta si es necesario)
libgame = ctypes.CDLL("./libgame.so")

# ------------------------------------------------------------
# Definición de tipos opacos con tamaño fijo
# ------------------------------------------------------------

class SDL_Window(ctypes.Structure):
	_fields_ = []

class SDL_Renderer(ctypes.Structure):
	_fields_ = []

class APP(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 280)]   # sizeof(APP) = 280

class EntityManager(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 32)]   # sizeof(EntityManager) = 32

class TextureManager(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 16)]   # sizeof(TextureManager) = 16

class Vector(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 24)]   # sizeof(Vector) = 24

class Timer(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 56)]   # sizeof(Timer) = 56

class Phisics(ctypes.Structure):
	_fields_ = [("opaque", ctypes.c_byte * 16)]   # sizeof(Phisics) = 16

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
#typedef struct{
#	// Public:
#	uint32_t rows,columns;
#	Vec2 position,velocity,aceleration;
#	bool __physics;
#	bool __colisions;
#	// Private:
#	SDL_FRect dimension;
#	SDL_Renderer *renderer;
#	SDL_Texture *sprite;
#	uint32_t countFrame;
#	SDL_FRect frame;
#	uint32_t STATESPRITE;
#	char * id;
#	float timer,duration;
#	uint32_t frames_t;
#}Entity;
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
	def SetStateColisions(self,state):
		self.colisions = ctypes.c_bool(state)
	def SetPosition(self,x,y):
		self.position.x = ctypes.c_float(x)
		self.position.y = ctypes.c_float(y)
	def SetVelocity(self,x,y):
		self.velocity.x = ctypes.c_float(x)
		self.velocity.y = ctypes.c_float(y)
	def SetAceleration(self,x,y):
		self.aceleration.x = ctypes.c_float(x)
		self.aceleration.y = ctypes.c_float(y)

# SDL_FRect es una estructura conocida, la definimos con sus campos


# ------------------------------------------------------------
# Prototipos de funciones (ahora Entity ya está definido)
# ------------------------------------------------------------

# Funciones de APP
libgame.Init.argtypes = [ctypes.POINTER(APP), ctypes.c_char_p]
libgame.Init.restype = ctypes.c_bool

libgame.CreateEntityManager.argtypes = [ctypes.POINTER(APP),ctypes.POINTER(EntityManager)]
libgame.CreateEntityManager.restype = None

libgame.ActivePhysics.argtypes = [ctypes.POINTER(APP),ctypes.POINTER(EntityManager),ctypes.c_float]
libgame.ActivePhysics.restype = None

libgame.DrawBegin.argtypes = [ctypes.POINTER(APP)]
libgame.DrawBegin.restype = None

libgame.GetDeltaTime.argtypes = [ctypes.POINTER(APP)]
libgame.GetDeltaTime.restype = ctypes.c_float

libgame.GetFPS.argtypes = [ctypes.POINTER(APP)]
libgame.GetFPS.restype = ctypes.c_float

# EVENTOS
libgame.GetEvent.argtypes = [ctypes.POINTER(APP),ctypes.c_int]
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
libgame.InitEntityManager.argtypes = [ctypes.POINTER(EntityManager), ctypes.POINTER(SDL_Renderer)]
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
libgame.SearchEntity.restype = ctypes.POINTER(Entity)   # Ahora Entity está definido

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

libgame.SetPosition.argtypes = [ctypes.POINTER(Entity),ctypes.c_float,ctypes.c_float]
libgame.SetPosition.restype = None

libgame.SetVelocity.argtypes = [ctypes.POINTER(Entity),ctypes.c_float,ctypes.c_float]
libgame.SetVelocity.restype = None

libgame.SetAceleration.argtypes = [ctypes.POINTER(Entity),ctypes.c_float,ctypes.c_float]
libgame.SetAceleration.restype = None

libgame.SetFrame.argtypes = [ctypes.POINTER(Entity),ctypes.c_int,ctypes.c_int,ctypes.c_int]
libgame.SetFrame.restype = None

libgame.SetDimension.argtypes = [ctypes.POINTER(Entity),ctypes.c_float]
libgame.SetDimension.restype = None

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


# Interfaz

class AnimationToken(Enum):
	STATIC=0
	DYNAMIC=1

from enum import IntEnum

class EventKeys(IntEnum):
    """Enumerado de scancodes de teclado de SDL3 (basado en SDL_Scancode)."""
    UNKNOWN = 0
    A = 4
    B = 5
    C = 6
    D = 7
    E = 8
    F = 9
    G = 10
    H = 11
    I = 12
    J = 13
    K = 14
    L = 15
    M = 16
    N = 17
    O = 18
    P = 19
    Q = 20
    R = 21
    S = 22
    T = 23
    U = 24
    V = 25
    W = 26
    X = 27
    Y = 28
    Z = 29
    NUMBER_1 = 30
    NUMBER_2 = 31
    NUMBER_3 = 32
    NUMBER_4 = 33
    NUMBER_5 = 34
    NUMBER_6 = 35
    NUMBER_7 = 36
    NUMBER_8 = 37
    NUMBER_9 = 38
    NUMBER_0 = 39
    RETURN = 40
    ESCAPE = 41
    BACKSPACE = 42
    TAB = 43
    SPACE = 44
    MINUS = 45
    EQUALS = 46
    LEFTBRACKET = 47
    RIGHTBRACKET = 48
    BACKSLASH = 49
    NONUSHASH = 50
    SEMICOLON = 51
    APOSTROPHE = 52
    GRAVE = 53
    COMMA = 54
    PERIOD = 55
    SLASH = 56
    CAPSLOCK = 57
    F1 = 58
    F2 = 59
    F3 = 60
    F4 = 61
    F5 = 62
    F6 = 63
    F7 = 64
    F8 = 65
    F9 = 66
    F10 = 67
    F11 = 68
    F12 = 69
    PRINTSCREEN = 70
    SCROLLLOCK = 71
    PAUSE = 72
    INSERT = 73
    HOME = 74
    PAGEUP = 75
    DELETE = 76
    END = 77
    PAGEDOWN = 78
    RIGHT = 79
    LEFT = 80
    DOWN = 81
    UP = 82
    NUMLOCKCLEAR = 83
    KP_DIVIDE = 84
    KP_MULTIPLY = 85
    KP_MINUS = 86
    KP_PLUS = 87
    KP_ENTER = 88
    KP_1 = 89
    KP_2 = 90
    KP_3 = 91
    KP_4 = 92
    KP_5 = 93
    KP_6 = 94
    KP_7 = 95
    KP_8 = 96
    KP_9 = 97
    KP_0 = 98
    KP_PERIOD = 99
    NONUSBACKSLASH = 100
    APPLICATION = 101
    POWER = 102
    KP_EQUALS = 103
    F13 = 104
    F14 = 105
    F15 = 106
    F16 = 107
    F17 = 108
    F18 = 109
    F19 = 110
    F20 = 111
    F21 = 112
    F22 = 113
    F23 = 114
    F24 = 115
    EXECUTE = 116
    HELP = 117
    MENU = 118
    SELECT = 119
    STOP = 120
    AGAIN = 121
    UNDO = 122
    CUT = 123
    COPY = 124
    PASTE = 125
    FIND = 126
    MUTE = 127
    VOLUMEUP = 128
    VOLUMEDOWN = 129
    KP_COMMA = 133
    KP_EQUALSAS400 = 134
    INTERNATIONAL1 = 135
    INTERNATIONAL2 = 136
    INTERNATIONAL3 = 137
    INTERNATIONAL4 = 138
    INTERNATIONAL5 = 139
    INTERNATIONAL6 = 140
    INTERNATIONAL7 = 141
    INTERNATIONAL8 = 142
    INTERNATIONAL9 = 143
    LANG1 = 144
    LANG2 = 145
    LANG3 = 146
    LANG4 = 147
    LANG5 = 148
    LANG6 = 149
    LANG7 = 150
    LANG8 = 151
    LANG9 = 152
    ALTERASE = 153
    SYSREQ = 154
    CANCEL = 155
    CLEAR = 156
    PRIOR = 157
    RETURN2 = 158
    SEPARATOR = 159
    OUT = 160
    OPER = 161
    CLEARAGAIN = 162
    CRSEL = 163
    EXSEL = 164
    KP_00 = 176
    KP_000 = 177
    THOUSANDSSEPARATOR = 178
    DECIMALSEPARATOR = 179
    CURRENCYUNIT = 180
    CURRENCYSUBUNIT = 181
    KP_LEFTPAREN = 182
    KP_RIGHTPAREN = 183
    KP_LEFTBRACE = 184
    KP_RIGHTBRACE = 185
    KP_TAB = 186
    KP_BACKSPACE = 187
    KP_A = 188
    KP_B = 189
    KP_C = 190
    KP_D = 191
    KP_E = 192
    KP_F = 193
    KP_XOR = 194
    KP_POWER = 195
    KP_PERCENT = 196
    KP_LESS = 197
    KP_GREATER = 198
    KP_AMPERSAND = 199
    KP_DBLAMPERSAND = 200
    KP_VERTICALBAR = 201
    KP_DBLVERTICALBAR = 202
    KP_COLON = 203
    KP_HASH = 204
    KP_SPACE = 205
    KP_AT = 206
    KP_EXCLAM = 207
    KP_MEMSTORE = 208
    KP_MEMRECALL = 209
    KP_MEMCLEAR = 210
    KP_MEMADD = 211
    KP_MEMSUBTRACT = 212
    KP_MEMMULTIPLY = 213
    KP_MEMDIVIDE = 214
    KP_PLUSMINUS = 215
    KP_CLEAR = 216
    KP_CLEARENTRY = 217
    KP_BINARY = 218
    KP_OCTAL = 219
    KP_DECIMAL = 220
    KP_HEXADECIMAL = 221
    LCTRL = 224
    LSHIFT = 225
    LALT = 226
    LGUI = 227
    RCTRL = 228
    RSHIFT = 229
    RALT = 230
    RGUI = 231
    MODE = 257
    SLEEP = 258
    WAKE = 259
    CHANNEL_INCREMENT = 260
    CHANNEL_DECREMENT = 261
    MEDIA_PLAY = 262
    MEDIA_PAUSE = 263
    MEDIA_RECORD = 264
    MEDIA_FAST_FORWARD = 265
    MEDIA_REWIND = 266
    MEDIA_NEXT_TRACK = 267
    MEDIA_PREVIOUS_TRACK = 268
    MEDIA_STOP = 269
    MEDIA_EJECT = 270
    MEDIA_PLAY_PAUSE = 271
    MEDIA_SELECT = 272
    AC_NEW = 273
    AC_OPEN = 274
    AC_CLOSE = 275
    AC_EXIT = 276
    AC_SAVE = 277
    AC_PRINT = 278
    AC_PROPERTIES = 279
    AC_SEARCH = 280
    AC_HOME = 281
    AC_BACK = 282
    AC_FORWARD = 283
    AC_STOP = 284
    AC_REFRESH = 285
    AC_BOOKMARKS = 286
    SOFTLEFT = 287
    SOFTRIGHT = 288
    CALL = 289
    ENDCALL = 290
    RESERVED = 400
    COUNT = 512



class Aplication:
	def __init__(self,title):
		self.app = APP()
		if isinstance(title,str):
			title = title.encode()
		if not libgame.Init(ctypes.byref(self.app),title):
			print("Fail to create window")
	def _get_app_ptr(self):
		return ctypes.byref(self.app)
	def EventProcess(self):
		return libgame.EventProcess_Exit(self._get_app_ptr())
	def DrawBegin(self):
		libgame.DrawBegin(self._get_app_ptr())
	def DrawEnd(self):
		libgame.DrawEnd(self._get_app_ptr())
	def Quit(self):
		libgame.Destroy(self._get_app_ptr())
	def CreateEntityManager(self):
		return EntityManagerPy(self)
	def GetDeltaTime(self):
		return libgame.GetDeltaTime(self._get_app_ptr())
	def GetCam(self):
		return libgame.GetCam(self._get_app_ptr())
	def GetEvent(self,EVENT):
		return libgame.GetEvent(self._get_app_ptr(),ctypes.c_int(EVENT))
	def GetFPS(self):
		return libgame.GetFPS(self._get_app_ptr())

class EntityManagerPy:
	def __init__(self,app):
		self.app = app
		self.man = EntityManager()
		libgame.CreateEntityManager(app._get_app_ptr(),ctypes.byref(self.man))
	def LoadSprite(self,path,nameSprite):
		libgame.LoadSprite_EntityManager(ctypes.byref(self.man),path.encode(),nameSprite.encode())
	def ChangSprite(self,entity,nameSprite):
		if isinstance(entity,str):
			entity = entity.encode()
		if isinstance(nameSprite,str):
			nameSprite = nameSprite.encode()
		libgame.ChangSprite_EntityManager(ctypes.byref(self.man),entity,nameSprite)
	def CreateEntity(self,nameSprite,nameEntity):
		libgame.CreateEntity(ctypes.byref(self.man),nameSprite.encode(),nameEntity.encode())
	def SearchEntity(self,nameEntity):
		if isinstance(nameEntity,str):
			nameEntity = nameEntity.encode()
		return libgame.SearchEntity(ctypes.byref(self.man),nameEntity)
	def SetPosition(self,e,x,y):
		libgame.SetPosition(e,ctypes.c_float(x),ctypes.c_float(y))
	def SetVelocity(self,e,x,y):
		libgame.SetVelocity(e,ctypes.c_float(x),ctypes.c_float(y))
	def SetAceleration(self,e,x,y):
		libgame.SetAceleration(e,ctypes.c_float(x),ctypes.c_float(y))
	def SetFrame(self,e,x,y,state):
		if isinstance(state,AnimationToken):
			state = state.value
		libgame.SetFrame(e,ctypes.c_int(x),ctypes.c_int(y),ctypes.c_int(state))
	def SetDimension(self,e,scale):
		libgame.SetDimension(e,ctypes.c_float(scale))
	def SetStateColisions(self,e,state):
		e.__colisions = ctypes.c_bool(state)
	def Draw(self,dt,cam):
		libgame.DrawEntities(ctypes.byref(self.man),dt,cam)
		libgame.ActivePhysics(self.app._get_app_ptr(),ctypes.byref(self.man),self.app.GetDeltaTime())
	def Free(self):
		libgame.DestroyEntityManager(ctypes.byref(self.man))


