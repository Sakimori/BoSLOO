import numpy, pygame, math
import pygame.freetype

class Point:
    """Numpy 3-vec"""
    def __init__(self, x, y, z):
        self.vector = numpy.array([x, y, z])

    def polar(self):
        rho = math.sqrt(self.vector[0] ** 2 + self.vector[1] ** 2 + self.vector[2] ** 2)
        theta = math.atan(self.vector[2]/self.vector[0])
        phi = math.acos((self.vector[1])/(rho))
        return [rho, theta, phi]

    def magnitude(self):
        return numpy.linalg.norm(self.vector)

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

class Camera:
    """Object which will be used to paint pixels on screen."""
    def __init__(self, surface:pygame.Surface, location:Point, target:"Planet", objects, hFOV = 55, vFOV = 55):
        self.surface = surface
        self.objects = objects
        self.location = location
        self.target = target
        self.hFOV = hFOV
        self.vFOV = vFOV

    def isInside(self, planet:"Planet"):
        """returns True if camera is inside the planet."""
        return numpy.linalg.norm(self.location.magnitude) < planet.radius

    def renderFrame(self):
        """generates a frame and draws it to the surface. Does not update screen; use pygame.display.flip()"""
        font = pygame.freetype.SysFont("Comic Sans MS", 14)
        winWidth, winHeight = self.surface.get_size()
        winDistance = winWidth * numpy.cos(numpy.radians(self.hFOV)/2) / 2 #distance for a virtual screen to exist in-space to give the correct FOV
        vecToCenter = Point.subtract(self.target.location, self.location)
        vecToCenter.normalize()
        screenPlane = Plane(Point.add(self.location, Point.scalarMult(vecToCenter, winDistance)), vecToCenter)
        screenSurface = pygame.Surface((winWidth, winHeight))
        #pygame uses 0,0 as the top left corner
        for obj in self.objects:
            if type(obj).__name__ == "OrbitingBody":
                sat = obj
                lineToCamera = Line(obj.location, self.location)
                intersectPoint = lineToCamera.intersectWithPlane(screenPlane)
                if intersectPoint is not None:
                    intersectPoint = Point.add(intersectPoint, Point(int(winWidth/2), int(winHeight/2), 0))
                    pygame.draw.circle(screenSurface, (255,255,150), (int(intersectPoint.vector[0]), int(intersectPoint.vector[1])), obj.displaySize)
            elif type(obj).__name__ == "Planet":
                target = obj
                lineToCamera = Line(obj.location, self.location)
                intersectPoint = lineToCamera.intersectWithPlane(screenPlane)
                if intersectPoint is not None:
                    intersectPoint = Point.add(intersectPoint, Point(int(winWidth/2), int(winHeight/2), 0))
                    pygame.draw.circle(screenSurface, (255,255,150), (int(intersectPoint.vector[0]), int(intersectPoint.vector[1])), 15)
            elif isinstance(obj, list):
                for orbitline in obj:
                    if orbitline.color != (0,0,0):
                        lineToCamera = Line(orbitline.location, self.location)
                        intersectPoint = lineToCamera.intersectWithPlane(screenPlane)
                        if intersectPoint is not None:
                            intersectPoint = Point.add(intersectPoint, Point(int(winWidth/2), int(winHeight/2), 0))
                            pygame.draw.circle(screenSurface, orbitline.color, (int(intersectPoint.vector[0]), int(intersectPoint.vector[1])), 1)


        screenSurface = pygame.transform.flip(screenSurface, False, True)

        #generate text
        rho, theta, phi = sat.location.polar()
        theta = math.degrees(theta)
        phi = math.degrees(phi)

        #textSurface, rect = font.render(f"Speed: {round(sat.velocity.magnitude())} m/s \nAltitude: {round(rho - target.radius)} m", False, (255,255,255))
        font.render_to(screenSurface, (0,0), f"Speed: {round(sat.velocity.magnitude())} m/s \nAltitude: {round(rho - target.radius)} m", (255,255,255))
        self.surface.blit(screenSurface, (0,0))
        

    def renderImage(self, sat:"OrbitingBody", planet:"Planet", points):
        """generates a single image and saves it to disk"""
        frozenSat = sat.location
        rotValue = math.modf(planet.rotationPercentage * 12)[0] * 3.14159 / 6 #get percentage of 1/12 of a revolution
        winWidth, winHeight = self.surface.get_size()
        winDistance = winWidth * numpy.cos(numpy.radians(self.hFOV)/2) / 2 #distance for a virtual screen to exist in-space to give the correct FOV
        vecToCenter = Point.subtract(self.target.location, self.location)
        vecToCenter.normalize()
        screenPlane = Plane(Point.add(self.location, Point.scalarMult(vecToCenter, winDistance)), vecToCenter)
        screenPlaneOrigin = Point.subtract(screenPlane.point, Point(int(winWidth/2), int(winHeight/2), 0))
        screenSurface = pygame.Surface((winWidth, winHeight))
        #pygame uses 0,0 as the top left corner

        satDistance = -1

        curveCoeff = 1.1

        for column in range(0, winWidth):
            for row in range(0, winHeight):
                #get line in world going through this pixel
                worldLine = Line(self.location, Point.add(screenPlaneOrigin, Point(column, row, 0)))
                #compare distance from center of planet to radius of planet to determine intersection           
                
                dist = frozenSat.distanceFromLine(worldLine)
                if satDistance < 0 or dist < satDistance:
                    satDistance = dist
                    satPixel = (column, row)

                if self.target.location.distanceFromLine(worldLine) < self.target.radius:
                    epsilon = 0.1
                    yPrime = min([abs((row + screenPlaneOrigin.vector[1]) * (self.location.vector[2] / winDistance)), self.target.radius])
                    yPrimeCurve = yPrime / (self.target.radius * curveCoeff)
                    xPrime = min([abs((column + screenPlaneOrigin.vector[0]) * (self.location.vector[2] / winDistance)), self.target.radius])
                    xPrimeCurve = xPrime / (self.target.radius * curveCoeff)
                    #treat yPrime like it's further from zero than it really is based on xPrime, and vice versa
                    yPrime /= math.sin(math.acos(xPrimeCurve))
                    xPrime /= math.sin(math.acos(yPrimeCurve))

                    try:
                        lat = math.modf((math.acos(yPrime / self.target.radius) / (3.141592/12.0)))[0] #pi/12 = 15 degrees
                    except:
                        screenSurface.set_at((column, row), (20,20,20))
                        continue

                    try:
                        long = math.modf(((math.acos((xPrime) / self.target.radius)) / (3.141592/6.0)))[0] #pi/6 = 30 degrees
                    except:
                        screenSurface.set_at((column, row), (20,20,20))
                        continue

                    if -epsilon < lat < epsilon or -epsilon < long < epsilon:
                        screenSurface.set_at((column, row), (180,180,180))
                    elif -epsilon < lat < epsilon and -epsilon < long < epsilon:
                        screenSurface.set_at((column, row), (255,255,255))
                    else:
                        screenSurface.set_at((column, row), (50,50,50))

        #check if satellite is behind or in front of planet (or unobscured)
        if screenSurface.get_at(satPixel) == (0,0,0):
            circleBorder = 0
        else:
            if self.location.distanceFromPoint(frozenSat) > self.location.distanceFromPoint(self.target.location):
                circleBorder = 2
            else:
                circleBorder = 0
        pygame.draw.circle(screenSurface, (230, 227, 64), satPixel, 4, width = circleBorder)
        screenSurface = pygame.transform.flip(screenSurface, False, True)
        pygame.image.save(screenSurface, "test.png")
        

        #for row in range(int(-winHeight/2), int(winHeight/2)):
        #    for column in range(int(-winWidth/2), int(winWidth/2)):
        #        line = Line(self.location, Point(self.location.x + column))