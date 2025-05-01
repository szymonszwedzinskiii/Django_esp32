
const int ledPin = 2;
const int tempraturepin=15;
float temperature;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(ledPin,OUTPUT);
  pinMode(tempraturepin,INPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(ledPin,HIGH);
  int sensorValue = analogRead(tempraturepin);
  float voltage = sensorValue *(3.3 / 4095.0);
  temperature = voltage * 100.0;
  Serial.print("Temperatura: ");
  Serial.print(temperature);
  Serial.println();
  delay(1000);
  digitalWrite(ledPin,LOW);
  delay(1000);
}
