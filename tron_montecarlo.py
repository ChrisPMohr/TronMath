# tron montecarlo

import random
import time
import logging

logging.basicConfig(level=logging.INFO)
# simulated_hands = {6} # This will cause simulation to only run for a subset of hands
simulated_hands = None # This will run the simulation for all hands
num_simul = 100000000


on_the_play = False

def make_cards(dist):
    cards = []
    for i, count in enumerate(dist):
        cards.extend([i] * count)
    return cards

CARD_NAMES = {
    0: "Tower",
    1: "Power Plant",
    2: "Mine",
    3: "Map",
    4: "Chromatic",
    5: "Scrying",
    6: "Stirrings",
    7: "Once Upon a Time",
    8: "Blank"
}

TOWER = 0
POWER_PLANT = 1
MINE = 2
MAP = 3
CHROMATIC = 4
SCRYING = 5
STIRRINGS = 6
ONCE = 7
no_once_card_dist = [4,4,4,4,8,4,4,0,28]
with_once_card_dist = [4,4,4,4,8,4,4,4,24]


hand_size = 7


def to_percent(f):
    return round(f*100,2)


def main(hand_conditions, card_dist):
    if sum(card_dist) != 60:
        raise ValueError("Decklist doesn't have 60 cards")
    cards = make_cards(card_dist)
    made_tron_counters = [0] * (len(hand_conditions))
    total_counters = [0] * (len(hand_conditions))
    rest_counter = 0

    for _ in range(num_simul):
        random.shuffle(cards)
        hand = cards[:hand_size]
        hand_set = set(hand)
        for hand_index, hand_condition in enumerate(hand_conditions):
            if hand_condition[1](hand_set, hand):
                break
        else:
            rest_counter += 1
            continue
        if simulated_hands is None or hand_index in simulated_hands:
            if simulated_hand_has_tron(cards):
                made_tron_counters[hand_index] += 1
        total_counters[hand_index] += 1

    for i, condition in enumerate(hand_conditions):
        if total_counters[i]:
            print(
                "{:36} {:5.2f} {:6.2f} {:10}".format(
                    condition[0],
                    to_percent(float(total_counters[i]) / num_simul),
                    to_percent(float(made_tron_counters[i]) / total_counters[i]) if total_counters[i] else 0,
                    total_counters[i]
                ))
    print("{:36} {:5.2f}".format("Rest", to_percent(float(rest_counter) / num_simul)))


