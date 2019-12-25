class Game:
    
    top_score = 0

    def __init__(self, player_name):
        self.player_name = player_name
        
    @staticmethod
    def show_help():
        print("幫助資訊 : 讓殭屍進入大門")

    @classmethod
    def show_top_score(cls):
        print("歷史紀錄 %d" % cls.top_score)

    def start_game(self):
        print("%s start to game..." % self.player_name)


Game.show_help()
Game.show_top_score()
newGame = Game("shock Lee")
newGame.start_game()

