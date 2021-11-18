from os import terminal_size
from Player import Player
from Board import Board
from copy import deepcopy

class EnhancedAbPlayer(Player): 
    MAX_DEPTH = 2
    INFINITY = 9999
    table = {}

    def alpha_beta_search(self, opponent: 'EnhancedAbPlayer'):
        v, action = self.ab(opponent, -self.INFINITY, self.INFINITY, self.MAX_DEPTH, True)
        return action

    def store(self, depth, score, flag, move):
        self.table[self.board.to_string()] = (depth, score, flag, move) 

    def retrieve(self):
        if self.board.to_string() in self.table:
            return self.table[self.board.to_string()]
        else:
            return None


    def ab(self, opponent: "EnhancedAbPlayer", alpha, beta, depth, is_max: bool):
        multiplier = 1 if is_max else -1
        #cache = self.retrieve()

        # if cache is not None:
        #     height, score, flag, move = cache
        #     if height >= depth:
        #         if flag == 'valid':
        #             return score, move
        #         if flag == 'lbound':
        #             alpha = max(alpha, score)
        #         if flag == 'ubound':
        #             beta = min(beta, score)
        #         if alpha >= beta:
        #             return score, move

        # if cache is not None:
        #     height, score, flag, move = cache
        #     if height >= 0:    
        #         if is_max:
        #             self.play(move, True)
        #             score, a = self.ab(opponent, -beta,-alpha, depth-1, not is_max, move)
        #             score = -score
        #             self.undo_last_action()
        #         else:
        #             opponent.play(move, True)
        #             score, a = self.ab(opponent, -beta,-alpha, depth-1, not is_max, move)
        #             score = -score
        #             opponent.undo_last_action()

        #         if(score >= beta):
        #             flag = 'valid'
        #             if score <= alpha:
        #                 flag = 'ubound'
        #             if score >= beta:
        #                 flag = 'lbound'
        #             if height <= depth:
        #                 self.store(depth, score, flag, move)
        #             return score, move
        score = -self.INFINITY
        move = None


        if is_max:
            actions = self.get_legal_actions(opponent)
        else:
            actions = opponent.get_legal_actions(self)
        
        for action in actions:
            # if cache is None or action != cache[3]: #cache[3] = move
                if is_max:
                    self.play(action, is_evaluating=True)
                    if self.is_winner():
                        value = self.INFINITY
                        self.undo_last_action()
                        return value, action
                    elif len(self.actions_logs) + len(opponent.actions_logs) >= self.MAX_DEPTH:
                        value = self.evaluate(opponent)
                    else:
                        value, a = self.ab(opponent, -beta, -alpha, depth-1, False)
                        value = -value
                    
                    self.undo_last_action()

                else:
                    opponent.play(action, is_evaluating=True)
                    if opponent.is_winner():
                        value = self.INFINITY
                    elif len(self.actions_logs) + len(opponent.actions_logs) >= self.MAX_DEPTH:
                        value = -self.evaluate(opponent)
                    else:
                        value, a = self.ab(opponent, -beta, -alpha, depth-1, True)
                        value = -value
                    
                    opponent.undo_last_action()

                if value > score:
                    score = value
                    move = action
                    alpha = max(alpha, score)
                    if score >= beta:
                        break

                    # if score >= beta:
                    #     # flag = 'valid'
                    #     # if score <= alpha:
                    #     #     flag = 'ubound'
                    #     # if score >= beta:
                    #     #     flag = 'lbound'
                    #     # self.store(depth, score, flag, move)
                    #     return score, move

        # flag = 'valid'
        # if score <= alpha:
        #     flag = 'ubound'
        # if score >= beta:
        #     flag = 'lbound'
        # self.store(depth, score, flag, move)
        return score, move

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

        return ((1+y2/self.board.ROWS_NUM*2)*opponent_distance - 2*self_distance
            + 0.5*self.walls_count*(self.board.ROWS_NUM-y2)/self.board.ROWS_NUM
            - opponent.walls_count*(y1)/self.board.ROWS_NUM)