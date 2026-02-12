
int waterSensorPin = A0; 
int lightSensorPin = A2;
int ledPin = LED_BUILTIN; 

const unsigned long DELAY_MS = 1000;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  //  Serial.println("Moisture sensor test starting...");
  //  Serial.println("Phototransistor test starting...");
}


void loop() {
  int waterValue = analogRead(waterSensorPin); 
  int lightValue = analogRead(lightSensorPin);

  Serial.print("{\"water\":");
  Serial.print(waterValue);
  Serial.print(",\"light\":");
  Serial.print(lightValue);
  Serial.println("}");

  delay(DELAY_MS); 
}


//  Serial.println("\n\n*************************************");
//  Serial.print("Soil moisture value: ");
//  Serial.println(waterValue);  
//  Serial.print("Light level: ");
//  Serial.println(lightValue);

//  // LED logic: ON if soil is dry
//  if(waterValue > threshold) {
//    Serial.println("HIGH");
//    digitalWrite(ledPin, HIGH);
//  } else {
//    digitalWrite(ledPin, LOW);
//  }


//
//
//
//
////
////Soil condition  Approx. Arduino reading (0–1023)  Notes
////Air / unplugged 550–650 Highest reading, completely dry baseline
////Very dry soil 450–550 Needs watering soon
////Moderately moist  300–450 Ideal for most plants
////Wet / saturated 180–300 Too much water — stop watering
////Submerged in water  150–250 Max moisture, not safe for long-term use
