from classes.game import Game
from classes.player import Player

player1 = Player('Louis')
player2 = Player('Carlo')
player3 = Player('Haris')
player4 = Player('Nico')

game = Game([player1, player2, player3, player4])

game.start()