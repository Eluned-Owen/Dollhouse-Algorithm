#include <Wire.h>
#include <Adafruit_LiquidCrystal.h>

//Initialising the LCDs 
Adafruit_LiquidCrystal lcd_1(0);
Adafruit_LiquidCrystal lcd_2(1);
Adafruit_LiquidCrystal lcd_3(2);

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  lcd_1.begin(16, 2);
  lcd_2.begin(16, 2);
  lcd_3.begin(16, 2);

  //Starting the LCD backlight
  lcd_1.setBacklight(HIGH);
  lcd_2.setBacklight(HIGH);
  lcd_3.setBacklight(HIGH);

  lcd_1.print("LCD 1 ready");
  lcd_2.print("LCD 2 ready");
  lcd_3.print("LCD 3 ready");
}

void printToLCD(Adafruit_LiquidCrystal &lcd, String line1, String line2) {
  lcd.clear();

  //Start from the top left, print Line1
  lcd.setCursor(0, 0);
  lcd.print(line1.substring(0, 16));

  //Start from bottom left, print Line2
  lcd.setCursor(0, 1);
  lcd.print(line2.substring(0, 16));
}

void loop() {
  if (Serial.available() > 0) {
    //Read the string untill it sees a new line (\n)
    String msg = Serial.readStringUntil('\n');
    //Remove unwanted spaces, carriage returns, or newline characters from the start and end of the message.
    msg.trim();

    //Find the first separator character, separating line 1 from line 2.
    int firstSep = msg.indexOf('|');
    int secondSep = msg.indexOf('|', firstSep + 1);

    //If either separator is missing, the message is not in the expected format,
    //ignore it and wait for the next message
    if (firstSep == -1 || secondSep == -1) {
      return;
    }

    //SSExtract the LCD target
    String target = msg.substring(0, firstSep);
    //Extract the first row of text for the LCD
    String line1 = msg.substring(firstSep + 1, secondSep);
    //Extract the second row of text for the LCD
    String line2 = msg.substring(secondSep + 1);

    //Send the extracted text to the correct LCD screen
    if (target == "LCD1") {
      printToLCD(lcd_1, line1, line2);
    } else if (target == "LCD2") {
      printToLCD(lcd_2, line1, line2);
    } else if (target == "LCD3") {
      printToLCD(lcd_3, line1, line2);
    }
  }
}