import subprocess
import time
import random
import serial
import pandas
from Card_Processing_Function import card_analyser
#Importing a module for reading serial communications

#Connecting to COM4 where the Arduino's USB is connected at with a baud rate of 9600 (same as the "NFC-Input" program)
#If it doesnt work, switch COM4 to COM3 and then back to COM4
ser = serial.Serial(port = "COM4", baudrate = 9600, timeout=1)
print(f"Connected to {ser.name}")

Game_Start = input(str("Would you like to start the Dollhouse Algorithm? (y/n)"))

if Game_Start == "y" :
    playing = input(str("Good, how many players are playing? (1-4) "))
    playing = int(playing)
    playing +=1

    class player_creator:
        def __init__(self, name, score):
            self.name = name
            self.score = score

    #Next, I need to find a way to change the values of the player scores
    i = 0
    #for i in range(i, Players):
    #    risk_scores["player_{0}_score".format(i)] = 60
    
    players = []

    #creating player objects and appending them to a list, the number of players is determined by the user input at the start of the game
    for i in range(i, playing):
      players.append(player_creator("player_{count}".format(count = i), 60))

    if playing < 5 and playing > 0:
        print(playing, "player/s are playing, starting the game...")
    if playing > 5 or playing == 0:
        print("This number isn't from 1-4 ")

    #Picking the bias model for the game
    model_list = ["Risk Model", "Unpredictability Model", "Concealment Model", "Obsession Model"]
    picked = random.randrange(0, 3)

    model_picked = []
    model_picked.append(model_list[picked])

    #Loading in the cards
    cards = pandas.read_csv("behavioural_surplus.csv")

    turn = 1
    #Begin the main game loop, runs for 8 turns, each player gets to scan their card once per turn
    while turn < 9:
        j = 1
        while j < playing:
            #if there is data in the serial buffer, run the card analyser function for the current player, then reset the buffer and move on to the next player
            if ser.in_waiting > 0:
                card_analyser(players[j], ser, model_picked, cards)
                ser.reset_input_buffer()
                j = j + 1
            
        print("===== Turn", turn, "end =====")
        turn = turn + 1
        if turn >= 9:
            print("==== Game Over ====")
            break
