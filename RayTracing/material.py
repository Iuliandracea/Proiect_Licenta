from abc import ABC, abstractmethod
from ray import Ray
from vec3 import Vec3 as Color
from vec3 import unit_vector, dot, random_unit_vector, reflect
from hittable import HitRecord


class Material(ABC):
    @abstractmethod
    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        pass


class Lambertian(Material):
    def __init__(self, a: Color):
        self.albedo = a

    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        scatter_direction = rec.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        r = Ray(rec.p, scatter_direction)
        scattered.orig = r.orig
        scattered.dir = r.dir

        for i in range(len(attenuation.v)):
            attenuation.v[i] = self.albedo.v[i]

        return True


class Metal(Material):
    def __init__(self, a: Color):
        self.albedo = a

    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        reflected = reflect(unit_vector(r_in.direction()), rec.normal)

        r = Ray(rec.p, reflected)
        scattered.orig = r.orig
        scattered.dir = r.dir

        for i in range(len(attenuation.v)):
            attenuation.v[i] = self.albedo.v[i]

        return dot(scattered.direction(), rec.normal) > 0


