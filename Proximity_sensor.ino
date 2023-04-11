// Define the pins
const int sensorPin = D5; // Change D5 to the pin connected to your sensor

// Initialize the serial communication
void setup() {
  Serial.begin(9600);
}

void loop() {
  // Read the sensor input
  int sensorValue = digitalRead(sensorPin);

  // If an object is detected, output "New input detected" and "........." repeatedly
  if (sensorValue == HIGH) {
    Serial.println("New input detected");
    while (sensorValue == HIGH) {
      Serial.println(".........");
      sensorValue = digitalRead(sensorPin);
      delay(100);
    }
  }
  // If no object is detected, output "Removed"
  else {
    Serial.println("Removed");
  }

  // Wait a short amount of time before repeating the loop
  delay(100);
}
