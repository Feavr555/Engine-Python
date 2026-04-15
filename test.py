from interface import *
from lib.EnumEvents import *
from time import sleep
import random

# ------------------------------------------------------------
# Ejemplo de uso básico
# ------------------------------------------------------------

if __name__ == "__main__":
	app = Aplication(b"Script_Test.py")

	speed=10
	x=100.1
	y=100.0
	num=0
	state=True

	def load_resource():
		app.man = app.CreateEntityManager()
		app.man.ActivateColisions(True)
		app.man.LoadSprite("assets/Animacion.png","SPRITE")
		app.man.LoadSprite("assets/CONFIG.png","BALL")
		app.man.CreateEntity("SPRITE","CAPA")
		e = app.man.SearchEntity("CAPA").contents
		app.man.SetFrame(e,2,2,1)
		app.man.SetDimension(e,0.5)

	def game_loop():
		global speed, x, y
		global num, state

		app.DrawBegin()
		e = app.man.SearchEntity("CAPA")
		app.man.SetPosition(e,x,y)
		#app.man.PrintPosition(e)
		if app.GetEvent(EventKeys.UP):
			y-=speed
		if app.GetEvent(EventKeys.DOWN):
			y+=speed
		if app.GetEvent(EventKeys.RIGHT):
			x+=speed
		if app.GetEvent(EventKeys.LEFT):
			x-=speed
		if app.GetEvent(EventKeys.Q):
			app.app.currenState = 4
		if app.GetEvent(EventKeys.P):
			for i in range(0,100):
				app.man.CreateEntity("BALL",f"Entity_{num}")
				o = app.man.SearchEntity(f"Entity_{num}")
				app.man.SetDimension(o,0.5)
				app.man.SetPosition(o,random.randint(0,640),random.randint(0,360))
				if not state:
					app.man.SetVelocity(o,0.1,0.0)
					state=True
				else:
					app.man.SetVelocity(o,0.0,0.1)
					state=False
				num += 1
		print(f"\033c")
		print(f"Entities => {num}")
		app.man.Draw(app.GetDeltaTime(),app.GetCam())
		print(f"FPS => {app.GetFPS()}\nMem => {app.GetMem()}")

		app.DrawEnd()

	app.run(game_loop=game_loop, load_resource=load_resource)

"""
if __name__ == "__main__":
	app = Aplication(b"My Game")
	man = app.CreateEntityManager()
	man.LoadSprite("assets/Animacion.png","SPRITE")
	man.CreateEntity("SPRITE","CAPA")
	e = man.SearchEntity("CAPA")
	man.SetFrame(e,2,2,AnimationToken.DYNAMIC)
	man.SetDimension(e,0.5)
	speed=10
	x=100
	y=100
	while not app.EventProcess():
		app.DrawBegin()
		e = man.SearchEntity("CAPA")
		if app.GetEvent(EventKeys.UP):
			y-=speed
		if app.GetEvent(EventKeys.DOWN):
			y+=speed
		if app.GetEvent(EventKeys.RIGHT):
			x+=speed
		if app.GetEvent(EventKeys.LEFT):
			x-=speed
		man.SetPosition(e,x,y)
		man.Draw(app.GetDeltaTime(),app.GetCam())
		app.DrawEnd()
	man.Free()
	app.Quit()
"""




