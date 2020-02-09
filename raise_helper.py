from position import Position

def toggle_position(pos, blindPos):
    """ Toggle position between BTN and the blinds. """
    return blindPos if pos == Position.BTN else Position.BTN

def calc_RFI_size(percent=100, pos=Position.BTN):
    bb = 1
    # if not SB then there's 0.5 dead
    init_pot = 0.5 if pos != Position.SB else 0
    # treating the BB as the bet and having the sb dead (in the pot)
    r = calc_raise_size(percent, bb, init_pot)
    sb_str = " from the SB" if pos == Position.SB else ""
    print("A {}% raise{} is {}".format(percent, sb_str, r))
    return r

def calc_3bet_size(percent, bet, pos):
    init_pot = 1 if pos == Position.SB else 0.5
    r = calc_raise_size(percent, bet, init_pot)
    return r

def calc_raise_size(percent, bet, init_pot):
    #print("percent: {} cur_bet: {} init_pot: {}".format(percent, bet, init_pot))
    p = percent/100

    # 2x bet since we need to call first then raise
    pot = 2*bet + init_pot
    r = bet + p*pot
    return r

"""
for BTN RFI, the initial pot is always 0.5 with a bet of 1
but then when calculating the SB 3!, the init_pot is 1 (since the BB is dead)
with a bet of BTN RFI
"""

def init_pot_for_sequence(pos):
    return 1 if pos == Position.SB else 0.5

def calc_raise_sequence(blind_pos, *percents):
    r = []
    pos = blind_pos
    # BTN RFI always has SB as dead money
    bet = 0.5
    r = 0
    for i, percent in enumerate(percents):
        percent = int(percent)
        init_pot = 1 if blind_pos == Position.SB else 0.5
        # RFI
        if i == 0:
            r = calc_raise_size(percent, 1, 0.5)
        else:
            r = calc_raise_size(percent, bet, init_pot)
                                
        pos = toggle_position(pos, blind_pos)
        #print("bet {} init_pot {}".format(bet, init_pot))
        bet = r
        print("{} {}%: {}".format(pos, percent, r))

#2.5, call 2.5 total 6; 1.5x = 9 + 2.5 = 11.5
def accept_raise_sequence():
    while True:
        s = str(input("Enter raise % sequence space separated e.g., 60 200\n"))
        s = [int(x) for x in s.split()]
        calc_raise_sequence(Position.BB, *s)
        print()
        calc_raise_sequence(Position.SB, *s)

def accept_action_sequence():
    s = str(input("Enter an action sequence sequence space separated e.g., 60 200\n"))
    s = [int(x) for x in s.split()]
