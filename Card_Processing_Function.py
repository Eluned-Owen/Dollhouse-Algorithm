def card_analyser(player, scanned_card, model_picked, cards, turn):
    finished_players = 0
    finished_player_name = ""

    player_score = player.score
    player_name = player.name
    player_number = 0

    player_jailed = False

        # Accept either a single card string or a list of card strings
    if isinstance(scanned_card, list):
        scanned_cards = scanned_card
    else:
        scanned_cards = [scanned_card]

    collected_cards = []

    for card_value in scanned_cards:
        card_value = str(card_value).strip()

        if card_value in ["", "NO_CARD", "READ_FAILED"]:
            continue
        card_index = int(card_value)

        collected_cards.append(card_index)

    score_tally = []

        # model_picked is currently a list like ["Risk Model"]
    model_name = model_picked[0]

        # Process all matched cards
    for i in collected_cards:
        card_finder = cards.iloc[i]

        score = card_finder[model_name]

            # Card re-use logic
        cards.loc[i, player.name] += 1

        if cards.loc[i, player.name] == 3:
            print("You can use", card_finder["Card"], "only once more")

        if cards.loc[i, player.name] >= 4:
            print("You've used", card_finder["Card"], "too much")
            break
        else:
            score_tally.append(score)


    print("Score tally:", score_tally)

    # Sum up the score for the turn and add it to the player's total score
    turn_score = 0

    for item in score_tally:
        turn_score += item

    if turn > 5:
        print("multiplier is on")
        turn_score *= 1.5
    
    turn_score = round(turn_score)

    print("score =", turn_score)

    player.score = player.score + turn_score

    if player.score >= 100:
        player_jailed = True
        print("=== You have been jailed ===")

    print("new score for", player.name, ":", player.score)

    player_score = player.score
    player_name = player.name


    # Assign player number for LCD display
    if player_name.endswith("1"):
        player_number = 1
    elif player_name.endswith("2"):
        player_number = 2
    elif player_name.endswith("3"):
        player_number = 3


    #turn_str = str(turn)
    #turn_num_encode = turn_str.encode("utf-8")

    #encoded_name = player.name.encode("utf-8")
    #encoded_column = ": ".encode("utf-8")
    #encoded_divider = " | ".encode("utf-8")
    #encoded_turn_first = str(turn_score)
    #encoded_turn = encoded_turn_first.encode("utf-8")

    #print_name = encoded_name + encoded_column

    #printer.write(encoded_divider)
    #printer.write(print_name)
    #printer.write(encoded_turn)

    # Check if the player has reached 0 points
    if player.score <= 0:
        finished_players += 1
        finished_player_name = player.name
    

    return finished_players, finished_player_name, player_jailed, player_score, player_name, player_number, turn

