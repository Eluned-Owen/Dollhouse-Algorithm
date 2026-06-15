from Card_Processing_Function import *
from flask import Flask, request
from threading import Thread
from queue import Queue
import pandas
import random
import serial
import time

# Queue stores NFC card values received over Wi-Fi
nfc_queue = Queue()

app = Flask(__name__)

@app.route("/scan", methods=["GET"])
def receive_scan():
    r1 = request.args.get("r1", "NO_CARD")
    r2 = request.args.get("r2", "NO_CARD")

    print(f"Received scan: R1={r1}, R2={r2}")

    nfc_queue.put({
        "cards": [r1, r2]
    })

    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running", 200

def start_wifi_server():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)


# Start Flask server in background
Thread(target=start_wifi_server, daemon=True).start()

# LCD Arduino still uses USB serial
LCD_PORT = "COM7"
lcd = serial.Serial(port=LCD_PORT, baudrate=9600, timeout=1)

time.sleep(2)
lcd.reset_input_buffer()

print(f"Connected to LCD Arduino on {lcd.name}")
print("Wi-Fi NFC server running on port 5000")

Game_Start = input(str("Would you like to start the Dollhouse Algorithm? (y/n) "))

if Game_Start == "y":
    player_count = int(input(str("Good, how many players are playing? (1-4) ")))

    if player_count < 1 or player_count > 4:
        print("This number isn't from 1-4")
        exit()

    print(player_count, "player/s are playing, starting the game...")

    class player_creator:
        def __init__(self, name, score, number):
            self.name = name
            self.score = score
            self.number = number

    def send_to_lcd(screen_number, line1, line2=""):
        message = f"LCD{screen_number}|{line1}|{line2}\n"
        lcd.write(message.encode("utf-8"))

    def clear_nfc_queue():
        while not nfc_queue.empty():
            nfc_queue.get()

    players = []

    # Player numbers start from 1, so LCD1/LCD2/LCD3 etc. match properly
    for i in range(1, player_count + 1):
        players.append(player_creator(f"player_{i}", 50, i))

    model_list = [
        "Risk Model",
        "Unpredictability Model",
        "Concealment Model",
        "Obsession Model"
    ]

    picked = random.randrange(0, len(model_list))
    model_picked = [model_list[picked]]

    cards = pandas.read_csv("behavioural_surplus.csv")

    clear_nfc_queue()
    print("===== Game Start =====")

    turn = 1
    finished_players = 0
    finished_player_name = ""
    jailed_count = []

    while turn < 9:
        print(f"== turn {turn} ==")

        j = 0

        while j < player_count:
            current_player = players[j]

            print(f"Waiting for {current_player.name} to scan...")

            # Wait for Arduino Uno R4 WiFi to send a scanned card
            scan_data = nfc_queue.get()

            nfc_values = scan_data["cards"]

            print(f"{current_player.name} scanned cards: {nfc_values}")

            finished_players, finished_player_name, jailed_count, player_score, player_name, player_number = card_analyser(
                current_player,
                nfc_values,
                model_picked,
                cards
            )
            
            send_to_lcd(
                player_number,
                f"{player_name} score:",
                str(player_score)
            )

            j += 1

        turn += 1
        print("== end turn", turn, "==")

        if player_count == 1 and len(jailed_count) >= player_count:
            print("You have been jailed by the algorithm, try again next time :)")
            break

        if player_count > 1 and len(jailed_count) >= player_count:
            print("All players have been jailed by the algorithm, try again next time :)")
            break

        if finished_players == 1:
            print("========", finished_player_name, "has reached 0 points, game over! ========")
            break

        if turn >= 9:
            send_to_lcd(1, "Game end", " ")
            send_to_lcd(2, "Game end", " ")
            send_to_lcd(3, "Game end", " ")
            print("== game end ==")