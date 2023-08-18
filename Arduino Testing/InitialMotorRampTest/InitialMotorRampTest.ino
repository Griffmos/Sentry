

void setup() {
  // put your setup code here, to run once:

    pinMode(8, OUTPUT);

    Serial.begin(9600);

    
}


int lastTime=millis();
int currDelay=50;

void loop() {
  // put your main code here, to run repeatedly: 

  int currTime = millis();

  if (currTime-lastTime>=1000){
    lastTime=currTime;
    currDelay--;
    Serial.println(currTime);
    
  }

  if (currDelay<1){
    currDelay=1;
  }


  
  digitalWrite(8, HIGH);
  delay(currDelay);
  digitalWrite(8, LOW);
  delay(currDelay);
  






}
