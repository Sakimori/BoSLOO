import numpy, pygame, math, os
import pygame.freetype

ASSET_DIR = "Assets"
SPHERE_FOLDER_NAME = "Sphere"
MAPS_FOLDER_NAME = "Maps"


class Point:
    """Numpy 3-vec"""
    def __init__(self, x, y, z):
        self.vector = numpy.array([x, y, z])

    def copy(self):
        return Point(self.vector[0], self.vector[1], self.vector[2])

    def polar(self):
        """Converts the vector rectangular coordinates to polar coordinates."""
        if self.vector[0] == 0:
            self.vector[0] = 0.1
        if self.vector[2] == 0:
            self.vector[2] = 0.1
        rho = math.sqrt(int(self.vector[0]) ** 2 + int(self.vector[1]) ** 2 + int(self.vector[2]) ** 2)
        theta = math.atan(self.vector[1]/self.vector[0]) #this has a range of -pi/2 to pi/2 but we need 0 to 2pi so more work needed
        phi = math.acos(self.vector[2]/rho) 
        if self.vector[0] < 0: 
            if self.vector[1] >= 0: #if x is positive, atan is fine. need to check if x is negative, first.
                theta += math.pi 
            else:
                theta -= math.pi
        return [rho, theta, phi]

    def magnitude(self):
        return float(numpy.linalg.norm(self.vector))

    def normalize(self):
        self.vector = self.vector/self.magnitude()
        return self

    def distanceFromPoint(self, otherPoint:"Point"):
        return numpy.linalg.norm(self.vector - otherPoint.vector)

    def distanceFromLine(self, line:"Line"):
        return numpy.linalg.norm(numpy.cross(line.p2.vector - line.p1.vector, self.vector - line.p1.vector)/numpy.linalg.norm(line.p2.vector - line.p1.vector))

    def add(p1, p2):
        sum = numpy.add(p1.vector, p2.vector)
        return Point(sum[0], sum[1], sum[2])

    def subtract(p1, p2):
        diff = numpy.subtract(p1.vector, p2.vector)
        return Point(diff[0], diff[1], diff[2])

    def dot(p1, p2):
        return numpy.dot(p1.vector, p2.vector)

    def scalarMult(p1, scalar):
        mult = p1.vector * scalar
        return Point(mult[0], mult[1], mult[2])


Point.zero = Point(0, 0, 0)

class Ray:
    def __init__(self, origin:Point, direction:Point):
        self.origin = origin
        self.direction = direction

class Line:
    def __init__(self, p1:Point, p2:Point):
        self.p1 = p1
        self.p2 = p2

    def intersectWithPlane(self, plane):
        lineVec = Point.subtract(self.p2, self.p1)
        dot = Point.dot(plane.normal, lineVec)

        if abs(dot) > 1e-6:
            w = Point.subtract(self.p1, plane.point)
            fac = -Point.dot(plane.normal, w) / dot
            u = Point.scalarMult(lineVec, fac)
            return Point.add(self.p1, u)
        else:
            return None

class Plane:
    def __init__(self, point:Point, normal:Point):
        self.point = point
        self.normal = normal

class PlanetSprite(pygame.sprite.Sprite):
    def __init__(self, camera, parentPlanet:"Planet"):
        pygame.sprite.Sprite.__init__(self)
        #the rotation animation loops every 64th of a rotation, so determine and store the frame number.
        self.frames = {}
        for imgName in os.listdir(os.path.join(ASSET_DIR, SPHERE_FOLDER_NAME)):
            if imgName.endswith(".png"): 
                self.frames[imgName.strip(".png")] = pygame.image.load(os.path.join(ASSET_DIR, SPHERE_FOLDER_NAME, imgName)).convert_alpha()
        self.parentPlanet = parentPlanet
        self.frameNumber = str(round(math.modf(self.parentPlanet.rotationPercentage/100 * 64)[0] * 49) + 1).zfill(4)
        self.image = self.frames[self.frameNumber]
        self.setSize(camera)
                

    def setSize(self, camera):
        winWidth, winHeight = camera.surface.get_size()
        #distance = Point.subtract(camera.location, self.parentPlanet.location).magnitude()
        #radius = self.parentPlanet.radius
        #self.sideLength = int((1/math.tan(numpy.radians(camera.hFOV)/2))*radius/math.sqrt(distance**2 - radius**2)*winWidth/2)

        lineToCam = Line(Point.add(self.parentPlanet.location, Point(0, self.parentPlanet.radius,0)), camera.location)
        intersectPoint = lineToCam.intersectWithPlane(camera.screenPlane)
        radius = intersectPoint.vector[1]
        self.sideLength = int(radius*2*600/530)

        self.image = pygame.transform.scale(self.image, (self.sideLength, self.sideLength))
        self.rect = self.image.get_rect()
        self.rect.center = (winWidth/2, winHeight/2)


    def update(self):
        self.frameNumber = str(round(math.modf(self.parentPlanet.rotationPercentage/100 * 64)[0] * 49) + 1).zfill(4)
        self.image = pygame.image.load(os.path.join(ASSET_DIR, SPHERE_FOLDER_NAME, f"{self.frameNumber}.png")).convert_alpha()
        if self.sideLength is not None:
            self.image = pygame.transform.scale(self.image, (self.sideLength, self.sideLength))



