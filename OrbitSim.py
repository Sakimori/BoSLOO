import os, json, numpy, pygame, time, threading
from renderer import *
from copy import deepcopy

groundControlPath = "GroundControlFiles"
configPath = os.path.join("ConfigFiles", "OrbitSim")
configFilename = os.path.join(configPath, "Universe.cfg")
mapFilename = os.path.join(configPath, "Map.png")

def config():
    """Returns the config dictionary. Generates with default values if no config dictionary exists."""

    if not os.path.exists(configPath):
        os.makedirs(configPath)
    if not os.path.exists(configFilename):
        #generate default
        config_dic = {
                "G": 6.674e-11,
                "earthMass": 5.972e24, #in kg
                "earthRadius": 6378000, #meters
                "timeScale": 1 #higher number go faster wheeeeee
            }
        with open(configFilename, "w") as file:
            json.dump(config_dic, file, indent = 4)
            return config_dic
    else:
        with open(configFilename) as file:
            return json.load(file)

class OrbitingBody:
    """a zero-mass point object parented to a planet"""
    def __init__(self, location:Point, velocity:Point, name, displaySize, parentPlanet):
        self.location = location
        self.velocity = velocity
        self.name = name
        self.displaySize = displaySize #the size of the object on camera in pixels, for visibility reasons
        self.parentPlanet = parentPlanet

class Planet:
    """A massive body at 0,0,0 and a given radius."""
    def __init__(self, name, mass, radius, rotationPeriod, location:Point = deepcopy(Point.zero)):
        """Rotation period given in seconds."""
        self.location = location
        self.name = name
        self.mass = mass
        self.radius = radius
        self.rotationPercentage = 0.00
        self.rotationPeriod = rotationPeriod

    def rotate(self, timeDelta:"Seconds"):
        self.rotationPercentage += timeDelta/self.rotationPeriod
        if self.rotationPercentage >= 100.0:
            self.rotationPercentage -= 100.0

class DisplayPoint:
    """A single point of any color"""
    def __init__(self, location, color):
        self.location = location
        self.color = color

class DecayPoint(DisplayPoint):
    """A display point that slowly fades to black"""
    decayTick = 1
    currentDecayTick = 0
    color = (255,255,255,255)

    def update(self):
        self.currentDecayTick += 1
        if self.currentDecayTick >= self.decayTick:
            self.currentDecayTick = 0
            self.color = (self.color[0], self.color[1], self.color[2], (max((self.color[3]-5, 0))))

    def copy(self):
        """returns a distinct copy of the point"""
        return DecayPoint(self.location, self.color)

Planet.Earth = Planet("Earth", config()["earthMass"], config()["earthRadius"], 86400)

def physicsUpdate(objects, orbitlines, deltaTime):
    """updates the positions of all orbiting objects in [objects] with timestep deltaTime"""
    for obj in objects:
        if type(obj).__name__ == "OrbitingBody":
            orbitlines.append(DecayPoint(deepcopy(obj.location), (255,255,255,255)))
            if len(orbitlines) > 100:
                orbitlines.pop(0)
            accel = Point.scalarMult(Point.subtract(obj.location, obj.parentPlanet.location).normalize(),-(config()["G"] * obj.parentPlanet.mass)/(Point.subtract(obj.location, obj.parentPlanet.location).magnitude() ** 2))
            obj.velocity = Point.add(obj.velocity, Point.scalarMult(accel, deltaTime))
            obj.location = Point.add(obj.location, Point.scalarMult(obj.velocity, deltaTime))
        elif type(obj).__name__ == "Planet":
            obj.rotate(deltaTime)
    for line in orbitlines:
        line.update()

if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption("Spinny")

    window = pygame.display.set_mode((900, 900))
    resolutionDownscaling = 2
    pygame.display.flip()

    FPS = 144 #max framerate
    frameTime = 1/144

    running = True
    display = False
    thisEarth = deepcopy(Planet.Earth)
    sat = OrbitingBody(Point(0, config()["earthRadius"] + 2042000, config()["earthRadius"] + 3000000), Point(-4800,0,-1800), "BoSLOO", 5, thisEarth)
    orbitlines = []
    renderObjects = [thisEarth, sat, orbitlines]
    clock = pygame.time.Clock()
    save = False
    
    clock.tick(FPS)

    while running:
        clock.tick(FPS)
        if display:
            #deltaTime = frameTime * config()["timeScale"]    
            deltaTime = (clock.get_time()/1000) * config()["timeScale"]      
            physicsUpdate(renderObjects, orbitlines, deltaTime)
            camera.renderFrame(save=save)
            save=False
            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not display:
                    display = True
                    camera = Camera(window, Point(5 * config()["earthRadius"], 0, 0), thisEarth, renderObjects)
                    camera.renderFrame()
                    pygame.display.flip()
                else:
                    save = True
        
        #time.sleep(frameTime)

    pygame.quit()

    print("Bye!")