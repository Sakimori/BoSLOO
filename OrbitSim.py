import os, json, numpy, pygame, time
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
    decayTick = 10
    currentDecayTick = 0

    def update(self):
        self.currentDecayTick += 1
        if self.currentDecayTick > self.decayTick:
            self.currentDecayTick = 0
            self.color = (max((self.color[0]-5, 0)), max((self.color[1]-5, 0)), max((self.color[2]-5, 0)))

Planet.Earth = Planet("Earth", config()["earthMass"], config()["earthRadius"], 86400)

def physicsUpdate(objects, orbitlines, deltaTime):
    """updates the positions of all orbiting objects in [objects] with timestep deltaTime"""
    for obj in objects:
        if type(obj).__name__ == "OrbitingBody":
            orbitlines.append(DecayPoint(deepcopy(obj.location), (255,255,255)))
            if len(orbitlines) > 500:
                orbitlines.pop(0)
            accel = Point.scalarMult(Point.subtract(obj.location, obj.parentPlanet.location).normalize(),-(config()["G"] * obj.parentPlanet.mass)/(Point.subtract(obj.location, obj.parentPlanet.location).magnitude() ** 2))
            obj.velocity = Point.add(obj.velocity, Point.scalarMult(accel, deltaTime))
            obj.location = Point.add(obj.location, Point.scalarMult(obj.velocity, deltaTime))
    for line in orbitlines:
        line.update()

if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption("Spinny")

    window = pygame.display.set_mode((600, 600))
    resolutionDownscaling = 2
    pygame.display.flip()

    frameTime = 1/30 #framerate

    running = True
    display = False
    thisEarth = deepcopy(Planet.Earth)
    sat = OrbitingBody(Point(config()["earthRadius"] * 1.1, 0, 0), Point(0,6000,-6500), "BoSLOO", 3, thisEarth)
    orbitlines = []
    renderObjects = [thisEarth, sat, orbitlines]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not display:
                    display = True
                    camera = Camera(window, Point(0, 0, 3 * config()["earthRadius"]), thisEarth, renderObjects)
                    pygame.draw.circle(window, (255,255,255), pygame.mouse.get_pos(), 100)
                    camera.renderFrame()
                    pygame.display.flip()
                else:
                    display = False
                    window.fill((0,0,0))
                    pygame.display.flip()
        if display:
            deltaTime = frameTime * config()["timeScale"]
            physicsUpdate(renderObjects, orbitlines, deltaTime)
            camera.renderFrame()
            pygame.display.flip()
        time.sleep(frameTime)

    pygame.quit()

    print("Bye!")