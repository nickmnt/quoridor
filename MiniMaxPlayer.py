from Player import Player
from copy import deepcopy


class MiniMaxPlayer(Player):
    MAX_DEPTH = 2
    INFINITY = float('inf')

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

    def evaluate(self, opponent: Player):
        self_distance, opponent_distance = self.bfs(opponent)
        # total_score = (5 * opponent_distance - self_distance) * (
        #     1 + self.walls_count / 2
        # )
        # return total_score
        # boxing strategy
        x1, y1 = self.get_position()
        x2, y2 = opponent.get_position()
        distance = abs(y2-y1) + abs(x2-x1)
        size = self.board.ROWS_NUM*self.board.COLS_NUM
        return (1.1*opponent_distance - self_distance + 0.5*self.walls_count*(y2)/self.board.COLS_NUM)

    def get_best_action(self, opponent):
        val, action = self.max(opponent)
        return action

    def max(self, opponent: "MiniMaxPlayer"):
        v = -self.INFINITY
        best_action = None
        
        
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            
            if self.is_winner():
                self.undo_last_action()
                action_value = self.INFINITY
                return action_value, action
            elif len(self.actions_logs) + len(opponent.actions_logs) >= self.MAX_DEPTH:
                action_value = self.evaluate(opponent)
            else:
                value, result_child = self.min(opponent)
                action_value = value
                
            if action_value > v:
                v = action_value
                best_action = action

            self.undo_last_action()

        return v, best_action

    def min(self, opponent: "MiniMaxPlayer"):
        v = self.INFINITY
        best_action = None

        for action in opponent.get_legal_actions(self):
            opponent.play(action, is_evaluating=True)
            
            if opponent.is_winner():
                opponent.undo_last_action()
                action_value = -self.INFINITY
                return action_value, action
            elif len(self.actions_logs) + len(opponent.actions_logs) >= self.MAX_DEPTH:
                action_value = self.evaluate(opponent)
            else:
                value, result_child = self.max(opponent)
                action_value = value
                
            if action_value < v:
                v = action_value
                best_action = action

            opponent.undo_last_action()

        return v, best_action