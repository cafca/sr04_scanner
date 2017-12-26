import PIL.Image
import serial

from circle import Circular

MAX_DISTANCE = 250.0
static_source = False

filename = "data6"

started = False
done = False
i = 0
c = Circular(2048)


if static_source:
    source = open('{}.data'.format(filename), 'rb')
else:
    source = serial.Serial('/dev/cu.usbmodem1421', 9600)
    out = open('{}.data'.format(filename), "wb")

while not done:
    msg = source.readline()

    if not static_source:
        out.write(msg)

    print(msg.strip())

    if msg.startswith(b"DONE"):
        if static_source:
            source.close()
        else:
            out.close()

        print("Saving to {}.png".format(filename))
        c.save('{}.png'.format(filename))
        c.show()
        done = True

    if started and not done:
        distance = float(msg)
        print(str(distance)),
        value = distance / MAX_DISTANCE if distance <= MAX_DISTANCE else 1.0
        c.place_point(value)

    if msg.startswith(b"OK"):
        started = True
        print("starting")

        rotations = source.readline()
        if not static_source:
            out.write(rotations)
        rotations = float(rotations)

        steps_at_a_time = source.readline()
        if not static_source:
            out.write(steps_at_a_time)
        steps_at_a_time = int(steps_at_a_time)

        print("{} measurements for {} rotations".format(
            int(2048 * rotations / steps_at_a_time), rotations))

        c.setup(rotations, steps_at_a_time)
