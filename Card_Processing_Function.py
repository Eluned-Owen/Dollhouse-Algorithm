import time


def card_analyser(player, ser, model_picked, cards):
    global jailed_count
    global jailed_player
    global finished_players
    global finished_player_name

    global player_score
    global player_name
    global player_number

    finished_players = 0
    finished_player_name = 0

    jailed_count = []
    jailed_player = []

    #if someone gets a score over 100, jail them by adding the player name to a list to know when to skip a turn and a counter to know if people are still playing
    if player.score >= 100:
        jailed_player.append(player.name)
        if player.name in jailed_player:
            print("=== You have been jailed ===")
        jailed_count.append("")

    collected_cards = []

    #Wait briefly so both NFC readers can finish sending
    time.sleep(0.3)

    #Collect all incoming serial data
    while ser.in_waiting > 0:
        available = ser.readline()
        print(f"Available data: {available}")
        decode_card = available.decode("UTF-8").strip()

        #Split incoming IDs
        clean_card = decode_card.split()

        #Convert to integers
        final_card = [int(i) for i in clean_card]
        collected_cards.extend(final_card)
        #Tiny delay to allow next reader to finish
        time.sleep(0.05)

    print("Collected cards:", collected_cards)

    score_tally = []

    #Process all cards together
    for i in collected_cards:
        card_finder = cards.iloc[i]
        score = card_finder[model_picked].item()

        #Card re-use logic
        cards.loc[i, player.name] += 1
        if cards.loc[i, player.name] == 3:
            print("You can use", card_finder['Card'], "only once more")
        if cards.loc[i, player.name] >= 4:
            print("You've used", card_finder['Card'], "too much")
            break
        else:
            score_tally.append(score)

    print(score_tally)

    #Sum up the score for the turn and add it to the player's total score
    turn_score = 0
    for item in score_tally:
        turn_score += item

    print("score = ", turn_score)
    player.score = player.score + turn_score
    print("new score for", player.name, ": ", player.score)
    player_score = player.score
    player_name = player.name

    #Assign player number for LCD display
    if player_name.endswith("1"):
        player_number = 1
    elif player_name.endswith("2"):
        player_number = 2
    elif player_name.endswith("3"):
        player_number = 3

    #Check if the player has reached 0 points and if so keep track of that for end game logic
    if player.score <= 0:
        finished_players = finished_players + 1
        finished_player_name = player.name

    #Clear leftover serial noise
    ser.reset_input_buffer()

    return finished_players, finished_player_name, jailed_count, player_score, player_name, player_number
    
