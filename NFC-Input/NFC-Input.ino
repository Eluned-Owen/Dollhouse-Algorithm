/*OriginallyBased on the MRFC exmaple code "Ntag216_AUTH". This program reads the NFC ultralight tag
(White NFC stickers) and converts the pages of bytes to ASCII. Furthermore there's a button to notify the arduino 
when to start reading the NFC reader inputs, once it gets pressed the arduino reads each reader one at a time to
help control the data payload.*/

#include <SPI.h>
#include <MFRC522.h>

#define BUTTONPIN 3
int buttonValue = 0;
int prevButton = 0;

#define RST_PIN 9

//defining each nfc reader
#define SS_1 5
#define SS_2 6

MFRC522 mfrc522_1(SS_1, RST_PIN);
MFRC522 mfrc522_2(SS_2, RST_PIN);



void setup() {
  //Initialise serial communications with the PC
  Serial.begin(9600);

  // sets the button pin to an input
  pinMode(BUTTONPIN, INPUT);
  digitalWrite(BUTTONPIN, HIGH);

  pinMode(SS_1, OUTPUT);
  pinMode(SS_2, OUTPUT);

  digitalWrite(SS_1, HIGH);
  digitalWrite(SS_2, HIGH);
  //Init SPI bus for ICSP communications
  SPI.begin();
  //Starting the MFRC522 instance
  mfrc522_1.PCD_Init();
  mfrc522_2.PCD_Init();
}

void loop() {
  buttonValue = digitalRead(BUTTONPIN);

  if (buttonValue == 0) {
    //Serial.println("Analysing cards...");

    // Reader 1
    digitalWrite(SS_2, HIGH);
    digitalWrite(SS_1, LOW);

    if (mfrc522_1.PICC_IsNewCardPresent() &&
        mfrc522_1.PICC_ReadCardSerial()) {

        //Serial.println("Reader 1 detected");
        readCard(mfrc522_1);
    }

    //delay(1000);
    
    // Reader 2
    digitalWrite(SS_1, HIGH);
    digitalWrite(SS_2, LOW);

    if (mfrc522_2.PICC_IsNewCardPresent() &&
        mfrc522_2.PICC_ReadCardSerial()) {

        //Serial.println("Reader 2 detected");
        readCard(mfrc522_2);
    }

    //delay(500);
  }  
}

void readCard(MFRC522 &reader) {
  //18 because theres 4 pages with 4 bytes each 4*4=16 + a couple of extra space for internal data
  byte buffer[18];
  byte len = sizeof(buffer);

  String text = "";

  // Start at page 4 
  byte page = 4;

  // Read multiple pages 
  for (int i = 0; i < 4; i++) {
    //Get all the status codes in the MFRC instance and save them in status
    MFRC522::StatusCode status = reader.MIFARE_Read(page, buffer, &len);


    //If the status code is not OK, let the user know the reading failed and why
    /* if (status != MFRC522::STATUS_OK) {
      Serial.print("Read failed: ");
      Serial.println(reader.GetStatusCodeName(status));
      return;
    } */

    //Each read = 16 bytes
    for (int j = 0; j < 16; j++) {
      byte b = buffer[j];
      
      //If b hits the end of the data, break the loop
      if (b == 0x00) {
            break;
        }

      //Keep only readable ASCII characters
      if (b >= 32 && b <= 126) {
        text += (char)b;
      }
    }
    //Move to next block of pages
    page += 4; 
  

  //Clean up common NFC/NDEF junk 
  //If text doesnt start with an "int", substring em by 10?
  if (text.startsWith("Ten")) {
    text = text.substring(3);
  }
  if (text.length() > 2) {
    text = text.substring(10);
  }
  text.trim();
  Serial.println(text);

  //delay(3000);


  reader.PICC_HaltA();
  reader.PCD_StopCrypto1();
}
}