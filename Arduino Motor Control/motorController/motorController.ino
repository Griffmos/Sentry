
#include "Keyboard.h"

char START_CHAR = 'r';
char STOP_CHAR= 'q';
void setup() {
  // put your setup code here, to run once:

  bool canRun=false;

  

    pinMode(8, OUTPUT);

    pinMode(10, OUTPUT);

    Serial.begin(9600);

  while (!canRun){
    if (Serial.available()>0){
      char inChar = Serial.read();
      if (inChar==START_CHAR){
        canRun=true;
      }
    }
  }

    
}











const unsigned int MAX_INPUT = 50;

void processIncomingByte (const byte inByte)
  {
  static char input_line [MAX_INPUT];
  static unsigned int input_pos = 0;

  switch (inByte)
    {

    case '\n':   // end of text
      input_line [input_pos] = 0;  // terminating null byte
      
      // terminator reached! process input_line here ...
      process_data (input_line);
      
      // reset buffer for next time
      input_pos = 0;  
      break;

    case '\r':   // discard carriage return
      break;

    default:
      // keep adding if not full ... allow for terminating null byte
      if (input_pos < (MAX_INPUT - 1))
        input_line [input_pos++] = inByte;
      break;

    }  // end of switch
   
  } // end of processIncomingByte  


long MAX_SPEED=100; //found min at 75?

long MIN_SPEED=15000;

long STOP_SPEED=5000;

int lastTime=millis();
long currDelay=STOP_SPEED;




int timeBetweenDecrements=2;


long requestedDelay=0;

bool reqStop=true; //requested to stop

bool onOff=false;


bool direction=true; // true = clockwise, positive number || false = counterclockwise, negative number
bool reqDirection=true;

bool reqChangeDir=false;


//http://www.gammon.com.au/serial
void process_data (const char * data)
  {
  // for now just display it
  // (but you could compare it to some value, convert to an integer, etc.)
    requestedDelay=atoi(data);

    if (requestedDelay==0){
  
      reqStop=true;
      //requestedDelay=max(STOP_SPEED,currDelay);
    }
    else{
      reqDirection = (requestedDelay>0) ? true : false;
      
      if (reqDirection!=direction){
        reqChangeDir=true;
      }

      requestedDelay=abs(requestedDelay);

      

      onOff=true;
    }

    
    Serial.println(requestedDelay);
  }  // end of process_data



int checkBadDelays(long currDelay, bool accelDir){ //true = going up in delay (down in speed), false = going down in delay (up in speed)

  if (currDelay>=2900 && currDelay<=3500){
      return accelDir ? 3500 : 2900;
  }

  if (currDelay>=6500 && currDelay<=5900){
      return accelDir ? 6500 : 5900;
  }

  if (currDelay>=8900 && currDelay<=9400){
      return accelDir ? 9400 : 8900;
  }



 
  return currDelay;
}


void accelerate(){
  int currTime = millis();

    if (currTime-lastTime>=timeBetweenDecrements){
      lastTime=currTime;
      currDelay-=(long)(0.025*currDelay);
      //currDelay-=microsDecremented;
    
    }

    currDelay = checkBadDelays(currDelay, false);

    if (currDelay<MAX_SPEED){
      currDelay=MAX_SPEED;
    }


  
    digitalWrite(8, HIGH);
    delayMicroseconds(currDelay);
    digitalWrite(8, LOW);
    delayMicroseconds(currDelay);
}

 void holdSpeed(){

    digitalWrite(8, HIGH);
    delayMicroseconds(currDelay);
    digitalWrite(8, LOW);
    delayMicroseconds(currDelay);
 }

 void deccelerate(){
    int currTime = millis();

    if (currTime-lastTime>=timeBetweenDecrements){
      lastTime=currTime;
      currDelay+=(long)(0.025*currDelay);
      //currDelay+=microsIncremented;
    
    }

    currDelay = checkBadDelays(currDelay, true);


    if (currDelay<MAX_SPEED){
      currDelay=MAX_SPEED;
    }


  
    digitalWrite(8, HIGH);
    delayMicroseconds(currDelay);
    digitalWrite(8, LOW);
    delayMicroseconds(currDelay);
 }


void loop() {
  // put your main code here, to run repeatedly: 
  // long currInput = getInput();

  while (Serial.available () > 0){
    processIncomingByte (Serial.read ());
  }

  if (reqStop){
    if (currDelay<STOP_SPEED){
      deccelerate();
    }
    else{
      onOff=false;
      reqStop=false;
      currDelay=STOP_SPEED;
    }
  }
  else if (reqChangeDir){
    if (currDelay<STOP_SPEED){
      deccelerate();
    }
    else{
      direction=reqDirection;
      (direction) ? digitalWrite(10, HIGH) : digitalWrite(10, LOW); //high is clockwise, low is counterclockwise
      reqChangeDir=false;
    }
  }
  else if (onOff){
    if (currDelay>requestedDelay){
      accelerate();
    }

    else if (currDelay>requestedDelay-50 && currDelay<requestedDelay+50){
      holdSpeed();
    }
    else if (currDelay<requestedDelay){
      deccelerate();
    }
  }
}
