/*Based on the MRFC exmaple code "Ntag216_AUTH". This program reads the NFC ultralight tag (White NFC stickers) and
 converts the pages of bytes to ASCII*/

#include <SPI.h>
#include <MFRC522.h>

//Defining the RST and SS pin 
#define RST_PIN 9
#define SS_PIN 10

//Creating a MFRC instance and letting the program know that
//the RST and SS pins are ICSP pins
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  //Initialise serial communications with the PC
  Serial.begin(9600);
  //Do nothing if no serial port is opened
  while (!Serial);
  //Init SPI bus for ICSP communications
  SPI.begin();
  //Starting the MFRC522 instance
  mfrc522.PCD_Init();

}

void loop() {
  // Wait for card
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;

  //18 because theres 4 pages with 4 bytes each 4*4=16 + a couple of extra space for internal data
  byte buffer[18];
  byte len = sizeof(buffer);

  String text = "";

  // Start at page 4 
  byte page = 4;

  // Read multiple pages 
  for (int i = 0; i < 12; i++) {
    //Get all the status codes in the MFRC instance and save them in status
    MFRC522::StatusCode status = mfrc522.MIFARE_Read(page, buffer, &len);

    //If the status code is not OK, let the user know the reading failed and why
    if (status != MFRC522::STATUS_OK) {
      Serial.print("Read failed: ");
      Serial.println(mfrc522.GetStatusCodeName(status));
      return;
    }

    //Each read = 16 bytes
    for (int j = 0; j < 16; j++) {
      byte b = buffer[j];

      //Keep only readable ASCII characters
      if (b >= 32 && b <= 126) {
        text += (char)b;
      }
    }
    //Move to next block of pages
    page += 4; 
  }

  //Clean up common NFC/NDEF junk 
  text.trim();
  if (text.startsWith("Ten")) {
  text = text.substring(3);
  }

  Serial.println(text);

  delay(3000);

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}