from BowlingGame import BowlingGame
from Database import Database

class PlayGame:
    def __init__(self):
        self.game = BowlingGame()
        self.db = Database("database/bowling.db")

    def play(self):   
        game_on = True
        print('\n********** WELCOME TO THE BOWLING CLUB **********\n')
        self.game.player = input('Enter your username: ')
        start_or_scores = input('To enter your scores, type "start",\nto see the list of high scores type "scores": ')
        while game_on == True:            
            if start_or_scores.lower() == 'start':
                self.db.insert_new_game(self.game.player)
                for i in range(10):
                    self.game.calculate_score(i)
                self.game.calculate_bonus_score()
                self.db.update_score(self.game.score)
                self.db.insert_frames(self.game.rounds)
                game_on = False
            elif start_or_scores.lower() == 'scores':
                games = self.db.print_all_games()
                print(games)
                back_or_exit = input('\nIf you want to see game data type number below the filed "id", if you want to go back type "back",'
                +'leave empty to exit: \n')
                if int(back_or_exit):
                    print(self.db.print_all_frames(int(back_or_exit)))
                elif back_or_exit.lower() != 'back':
                    game_on = False
            else:
                start_or_scores = input('Wrong input, please try again.\nTo enter your scores, type "start",'
                +'\nto see the list of high scores type "scores": ')  


def main():
    bowling = PlayGame()
    bowling.play()
    
if __name__ == '__main__':
    main()