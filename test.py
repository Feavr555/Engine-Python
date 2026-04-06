from interface import *
from lib.EnumEvents import *
from time import sleep

# ------------------------------------------------------------
# Ejemplo de uso básico
# ------------------------------------------------------------

if __name__ == "__main__":
	app = Aplication(b"Sida")

	speed=10
	x=100.1
	y=100.0

	def load_resource():
		app.man = app.CreateEntityManager()
		app.man.LoadSprite("assets/Animacion.png","SPRITE")
		app.man.CreateEntity("SPRITE","CAPA")
		e = app.man.SearchEntity("CAPA").contents
		app.man.SetFrame(e,2,2,1)
		app.man.SetDimension(e,0.5)

	def game_loop():
		global speed, x, y

		app.DrawBegin()
		e = app.man.SearchEntity("CAPA")
		app.man.SetPosition(e,x,y)
		app.man.PrintPosition(e)
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
		app.man.Draw(app.GetDeltaTime(),app.GetCam())
		#print(f"\033FPS => {app.GetFPS()}\nMem => {app.GetMem()}")

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




