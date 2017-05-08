int pm6 = 7;
int hf = 6;
int b3lypopt = 5;
int b3lypfreq = 4;
int mp2 = 3;
int finished = 2;
int button1 = 10;
int button2 = 9;
int button3 = 8;
int button1counter = 0;
int button2counter = 0;
int button3counter = 0;
int lastbutton1state = 0;
int lastbutton2state = 0;
int lastbutton3state = 0;

void setup(){
  Serial.begin(9600);
  pinMode(pm6, OUTPUT);
  pinMode(hf, OUTPUT);
  pinMode(b3lypopt, OUTPUT);
  pinMode(b3lypfreq, OUTPUT);
  pinMode(mp2, OUTPUT);
  pinMode(finished, OUTPUT);
  pinMode(button1, INPUT);
  pinMode(button2, INPUT);
  pinMode(button3, INPUT);
}

void loop(){
  int button1state = digitalRead(button1);
  int button2state = digitalRead(button2);
  int button3state = digitalRead(button3);
  if (button1state != lastbutton1state){
    if (button1state==HIGH){
      button1counter++;
    }
    delay(1000);
  }
  if (button2state != lastbutton2state){
    if (button2state==HIGH){
      button2counter++;
    }
    delay(50);
  }
  if (button3state != lastbutton3state){
    if (button3state==HIGH){
      button3counter++;
    }
    delay(50);
  }
  lastbutton1state = button1state;
  lastbutton2state = button2state;
  lastbutton3state = button3state;
    
  if (button1counter%2==0){
    Serial.println("button4");
  }
  if (button2counter%2==0){
    Serial.println("button5");
  }
  if (button3counter%2==0){
    Serial.println("button6");
  }
  if (button1counter%2!=0){
    Serial.println("button4");
  }
  if (button2counter%2!=0){
    Serial.println("button5");
  }
  if (button3counter%2!=0){
    Serial.println("button6");
  }
}
