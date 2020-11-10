from particle import Particle
import pygame as pg
import decimal

drawline = pg.draw.line


class Ray:
    #E: SONAR, ANGULO(Heading), FLAG VERIFICADOR DE PRIMARIO
    def __init__(self, pos, heading: float = 0, flagPrimary: bool = True):
        self.start = pos
        self.heading = heading
        self.end: pg.math.Vector2 = pg.math.Vector2()
        self.image = None
        self.flagPrimary = flagPrimary

    
    def update(self, screen: pg.display, boundaries: list):

        colorP = (0,100,0)
        colorS = (0, 100, 0)
        white = (255,255,255)
        light = [1, 1, 0.75]
        self.end.from_polar((10000, self.heading))

        closest = float("inf")
        new_end = pg.Vector2()

        x3 = self.start.x
        x4 = self.end.x
        y3 = self.start.y
        y4 = self.end.y

        for b in boundaries:
            x1 = b.start.x
            x2 = b.end.x
            y1 = b.start.y
            y2 = b.end.y

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den == 0:
                return

            t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
            t = t_num / den
            u_num = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))
            u = u_num / den

            if u >= 0 and 0 <= t <= 1:
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                #Distancia del rayo al bounderie
                dist = self.start.distance_to((x, y))
                #Intensidad del rayo
                intensidad = (1-(dist/500))**2
                intensidad = max(0, min(intensidad, 255))
                #print(intensidad)
                if dist < closest:
                    closest = dist
                    new_end.xy = x, y
                

        if closest == float("inf"):
            self.end = self.start
            self.image = None
            
        else:
            
            self.end = new_end
            
            if self.flagPrimary:
                
                color =  (((x+y)/2) * intensidad)
                white = (color,color,color)
                self.image = drawline(screen, colorP, self.start, self.end, 1) # COLOR
                #drawline(screen, white, self.end, self.end, 1) # COLOR
                
                
            else:
                self.image = drawline(screen, colorS, self.start, self.end, 1) # COLOR
    
