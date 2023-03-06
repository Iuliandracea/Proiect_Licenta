import math
import random
from abc import ABC, abstractmethod
from ray import Ray
from vec3 import Vec3 as Color
from vec3 import unit_vector, dot, random_in_unit_sphere, random_unit_vector, reflect, refract
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
    def __init__(self, a: Color, f: float):
        self.albedo = a
        self.fuzz = f if f < 1.0 else 1.0

    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        reflected = reflect(unit_vector(r_in.direction()), rec.normal)

        r = Ray(rec.p, reflected + self.fuzz * random_in_unit_sphere())
        scattered.orig = r.orig
        scattered.dir = r.dir

        for i in range(len(attenuation.v)):
            attenuation.v[i] = self.albedo.v[i]

        return dot(scattered.direction(), rec.normal) > 0


class Dielectric(Material):
    def __init__(self, refraction_index):
        self.ri = refraction_index

    def scatter(self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray) -> bool:
        for i in range(len(attenuation.v)):
            attenuation.v[i] = 1.0

        refraction_ratio = 1.0 / self.ri if rec.front_face else self.ri
        unit_dir = unit_vector(r_in.direction())

        cos_theta = min(dot(-unit_dir, rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta**2)
        no_refract = refraction_ratio * sin_theta > 1.0

        if no_refract or Dielectric.reflectance(cos_theta, refraction_ratio) > random.random():
            ray_dir = reflect(unit_dir, rec.normal)
        else:
            ray_dir = refract(unit_dir, rec.normal, refraction_ratio)

        r = Ray(rec.p, ray_dir)
        scattered.orig = r.orig
        scattered.dir = r.dir

        return True

    @staticmethod
    def reflectance(cos: float, ref_ratio: float):
        r0 = (1.0 - ref_ratio) / (1.0 + ref_ratio)
        r0 = r0 * r0
        return r0 + (1.0 - r0) * (1.0 - cos)**5
