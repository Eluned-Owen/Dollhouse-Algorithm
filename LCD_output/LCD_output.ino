#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>

Adafruit_LiquidCrystal lcd(0);

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.print("Dollhouse Algorithm");
}

void loop() {
  if (Serial.available() > 0) {
    //If there's bytes in the serial, read them, trim them and note when they have a new line \n
    String incomingMessage = Serial.readString();

    incomingMessage.trim();

    int newlineIndex = incomingMessage.indexOf('\n');

    String line1;
    String line2;

    if (newlineIndex >= 0) {
      line1 = incomingMessage.substring(0, newlineIndex);
      line2 = incomingMessage.substring(newlineIndex + 1);
    } else {
      line1 = incomingMessage.substring(0, 16);
      line2 = incomingMessage.substring(16, 32);
    }

    lcd.clear();

    lcd.setCursor(0, 0);
    lcd.print(line1.substring(0, 16));

    lcd.setCursor(0, 1);
    lcd.print(line2.substring(0, 16));
  }
}