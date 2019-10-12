# tron montecarlo

import random
import time

def make_cards(dist):
    cards = []
    for i, count in enumerate(dist):
        cards.extend([i] * count)
    return cards


# 0 1 2 Tower Power Plant Mine
# 3 Map
# 4 Chromatic
# 5 Scrying
# 6 Stirrings
opening_card_dist = [4,4,4,4,8,4,4,28]

xy_chrom_stir_play_dist = [0,0,4,0,7,4,0,38]
xy_chrom_stir_draw_dist = [0,0,4,0,7,4,0,37]
xy_chrom_chrom_play_dist = [0,0,4,0,0,4,4,41]
xy_chrom_chrom_draw_dist = [0,0,4,0,0,4,4,40]
xy_chrom_play_dist = [0,0,4,0,7,4,4,34]
xy_chrom_draw_dist = [0,0,4,0,7,4,4,33]


num_simul = 100000000


def main(conditions, hand_size, card_dist):
    cards = make_cards(card_dist)
    counters = [0] * len(conditions)
    rest = 0
    for _ in range(num_simul):
        hand_mul = random.sample(cards, hand_size)
        hand = set(hand_mul)
        for i, condition in enumerate(conditions):
            if condition[1](hand, hand_mul):
                counters[i] += 1
                break
        else:
            rest += 1

    for i, condition in enumerate(conditions):
        print(condition[0], float(counters[i]) / num_simul)
    print("Rest", float(rest) / num_simul)


def is_xyz(hand, hand_mul):
    return 0 in hand and 1 in hand and 2 in hand

def is_xy(hand, hand_mul):
    return ((0 in hand) + (1 in hand) + (2 in hand)) == 2

def is_xy_map(hand, hand_mul):
    return is_xy(hand, hand_mul) and 3 in hand

def is_xy_chrom_scry(hand, hand_mul):
    return is_xy(hand, hand_mul) and 4 in hand and 5 in hand

def is_xy_chrom_stir(hand, hand_mul):
    return is_xy(hand, hand_mul) and 4 in hand and 6 in hand

def is_xy_chrom_chrom(hand, hand_mul):
    return is_xy(hand, hand_mul) and hand_mul.count(4) >= 2

def is_xy_chrom_chrom_stir(hand, hand_mul):
    return is_xy(hand, hand_mul) and hand_mul.count(4) >= 2 and 6 in hand

def is_xy_chrom(hand, hand_mul):
    return is_xy(hand, hand_mul) and 4 in hand

def is_xy_stir(hand, hand_mul):
    return is_xy(hand, hand_mul) and 6 in hand

def is_xy_scry(hand, hand_mul):
    return is_xy(hand, hand_mul) and 5 in hand

def is_xy_scry_stir(hand, hand_mul):
    return is_xy(hand, hand_mul) and 5 in hand and 6 in hand

def has_anything(hand, hand_mul):
    return 3 in hand or 4 in hand or 5 in hand or 6 in hand

def is_xy_and_has_anything(hand, hand_mul):
    return is_xy(hand, hand_mul)  and has_anything(hand, hand_mul)

on_the_play_conditions = [
    ("XYZ", is_xyz),
    ("XY + Map", is_xy_map),
    ("XY + Chrom + Scry", is_xy_chrom_scry),
    ("XY + Chrom + Chrom + Stir", is_xy_chrom_chrom_stir),
    ("XY + Chrom + Stir", is_xy_chrom_stir),
    ("XY + Chrom + Chrom", is_xy_chrom_chrom),
    ("XY + Chrom", is_xy_chrom),
    ("XY + Stir", is_xy_stir),
    ("XY + Scry", is_xy_scry),
    ("XY", is_xy)
]

on_the_draw_conditions = [
    ("XYZ", is_xyz),
    ("XY + Map", is_xy_map),
    ("XY + Chrom + Scry", is_xy_chrom_scry),
    ("XY + Chrom + Chrom + Stir", is_xy_chrom_chrom_stir),
    ("XY + Chrom + Stir", is_xy_chrom_stir),
    ("XY + Chrom + Chrom", is_xy_chrom_chrom),
    ("XY + Chrom", is_xy_chrom),
    ("XY + Scry + Stir", is_xy_scry_stir),
    ("XY + Scry", is_xy_scry),
    ("XY + Stir", is_xy_stir),
    ("XY", is_xy)
]


def is_land_or_scrying(hand, hand_mul):
    return 2 in hand or 5 in hand

def is_stirrings(hand, hand_mul):
    return 6 in hand

def is_chrom(hand, hand_mul):
    return 4 in hand

def is_chrom_and_stirrings(hand, hand_mul):
    return 6 in hand and 4 in hand

def is_land(hand, hand_mul):
    return 2 in hand

xy_chrom_chrom_conditions = [
    ("land / scry", is_land_or_scrying),
    ("stirrings", is_stirrings)
]

xy_chrom_stir_conditions = [
    ("land / scry", is_land_or_scrying),
    ("chrom", is_chrom)
]

xy_chrom_conditions = [
    ("land / scry", is_land_or_scrying),
    ("chrom + stirrings", is_chrom_and_stirrings),
    ("stirrings", is_stirrings),
    ("chrom", is_chrom)
]


if __name__ == '__main__':
    start_time = time.time()
    main(on_the_draw_conditions, 7, opening_card_dist)
    #main(xy_chrom_stir_conditions, 2, xy_chrom_stir_draw_dist)
    #main(xy_chrom_chrom_conditions, 2, xy_chrom_chrom_draw_dist)
    #main(xy_chrom_conditions, 2, xy_chrom_draw_dist)
    print(time.time() - start_time)