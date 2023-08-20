
#include "Keyboard.h"

char START_CHAR = 'r';
char STOP_CHAR= 'q';
void setup() {
  // put your setup code here, to run once:

  bool canRun=false;

  

    pinMode(8, OUTPUT);

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


int lastTime=millis();
long currDelay=2000;

int MAX_SPEED=100; //found min at 75?

int MIN_SPEED=100000;

// int microsDecremented=25;

// int microsIncremented=25;

int timeBetweenDecrements=2;


long requestedDelay=1000;

bool onOf=true;


// long getInput(){
//     if (Serial.available()>0){
//       long inChar = Serial.parseInt();

//       return inChar;
//     }
//     return -1;
// }


//http://www.gammon.com.au/serial
void process_data (const char * data)
  {
  // for now just display it
  // (but you could compare it to some value, convert to an integer, etc.)
    Serial.println (data);
    requestedDelay=atoi(data);

    if (requestedDelay==-1){
      onOf=false;
      currDelay=100000;
      Serial.println(currDelay);
    }
    else{
      onOf=true;
    }

    
    Serial.println(requestedDelay);
  }  // end of process_data


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



int checkBadDelays(int currDelay, bool accelDir){ //true = going up in delay (down in speed), false = going down in delay (up in speed)

  if (currDelay>=3100 && currDelay<=3400){
      return accelDir ? 3300 : 2500;
  }

  if (currDelay>=6100 && currDelay<=6400){
      return accelDir ? 5900 : 5200;
  }

  if (currDelay>=9100 && currDelay<=9400){
      return accelDir ? 8600 : 7700;
  }



 
  return currDelay;
}



void loop() {
  // put your main code here, to run repeatedly: 
  // long currInput = getInput();

  while (Serial.available () > 0){
    processIncomingByte (Serial.read ());
  }
  if (onOf){
    if (currDelay>requestedDelay){

    

    int currTime = millis();

    if (currTime-lastTime>=timeBetweenDecrements){
      lastTime=currTime;
      currDelay-=(int)(0.01*currDelay);
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

  else if (currDelay>requestedDelay-50 && currDelay<requestedDelay+50){

    

    digitalWrite(8, HIGH);
    delayMicroseconds(currDelay);
    digitalWrite(8, LOW);
    delayMicroseconds(currDelay);
  }
  else if (currDelay<requestedDelay){

    
    int currTime = millis();

    if (currTime-lastTime>=timeBetweenDecrements){
      lastTime=currTime;
      currDelay+=(int)(0.01*currDelay);
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
  }
  


  


  
  
  






}
