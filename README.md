<h1>Dollhouse Algorithm</h1>

Dollhouse Algorithm is an arduino powered table top game where a biased algorithm thinks the player is the killer, the players must reduce the algorithms suspicion by
identifying what traits the algorithm is biased towards and then building a digital trail that the algorithm deems unsuspicious. Gameplay loop includes NFC stickered 
"Behavioural Surplus" cards that have written statements such as "Clears browsing history often" and "Checks bank balance daily" on them. The player will then place these 
cards on the "Card Analyser" which contains two NFC readers and a button, where the cards will be communicated to the laptop via serial, the cards will be processed and the
resulting score of the combination would output onto the players LCD screen. The aim of the game is to get to 0%, and if this is played multiplayer, who gets to 0% first.

<h3> Getting Started </h3>
<p>The project needs the following physical components:
3 x LCD
1 x Button
1 x Arduino Leonardo 
1 x Arduino Uno R4 WiFi
1 x 8-channel level shifter
1 x Medium Bread board
1 x Mini Bread Board
2 x NFC readers
1 x Laptop for Serial communications 

The project depends on the following digital libraries:
Python:
PySerial
Random
Pandas
Time

Arduino IDE (C++):
Wire
Adafruit_LiquidCrystal
SPI
MFRC522</p>