class Camera:
    """Object in charge of rendering both the realtime 3D scene and a ground track map."""
    def __init__(self, surface:pygame.Surface, location:Point, target:"Planet", objects, hFOV = 60):
        self.surface = surface
        self.objects = objects
        self.location = location
        self.target = target
        self.hFOV = hFOV
        self.spriteGroup = pygame.sprite.Group()
        self.pastTrackPoints = []
        self.trackSampleRate = 8
        self.trackSampleCount = 0

        self.mapSurface = pygame.image.load(os.path.join(ASSET_DIR, MAPS_FOLDER_NAME, "rect_color.png"))
        self.mapWidth, self.mapHeight = self.mapSurface.get_size()

        winWidth, winHeight = self.surface.get_size()
        winDistance = winWidth / (2 * math.tan(numpy.radians(self.hFOV/2))) #distance for a virtual screen to exist in-space to give the correct FOV
        vecToCenter = Point.subtract(self.target.location, self.location)
        vecToCenter.normalize()
        self.screenPlane = Plane(Point.add(self.location, Point.scalarMult(vecToCenter, winDistance)), vecToCenter)

        self.spriteGroup.add(PlanetSprite(self, self.target))
                

    def isInside(self, planet:"Planet"):
        """returns True if camera is inside the planet."""
        return numpy.linalg.norm(self.location.magnitude) < planet.radius

    def renderFrame(self, save=False):
        """generates a frame and draws it to the surface. Does not update screen; use pygame.display.flip()"""
        font = pygame.freetype.SysFont("Comic Sans MS", 14)
        winWidth, winHeight = self.surface.get_size()

        frontSurface = pygame.Surface((winWidth, winHeight), pygame.SRCALPHA)
        backSurface = pygame.Surface((winWidth, winHeight), pygame.SRCALPHA)
        backgroundSurface = pygame.Surface((winWidth, winHeight))

        backgroundSurface.fill((15,15,15))
        backSurface.fill((0,0,0,0))
        frontSurface.fill((0,0,0,0))



        #pygame uses 0,0 as the top left corner
        for obj in self.objects:
            if type(obj).__name__ == "OrbitingBody":
                sat = obj
                lineToCamera = Line(obj.location, self.location)
                intersectPoint = lineToCamera.intersectWithPlane(self.screenPlane)
                intersectPoint.vector[2] = -intersectPoint.vector[2]
                if intersectPoint is not None:
                    intersectPoint = Point.add(intersectPoint, Point(0, int(winWidth/2), int(winHeight/2))) #x is meaningless here
                    if sat.location.vector[0] < 0:
                        drawSurface = backSurface
                    else:
                        drawSurface = frontSurface
                    pygame.draw.circle(drawSurface, (255,255,150,255), (int(intersectPoint.vector[1]), int(intersectPoint.vector[2])), obj.displaySize)

            elif isinstance(obj, list):
                for orbitline in obj:
                    if orbitline.color != (0,0,0):
                        lineToCamera = Line(orbitline.location, self.location)
                        intersectPoint = lineToCamera.intersectWithPlane(self.screenPlane)
                        intersectPoint.vector[2] = -intersectPoint.vector[2]
                        if intersectPoint is not None:
                            intersectPoint = Point.add(intersectPoint, Point(0, int(winWidth/2), int(winHeight/2)))
                            if orbitline.color[3] != 0:
                                if orbitline.location.vector[0] < 0:
                                    drawSurface = backSurface
                                else:
                                    drawSurface = frontSurface
                                pygame.draw.circle(drawSurface, orbitline.color, (int(intersectPoint.vector[1]), int(intersectPoint.vector[2])), 1)

        #DEBUG DOTS
        #lineToCam = Line(Point.add(self.target.location, Point(0,self.target.radius,0)), self.location)
        #intersectPoint = lineToCam.intersectWithPlane(self.screenPlane)
        #intersectPoint = Point.add(intersectPoint, Point(0, int(winWidth/2), int(winHeight/2)))
        #pygame.draw.circle(frontSurface, (255,150,150,255), (int(intersectPoint.vector[1]), int(intersectPoint.vector[2])), 5)

        #newLineToCam = Line(Point.add(self.screenPlane.point, Point(0,750,0)), self.location)
        #intersectPoint = newLineToCam.intersectWithPlane(self.screenPlane)
        #intersectPoint = Point.add(intersectPoint, Point(0, int(winWidth/2), int(winHeight/2)))
        #pygame.draw.circle(screenSurface, (150,255,150), (int(intersectPoint.vector[1]), int(intersectPoint.vector[2])), 5)

        #generate text

        alt, rawLat, rawLong = sat.latLongAlt()
        self.updateTrackList(rawLat, rawLong)
        latString = f"Latitude: {round(rawLat,4)}⁰ S" if rawLat >= 0 else f"Latitude: {-round(rawLat,4)}⁰ N"
        longString = f"Longitude: {round(rawLong,4)}⁰ E" if rawLong >= 0 else f"Longitude: {-round(rawLong,4)}⁰ W"
        font.render_to(backSurface, (0,0), f"Speed: {round(sat.velocity.magnitude()/1000,3)} km/s", (255,255,255))
        font.render_to(backSurface, (0,20), f"Altitude: {round((alt)/1000)} km", (255,255,255))
        font.render_to(backSurface, (0,50), latString, (255,255,255))
        font.render_to(backSurface, (0,70), longString, (255,255,255))

        self.spriteGroup.update()
        self.spriteGroup.draw(backSurface)
           
        self.surface.blit(backgroundSurface, (0,0))
        self.surface.blit(backSurface, (0,0))
        self.surface.blit(frontSurface, (0,0))

        if save:
            pygame.image.save(self.surface, "test.png")
        
        

    def updateTrackList(self, lat, long):
        """Updates the ground track map list of points."""
        if self.trackSampleCount != self.trackSampleRate:
            self.trackSampleCount += 1
            return
        if len(self.pastTrackPoints) > 20000:
            self.pastTrackPoints.pop(0)
        #latitude is from -90 to 90; longitude is from -180 to 180.
        latPercent = (lat + 90)/180
        longPercent = (long + 180)/360
        lat = self.mapHeight * latPercent
        long = self.mapWidth * longPercent
        self.pastTrackPoints.append((long, lat))
        self.trackSampleCount = 0

    def saveGroundTrack(self):
        mapSurface = pygame.Surface.copy(self.mapSurface)
        sets = []
        currStart = 0
        for i in range(1,len(self.pastTrackPoints)):
            if abs(self.pastTrackPoints[i][0] - self.pastTrackPoints[i-1][0]) > 400:
                sets.append(self.pastTrackPoints[currStart:i])
                currStart = i
        sets.append(self.pastTrackPoints[currStart:])
        colors = [(122,255,243), (211,122,255), (222,0,177)]
        for i in range(0,len(sets)):
            try:
                pygame.draw.lines(mapSurface, colors[i%3], False, sets[i], width=5)
                #pygame.draw.aalines(mapSurface, colors[i%3], False, [(long, lat+1) for long, lat in sets[i]])
                #pygame.draw.aalines(mapSurface, colors[i%3], False, [(long+1, lat) for long, lat in sets[i]])
                #pygame.draw.aalines(mapSurface, colors[i%3], False, [(long, lat-1) for long, lat in sets[i]])
                #pygame.draw.aalines(mapSurface, colors[i%3], False, [(long-1, lat) for long, lat in sets[i]])
            except:
                pass
        pygame.image.save(mapSurface, "testMap.png")