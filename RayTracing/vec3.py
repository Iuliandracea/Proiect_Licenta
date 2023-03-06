import math
import random


class Vec3:
    def __init__(self, e1=0.0, e2=0.0, e3=0.0):
        self.v = [0.0] * 3
        self.v[0] = e1
        self.v[1] = e2
        self.v[2] = e3

    def x(self):
        return self.v[0]

    def r(self):
        return self.x()

    def y(self):
        return self.v[1]

    def g(self):
        return self.y()

    def z(self):
        return self.v[2]

    def b(self):
        return self.z()

    def __mul__(self, other):
        if isinstance(other, float):
            return Vec3(self.v[0] * other, self.v[1] * other, self.v[2] * other)
        if isinstance(other, Vec3):
            return Vec3(self.v[0] * other.x(), self.v[1] * other.y(), self.v[2] * other.z())

    def __neg__(self):
        return self * -1.0

    def __add__(self, other):
        if isinstance(other, float):
            return Vec3(self.v[0] + other, self.v[1] + other, self.v[2] + other)
        if isinstance(other, Vec3):
            return Vec3(self.v[0] + other.x(), self.v[1] + other.y(), self.v[2] + other.z())

    def __sub__(self, other):
        return self + (other * -1.0)

    def __truediv__(self, other):
        if isinstance(other, float):
            return self * (1.0 / other)
        if isinstance(other, Vec3):
            return Vec3(self.v[0] / other.x(), self.v[1] / other.y(), self.v[2] / other.z())

    def __rdiv__(self, other):
        if isinstance(other, float):
            return self * (1.0 / other)
        if isinstance(other, Vec3):
            return Vec3(self.v[0] / other.x(), self.v[1] / other.y(), self.v[2] / other.z())

    def __rmul__(self, other):
        if isinstance(other, float):
            return Vec3(self.v[0] * other, self.v[1] * other, self.v[2] * other)
        if isinstance(other, Vec3):
            return Vec3(self.v[0] * other.x(), self.v[1] * other.y(), self.v[2] * other.z())

    def length_squared(self):
        return sum([x**2 for x in self.v])

    def length(self):
        return math.sqrt(self.length_squared())

    def __repr__(self):
        return f'{self.v[0]} {self.v[1]} {self.v[2]}'

    def near_zero(self):
        s = 1e-8
        return math.fabs(self.v[0]) < s and math.fabs(self.v[1]) < s and math.fabs(self.v[2]) < s

    @staticmethod
    def random(min_val=0.0, max_val=0.0):
        if min_val == max_val and min_val == 0.0:
            return Vec3(random.random(), random.random(), random.random())
        dif = max_val - min_val
        return Vec3(min_val + dif * random.random(), min_val + dif * random.random(), min_val + dif * random.random())


def random_in_unit_sphere():
    while True:
        p = Vec3.random(-1.0, 1.0)
        if p.length_squared() < 1.0:
            return p


# For True Lambertian Reflection
def random_unit_vector():
    return unit_vector(random_in_unit_sphere())


def random_in_hemisphere(normal: Vec3):
    unit_sphere = random_in_unit_sphere()
    if dot(unit_sphere, normal) > 0.0:
        return unit_sphere
    else:
        return -unit_sphere


def dot(u: Vec3, v: Vec3):
    return u.x() * v.x() + u.y() * v.y() + u.z() * v.z()


def cross(u: Vec3, v: Vec3):
    return Vec3(u.y() * v.z() - u.z() * v.y(), u.x() * v.z() - u.z() * v.x(), u.x() * v.y() - u.y() * v.x())


def reflect(v: Vec3, n: Vec3):
    return v - 2 * dot(v, n) * n


def unit_vector(u: Vec3):
    return u / u.length()
