int boton = 7;
//int luz = 8;
int luz = LED_BUILTIN;
int torniquete = 10;
int tiempo = 5000; 

void setup() {
  
  pinMode(torniquete, OUTPUT);
  pinMode(luz, OUTPUT);
  pinMode(boton, INPUT_PULLUP);

  digitalWrite(torniquete, LOW);
  digitalWrite(luz, LOW);
  
  Serial.begin(9600);
}

void loop() {
  
  if (Serial.available() > 0) {
    int input = Serial.read();
      if (input == '1') {
        
        digitalWrite(luz, HIGH);
        digitalWrite(torniquete, HIGH);
        delay(tiempo);
        digitalWrite(luz, LOW);
        digitalWrite(torniquete, LOW);
      }
  }

  if (digitalRead(boton) == HIGH) {

        delay(20);

        if (digitalRead(boton) == HIGH) {
          digitalWrite(luz, HIGH);
          digitalWrite(torniquete, HIGH);
          delay(tiempo);
          digitalWrite(luz, LOW);
          digitalWrite(torniquete, LOW);
          Serial.println("boton");
        }
      }
}
