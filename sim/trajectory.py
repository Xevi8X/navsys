
import math

class NEDConverter:
    def __init__(self, origin_lat, origin_lon, origin_alt):
        self.origin_lat_rad = math.radians(origin_lat)
        self.origin_lon_rad = math.radians(origin_lon)
        self.origin_alt = origin_alt

    def to_lla(self, x, y, z):
        R = 6378137.0
        lat = self.origin_lat_rad + (x / R)
        lon = self.origin_lon_rad + (y / (R * math.cos(self.origin_lat_rad)))
        return math.degrees(lat), math.degrees(lon), self.origin_alt - z
    

class TrajectoryForwardFlght:
    def __init__(self, altitude, speed, heading, sideslip=0):
        self.altitude = altitude
        self.speed = speed
        self.heading = heading
        self.sideslip = sideslip

    def get_state(self, time):
        x = self.speed * time * math.cos(math.radians(self.heading))
        y = self.speed * time * math.sin(math.radians(self.heading))
        z = -self.altitude
        phi = 0
        theta = 0
        psi = math.radians(self.heading - self.sideslip) 
        psi = psi % (2 * math.pi)
        vx = self.speed * math.cos(math.radians(self.heading))
        vy = self.speed * math.sin(math.radians(self.heading))
        vz = 0
        return x, y, z, phi, theta, psi, vx, vy, vz
    
class TrajectoryForwardFlghtAccelerated:
    def __init__(self, altitude, heading, initspeed, endspeed, acceleration, acceleration_starttime):
        self.altitude = altitude
        self.initspeed = initspeed
        self.endspeed = endspeed
        self.acceleration = acceleration
        self.acceleration_starttime = acceleration_starttime
        self.acceleration_endtime = acceleration_starttime + (endspeed - initspeed) / acceleration
        self.heading = heading

    def get_state(self, time):
        if time < self.acceleration_starttime:
            self.speed = self.initspeed
            dist = self.initspeed * time
        
        elif time > self.acceleration_endtime:
            self.speed = self.endspeed
            dist = self.initspeed * self.acceleration_endtime + 0.5 * self.acceleration * (self.acceleration_endtime - self.acceleration_starttime) ** 2 + self.endspeed * (time - self.acceleration_endtime)

        else:
            self.speed = self.initspeed + self.acceleration * (time - self.acceleration_starttime)
            dist = self.initspeed * time + 0.5 * self.acceleration * (time - self.acceleration_starttime) ** 2
        
        x = dist * math.cos(math.radians(self.heading))
        y = dist * math.sin(math.radians(self.heading))
        z = -self.altitude
        phi = 0
        theta = 0
        psi = math.radians(self.heading) 
        psi = psi % (2 * math.pi)
        vx = self.speed * math.cos(math.radians(self.heading))
        vy = self.speed * math.sin(math.radians(self.heading))
        vz = 0
        return x, y, z, phi, theta, psi, vx, vy, vz
    
class TrajectoryFlatTurn:
    def __init__(self, altitude, speed, radius):
        self.altitude = altitude
        self.speed = speed
        self.turn_radius = radius

    def get_state(self, time):
        x = self.turn_radius * math.cos(self.speed * time / self.turn_radius)
        y = self.turn_radius * math.sin(self.speed * time / self.turn_radius)
        z = -self.altitude
        phi = 0
        theta = 0
        psi = (self.speed * time / self.turn_radius + math.pi / 2) % (2 * math.pi)
        vx = -self.speed * math.sin(self.speed * time / self.turn_radius)
        vy = self.speed * math.cos(self.speed * time / self.turn_radius)
        vz = 0
        return x, y, z, phi, theta, psi, vx, vy, vz
    
class TrajectoryCoordinatedTurn:
    def __init__(self, altitude, speed, radius):
        self.altitude = altitude
        self.speed = speed
        self.turn_radius = radius
        self.G = 9.81

    def get_state(self, time):
        x = self.turn_radius * math.cos(self.speed * time / self.turn_radius)
        y = self.turn_radius * math.sin(self.speed * time / self.turn_radius)
        z = -self.altitude
        phi = math.atan(self.speed * self.speed / (self.turn_radius * self.G))
        theta = 0
        psi = (self.speed * time / self.turn_radius + math.pi / 2) % (2 * math.pi)
        vx = -self.speed * math.sin(self.speed * time / self.turn_radius)
        vy = self.speed * math.cos(self.speed * time / self.turn_radius)
        vz = 0
        return x, y, z, phi, theta, psi, vx, vy, vz


class TrajectoryHeightChange:
    def __init__(self, altitude, speed, heading, amplitude, max_rate):
        self.altitude = altitude
        self.speed = speed
        self.heading = heading
        self.amplitude = amplitude
        self.omega = max_rate / amplitude

    def get_state(self, time):
        x = self.speed * time * math.cos(math.radians(self.heading))
        y = self.speed * time * math.sin(math.radians(self.heading))
        z = -self.altitude + self.amplitude * math.sin(time * self.omega)

        vx = self.speed * math.cos(math.radians(self.heading))
        vy = self.speed * math.sin(math.radians(self.heading))
        vz = self.amplitude * self.omega * math.cos(time * self.omega)


        phi = 0
        theta = math.atan2(-vz, self.speed)
        psi = math.radians(self.heading) 

        return x, y, z, phi, theta, psi, vx, vy, vz