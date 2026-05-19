import time


def card_analyser(player, ser, lcd, model_picked, cards, send_to_lcd, playing):
    #turn_text = "Your turn"
    #turn_text_encoded = turn_text("utf-8")
    #lcd.write(turn_text_encoded)


    global jailed_count
    global jailed_player
    jailed_count = []
    jailed_player = []

    #if someone gets a score over 100, jail them by adding the player name to a list to know when to skip a turn and a counter to know if people are still playing
    #if player.score >= 100:
    #    jailed_player.append(player.name)
    #    if player.name in jailed_player:
    #        print("=== You have been jailed ===")
    #    jailed_count.append("")

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

        cards.loc[i, player.name] += 1
        if cards.loc[i, player.name] == 3:
            print("You can use", card_finder['Card'], "only once more")
        if cards.loc[i, player.name] >= 4:
            print("You've used", card_finder['Card'], "too much")
            break
        else:
            score_tally.append(score)

    print(score_tally)

    turn_score = 0
    for item in score_tally:
        turn_score += item

    global finished_players
    global finished_player_name

    global player_score
    global player_name
    global player_number

    global player_one_score
    global player_two_score 
    global player_three_score

    finished_players = 0
    finished_player_name = 0

    print("score = ", turn_score)
    player.score = player.score + turn_score
    print("new score for", player.name, ": ", player.score)
    player_score = player.score
    player_name = player.name
    new_score = "{name} score:\n {score}".format(name = player.name, score = player.score)

    if player_name.endswith("1"):
        player_number = 1
    elif player_name.endswith("2"):
        player_number = 2
    elif player_name.endswith("3"):
        player_number = 3

    if player.score <= 0:
        finished_players = finished_players + 1
        finished_player_name = player.name

    #Sending the new scores bytes to the LCD to display
    #score_new_encoded = new_score.encode("utf-8")
    #lcd.write(score_new_encoded)


    #Clear leftover serial noise
    ser.reset_input_buffer()

    return finished_players, finished_player_name, jailed_count, player_score, player_name, player_number
    
