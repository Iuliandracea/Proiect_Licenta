import math
from hittable import Hittable, HitRecord
from vec3 import Vec3, dot
from ray import Ray
from material import Material


class Sphere(Hittable):
    def __init__(self, c=Vec3(), radius=1.0, m: Material = None):
        self.center = c
        self.radius = radius
        self.mat = m

    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:
        oc = r.origin() - self.center
        a = r.direction().length_squared()
        half_b = dot(r.direction(), oc)
        c = oc.length_squared() - self.radius**2

        delta = half_b**2 - a * c
        if delta < 0:
            return False

        sqr = math.sqrt(delta)

        root = (-half_b - sqr) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqr) / a
            if root < t_min or t_max < root:
                return False

        rec.t = root
        rec.p = r.at(root)
        out_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, out_normal)
        rec.mat_ptr = self.mat

        return True
