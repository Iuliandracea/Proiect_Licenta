import math
import sys
import random

from vec3 import Vec3, unit_vector
from vec3 import Vec3 as Color
from ray import Ray
from hittable import Hittable, HittableList, HitRecord
from sphere import Sphere
from camera import Camera
from material import Lambertian, Metal, Dielectric


def clamp(x: float, min_val: float, max_val: float) -> float:
    if x < min_val:
        return min_val
    if x > max_val:
        return max_val
    return x


def write_color(f, pixel: Color, samples_per_pixel: int):
    scale = 1.0 / samples_per_pixel
    r = math.sqrt(scale * pixel.r())
    g = math.sqrt(scale * pixel.g())
    b = math.sqrt(scale * pixel.b())
    f.write(f'{256 * clamp(r, 0.0, 0.999)} {256 * clamp(g, 0.0, 0.999)} {256 * clamp(b, 0.0, 0.999)}\n')


def ray_color(r: Ray, world: Hittable, depth: int):
    rec = HitRecord()

    if depth <= 0:
        return Color()  # the same as Color(0.0, 0.0, 0.0)

    if world.hit(r, 0.001, float('inf'), rec):
        scattered = Ray()
        attenuation = Color()
        if rec.mat_ptr.scatter(r, rec, attenuation, scattered):
            return attenuation * ray_color(scattered, world, depth - 1)
        return Color(0.0, 0.0, 0.0)

    unit_direction = unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Color(1.0, 1.0, 1.0) + t * Color(0.5, 0.7, 1.0)


def main():
    # Image
    aspect_ratio = 16.0 / 9.0
    image_width = 400
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 50
    max_depth = 10

    # World
    world = HittableList()

    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left = Dielectric(1.5)
    material_right = Metal(Color(0.8, 0.6, 0.2), 0.0)

    world.add(Sphere(Vec3(0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Vec3(0.0, 0.0, -1.0), 0.5, material_center))
    world.add(Sphere(Vec3(-1.0, 0.0, -1.0), 0.5, material_left))
    world.add(Sphere(Vec3(-1.0, 0.0, -1.0), -0.4, material_left))
    world.add(Sphere(Vec3(1.0, 0.0, -1.0), 0.5, material_right))

    # Camera
    cam = Camera()

    # Render
    img = open('img.ppm', 'w')
    img.write(f'P3\n{image_width} {image_height}\n255\n')

    for i in range(image_height - 1, -1, -1):
        print(f'Lines Remaining {i}', file=sys.stderr)
        for j in range(image_width):
            pixel_color = Color()
            for s in range(samples_per_pixel):
                u = float(j + random.random()) / float(image_width - 1)
                v = float(i + random.random()) / float(image_height - 1)
                r = cam.get_ray(u, v)
                pixel_color += ray_color(r, world, max_depth)
            write_color(img, pixel_color, samples_per_pixel)

    img.close()


if __name__ == '__main__':
    main()
