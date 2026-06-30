#include "Adafruit_Thermal.h"
#include "SoftwareSerial.h"
#define baudrate 19600
#define TX_PIN 6 
#define RX_PIN 5

SoftwareSerial mySerial(RX_PIN, TX_PIN); // Declare SoftwareSerial obj first
Adafruit_Thermal printer(&mySerial);
void setup() {
  // put your setup code here, to run once:
  mySerial.begin(19200);
  printer.println("Printer is ready");

}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    //Read the string untill it sees a new line (\n)
    String msg = Serial.readStringUntil('\n');
    //Remove unwanted spaces, carriage returns, or newline characters from the start and end of the message.
    msg.trim();
    printer.println(msg);
  }


}
