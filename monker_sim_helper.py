import math
import itertools
from raise_helper import *
from position import Position, BB_AMT, SB_AMT

class Player:
    def __init__(self, pos):
        self.pos = pos
        self.stack = 100
        self.folded = False
        self.has_option = True
        invested = {
            Position.BB: BB_AMT,
            Position.SB: SB_AMT,
        }
        self.invested = invested.get(pos, 0)
    
    def raise_to(self, amt):
        extra_invested = self.call(amt)
        self.has_option = True
        return extra_invested

    def call(self, amt):
        extra_invested = max(amt-self.invested, 0)
        self.stack -= extra_invested
        self.invested = amt
        self.has_option = True
        return extra_invested

    def fold(self):
        self.folded = True
        self.has_option = False

    def check(self):
        self.call(0)

    def available(self):
        return not self.folded and self.has_option

    def __str__(self):
        return str(self.pos).split(".")[1]

class Game:
    MAX_PLAYERS = 6
    def __init__(self, num_players):
        self.num_players_rem = self.num_players = min(num_players, Game.MAX_PLAYERS)
        print("Initializing game with {} players".format(self.num_players))
        ommited_players = Game.MAX_PLAYERS - self.num_players
        positions = [x for x in Position][ommited_players:]
        self.players = []
        self.player_idx = 0
        # BB is encoded as a bet
        self.pot = SB_AMT
        self.bet = BB_AMT
        for position in positions:
            p = Player(position)
            self.players.append(p)
            print(position)
        print("Currently in pot {}".format(self.total_pot()))

    def get_cur_player(self):
        return self.players[self.player_idx]

    def next_player(self):
        while True:
            self.player_idx = (self.player_idx+1) % len(self.players)
            if self.players[self.player_idx].available():
                break
        return self.players[self.player_idx]

    def total_pot(self):
        return self.pot + self.bet

    def fold(self):
        p = self.get_cur_player()
        print("{} folded".format(p))
        if self.num_players_rem == 2:
            raise ValueError("No more remaining players")
        p.fold()
        self.num_players_rem -= 1

    def raise_to_amt(self, amt):
        p = self.get_cur_player()
        self.pot += self.bet
        self.bet = p.raise_to(amt)

    def raise_by_percent(self, percent):
        try:
            int(percent)
        except:
            raise NameError("Invalid Raise Size")
        p = self.get_cur_player()
        raise_amt = calc_raise_size(percent, self.bet, self.pot-p.invested)
        print("Raising by {}% = {}x".format(percent, raise_amt))
        self.raise_to_amt(raise_amt)

    def call(self):
        p = self.get_cur_player()
        self.pot += p.call(self.bet)
        print("{} calls. Total in pot is {}.".format(p, self.total_pot()))

    def rewind(self):
        pass

    def parse_action(self, s):
        action = "".join(itertools.takewhile(str.isalpha, s))
        size = "".join(itertools.takewhile(str.isnumeric, s[len(action):]))
        if len(size) != 0:
            size = int(size)
        actions = {
            'r': lambda : self.raise_by_percent(size),
            'c': self.call,
            'f': self.fold,
            'back': self.rewind
        }
        if action not in actions:
            raise NameError("Invalid Action")
        return actions[action]
        
    def start(self):
        player = None
        while True:
            player = self.get_cur_player()
            s = input("What's {}'s action?\n".format(player))
            try:
                f = self.parse_action(s)
                f()
            except NameError as e:
                print(e)
                continue
            except ValueError as e:
                print(e)
                break
            self.next_player()

class GameDriver:
    def __init__(self, num_players):
        self.history = []
        history.append(Game(num_players))

if __name__ == "__main__":
    n = int(input("How many handed?\n"))
    g = Game(n)
    g.start()
