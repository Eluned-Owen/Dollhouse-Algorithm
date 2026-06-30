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
lcd = serial.Serial(port="COM7", baudrate=9600, timeout=1)
printer = serial.Serial(port="COM4", baudrate=19200, timeout=1)

time.sleep(2)
lcd.reset_input_buffer()
printer.reset_input_buffer()

print(f"Connected to LCD Arduino on {lcd.name}")
print(f"Connected to Printer Arduino on {printer.name}")
print("Wi-Fi NFC server running on port 5000")

Game_Start = input(str("Would you like to start the Dollhouse Algorithm? (y/n) "))

if Game_Start == "y":
    player_count = int(input(str("Good, how many players are playing? (1-4) ")))

    if Game_Start !=  "y":
        print("Game turning off")
        exit()

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

        print("Sending LCD:", message)

        lcd.write(message.encode("utf-8"))

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

    #picking the algorithm for the round
    picked = random.randrange(0, len(model_list))
    model_picked = [model_list[picked]]

    print(model_picked)
    
    #importing the card data from the csv file
    cards = pandas.read_csv("behavioural_surplus.csv")

    print("===== Game Start =====")

    turn = 1

    finished_players = 0
    finished_player_name = ""

    jailed_players = set()

    #starting the game loop for 10 turns
    while turn <= 10:

        print(f"\n===== TURN {turn} =====")

        j = 0

        #looping through each player for the turn
        while j < player_count:

            current_player = players[j]

            # Skip jailed players
            if current_player.name in jailed_players:

                print(current_player.name, "is jailed")

                send_to_lcd(
                    str(current_player.number),
                    "JAILED",
                    "TURN SKIPPED"
                )

                j += 1
                continue

            print(f"Waiting for {current_player.name} to scan...")

            scan_data = nfc_queue.get()

            print("Queue returned:", scan_data)

            nfc_values = scan_data["cards"]
            #print("About to call analyser")

            # No cards on either reader
            if nfc_values[0] == "NO_CARD" and nfc_values[1] == "NO_CARD":

                print("No cards scanned. Waiting again...")

                continue
            try:
                (
                    finished_players,
                    finished_player_name,
                    player_jailed,
                    player_score,
                    player_name,
                    player_number,
                    printer,
                    turn
                ) = card_analyser(
                    current_player,
                    nfc_values,
                    model_picked,
                    cards,
                    printer,
                    turn
                )

            except Exception as e:
                import traceback
                print("CARD ANALYSER ERROR:")
                traceback.print_exc()

            send_to_lcd(
                str(player_number),
                f"{player_name} score:",
                str(player_score)
            )

            print(
                f"LCD DEBUG: {player_number} "
                f"{player_name} "
                f"{player_score}"
            )

            if player_jailed:

                jailed_players.add(current_player.name)

                send_to_lcd(
                    str(player_number),
                    "YOU ARE",
                    "JAILED"
                )
            print(f"===== END TURN {turn} =====")
            j += 1
        turn += 1

    # Entire round finished
    active_players = player_count - len(jailed_players)

    if active_players <= 0:

        print("All players jailed")

        send_to_lcd("1", "EVERYONE", "JAILED")
        send_to_lcd("2", "EVERYONE", "JAILED")
        exit()

    if finished_players > 0:
        print(
            f"{finished_player_name} "
            "has reached 0 points"
        )

        send_to_lcd(
            "1",
            f"{finished_player_name}",
            "WINS"
        )

        send_to_lcd(
            "2",
            f"{finished_player_name}",
            "WINS"
        )
        exit()

        turn += 1

    print("===== GAME OVER =====")

    send_to_lcd("1", "GAME", "OVER")
    send_to_lcd("2", "GAME", "OVER")