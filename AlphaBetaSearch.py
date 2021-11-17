from os import terminal_size
from Player import Player
from copy import deepcopy

class AlphaBetaPlayer(Player): 
    INFINITY = 9999
    MAX_DEPTH = 2

    def alpha_beta_search(self, opponent: Player):
        v = self.max_value(opponent, float('-inf'), float('inf'))
        return self.last_action

    def terminal_test(self, opponent: Player):
        if self.is_winner() or opponent.is_winner():
            return True

        return False

    def utility(self, opponent: Player):
        if self.is_winner():
            return 1
        elif opponent.is_winner():
            return -1

    def min_value(self, opponent: Player, alpha, beta):
        if len(self.actions_logs) + len(opponent.actions_logs) > self.MAX_DEPTH:
            return opponent.evaluate(self)
        if self.terminal_test(opponent):
            return opponent.evaluate(self)

        v = float('inf')
        for a in opponent.get_legal_actions(self):
            opponent.play(a, is_evaluating=True)
            v = min(v, self.max_value(opponent, alpha, beta))
            opponent.undo_last_action()
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
        

    def max_value(self, opponent: Player, alpha, beta):
        if len(self.actions_logs) + len(opponent.actions_logs) > self.MAX_DEPTH:
            return self.evaluate(opponent)
        if self.terminal_test(opponent):
            return self.evaluate(opponent)

        v = float('-inf')
        for a in self.get_legal_actions(opponent):
            self.play(a, is_evaluating=True)
            result = self.min_value(opponent, alpha, beta)
            if result > v:
                v = result
                self.last_action = a
            self.undo_last_action()
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def bfs(self, opponent: Player):
        for player in [self, opponent]:
            destination = (
                self.board.get_white_goal_pieces()
                if player.color == "white"
                else self.board.get_black_goal_pieces()
            )
            visited = {}
            distances = {}
            for row in self.board.map:
                for piece in row:
                    visited[piece] = False
                    distances[piece] = self.INFINITY

            player_piece = self.board.get_piece(*player.get_position())

            queue = []
            queue.append(player_piece)
            visited[player_piece] = True
            distances[player_piece] = 0

            while queue:
                piece = queue.pop(0)

                for i in self.board.get_piece_neighbors(piece):
                    if visited[i] == False:
                        distances[i] = distances[piece] + 1
                        visited[i] = True
                        queue.append(i)

            min_distance = self.INFINITY
            for piece, dist in distances.items():
                if piece in destination:
                    if dist < min_distance:
                        min_distance = dist

            if player == self:
                self_distance = min_distance
            else:
                opponent_distance = min_distance

        return self_distance, opponent_distance

    def evaluate(self, opponent):
        self_distance, opponent_distance = self.bfs(opponent)
        total_score = (5 * opponent_distance - self_distance) * (
            1 + self.walls_count / 2
        )
        return total_score