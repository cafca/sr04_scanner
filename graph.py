import PIL.Image
import serial
import time

from circle import Circular

STEPS_AT_A_TIME = 5
ROTATIONS = 0.5
NUM_POINTS = ROTATIONS * 2048
MAX_DISTANCE = 250.0
static_source = False

filename = "data3"

c = Circular(NUM_POINTS, ROTATIONS, steps=STEPS_AT_A_TIME)

started = False
done = False
i = 0


if static_source:
    f = open('{}.json'.format(filename), 'rb')
else:
    ser = serial.Serial('/dev/cu.usbmodem1421', 9600)
    out = open('{}.json'.format(filename), "wb")

while not done:
    msg = f.readline() if static_source else ser.readline()

    if not static_source:
        out.write(msg)

    print(msg)

    if msg.startswith(b"]"):
        done = True
        print("done")

    if started and not done:
        distance = float(msg)
        value = distance / MAX_DISTANCE if distance <= MAX_DISTANCE else MAX_DISTANCE
        c.place_point(value)
        c.save()

    if msg.startswith(b"["):
        started = True
        print("starting")

if static_source:
    f.close()
else:
    out.close()

print("Saving to {}.png".format(filename))
c.save('{}.png'.format(filename))
c.show()
