
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
int currDelay=2000;

int MAX_SPEED=125; //found min at 75?

int MIN_SPEED=100000;

// int microsDecremented=5;

// int microsIncremented=5;

int timeBetweenDecrements=2;


int requestedSpeed=1000;


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
    requestedSpeed=atoi(data);
    Serial.println(requestedSpeed);
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





void loop() {
  // put your main code here, to run repeatedly: 
  // long currInput = getInput();

  while (Serial.available () > 0){
    processIncomingByte (Serial.read ());
  }
  // switch(currInput){
  //   case -1:
  //     break;
  //   case 0:
  //     break;
  //   default:
  //     requestedSpeed=currInput;
  //     //Serial.println(requestedSpeed);
  // }
  
  


  if (currDelay>requestedSpeed){

    

    int currTime = millis();

    if (currTime-lastTime>=timeBetweenDecrements){
      lastTime=currTime;
      currDelay-=(int)(0.1*currDelay);
    
    }

    if (currDelay<MAX_SPEED){
      currDelay=MAX_SPEED;
    }


  
    digitalWrite(8, HIGH);
    delayMicroseconds(currDelay);
    digitalWrite(8, LOW);
    delayMicroseconds(currDelay);
  }

  else if (currDelay==requestedSpeed){

    

    digitalWrite(8, HIGH);
    delayMicroseconds(currDelay);
    digitalWrite(8, LOW);
    delayMicroseconds(currDelay);
  }
  else if (currDelay<requestedSpeed){

    
    int currTime = millis();

    if (currTime-lastTime>=timeBetweenDecrements){
      lastTime=currTime;
      currDelay+=(int)(0.1*currDelay);
    
    }

    if (currDelay<MAX_SPEED){
      currDelay=MAX_SPEED;
    }


  
    digitalWrite(8, HIGH);
    delayMicroseconds(currDelay);
    digitalWrite(8, LOW);
    delayMicroseconds(currDelay);
  }


  
  
  






}
