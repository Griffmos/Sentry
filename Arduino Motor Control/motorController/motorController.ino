
#include "Keyboard.h"

char START_CHAR = 'r';
char STOP_CHAR = 'q';
char RETURN_CHAR = 'g'

void(* resetFunc) (void) = 0; //declare reset function @ address 0


void setup() {
  // put your setup code here, to run once:

  bool canRun = false;



  pinMode(8, OUTPUT);

  pinMode(10, OUTPUT);

  Serial.begin(9600);

  while (!canRun) {
    if (Serial.available() > 0) {
      char inChar = Serial.read();
      if (inChar == START_CHAR) {
        canRun = true;
      }
    }
  }
}











const unsigned int MAX_INPUT = 50;

void processIncomingByte(const byte inByte) {
  static char input_line[MAX_INPUT];
  static unsigned int input_pos = 0;

  switch (inByte) {

    case '\n':                    // end of text
      input_line[input_pos] = 0;  // terminating null byte

      // terminator reached! process input_line here ...
      process_data(input_line);

      // reset buffer for next time
      input_pos = 0;
      break;

    case '\r':  // discard carriage return
      break;

    default:
      // keep adding if not full ... allow for terminating null byte
      if (input_pos < (MAX_INPUT - 1))
        input_line[input_pos++] = inByte;
      break;

  }  // end of switch

}  // end of processIncomingByte



//hardware constants
int GEAR_RATIO = 1

int NUM_STEPS_IN_BIG_GEAR_REV = GEAR_RATIO*1600;

//extreme constants
long MIN_DELAY = 50;

long MAX_DELAY = 15000;

long STOP_SPEED = 5000;



//performance constants

int timeBetweenDecrements = 2;

float accelMultiplier = 0.1;

float deccelMultiplier = 0.1;

float errorPercent = 0.05;


//tracking variables

unsigned long long lastTime = millis();

long currDelay = STOP_SPEED;

int direction = 0;  //1 is clockwise, -1 is ccw, 0 is uninitialized

int currPos = 0;

bool onOff = false;



//requested/target values

long requestedDelay = 0;

bool reqStop = true;  //requested to stop

int reqDirection = 0;  //1 is clockwise, -1 is ccw, 0 is uninitialized

bool reqChangeDir = false;


void returnPos(){
    return currPos;
}


//http://www.gammon.com.au/serial
void process_data(const char* data) {
  // for now just display it
  // (but you could compare it to some value, convert to an integer, etc.)

    if (data[0]==STOP_CHAR){
        resetFunc();
    }
    if (data[0]==RETURN_CHAR){
        Serial.write(returnPos());
    }
    else{
        requestedDelay = atoi(data);

        if (requestedDelay == 0) {

        reqStop = true;
        //requestedDelay=max(STOP_SPEED,currDelay);
        }
        else {
            reqDirection = (requestedDelay > 0) ? 1 : -1;


            if (reqDirection !=0 && reqDirection != direction) {
                reqChangeDir = true;
            }

            // Serial.println(requestedDelay);
            // Serial.println(reqDirection);
            // Serial.println(direction);
            //Serial.println(reqChangeDir);

            requestedDelay = abs(requestedDelay);


            if (requestedDelay < MIN_DELAY) {
            requestedDelay = MIN_DELAY;
            }
            if (requestedDelay > MAX_DELAY) {
            requestedDelay = MAX_DELAY;
            reqStop = true;
            } else {
            reqStop = false;
            }


            Serial.write(1);
            onOff = true;
         }
    }

  


  //Serial.println(requestedDelay);
  //Serial.println(currDelay);
}  // end of process_data



// int checkBadDelays(long delay, bool accelDir){ //true = going up in delay (down in speed), false = going down in delay (up in speed)

//   // if (delay>=2900 && delay<=3500){
//   //     return accelDir ? 3500 : 2900;
//   // }

//   return delay;
// }

void step(long delay) {
  currPos +=direction;
  digitalWrite(8, HIGH);
  delayMicroseconds(delay);
  digitalWrite(8, LOW);
  delayMicroseconds(delay);
}

void accelerate() {
    int currTime = millis();

  if (currTime - lastTime >= timeBetweenDecrements) {
    lastTime = currTime;
    currDelay -= (long)(accelMultiplier * currDelay);
  }

  //currDelay = checkBadDelays(currDelay, false);

  if (currDelay < MIN_DELAY) {
    currDelay = MIN_DELAY;
  }
  if (currDelay > MAX_DELAY) {
    currDelay = MAX_DELAY;
  }


  step(currDelay);
}

void holdSpeed() {

  //currDelay = checkBadDelays(currDelay, false);

  step(currDelay);
}

void deccelerate() {
  int currTime = millis();

  if (currTime - lastTime >= timeBetweenDecrements) {
    lastTime = currTime;
    currDelay += (long)(deccelMultiplier * currDelay);
  }

  //currDelay = checkBadDelays(currDelay, true);


  if (currDelay < MIN_DELAY) {
    currDelay = MIN_DELAY;
  }
  if (currDelay > MAX_DELAY) {
    currDelay = MAX_DELAY;
  }



  step(currDelay);
}


void loop() {
  // put your main code here, to run repeatedly:
  // long currInput = getInput();


  

  if (abs(currPos) >= NUM_STEPS_IN_BIG_GEAR_REV / 2 && (reqDirection>0) == (currPos > 0)) {
    reqStop = true;
  }

  while (Serial.available() > 0) {
    processIncomingByte(Serial.read());
  }

  if (reqStop) {
    if (currDelay < STOP_SPEED) {
      deccelerate();
    } else {
      onOff = false;
      reqStop = false;
      currDelay = STOP_SPEED;
    }
  } else if (reqChangeDir) {
    if (currDelay < STOP_SPEED) {
      deccelerate();
    } 
    else {
        direction = reqDirection;
      
      (direction==1) ? digitalWrite(10, HIGH) : digitalWrite(10, LOW);  //high is clockwise, low is counterclockwise
      reqChangeDir = false;
    }
  } else if (onOff) {
    if (currDelay > requestedDelay) {
      accelerate();
    }

    else if (currDelay > requestedDelay - (requestedDelay * errorPercent) && currDelay < requestedDelay + (requestedDelay * errorPercent)) {
      holdSpeed();
    } else if (currDelay < requestedDelay) {
      deccelerate();
    }
  }
}
