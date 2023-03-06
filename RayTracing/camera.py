import math

from vec3 import Vec3, unit_vector, cross, random_in_unit_disk
from ray import Ray


class Camera:
    def __init__(self, look_from: Vec3, look_at: Vec3, vup: Vec3, vfov: float,
                 aspect_ratio: float, aperture: float, focus_dist: float):
        theta = math.radians(vfov)
        h = math.tan(theta / 2.0)
        viewport_height = 2.0 * h
        viewport_width = aspect_ratio * viewport_height

        self.w = unit_vector(look_from - look_at)
        self.u = unit_vector(cross(vup, self.w))
        self.v = cross(self.w, self.u)

        self.origin = look_from
        self.horizontal = focus_dist * viewport_width * self.u
        self.vertical = focus_dist * viewport_height * self.v
        self.lower_left_corner = -1.0 * self.horizontal / 2.0 - self.vertical / 2.0 - focus_dist * self.w

        self.lens_radius = aperture / 2.0

    def get_ray(self, s: float, t: float):
        rd = self.lens_radius * random_in_unit_disk()
        offset = self.u * rd.x() + self.v * rd.y()

        return Ray(self.origin + offset, self.lower_left_corner + s * self.horizontal + t * self.vertical - offset)
