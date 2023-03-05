import math


class Vec3:
    def __init__(self, e1=0.0, e2=0.0, e3=0.0):
        self.v = [0.0] * 3
        self.v[0] = e1
        self.v[1] = e2
        self.v[2] = e3

    def x(self):
        return self.v[0]

    def y(self):
        return self.v[1]

    def z(self):
        return self.v[2]

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


def dot(u: Vec3, v: Vec3):
    return u.x() * v.x() + u.y() * v.y() + u.z() * v.z()


def cross(u: Vec3, v: Vec3):
    return Vec3(u.y() * v.z() - u.z() * v.y(), u.x() * v.z() - u.z() * v.x(), u.x() * v.y() - u.y() * v.x())


def unit_vector(u: Vec3):
    return u / u.length()
