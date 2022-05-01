from collections import defaultdict
import requests

class OutOfBoundsError(Exception):
    """Custom error that is raised when number of pins is out of bounds"""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

class Frame:
    def __init__(self):
        self.try1: int = 0
        self.try2: int = 0
        self.try3: int = 0
        self.bonus: int = 0        

class BowlingGame:   
    def __init__(self, player = 'Player 1'):
        """Initialize the game"""
        self.player: str = player
        self.score: int = 0
        self.frame: int = 1
        self.remaining_pins: int = 10
        self.frames = defaultdict(list)
        self.rounds =[Frame() for _ in range(10)]

    def pins_validation(self, pins) -> None:
        """Validation of the number of pins"""
        if pins < 0:
            raise OutOfBoundsError('Cannot roll less than zero pins.')
        if pins > 10:
            raise OutOfBoundsError('Cannot roll more than ten pins.')
        if pins > self.remaining_pins:
            raise OutOfBoundsError(f'Cannot roll more than {self.remaining_pins}.')

    def roll(self, pins):
        """Emulate the Ball launch."""
        self.pins_validation(pins)
        
        if pins == 10:
            if self.frames[self.frame] != [] and self.frames[self.frame] != [0] and self.frame < 11:
                self.frame += 1
            self.frames[self.frame].append(pins)
            if self.frame < 11:
                self.frame += 1
        elif len(self.frames[self.frame]) == 0:
            self.frames[self.frame].append(pins)
        elif len(self.frames[self.frame]) == 1:
            self.frames[self.frame].append(pins)
            if self.frame < 11:
                self.frame += 1
        else:
            if self.frame < 11:
                self.frame += 1
            self.frames[self.frame].append(pins)

        self.remaining_pins = 10 - int(sum(self.frames[self.frame]))
        self.pins_left = f'Remaining number of pins in round: {self.frame} is {self.remaining_pins}.'
        pins = 0

    def bonus_roll(self, pins):
        """Additional roll for the end of the game bonus"""
        self.pins_validation(pins) 
        self.frames[10].append(pins)
    
    def calculate_score(self, i):
        '''Calculating the score of the game'''
        self.rounds[i].try1 = self.bowl()
        if self.rounds[i].try1 == 10:
            self.rounds[i].try2 = 0
        else:
            self.rounds[i].try2 = self.bowl()

        if i > 0 and (self.rounds[i-1].try1 + self.rounds[i-1].try2) == 10:         #bonus for a spare
            self.rounds[i-1].bonus = self.rounds[i].try1
        if i > 1 and self.rounds[i-2].try1 == 10 and self.rounds[i-1].try1 == 10:   #2 strikes in a row
            self.score += 20 + self.rounds[i].try1 + self.rounds[i].try2
            if i == 2 and self.rounds[0].try1 == 10 and self.rounds[1].try1 == 10:
                self.score += 10
        elif i > 0 and self.rounds[i-1].try1 == 10:                                 #strike
            self.score += 10 + self.rounds[i].try1 + self.rounds[i].try2
        elif i > 0 and (self.rounds[i-1].try1 + self.rounds[i-1].try2) == 10:       #spare
            self.score += 10 + self.rounds[i-1].bonus
        if (self.rounds[i].try1 + self.rounds[i].try2) < 10:                        #failed to knock all of the pins
            self.score += self.rounds[i].try1 + self.rounds[i].try2
        self.print_frames()
        print(f'Score is {self.score}')

    def calculate_bonus_score(self):
        '''Calculating the score of the game in the last round'''
        if self.rounds[9].try1 == 10:
            self.rounds[9].try2 = self.bonus_bowl()
        if self.rounds[9].try2 == 10 or (self.rounds[9].try1 + self.rounds[9].try2) == 10:
            self.rounds[9].try3 = self.bonus_bowl()   
        if self.rounds[9].try2 == 10 or (self.rounds[9].try1 + self.rounds[9].try2) == 10:
                self.score += self.rounds[9].try1 + self.rounds[9].try2 + self.rounds[9].try3                 
        print(f'Total score is: {self.score}')

    def print_frames(self):
        for frame in self.frames:
            if self.frames[frame] != []:
                print(f'{frame}: {self.frames[frame]}')

    def user_input(self) -> int:
        """Input the number of knocked pins and get a response through an API"""
        pins = int(input('\nHow many pins have you knocked? '))
        resp = requests.get(f'http://127.0.0.1:8000/scores?pins={pins}')
        rolls = resp.json()
        return int(rolls["current_roll"])

    def bowl(self) -> int:
        pins_knocked = self.user_input()
        self.roll(pins_knocked)
        print(self.pins_left)
        return pins_knocked
    
    def bonus_bowl(self) -> int:
        pins_knocked = self.user_input()
        self.bonus_roll(pins_knocked)
        return pins_knocked
