from interface import *
import random
# ------------------------------------------------------------
# Ejemplo de uso básico
# ------------------------------------------------------------
if __name__ == "__main__":
    app = Aplication(b"My Game")
    man = app.CreateEntityManager()
    man.LoadSprite("assets/Animacion.png", "SPRITE")
    man.LoadSprite("assets/CONFIG.png", "BALL")
    man.CreateEntity("SPRITE", "CAPA")
    e = man.SearchEntity("CAPA").contents
    man.SetFrame(e, 2, 2, AnimationToken.DYNAMIC)
    man.SetDimension(e, 0.5)
    e.SetStateColisions(True)
    speed=10
    x=100
    y=100
    num=0
    while not app.EventProcess():
        app.DrawBegin()
        if app.GetEvent(EventKeys.UP):
            y-=speed
        if app.GetEvent(EventKeys.DOWN):
            y+=speed
        if app.GetEvent(EventKeys.RIGHT):
            x+=speed
        if app.GetEvent(EventKeys.LEFT):
            x-=speed
        if app.GetEvent(EventKeys.P):
            state=False
            for i in range(0,100):
                man.CreateEntity("BALL",f"ENTITY_{num}")
                o = man.SearchEntity(f"ENTITY_{num}").contents
                man.SetDimension(o,0.5)
                o.SetStateColisions(True)
                o.SetPosition(random.randint(0,640),random.randint(0,360))
                if not state:
                    o.SetVelocity(0.1,0.0)
                else:
                    o.SetVelocity(0.0,0.1)
                num += 1
                print(f"\033cEntities => {num}\nFPS => {app.GetFPS()}")
        e = man.SearchEntity("CAPA")
        man.SetPosition(e,x,y)
        man.Draw(app.GetDeltaTime(),app.GetCam())
        app.DrawEnd()
    man.Free()
    app.Quit()
