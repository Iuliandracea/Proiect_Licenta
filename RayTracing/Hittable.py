from abc import ABC, abstractmethod
from ray import Ray
from vec3 import Vec3, dot


class HitRecord:
    def __init__(self, p=Vec3(), n=Vec3(), t=0.0):
        self.p = p
        self.normal = n
        self.t = t
        self.front_face = False

    def set_face_normal(self, r: Ray, out_normal: Vec3):
        self.front_face = dot(r.direction(), out_normal) < 0
        self.normal = out_normal if self.front_face else -out_normal

    def __repr__(self):
        return f'{self.p} {self.normal} {self.t} {self.front_face}'


class Hittable(ABC):
    @abstractmethod
    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:
        pass


class HittableList(Hittable):
    def __init__(self):
        self.l: list[Hittable] = []

    def add(self, obj: Hittable):
        self.l.append(obj)

    def clear(self):
        self.l.clear()

    def hit(self, r: Ray, t_min: float, t_max: float, rec: HitRecord) -> bool:
        temp_rec = HitRecord()
        any_hit = False
        closest = t_max

        for obj in self.l:
            if obj.hit(r, t_min, closest, temp_rec):
                any_hit = True
                closest = temp_rec.t

                # rec = temp_rec
                rec.t = temp_rec.t
                rec.normal = temp_rec.normal
                rec.p = temp_rec.p
                rec.front_face = temp_rec.front_face

        return any_hit
