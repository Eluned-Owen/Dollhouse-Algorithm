import subprocess
import serial
import pandas

#Importing a module for reading serial communications

#Connecting to COM4 where the Arduino's USB is connected at with a baud rate of 9600 (same as the "NFC-Input" program)
#If it doesnt work, switch COM4 to COM3 and then back to COM4
ser = serial.Serial(port = "COM4", baudrate = 9600, timeout=1)
print(f"Connected to {ser.name}")

Game_Start = input(str("Would you like to start the Dollhouse Algorithm? (y/n)"))

if Game_Start == "y" :
    Players = input(str("Good, how many players are playing? (1-4) "))
    Players = int(Players)
    Players +=1

    risk_scores = {}

    #Next, I need to find a way to change the values of the player scores 
    Player_1_score = []
    i = 1
    for i in range(i, Players):
        risk_scores["player_{0}_score".format(i)] = 60
        print(risk_scores)
        
    print(risk_scores)

    if Players < 5 and Players > 0:
        print(Players, "player/s are playing, starting the game...")
    if Players > 5 or Players == 0:
        print("This number isn't from 1-4 ")

    import random
    model_list = ["Risk Model", "Unpredictability Model", "Concealment Model", "Obsession Model"]
    picked = random.randrange(0, 3)

    model_picked = []
    model_picked.append(model_list[picked])
    model_picked

    cards = pandas.read_csv("behavioural_surplus.csv")

    def cardAnalyser(turn_score):
            if ser.in_waiting > 0:
                available = ser.read(ser.in_waiting)
                print(f"Available data: {available}")
                card = available

            #As the card variable is a byte, convert card to a string using utf-8 \r\n\r\n\r\n\r\n
                #print(type(card))
                decode_card = card.decode("UTF-8")
                clean_card = decode_card.split()
                final_card = [int(i) for i in clean_card]
                print(final_card)

                score_tally = []

                for i in final_card:
                    card_finder = cards.iloc[i]
                    score = card_finder[model_picked].item()
                    score_tally.append(score)
                print(score_tally)

                turn_score = 0

                for item in score_tally:
                    turn_score += item

                print("score = ", turn_score)

    turn = 0
    x = 0
    while x < 9:
        j = 1
        #find the player in the dictionary from j, do the cardAnalyser function and then add the turn_score to the player_{j}_score
        while j in range(j, Players):
            print(risk_scores.get({1}))
            j+ 1
            

        turn + 1
