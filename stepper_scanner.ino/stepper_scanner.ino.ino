/*
* Raumvermessung
*
* 25.12.2017
*
*/
#include <Stepper.h>

const int STEPS_PER_REVOLUTION = 2048;

// Wie viele Umdrehungen sollen gemacht werden?
const float ROTATIONS = 0.5;

// Wie viele Messungen gemittelt werden sollen
const int REPEAT_MEASUREMENTS = 1;

const int STEPS_AT_A_TIME = 5;

// defines pins numbers
const int TRIG_PIN = 7;
const int ECHO_PIN = 6;

Stepper myStepper(STEPS_PER_REVOLUTION, 8, 10, 9, 11);

// defines variables
float distance;
float timings;
int stepCount;
bool done;

void setup() {
  myStepper.setSpeed(10);

  pinMode(TRIG_PIN, OUTPUT); // Sets the TRIG_PIN as an Output
  pinMode(ECHO_PIN, INPUT); // Sets the ECHO_PIN as an Input

  Serial.begin(9600); // Starts the serial communication
  Serial.println("[");

  stepCount = 0;
  done = false;
}

void step() {
  myStepper.step(STEPS_AT_A_TIME);
  stepCount+= STEPS_AT_A_TIME;
  delay(60);
}

float measure() {
  timings = 0.0;

  for (int i=0; i < REPEAT_MEASUREMENTS; i++) {
    // Clears the TRIG_PIN
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    // Sets the TRIG_PIN on HIGH state for 10 micro seconds
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    // Reads the ECHO_PIN, returns the sound wave travel time in microseconds
    timings += pulseIn(ECHO_PIN, HIGH);
    delay(60);
  }
  return (timings / float(REPEAT_MEASUREMENTS)) * 0.034 / 2;
}

void loop() {
  if (stepCount < (ROTATIONS * STEPS_PER_REVOLUTION)) {
    // Messen, bis STEPS_PER_REVOLUTION erreich wurde
    float measurement = measure();
    if (measurement < 400.0) {
      Serial.println(measurement);
    } else {
      Serial.println("0.0");
    }
    step();
  }

  if (stepCount >= (ROTATIONS * STEPS_PER_REVOLUTION) && done == false) {
    // Zurückdrehen
    myStepper.setSpeed(10);
    myStepper.step(-1.0 * int(ROTATIONS * STEPS_PER_REVOLUTION));
    done = true;
    Serial.println("]");
  }
}

