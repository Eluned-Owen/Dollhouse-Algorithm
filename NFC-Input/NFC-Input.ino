/*OriginallyBased on the MRFC exmaple code "Ntag216_AUTH". This program reads the NFC ultralight tag
(White NFC stickers) and converts the pages of bytes to ASCII. Furthermore there's a button to notify the arduino 
when to start reading the NFC reader inputs, once it gets pressed the arduino reads each reader one at a time to
help control the data payload.*/
#include <SPI.h>
#include <MFRC522.h>
#include <WiFiS3.h>

// ---------- Wi-Fi details ----------
char ssid[] = ssid_wifi;
char pass[] = pass_wifi;

char server[] = ip;

int serverPort = 5000;
WiFiClient client;

// ---------- Button + NFC setup ----------
#define BUTTONPIN 3

#define LEDPIN LED_BUILTIN

#define RST_PIN 9

#define SS_1 5
#define SS_2 6

int buttonValue = HIGH;
int prevButton = HIGH;

MFRC522 mfrc522_1(SS_1, RST_PIN);
MFRC522 mfrc522_2(SS_2, RST_PIN);

// ---------- Wi-Fi connection ----------
void connectWiFi() {
  Serial.println(ssid);

  int status = WL_IDLE_STATUS;

  while (status != WL_CONNECTED) {
    status = WiFi.begin(ssid, pass);
    delay(3000);
    Serial.print(".");
  }

  Serial.println(WiFi.localIP());
}

// ---------- URL encode card text ----------
String urlEncode(String input) {
  String encoded = "";

  for (int i = 0; i < input.length(); i++) {
    char c = input.charAt(i);

    if (
      (c >= 'a' && c <= 'z') ||
      (c >= 'A' && c <= 'Z') ||
      (c >= '0' && c <= '9')
    ) {
      encoded += c;
    } else if (c == ' ') {
      encoded += "%20";
    } else {
      encoded += "%";
      if (c < 16) encoded += "0";
      encoded += String(c, HEX);
    }
  }

  return encoded;
}

// ---------- Send NFC result to Python ----------
void sendScanToPython(String card1, String card2) {
  String path = "/scan?r1=" + urlEncode(card1) + "&r2=" + urlEncode(card2);

  Serial.print("Sending scan to Python: ");

  if (client.connect(server, serverPort)) {
    client.print("GET ");
    client.print(path);
    client.println(" HTTP/1.1");

    client.print("Host: ");
    client.println(server);

    client.println("Connection: close");
    client.println();

    delay(50);
    client.stop();

    Serial.println("Scan sent OK");
  } else {
    Serial.println("Connection to Python failed");
  }
}

void setup() {
  Serial.begin(9600);
  delay(1000);

  pinMode(BUTTONPIN, INPUT_PULLUP);

  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, LOW);

  pinMode(SS_1, OUTPUT);
  pinMode(SS_2, OUTPUT);

  digitalWrite(SS_1, HIGH);
  digitalWrite(SS_2, HIGH);

  SPI.begin();

  mfrc522_1.PCD_Init();
  mfrc522_2.PCD_Init();

  // Connect to Wi-Fi before trying to contact Python
  connectWiFi();

  if (client.connect(server, serverPort)) {
    Serial.println("Connected to Python!");

    client.println("GET / HTTP/1.1");
    client.print("Host: ");
    client.println(server);
    client.println("Connection: close");
    client.println();

    delay(50);
    client.stop();
  } else {
    Serial.println("Connection to Python failed");
  }

  Serial.println("READY");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
  Serial.println("Wi-Fi disconnected. Reconnecting...");
  connectWiFi();
    }
  buttonValue = digitalRead(BUTTONPIN);

  // Button uses INPUT_PULLUP:
  // not pressed = HIGH
  // pressed = LOW
  if (prevButton == HIGH && buttonValue == LOW) {
  Serial.println("Button pressed. Reading NFC readers...");
  digitalWrite(LEDPIN, HIGH);

  String card1 = "NO_CARD";
  String card2 = "NO_CARD";

  // Reader 1
  digitalWrite(SS_2, HIGH);
  digitalWrite(SS_1, LOW);
  delay(20);

  if (mfrc522_1.PICC_IsNewCardPresent() &&
      mfrc522_1.PICC_ReadCardSerial()) {
    card1 = readCard(mfrc522_1);
  }

  digitalWrite(SS_1, HIGH);
  delay(50);

  // Reader 2
  digitalWrite(SS_1, HIGH);
  digitalWrite(SS_2, LOW);
  delay(20);

  if (mfrc522_2.PICC_IsNewCardPresent() &&
      mfrc522_2.PICC_ReadCardSerial()) {
    card2 = readCard(mfrc522_2);
  }

  digitalWrite(SS_2, HIGH);

  Serial.print("Reader 1: ");
  Serial.println(card1);

  Serial.print("Reader 2: ");
  Serial.println(card2);

  // Send both cards to Python in one HTTP request
  sendScanToPython(card1, card2);

  digitalWrite(SS_1, HIGH);
  digitalWrite(SS_2, HIGH);

  digitalWrite(LEDPIN, LOW);

  delay(300);
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
      reader.PICC_HaltA();
      reader.PCD_StopCrypto1();
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

  // Clean up common NFC/NDEF junk
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
  return text;
}
