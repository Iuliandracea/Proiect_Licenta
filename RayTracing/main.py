import sys
import random

from vec3 import Vec3, unit_vector
from vec3 import Vec3 as Color
from ray import Ray
from hittable import Hittable, HittableList, HitRecord
from sphere import Sphere
from camera import Camera


def clamp(x: float, min_val: float, max_val: float) -> float:
    if x < min_val:
        return min_val
    if x > max_val:
        return max_val
    return x


def write_color(f, pixel: Color, samples_per_pixel: int):
    scale = 1.0 / samples_per_pixel

    r = 256 * clamp(scale * pixel.r(), 0.0, 0.999)
    g = 256 * clamp(scale * pixel.g(), 0.0, 0.999)
    b = 256 * clamp(scale * pixel.b(), 0.0, 0.999)
    f.write(f'{r} {g} {b}\n')


def ray_color(r: Ray, world: Hittable):
    rec = HitRecord()
    if world.hit(r, 0.0, float('inf'), rec):
        return 0.5 * (rec.normal + 1.0)

    unit_direction = unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0)
    return (1.0 - t) * Color(1.0, 1.0, 1.0) + t * Color(0.5, 0.7, 1.0)


def main():
    # Image
    aspect_ratio = 16.0 / 9.0
    image_width = 400
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 100

    # World
    world = HittableList()
    world.add(Sphere(Vec3(0.0, 0.0, -1.0), 0.5))
    world.add(Sphere(Vec3(0.0, -100.5, -1.0), 100.0))

    # Camera
    cam = Camera()

    # Render
    img = open('img.ppm', 'w')
    img.write(f'P3\n{image_width} {image_height}\n255\n')

    for i in range(image_height - 1, -1, -1):
        print(f'Lines Remaining {i}\n', file=sys.stderr)
        for j in range(image_width):
            pixel_color = Color()
            for s in range(samples_per_pixel):
                u = float(j + random.random()) / float(image_width - 1)
                v = float(i + random.random()) / float(image_height - 1)
                r = cam.get_ray(u, v)
                pixel_color += ray_color(r, world)
            write_color(img, pixel_color, samples_per_pixel)

    img.close()


if __name__ == '__main__':
    main()