def simulated_hand_has_tron(cards):
    hand = cards[:hand_size]
    next_card_index = hand_size
    hand_set = set(hand)
    # apply rules

    logging.debug("---- Started new hand ----")
    logging.debug(hand)

    missing_land_set = list({0,1,2} - hand_set)
    if missing_land_set:
        missing_land = missing_land_set[0]
    else:
        logging.debug("RULE: TRON - Have natural tron")
        return True

    turn = 1 if on_the_play else 0
    mana = turn
    green_mana = 0
    chrom_in_play = False
    have_cast_spell = False
    while True:
        logging.debug(
            "turn %d, mana %d, green_mana %d, chrom_in_play %r, have_cast_spell %r",
            turn, mana, green_mana, chrom_in_play, have_cast_spell)
        if is_xyz(hand_set, hand):
            logging.debug("RULE: TRON - Drew natural tron")
            return True
        elif turn == 3:
            logging.debug("RULE: FAIL - Is turn 3")
            return False
        elif turn == 1 and mana == 1 and MAP in hand_set:
            logging.debug("RULE: TRON - Have turn 1 map")
            return True
        elif mana >= 1 and green_mana >= 1 and SCRYING in hand_set:
            logging.debug("RULE: TRON - Played Scrying")
            return True
        elif not have_cast_spell and ONCE in hand_set:
            logging.debug("RULE: Played Once Upon a Time 1")
            hand, hand_set = play_card(hand, ONCE)
            have_cast_spell = True

            once_cards = cards[next_card_index:next_card_index+5]
            next_card_index += 5
            if missing_land in once_cards:
                logging.debug("RULE: TRON - Once Upon a Time hit tron")
                return True
        elif chrom_in_play and (mana + green_mana) >= 1:
            logging.debug("RULE: Cracked Chromatic")
            chrom_in_play = False
            mana, green_mana = spend_mana(mana, green_mana, 1, 0)

            green_mana += 1
            card = cards[next_card_index]
            next_card_index += 1
            hand.append(card)
            hand_set.add(card)
            logging.debug("DRAW: %s", CARD_NAMES[card])
        elif have_cast_spell and ONCE in hand_set and green_mana >= 1 and (mana + green_mana) >= 2 and not (CHROMATIC in hand_set and STIRRINGS in hand_set):
            logging.debug("RULE: Played Once Upon a Time 2")
            hand, hand_set = play_card(hand, ONCE)
            mana, green_mana = spend_mana(mana, green_mana, 1, 1)
            have_cast_spell = True

            once_cards = cards[next_card_index:next_card_index+5]
            next_card_index += 5
            if missing_land in once_cards:
                logging.debug("RULE: TRON - Once Upon a Time hit tron")
                return True
        elif (mana + green_mana) >= 2 and CHROMATIC in hand_set:
            logging.debug("RULE: Played chromatic with spare mana")
            mana, green_mana = spend_mana(mana, green_mana, 1, 0)
            hand, hand_set = play_card(hand, CHROMATIC)
            have_cast_spell = True

            chrom_in_play = True
        elif green_mana == 1 and STIRRINGS in hand_set:
            logging.debug("RULE: Played stirrings")
            mana, green_mana = spend_mana(mana, green_mana, 0, 1)
            hand, hand_set = play_card(hand, STIRRINGS)
            have_cast_spell = True

            stirrings_cards = cards[next_card_index:next_card_index+5]
            next_card_index += 5
            if missing_land in stirrings_cards:
                logging.debug("RULE: TRON - Stirrings hit tron")
                return True
        elif have_cast_spell and ONCE in hand_set and green_mana >= 1 and (mana + green_mana) >= 2:
            logging.debug("RULE: Played Once Upon a Time 3")
            hand, hand_set = play_card(hand, ONCE)
            mana, green_mana = spend_mana(mana, green_mana, 1, 1)
            have_cast_spell = True

            once_cards = cards[next_card_index:next_card_index+5]
            next_card_index += 5
            if missing_land in once_cards:
                logging.debug("RULE: TRON - Once Upon a Time hit tron")
                return True
        elif (mana + green_mana) >= 1 and CHROMATIC in hand_set:
            logging.debug("RULE: Played chromatic without spare mana")
            mana, green_mana = spend_mana(mana, green_mana, 1, 0)
            hand, hand_set = play_card(hand, CHROMATIC)
            have_cast_spell = True

            chrom_in_play = True
        else:
            logging.debug("RULE: Finished turn")
            turn += 1
            mana = turn
            green_mana = 0

            card = cards[next_card_index]
            next_card_index += 1
            hand.append(card)
            hand_set.add(card)
            logging.debug("DRAW: %s", CARD_NAMES[card])


def spend_mana(current_colorless, current_green, cost_colorless, cost_green):
    colorless_spent = min(current_colorless, cost_colorless)
    current_colorless -= colorless_spent
    if colorless_spent < cost_colorless:
        current_green -= (cost_colorless - colorless_spent)
    current_green -= cost_green
    return current_colorless, current_green


def play_card(hand, card):
    hand.remove(card)
    hand_set = set(hand)
    return hand, hand_set


def is_xyz(hand, hand_mul):
    return 0 in hand and 1 in hand and 2 in hand

def is_xy(hand, hand_mul):
    return ((0 in hand) + (1 in hand) + (2 in hand)) == 2

def is_xy_map(hand, hand_mul):
    return is_xy(hand, hand_mul) and MAP in hand

def is_xy_chrom_scry(hand, hand_mul):
    return is_xy(hand, hand_mul) and CHROMATIC in hand and SCRYING in hand

def is_xy_chrom_stir(hand, hand_mul):
    return is_xy(hand, hand_mul) and CHROMATIC in hand and STIRRINGS in hand

def is_xy_chrom_chrom(hand, hand_mul):
    return is_xy(hand, hand_mul) and hand_mul.count(CHROMATIC) >= 2

def is_xy_chrom_chrom_stir(hand, hand_mul):
    return is_xy(hand, hand_mul) and hand_mul.count(CHROMATIC) >= 2 and STIRRINGS in hand

def is_xy_chrom(hand, hand_mul):
    return is_xy(hand, hand_mul) and CHROMATIC in hand

def is_xy_stir(hand, hand_mul):
    return is_xy(hand, hand_mul) and STIRRINGS in hand

