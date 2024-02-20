import os, json, numpy, pygame, time, threading, jsonpickle
from renderer import *
from copy import deepcopy

groundControlPath = "GroundControl"
stateFilePath = os.path.join("SatState.json")

configPath = os.path.join("ConfigFiles", "OrbitSim")
configFilename = os.path.join(configPath, "Universe.cfg")
satSavePath = os.path.join(configPath, "Orbit.cfg")
mapFilename = os.path.join(configPath, "Map.png")

STATE_EVENT = pygame.event.custom_type()

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
                "timeScale": 1, #higher number go faster wheeeeee
                "updateTick": 300 #seconds to wait between save to file
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
        self.resetLocation = location.copy()
        self.velocity = velocity
        self.resetVelocity = velocity.copy()
        self.name = name
        self.displaySize = displaySize #the size of the object on camera in pixels, for visibility reasons
        self.parentPlanet = parentPlanet
        self.lastDelta = 0
        self.lastSecondDelta = 0
        self.keepFreeze = 3

    def stationKeep(self):
        currDelta = Point.subtract(self.resetLocation, self.location).magnitude()
        currSecondDelta = currDelta - self.lastDelta
        if (currSecondDelta > 0) and (self.lastSecondDelta <= 0) and self.keepFreeze <= 0:
            self.location = self.resetLocation.copy()
            self.velocity = self.resetVelocity.copy()
            self.keepFreeze = 3
        elif self.keepFreeze > 0:
            self.keepFreeze -= 1
        self.lastDelta = currDelta
        self.lastSecondDelta = currSecondDelta

    def latLongAlt(self):
        rho, theta, phi = self.location.polar()
        rawLat, rawLong = self.parentPlanet.sphericalToLatLong(theta, phi) #negative lat is north, positive lat is south, positive long is east, negative long is west
        return (rho - self.parentPlanet.radius), rawLat, rawLong

    def writeStateReadable(self):
        alt, lat, long = self.latLongAlt()
        stateDic = {
                "notes": "lat: pos S, neg N; long: pos E, neg W",
                "latitude": lat,
                "longitude": long,
                "altitude": alt,
                "velocity": self.velocity.magnitude()
            }
        with open(stateFilePath, "w") as file:
            json.dump(stateDic, file, indent=4)

    def saveState(self):
        stateDic = {
                "location": jsonpickle.encode(self.location),
                "velocity": jsonpickle.encode(self.velocity),
            }

    def loadState(self):
        if os.path.exists(satSavePath):
            with open(satSavePath) as file:
                state = json.load(file)
                self.location = jsonpickle.decode(state["location"])
                self.velocity = jsonpickle.decode(state["velocity"])
            return True
        else:
            return False


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

    def rotate(self, timeDelta):
        self.rotationPercentage += timeDelta*100/self.rotationPeriod
        if self.rotationPercentage >= 100.0:
            self.rotationPercentage -= 100.0

    def sphericalToLatLong(self, theta, phi):
        """Converts theta and phi spherical coordinates to latitude and longitude. -> lat, long"""
        rotRadian = self.rotationPercentage/100 * 2 * math.pi
        lat = math.degrees(phi - (math.pi/2)) #negative lat is north, positive is south
        long = rotRadian - theta #positive long is east, negative is west
        if long < -math.pi:
            long += math.pi*2
        elif long > math.pi:
            long -= math.pi*2 
        return (lat, math.degrees(long))

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
            obj.stationKeep()
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
    sat = OrbitingBody(Point(0, config()["earthRadius"]*5, config()["earthRadius"]*2), Point(-2500,0,0), "BoSLOO", 5, thisEarth)
    orbitlines = []
    renderObjects = [thisEarth, sat, orbitlines]
    configFile = config()
    clock = pygame.time.Clock()
    stateTimer = pygame.time.set_timer(STATE_EVENT, configFile["updateTick"]*1000)
    mapThread = threading.Thread()

    save = False
    
    clock.tick(FPS)

    while running:
        clock.tick(FPS)
        if display:
            #deltaTime = frameTime * config()["timeScale"]    
            deltaTime = (clock.get_time()/1000) * configFile["timeScale"]      
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
                    camera = Camera(window, Point(10 * configFile["earthRadius"], 0, 0), thisEarth, renderObjects)
                    camera.renderFrame()
                    pygame.display.flip()
                else:
                    save = True
                    if not mapThread.is_alive():
                        mapThread = threading.Thread(target=camera.saveGroundTrack())
                        mapThread.start()

            elif event.type == STATE_EVENT:
                sat.writeStateReadable()
                configFile = config()
        
        #time.sleep(frameTime)

    pygame.quit()

    print("Bye!")