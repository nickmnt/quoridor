from AlphaBetaSearch import AlphaBetaPlayer
from EnhancedAbPlayer import EnhancedAbPlayer
from MiniMaxPlayer import MiniMaxPlayer
from MiniMaxPlayer import MiniMaxPlayer
from Board import Board
from time import sleep
from random import choice

def play_default():
    board = Board()

    white_player = MiniMaxPlayer("white", 4, 8, board)
    black_player = MiniMaxPlayer("black", 4, 0, board)

    walls_count = 0

    while True:
        #  play_default()
        action = white_player.get_best_action(opponent=black_player)
        white_player.play(action)
        board.print_map()
        print(
            f"white: {action}, evaluation: {white_player.evaluate(opponent=black_player):.2f}, left walls: {white_player.walls_count}"
        )
        if white_player.is_winner():
            print(f"White player just won with {white_player.moves_count} moves!")
            break
        if action.split("#")[0] == "wall":
            walls_count += 1
        sleep(0.3)
        action = black_player.get_best_action(opponent=white_player)
        black_player.play(action)
        board.print_map()
        print(
            f"black: {action}, evaluation: {black_player.evaluate(opponent=white_player):.2f}, left walls: {black_player.walls_count}"
        )
        if black_player.is_winner():
            print(f"Black player just won with {black_player.moves_count} moves!")
            break

        if action.split("#")[0] == "wall":
            walls_count += 1
        sleep(0.3)
    print(f"walls count {walls_count}")

if __name__ == "__main__":
    # play_default()
    board = Board()

    white_player = EnhancedAbPlayer("white", 4, 8, board)
    black_player = EnhancedAbPlayer("black", 4, 0, board)

    walls_count = 0

    while True:
        #  play_default()
        action = white_player.alpha_beta_search(opponent=black_player)
        white_player.play(action)
        board.print_map()
        print(
            f"white: {action}, evaluation: {white_player.evaluate(opponent=black_player):.2f}, left walls: {white_player.walls_count}"
        )
        if white_player.is_winner():
            print(f"White player just won with {white_player.moves_count} moves!")
            break
        if action.split("#")[0] == "wall":
            walls_count += 1
        #sleep(0.3)
        action = black_player.alpha_beta_search(opponent=white_player)
        black_player.play(action)
        board.print_map()
        print(
            f"black: {action}, evaluation: {black_player.evaluate(opponent=white_player):.2f}, left walls: {black_player.walls_count}"
        )
        if black_player.is_winner():
            print(f"Black player just won with {black_player.moves_count} moves!")
            break

        if action.split("#")[0] == "wall":
            walls_count += 1
        #sleep(0.3)
    print(f"walls count {walls_count}")

