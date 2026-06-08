from enum import Enum
from dataclasses import dataclass
from typing import Final, Optional from random import shuffle

NUM_BLUE_POLICIES: Final = 6
NUM_RED_POLICIES: Final = 11
POLICY_DRAW_COUNT: Final = 3
TYRANT_ZONE_COUNT: Final = 3

class Party(Enum):
    RED = "RED"
    BLUE = "BLUE"

class Role(Enum):
    RED = "RED"
    BLUE = "BLUE"
    TYRANT = "TYRANT"

@dataclass
class Player:
    uid: int
    party: Party
    role: Role

class PolicyTile(Enum):
    RED = "RED"
    BLUE = "BLUE"

class PresidentialPower(Enum):
    NONE = "NO POWER"
    INVESTIGATE = "INVESTIGATE LOYALTY"
    SPECIAL_ELECTION = "CALL SPECIAL ELECTION"
    POLICY_PEEK = "POLICY_PEEK"
    EXECUTION = "EXECUTION"

class Vote(Enum):
    JA = "JA"
    NEIN = "NEIN"

class Deck:
    def __init__(self):
        self.draw_pile = []
        self.discard_pile = NUM_BLUE_POLICIES * [PolicyTile.BLUE] + NUM_RED_POLICIES * [PolicyTile.RED]
        self.shuffle()

    def shuffle(self) -> bool:
        '''shuffles only if less than 3 tiles in draw pile and returns whether shuffle occurred'''
        if len(self.draw_pile) < POLICY_DRAW_COUNT:
            self.draw_pile.extend(self.discard_pile)
            shuffle(self.draw_pile)
            self.discard_pile = []

            return True
        
        return False

    def _check_draw_size(self):
        if len(self.draw_pile) < POLICY_DRAW_COUNT:
            raise RuntimeError(f"Draw pile should always contain at least 3 tiles but contains {len(self.draw_pile)}")

    def draw(self):
        self._check_draw_size()
        top_three = (self.draw_pile.pop(), self.draw_pile.pop(), self.draw_pile.pop())
        return top_three

    def top_deck(self):
        self._check_draw_size()
        tile = self.draw_pile.pop()
        return tile

    def peek(self):
        self._check_draw_size()
        return self.draw_pile[-3:]
    
    def discard(self, tile1: PolicyTile, tile2: PolicyTile):
        self.discard_pile.extend([tile1, tile2])

class Board:
    RED_TRACK_5_6: Final = (
        PresidentialPower.NONE,
        PresidentialPower.NONE,
        PresidentialPower.POLICY_PEEK,
        PresidentialPower.EXECUTION,
        PresidentialPower.EXECUTION,
        PresidentialPower.NONE
    )
    RED_TRACK_7_8: Final = (
        PresidentialPower.NONE,
        PresidentialPower.INVESTIGATE,
        PresidentialPower.SPECIAL_ELECTION,
        PresidentialPower.EXECUTION,
        PresidentialPower.EXECUTION,
        PresidentialPower.NONE
    )
    RED_TRACK_9_10: Final = (
        PresidentialPower.INVESTIGATE,
        PresidentialPower.INVESTIGATE,
        PresidentialPower.SPECIAL_ELECTION,
        PresidentialPower.EXECUTION,
        PresidentialPower.EXECUTION,
        PresidentialPower.NONE
    )

    def __init__(self, player_count: int):
        if player_count < 5 or player_count > 10:
            raise ValueError(f"Player count must be between 5 and 10 inclusive. Board received {player_count} for player count.") 

        if 5 <= player_count <= 6:
            self.RED_TRACK = Board.RED_TRACK_5_6
        elif 7 <= player_count <= 8:
            self.RED_TRACK = Board.RED_TRACK_7_8
        else:
            self.RED_TRACK = Board.RED_TRACK_9_10

        self.blue_played = 0
        self.red_played = 0

    def play_tile(self, tile: PolicyTile) -> PresidentialPower:
        match tile:
            case PolicyTile.BLUE:
                self.blue_played += 1
                return PresidentialPower.NONE
            case PolicyTile.RED:
                self.red_played += 1
                return self.RED_TRACK[self.red_played - 1]

    def check_win(self) -> Optional[Party]:
        if self.blue_played >= 5:
            return Party.BLUE
        elif self.red_played >= 6:
            return Party.RED
        else:
            return None

    def check_tyrant_zone(self) -> bool:
        return self.red_played >= TYRANT_ZONE_COUNT 
                
class ElectionTracker:
    def __init__(self):
        self.failed_elections = 0

    def increment(self) -> bool:
        self.failed_elections = (self.failed_elections + 1) % 4
        return self.failed_elections == 3

class BallotBox:
    def __init__(self):
        self.votes = {}

    def submit_vote(self, uid: int, vote: Vote):
        self.votes[uid] = vote

    def vote_count(self) -> int:
        return len(self.votes)
    
    def get_result(self) -> Vote:
        ja_count = list(self.votes.values()).count(Vote.JA)

        return Vote.JA if ja_count > len(self.votes.values()) // 2 else Vote.NEIN

