import os, json, numpy, pygame

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
                "g": 6674,
                "gExp": -14, #G = g * 10^gExp
                "earthMass": 5972,
                "earthMassExp": 21, #Me = earthMass * 10^earthMassExp; in kg
                "earthRadius": 6378000, #meters
                "timeScale": 1 #higher number go faster wheeeeee
            }
        with open(configFilename, "w") as file:
            json.dump(config_dic, file, indent = 4)
            return config_dic
    else:
        with open(configFilename) as file:
            return json.load(file)

class Point:
    """Numpy 3-vec"""
    def __init__(self, x, y, z):
        self.vector = numpy.array([x, y, z])

    def magnitude(self):
        return numpy.linalg.norm(self.vector)

    def distanceFrom(self, otherPoint:"Point"):
        return numpy.linalg.norm(self.vector - otherPoint.vector)

Point.zero = Point(0, 0, 0)

class Camera:
    """Object which will be used to paint pixels on screen."""
    def __init__(self, location:Point, target:Point = Point.zero, FOV = 75):
        self.location = location
        self.target = target
        self.FOV = FOV

    def isInside(self, planet:"Planet"):
        """returns True if camera is inside the planet."""
        return numpy.linalg.norm(self.location.magnitude) < planet.radius

class OrbitingBody:
    """a zero-mass point object parented to a planet"""
    def __init__(self, location:Point, velocity:Point, name, displaySize, parentPlanet):
        self.location = location
        self.velocity = velocity
        self.name = name
        self.displaySize = displaySize #the size of the object on camera, for visibility reasons
        self.parentPlanet = parentPlanet

class Planet:
    """A massive body at 0,0,0 and a given radius."""
    def __init__(self, name, mass, radius, rotationPeriod):
        """Rotation period given in seconds."""
        self.name = name
        self.mass = mass
        self.radius = radius
        self.rotationPercentage = 0
        self.rotationPeriod = rotationPeriod

Planet.Earth = Planet("Earth", (config()["earthMass"] * 10**config()["earthMassExp"]), config()["earthRadius"], 86400)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_caption("Spinny")

    window = pygame.display.set_mode((400, 400))
    resolutionDownscaling = 2
    pygame.display.flip()

    running = True
    display = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not display:
                    display = True
                    camera = Camera(Point(0, 0, 6378000*4))
    pygame.quit()

    print("Bye!")