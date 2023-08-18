

void setup() {
  // put your setup code here, to run once:

    pinMode(8, OUTPUT);

    Serial.begin(9600);

    
}


int currDelay=20000;


void loop() {
  // put your main code here, to run repeatedly: 

  if (currDelay<100){
    currDelay=100;
  }
  
  digitalWrite(8, HIGH);
  delayMicroseconds(currDelay);
  digitalWrite(8, LOW);
  delayMicroseconds(currDelay);

  int currReduc=(int)(currDelay*0.025);

  if (currReduc<1){
    currReduc=1;
  }
  
  currDelay-=currReduc;

  








}
