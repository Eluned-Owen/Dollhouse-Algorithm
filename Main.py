import subprocess

Game_Start = input(str("Would you like to start the Dollhouse Algorithm? (y/n)"))

if Game_Start == "y" :
    Players = input(str("Good, how many players are playing? (1-4) "))
    Players = int(Players)

    if Players < 4 and Players > 0:
        print(Players, "player/s are playing, starting the game...")
    if Players > 4 or Players == 0:
        print("This number isn't from 1-4 ")

    #i = 0
    #while i <= 1:
    #    subprocess.call(["python", "CardProcessing.ipynb"])
