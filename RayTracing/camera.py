import math

from vec3 import Vec3, unit_vector, cross
from ray import Ray


class Camera:
    def __init__(self, look_from: Vec3, look_at: Vec3, vup: Vec3, vfov: float, aspect_ratio: float):
        theta = math.radians(vfov)
        h = math.tan(theta / 2.0)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        w = unit_vector(look_from - look_at)
        u = unit_vector(cross(vup, w))
        v = cross(w, u)

        self.origin = look_from
        self.horizontal = viewport_width * u
        self.vertical = viewport_height * v
        self.lower_left_corner = -1.0 * self.horizontal / 2.0 - self.vertical / 2.0 - w

    def get_ray(self, s: float, t: float):
        return Ray(self.origin, self.lower_left_corner + s * self.horizontal + t * self.vertical)