def is_xy_scry(hand, hand_mul):
    return is_xy(hand, hand_mul) and SCRYING in hand

def is_xy_scry_stir(hand, hand_mul):
    return is_xy(hand, hand_mul) and SCRYING in hand and STIRRINGS in hand

# hands with once upon a time
def is_xy_chrom_stir_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and CHROMATIC in hand and STIRRINGS in hand and ONCE in hand

def is_xy_chrom_chrom_once_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and hand_mul.count(CHROMATIC) >= 2 and hand_mul.count(ONCE) >= 2

def is_xy_chrom_chrom_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and hand_mul.count(CHROMATIC) >= 2 and ONCE in hand

def is_xy_chrom_chrom_stir_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and hand_mul.count(CHROMATIC) >= 2 and STIRRINGS in hand and ONCE in hand

def is_xy_chrom_once_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and CHROMATIC in hand and hand_mul.count(ONCE) >= 2

def is_xy_chrom_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and CHROMATIC in hand and ONCE in hand

def is_xy_stir_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and STIRRINGS in hand and ONCE in hand

def is_xy_scry_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and SCRYING in hand and ONCE in hand

def is_xy_scry_stir_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and SCRYING in hand and STIRRINGS in hand and ONCE in hand

def is_xy_once_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and hand_mul.count(ONCE) >= 2

def is_xy_once(hand, hand_mul):
    return is_xy(hand, hand_mul) and ONCE in hand


on_the_play_conditions = [
    ("XYZ", is_xyz),
    ("XY + Map", is_xy_map),
    ("XY + Chrom + Scry", is_xy_chrom_scry),
    ("XY + Chrom + Chrom + Stir + Once", is_xy_chrom_chrom_stir_once),
    ("XY + Chrom + Stir + Once", is_xy_chrom_stir_once),
    ("XY + Chrom + Chrom + Once + Once", is_xy_chrom_chrom_once_once),
    ("XY + Chrom + Once + Once", is_xy_chrom_once_once),
    ("XY + Chrom + Chrom + Once", is_xy_chrom_chrom_once),
    ("XY + Chrom + Chrom + Stir", is_xy_chrom_chrom_stir),
    ("XY + Chrom + Once", is_xy_chrom_once),
    ("XY + Chrom + Stir", is_xy_chrom_stir),
    ("XY + Chrom + Chrom", is_xy_chrom_chrom),
    ("XY + Stir + Once", is_xy_stir_once),
    ("XY + Once + Once", is_xy_once_once),
    ("XY + Once", is_xy_once),
    ("XY + Chrom", is_xy_chrom),
    ("XY + Stir", is_xy_stir),
    ("XY", is_xy)
]

on_the_draw_conditions = [
    ("XYZ", is_xyz),
    ("XY + Map", is_xy_map),
    ("XY + Chrom + Scry", is_xy_chrom_scry),
    ("XY + Chrom + Chrom + Stir + Once", is_xy_chrom_chrom_stir_once),
    ("XY + Chrom + Stir + Once", is_xy_chrom_stir_once),
    ("XY + Chrom + Chrom + Once + Once", is_xy_chrom_chrom_once_once),
    ("XY + Chrom + Once + Once", is_xy_chrom_once_once),
    ("XY + Chrom + Chrom + Once", is_xy_chrom_chrom_once),
    ("XY + Chrom + Chrom + Stir", is_xy_chrom_chrom_stir),
    ("XY + Chrom + Once", is_xy_chrom_once),
    ("XY + Chrom + Stir", is_xy_chrom_stir),
    ("XY + Chrom + Chrom", is_xy_chrom_chrom),
    ("XY + Scry + Once", is_xy_scry_once),
    ("XY + Chrom", is_xy_chrom),
    ("XY + Stir + Once", is_xy_stir_once),
    ("XY + Once + Once", is_xy_once_once),
    ("XY + Scry + Stir + Once", is_xy_scry_stir_once),
    ("XY + Scry + Stir", is_xy_scry_stir),
    ("XY + Once", is_xy_once),
    ("XY + Scry", is_xy_scry),
    ("XY + Stir", is_xy_stir),
    ("XY", is_xy)
]


if __name__ == '__main__':
    start_time = time.time()
    main(
        on_the_play_conditions if on_the_play else on_the_draw_conditions,
        with_once_card_dist)
    print(time.time() - start_time)