import sqlite3
import datetime
import pandas as pd

time = datetime.datetime.now()
time = time.strftime("%d/%m/%Y, %H:%M:%S")

class Database:
    def __init__(self, db_path):
        self.__connection = sqlite3.connect(db_path)
        self.__cursor = self.__connection.cursor()

    def insert_new_game(self, player):
        query = ("INSERT INTO game(username, time, score) VALUES (?,?,?)")
        self.__cursor.execute(query, (player, time, 0))
        self.__connection.commit()

    def get_game_id(self):
        query = ("SELECT id FROM game ORDER BY id DESC LIMIT 1")
        c = self.__cursor.execute(query)
        game_id = c.fetchone()[0]
        self.__connection.commit()
        return game_id

    def update_score(self, score):
        
        game_id = self.get_game_id()
        query = ("UPDATE game SET score="+str(score)+" WHERE id="+str(game_id))
        self.__cursor.execute(query)
        self.__connection.commit()

    def insert_frames(self, frames):

        game_id = self.get_game_id()     
        for i in range(10):
            query = ("INSERT INTO frame(try1, try2, try3, frame_id, game_id) VALUES (?,?,?,?,?)")
            self.__cursor.execute(query, (frames[i].try1, frames[i].try2, frames[i].try3, i, game_id))            
            self.__connection.commit()

        
    def print_all_games(self):
        query = ("SELECT * FROM game order by score desc")
        df = pd.read_sql_query(query, self.__connection)
        return df.head(10)

    def print_all_frames(self, game_id):
        query = ("SELECT frame_id, try1, try2, try3, username, time"
                + " FROM frame JOIN game ON game.id=frame.game_id WHERE game_id="+str(game_id))
        df = pd.read_sql_query(query, self.__connection)
        return df.head(10)
        
test = Database("database/bowling.db")
test.print_all_frames(19)
