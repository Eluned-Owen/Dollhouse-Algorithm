/*OriginallyBased on the MRFC exmaple code "Ntag216_AUTH". This program reads the NFC ultralight tag
(White NFC stickers) and converts the pages of bytes to ASCII. Furthermore there's a button to notify the arduino 
when to start reading the NFC reader inputs, once it gets pressed the arduino reads each reader one at a time to
help control the data payload.*/

#include <SPI.h>
#include <MFRC522.h>


#define BUTTONPIN 3
#define LEDPIN 9
int buttonValue = 0;
int prevButton = 0;

#define RST_PIN 9

//defining each nfc reader
#define SS_1 5
#define SS_2 6

MFRC522 mfrc522_1(SS_1, RST_PIN);
MFRC522 mfrc522_2(SS_2, RST_PIN);

#define Serial1 _UART2_


void setup() {
  //Initialise serial communications with the PC for debugging
  //Serial.begin(9600);

  //Initialise bluetooth serial communications
  Serial1.begin(9600);

  // sets the button pin to an input
  pinMode(BUTTONPIN, INPUT_PULLUP);

  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, HIGH);

  pinMode(SS_1, OUTPUT);
  pinMode(SS_2, OUTPUT);

  digitalWrite(SS_1, HIGH);
  digitalWrite(SS_2, HIGH);
  //Init SPI bus for ICSP communications
  SPI.begin();
  //Starting the MFRC522 instance
  mfrc522_1.PCD_Init();
  mfrc522_2.PCD_Init();

  Serial1.println("READY");
}

void loop() {
  buttonValue = digitalRead(BUTTONPIN);

  if (prevButton == HIGH && buttonValue == LOW) {
    // Button was just pressed

    // Reader 1
    digitalWrite(SS_2, HIGH);
    digitalWrite(SS_1, LOW);

    if (mfrc522_1.PICC_IsNewCardPresent() &&
        mfrc522_1.PICC_ReadCardSerial()) {

      String cardText = readCard(mfrc522_1);
      Serial1.println(cardText);
      //Serial.println(cardText);
    }

    delay(100);

    // Reader 2
    digitalWrite(SS_1, HIGH);
    digitalWrite(SS_2, LOW);

    if (mfrc522_2.PICC_IsNewCardPresent() &&
        mfrc522_2.PICC_ReadCardSerial()) {

      String cardText = readCard(mfrc522_2);
      Serial.println(cardText);
      //Serial.println(cardText);
    }

    digitalWrite(SS_1, HIGH);
    digitalWrite(SS_2, HIGH);

    delay(300); // debounce
  }

  prevButton = buttonValue;
}

String readCard(MFRC522 &reader) {
  byte buffer[18];
  String text = "";

  byte page = 4;

  for (int i = 0; i < 4; i++) {
    byte len = sizeof(buffer);

    MFRC522::StatusCode status = reader.MIFARE_Read(page, buffer, &len);

    if (status != MFRC522::STATUS_OK) {
      return "READ_FAILED";
    }

    for (int j = 0; j < 16; j++) {
      byte b = buffer[j];

      if (b == 0x00) {
        break;
      }

      if (b >= 32 && b <= 126) {
        text += (char)b;
      }
    }

    page += 4;
  }

  // Clean up common NFC/NDEF junk AFTER all pages have been read
  if (text.startsWith("Ten")) {
    text = text.substring(3);
  }

  if (text.length() > 10) {
    text = text.substring(10);
  }

  text.trim();

  reader.PICC_HaltA();
  reader.PCD_StopCrypto1();

  return text;
}