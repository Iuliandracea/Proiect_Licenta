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


def random_scene():
    world = HittableList()

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Vec3(0.0, -1000.0, 0.0), 1000.0, ground_material))

    for a in range(-11, 11, 1):
        for b in range(-11, 11, 1):
            choose_mat = random.random()
            center = Vec3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())

            if (center - Vec3(4.0, 0.2, 0.0)).length() > 0.9:
                sphere_material = Lambertian(Vec3())

                if choose_mat < 0.8:  # diffuse
                    albedo = Vec3.random() * Vec3.random()
                    sphere_material = Lambertian(albedo)
                elif choose_mat < 0.95:  # metal
                    albedo = Vec3.random(0.5, 1.0)
                    fuz = random.random() / 2.0
                    sphere_material = Metal(albedo, fuz)
                else:  # dielectric
                    sphere_material = Dielectric(1.5)

                world.add(Sphere(center, 0.2, sphere_material))

    mat_1 = Dielectric(1.5)
    world.add(Sphere(Vec3(0.0, 1.0, 0.0), 1.0, mat_1))

    mat_2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Vec3(-4.0, 1.0, 0.0), 1.0, mat_2))

    mat_3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Vec3(4.0, 1.0, 0.0), 1.0, mat_3))

    return world


def three_balls_scene():
    world = HittableList()

    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left = Dielectric(1.5)
    material_right = Metal(Color(0.8, 0.6, 0.2), 0.0)

    world.add(Sphere(Vec3(0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Vec3(0.0, 0.0, -1.0), 0.5, material_center))
    world.add(Sphere(Vec3(-1.0, 0.0, -1.0), 0.5, material_left))
    world.add(Sphere(Vec3(-1.0, 0.0, -1.0), -0.45, material_left))
    world.add(Sphere(Vec3(1.0, 0.0, -1.0), 0.5, material_right))

    return world


def main():
    # Image
    aspect_ratio = 3.0 / 2.0
    image_width = 1200
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 50
    max_depth = 10

    # World
    world = random_scene()

    # Camera
    look_from = Vec3(13.0, 2.0, 3.0)
    look_at = Vec3(0.0, 0.0, 0.0)
    up = Vec3(0.0, 1.0, 0.0)
    dist_to_focus = 10.0  # (look_from - look_at).length()
    aperture = 0.1  # 2.0
    cam = Camera(look_from, look_at, up, 20.0, aspect_ratio, aperture, dist_to_focus)

    # Render
    img = open('final_img.ppm', 'w')
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
