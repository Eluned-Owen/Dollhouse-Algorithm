#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>

Adafruit_LiquidCrystal lcd_1(0);
Adafruit_LiquidCrystal lcd_2(1);
Adafruit_LiquidCrystal lcd_3(2);

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  lcd_1.begin(16, 2);
  lcd_2.begin(16, 2);
  lcd_3.begin(16, 2);

  lcd_1.setBacklight(HIGH);
  lcd_2.setBacklight(HIGH);
  lcd_3.setBacklight(HIGH);

  lcd_1.print("LCD 1 ready");
  lcd_2.print("LCD 2 ready");
  lcd_3.print("LCD 3 ready");
}

void printToLCD(Adafruit_LiquidCrystal &lcd, String line1, String line2) {
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print(line1.substring(0, 16));

  lcd.setCursor(0, 1);
  lcd.print(line2.substring(0, 16));
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    int firstSep = msg.indexOf('|');
    int secondSep = msg.indexOf('|', firstSep + 1);

    if (firstSep == -1 || secondSep == -1) {
      return;
    }

    String target = msg.substring(0, firstSep);
    String line1 = msg.substring(firstSep + 1, secondSep);
    String line2 = msg.substring(secondSep + 1);

    if (target == "LCD1") {
      printToLCD(lcd_1, line1, line2);
    } else if (target == "LCD2") {
      printToLCD(lcd_2, line1, line2);
    } else if (target == "LCD3") {
      printToLCD(lcd_3, line1, line2);
    }
  }
}