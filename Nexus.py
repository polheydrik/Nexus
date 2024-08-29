import pygame
import sys
import random
import copy

# Constants
BOARD_SIZE = 6
CELL_SIZE = 50
SCORE_HEIGHT = 30
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + SCORE_HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BACKGROUND_COLOR = (128, 128, 128)


class Nexus:
    def __init__(self):
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'W'

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'B' if self.current_player == 'W' else 'W'
            return True
        return False

    def get_available_moves(self):
        return [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == ' ']

    def is_board_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def count_connections(self, player):
        count = 0

        # Count horizontal connections
        for j in range(BOARD_SIZE):
            connected = False
            one_dot = False
            for i in range(BOARD_SIZE):
                if self.board[i][j] == player:
                    if not one_dot:
                        one_dot = True
                    elif connected:
                        continue
                    else:
                        count += 1
                        connected = True
                else:
                    connected = False
                    one_dot = False

        # Count vertical connections
        for i in range(BOARD_SIZE):
            connected = False
            one_dot = False
            for j in range(BOARD_SIZE):
                if self.board[i][j] == player:
                    if not one_dot:
                        one_dot = True
                    elif connected:
                        continue
                    else:
                        count += 1
                        connected = True
                else:
                    connected = False
                    one_dot = False

        return count


def draw_board(screen, game):
    screen.fill(BACKGROUND_COLOR)

    # Draw score
    font = pygame.font.Font(None, 24)
    white_score = game.count_connections('W')
    black_score = game.count_connections('B')
    score_text = f"White: {white_score}   Black: {black_score}"
    text_surface = font.render(score_text, True, WHITE)
    screen.blit(text_surface, (10, 5))

    # Draw board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            pygame.draw.rect(screen, WHITE, (i * CELL_SIZE, j * CELL_SIZE + SCORE_HEIGHT, CELL_SIZE, CELL_SIZE), 1)
            if game.board[i][j] == 'W':
                pygame.draw.circle(screen, WHITE,
                                   (i * CELL_SIZE + CELL_SIZE // 2, j * CELL_SIZE + SCORE_HEIGHT + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 5)
            elif game.board[i][j] == 'B':
                pygame.draw.circle(screen, BLACK,
                                   (i * CELL_SIZE + CELL_SIZE // 2, j * CELL_SIZE + SCORE_HEIGHT + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - 5)
    pygame.display.flip()


class NexusAI:
    def __init__(self, player, depth=3):
        self.player = player
        self.opponent = 'W' if player == 'B' else 'B'
        self.depth = depth

    def make_move(self, game):
        _, best_move = self.minimax(game, self.depth, float('-inf'), float('inf'), True)
        return best_move

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.is_board_full():
            return self.evaluate_board(game), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in game.get_available_moves():
                new_game = self.simulate_move(game, move, self.player)
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in game.get_available_moves():
                new_game = self.simulate_move(game, move, self.opponent)
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def simulate_move(self, game, move, player):
        new_game = copy.deepcopy(game)
        new_game.make_move(move[0], move[1])
        new_game.current_player = 'B' if player == 'W' else 'W'
        return new_game

    def evaluate_board(self, game):
        ai_score = game.count_connections(self.player)
        opponent_score = game.count_connections(self.opponent)
        return ai_score - opponent_score + self.evaluate_potential(game)

    def evaluate_potential(self, game):
        ai_potential = self.count_potential_connections(game, self.player)
        opponent_potential = self.count_potential_connections(game, self.opponent)
        return (ai_potential - opponent_potential) * 0.25

    def count_potential_connections(self, game, player):
        potential = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if game.board[i][j] == ' ':
                    # Check horizontal
                    if (j > 0 and game.board[i][j - 1] == player) or (
                            j < BOARD_SIZE - 1 and game.board[i][j + 1] == player):
                        potential += 1
                    # Check vertical
                    if (i > 0 and game.board[i - 1][j] == player) or (
                            i < BOARD_SIZE - 1 and game.board[i + 1][j] == player):
                        potential += 1
        return potential


def display_result(screen, result_text):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(result_text, True, RED)
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text_surface, text_rect)

    retry_font = pygame.font.Font(None, 22)
    retry_text = retry_font.render("Press SPACE to play again or ESC to quit", True, RED)
    retry_rect = retry_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
    screen.blit(retry_text, retry_rect)

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Nexus")

    while True:
        game = Nexus()
        ai = NexusAI('B', depth=2)  # AI plays as Black

        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and game.current_player == 'W':
                    x, y = pygame.mouse.get_pos()
                    row, col = x // CELL_SIZE, (y - SCORE_HEIGHT) // CELL_SIZE
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        if game.make_move(row, col):
                            draw_board(screen, game)
                            pygame.time.wait(300)

            if game.current_player == 'B':
                ai_move = ai.make_move(game)
                if ai_move:
                    game.make_move(ai_move[0], ai_move[1])
                    draw_board(screen, game)
                    pygame.time.wait(300)

            draw_board(screen, game)

            if game.is_board_full():
                game_over = True
                white_score = game.count_connections('W')
                black_score = game.count_connections('B')
                print(f"Game over!")
                print(f"White's score: {white_score}")
                print(f"Black's score: {black_score}")
                if white_score > black_score:
                    result_text = "White wins!"
                elif black_score > white_score:
                    result_text = "Black wins!"
                else:
                    result_text = "It's a tie!"

                display_result(screen, result_text)

        # Wait for player decision to retry or quit
        waiting_for_decision = True
        while waiting_for_decision:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting_for_decision = False  # Start a new game
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()


if __name__ == '__main__':
    main()