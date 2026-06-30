<h1>Dollhouse Algorithm</h1>
<img src= "https://23008862.myblog.arts.ac.uk/files/2026/05/dollhouseLazyOne.png"  alt="A table top game with a miniature dollhoue and cards">

Dollhouse Algorithm is an arduino powered table top game where a biased algorithm thinks the player is the killer, the players must reduce the algorithms suspicion by
identifying what traits the algorithm is biased towards and then building a digital trail that the algorithm deems unsuspicious. Gameplay loop includes NFC stickered 
"Behavioural Surplus" cards that have written statements such as "Clears browsing history often" and "Checks bank balance daily" on them. The player will then place these 
cards on the "Card Analyser" which contains two NFC readers and a button, where the cards will be communicated to the laptop via serial, the cards will be processed and the
resulting score of the combination would output onto the players LCD screen. The aim of the game is to get to 0%, and if this is played multiplayer, who gets to 0% first.

Video: https://www.youtube.com/watch?v=5wlFyxIc4vU
Blog: https://23008862.myblog.arts.ac.uk/the-dollhouse-algorithm/

<h3> Getting Started </h3>
The project needs the following physical components:
<ul>
<li>2 x LCD</li>
<li>1 x Button</li>
<li>1 x Arduino Leonardo </li>
<li>1 x Arduino Uno R4 WiFi</li>
<li>2 x 8-channel level shifter</li>
<li>1 x Medium Bread board</li>
<li>3 x Mini Bread Board</li>
<li>2 x NFC readers</li>
<li>1 x Laptop for Serial communications </li>
<li>WiFi or a hotspot</li>
</ul>

The project depends on the following digital libraries:
Python:
<ul>
<li>PySerial</li>
<li>Random</li>
<li>Pandas</li>
<li>Time </li>
</ul>

Arduino IDE (C++):
<ul>
<li>Wire</li>
<li>Adafruit_LiquidCrystal</li>
<li>SPI</li>
<li>MFRC522</li>
</ul>

<h3>How To Play</h3>
<ol type=1>
<li>When prompted to play in the terminal, type "y" and enter</li>
<li>Type how many people are playing</li>
<li>Pick a combination of cards, note what traits are being shown through the cards, for example, "Clears browser histroy often" reveals concealment like traits</li>
<li>Place each card on the card analyser and press the button</li>
<li>Your new score will now display on the LCD and the next player plays/goes to the next round</li>
<li>The first to 0% risk winds, if you reach 100% you get jailed and if nobody win in 9 rounds, the game is over</li>
</ol>

Tip: Your first goal should be to find out which traits the algorithm is biased towards, and then cater your card combinations to be unlike the bias as much as you can!

<img src= "https://i.ibb.co/k6zJ0t3N/festival.jpg"  alt="A table top game with a miniature dollhoue and cards">
