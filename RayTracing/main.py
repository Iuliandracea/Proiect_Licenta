import sys

from vec3 import Vec3, unit_vector
from vec3 import Vec3 as Color
from ray import Ray
from Hittable import Hittable, HittableList, HitRecord
from Sphere import Sphere


def write_color(f, v: Color):
    r = int(255.999 * v.x())
    g = int(255.999 * v.y())
    b = int(255.999 * v.z())
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

    # World
    world = HittableList()
    world.add(Sphere(Vec3(0.0, 0.0, -1.0), 0.5))
    world.add(Sphere(Vec3(0.0, -100.5, -1.0), 100.0))

    # Camera
    viewport_height = 2.0
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1.0

    origin = Vec3()
    horizontal = Vec3(viewport_width, 0.0, 0.0)
    vertical = Vec3(0.0, viewport_height, 0.0)
    lower_left_corner = origin - horizontal / 2.0 - vertical / 2.0 - Vec3(0.0, 0.0, focal_length)

    # Render
    img = open('img.ppm', 'w')
    img.write(f'P3\n{image_width} {image_height}\n255\n')

    for i in range(image_height - 1, -1, -1):
        print(f'Lines Remaining {i}\n', file=sys.stderr)
        for j in range(image_width):
            u = float(j) / float(image_width - 1)
            v = float(i) / float(image_height - 1)
            r = Ray(origin, lower_left_corner + u * horizontal + v * vertical - origin)
            pixel = ray_color(r, world)
            write_color(img, pixel)

    img.close()


if __name__ == '__main__':
    main()
