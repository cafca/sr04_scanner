import PIL.Image
import serial
import time
import math
import json
from random import random


class Circular(object):
    def __init__(self, total, rotations=0.25, size=(2000, 2000), scale=0.8, steps=3):
        self.size = size
        self.total = total
        self.steps = steps
        self.rotations = rotations
        self.counter = 0
        self.radius = scale * size[0] / 2
        self.img = PIL.Image.new('RGB', size)
        self.pixels = self.img.load()
        self.set_pixel(size[0] / 2, size[1] / 2)

    def setup(self, rotations, steps):
        self.rotations = rotations
        self.steps = steps
        print("Circle size {} with {} steps".format(self.size, self.steps))

    def set_pixel(self, x, y):
        self.pixels[x, y] = (255, 255, 255)
        self.pixels[x + 1, y] = (255, 255, 255)
        self.pixels[x + 1, y + 1] = (255, 255, 255)
        self.pixels[x, y + 1] = (255, 255, 255)

    def place_point(self, value):

        # Kreis zeichnen
        x = self.radius * math.cos(3.14 * self.counter / self.total * 2.0)
        y = self.radius * math.sin(3.14 * self.counter / self.total * 2.0)

        # In die Mitte schieben
        x += self.size[0] / 2
        y += self.size[1] / 2

        # Je nach Wert korrigieren
        x = (x * value) + (self.size[0] / 2) * (1.0 - value)
        y = (y * value) + (self.size[1] / 2) * (1.0 - value)

        try:
            self.set_pixel(x, y)
        except IndexError:
            print("Tried placing {} {}".format(x, y))

        self.counter += self.steps

    def show(self):
        self.img.show()

    def save(self, fn="output.png"):
        self.img.save(fn, "PNG")


if __name__ == "__main__":

    with open("data.json") as f:
        data = json.load(f)

    c = Circular(len(data), 0.25)
    data = [(x / 400.0 if x <= 400.0 else 1.0) for x in data]

    for d in data:
        c.place_point(d)

    c.show()
