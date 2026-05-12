import time

def card_analyser(player, ser, model_picked, cards):

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
        score_tally.append(score)

    print(score_tally)

    turn_score = 0
    for item in score_tally:
        turn_score += item

    print("score = ", turn_score)
    player.score = player.score + turn_score
    print("new score for", player.name, ": ", player.score)

    #Clear leftover serial noise
    ser.reset_input_buffer()