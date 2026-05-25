from Card_Processing_Function import *
import pandas
import random
import serial

#Connecting to COM4 where the Arduino's USB is connected at with a baud rate of 9600 
ser = serial.Serial(port = "COM4", baudrate = 9600, timeout=1)
lcd = serial.Serial(port = "COM7", baudrate = 9600, timeout=1)
print(f"Connected to {ser.name}")

Game_Start = input(str("Would you like to start the Dollhouse Algorithm? (y/n)"))

if Game_Start == "y" :
    playing = input(str("Good, how many players are playing? (1-4) "))
    playing = int(playing)
    playing = playing + 1

    #Player creation instructions
    class player_creator:
        def __init__(self, name, score):
            self.name = name
            self.score = score

    #Function that packages the screen number + message and sends it to the arduino controlling the LCDs
    def send_to_lcd(screen_number, line1, line2=""):
            message = f"LCD{screen_number}|{line1}|{line2}\n"
            lcd.write(message.encode("utf-8"))
        

    #Next, I need to find a way to change the values of the player scores
    i = 0
    players = []
    #creating player objects and appending them to a list, the number of players is determined by the user input at the start of the game
    for i in range(i, playing):
      players.append(player_creator("player_{count}".format(count = i), 50))

    if playing < 4 and playing > 0:
        print(playing, "player/s are playing, starting the game...")
    if playing > 4 or playing == 0:
        print("This number isn't from 1-4 ")

    #Picking the bias model for the game
    model_list = ["Risk Model", "Unpredictability Model", "Concealment Model", "Obsession Model"]
    picked = random.randrange(0, 3)

    model_picked = []
    model_picked.append(model_list[picked])

    #Loading in the cards into a Panda Dataframe
    cards = pandas.read_csv("behavioural_surplus.csv")

    print("===== Game Start =====")

    turn = 1
    #Begin the main game loop, runs for 8 turns, each player gets to scan their card once per turn
    while turn < 9:
        j = 1
        while j < playing:
            #if there is data in the serial buffer, run the card analyser function for the current player, then reset the buffer and move on to the next player
            if ser.in_waiting > 0:
                #"finished_players, finished_player_name" calls the function but also keeps track of when a player has reached 0 points, who reaches 0 points and if anyone has gone to jail
                finished_players, finished_player_name, jailed_count, player_score, player_name, player_number = card_analyser(players[j], ser, model_picked, cards)
                ser.reset_input_buffer()

                #Sending the player data to the send_to_lcd function where it will then end it to the LCDs
                send_to_lcd(player_number,  f"{player_name} score:", str(player_score))
                j = j + 1

        turn = turn + 1

        print("== end turn", turn, "==")

        #Jail logic
        if len(players) == 1 and len(jailed_count) >= playing:
            print("You have been jailed by the algorithm, try again next time :)")
            
        #Game over logic
        if len(players) > 1 and len(jailed_count) >= playing:
            print("All players have been jailed by the algorithm, try again next time :)")
            break
        if finished_players == 1:
            print("========", finished_player_name, "has reached 0 points, game over! ========")
            break
        if turn >= 9:
            send_to_lcd(1, f"Game end", " ")
            send_to_lcd(2, f"Game end", " ")
            send_to_lcd(3, f"Game end", " ")
            print("== game end ==")

