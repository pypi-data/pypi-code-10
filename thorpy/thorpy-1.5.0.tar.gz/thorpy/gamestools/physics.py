"""for 2-dimensional physics"""
import math, pygame


#functions for discrete bodies (not continuum)
def discrete_compute_center_mass(m, q):
    """m : list of masses
    q : list of corresponding positions.
    """
    M = sum(m)
    Rx = sum([m[i]*q[i][0] for i in range(len(m))]) / M
    Ry = sum([m[i]*q[i][1] for i in range(len(m))]) / M
    R = pygame.math.Vector2(Rx,Ry)
    return R

def discrete_compute_I(m, q):
    """m : list of masses
    q : list of corresponding positions.
    """
    return sum([m[i]*q.length()**2 for i in range(len(m))])

def I_box(m,w,l):
    """Moment of a box with mass m, width w and length l."""
    return m * (w**2 + l**2) / 12

class RigidBody(object):

    def __init__(self, m=1, cm=(0,0), I=1, t=0, q=(0,0)):
        #translations:
        self.m = m #mass
        self.q = pygame.math.Vector2(q) #position
        self.v = pygame.math.Vector2(0,0) #velocity
        self.f = pygame.math.Vector2(0,0) #external force
        #rotations (z-axis only):
        self.cm = pygame.math.Vector2(cm) #to be updated!
        self.I = I # ~rotational mass
        self.t = t # ~rotational position
        self.w = 0 # ~rotational velocity (dteta/dt)
        self.tau = 0.# torque~rotational external force

    def kinetic_translation_energy(self):
        return 0.5 * self.m * self.vnorm()**2

    def kinetic_rotation_energy(self):
        return 0.5 * self.I * self.w**2

    def apply_force(self, force, point):
        """Returns:
            a) A vector that is the force for translations;
            b) A scalar that is the torque.
        """
        cm_to_point = self.cm - point
        if cm_to_point: #rotation + translation
            cm_unit = cm_to_point.normalize()
            angle = cm_to_point.angle_to(force)
            angle_rad = math.radians(angle)
            sin, cos = math.sin(angle_rad), math.cos(angle_rad)
            norm = force.length()
            return cos*norm*cm_unit, sin*norm*cm_to_point.length()
        else: #translation only
            return force, 0.


    def iterate(self, dt):
        #translation
        a = self.f / self.m
        self.v += a*dt
        self.q += self.v*dt
        #rotation
        a = self.tau / self.I
        self.w += a*dt
        self.t += self.w*dt

    def vnorm(self):
        return self.v.length()

    def get_cm_to_point(self, q):
        return self.cm - q

    def get_point(self, q0):
        """Returns the location of q0, taking into account the fact that the
        body rotate. q0 here is the location of the point for teta = 0.
        """
        cm_to_point = self.get_cm_to_point(q0)
        return q0 + cm_to_point - cm_to_point.rotate(self.t)
