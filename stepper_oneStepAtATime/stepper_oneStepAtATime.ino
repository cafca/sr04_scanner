
#include <Stepper.h>

bool done = false;
const int fullRotation = 2048;
Stepper myStepper(fullRotation, 8, 10, 9, 11);


// negativ ist uhrzeigersinn
int steps = 100;  


void setup() { }

void loop() {
  if (done == false) {
    myStepper.setSpeed(5);
    myStepper.step(steps);
    done = true;
  }
}

