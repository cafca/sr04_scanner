import PIL.Image
import serial
import time
import math
import json
from time import sleep
from random import random


class Circular(object):
    def __init__(self, total, rotations, size=(2000, 2000), scale=0.8, steps=5):
        self.size = size
        self.step = total
        self.steps = steps
        self.rotations = rotations
        self.counter = 0
        self.radius = scale * size[0] / 2
        self.img = PIL.Image.new('RGB', size)
        self.pixels = self.img.load()
        print("Circle size {} with {} steps".format(size, self.step))
        self.pixels[size[0] / 2, size[1] / 2] = (1, 0, 100)

    def place_point(self, value):
        def pixel(x, y):
            self.pixels[x, y] = (255, 255, 255)
            self.pixels[x + 1, y] = (255, 255, 255)
            self.pixels[x + 1, y + 1] = (255, 255, 255)
            self.pixels[x, y + 1] = (255, 255, 255)

        # Kreis zeichnen
        x = self.radius * math.cos(3.14 * -self.counter / self.step * 2.0 * self.rotations)
        y = self.radius * math.sin(3.14 * -self.counter / self.step * 2.0 * self.rotations)

        # In die Mitte schieben
        x += self.size[0] / 2
        y += self.size[1] / 2

        # Je nach Wert korrigieren
        x = (x * value) + (self.size[0] / 2) * (1.0 - value)
        y = (y * value) + (self.size[1] / 2) * (1.0 - value)

        try:
            pixel(x, y)
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
