import pygame
import sys
import random

# 定数の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
SIZE = 600
BOARD_SIZE = 8
GRID_SIZE = SIZE // BOARD_SIZE

# Pygameの初期化
pygame.init()
screen = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("オセロゲーム")

class Othello:
    def __init__(self, mode):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        mid = BOARD_SIZE // 2
        self.board[mid - 1][mid - 1] = WHITE
        self.board[mid - 1][mid] = BLACK
        self.board[mid][mid - 1] = BLACK
        self.board[mid][mid] = WHITE
        self.turn = BLACK
        self.running = True
        self.mode = mode  # "single" or "multi"

    def draw_board(self):
        screen.fill(GREEN)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if self.board[x][y] is not None:
                    self.draw_stone(x, y, self.board[x][y])
                elif self.is_valid_move(x, y):
                    pygame.draw.circle(screen, YELLOW, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), 5)

    def draw_stone(self, x, y, color):
        pygame.draw.circle(screen, color, (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 4)

    def is_valid_move(self, x, y):
        if self.board[x][y] is not None:
            return False
        opponent = WHITE if self.turn == BLACK else BLACK
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nx, ny = x + dx, y + dy
            pieces_to_flip = []
            while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == opponent:
                pieces_to_flip.append((nx, ny))
                nx += dx
                ny += dy
            if pieces_to_flip and 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == self.turn:
                return True
        return False

    def flip_stones(self, x, y):
        opponent = WHITE if self.turn == BLACK else BLACK
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            pieces_to_flip = []
            nx, ny = x + dx, y + dy
            while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == opponent:
                pieces_to_flip.append((nx, ny))
                nx += dx
                ny += dy
            if pieces_to_flip and 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == self.turn:
                for px, py in pieces_to_flip:
                    self.board[px][py] = self.turn

    def has_valid_move(self):
        return any(self.is_valid_move(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE))

    def game_end(self):
        black_count = sum(row.count(BLACK) for row in self.board)
        white_count = sum(row.count(WHITE) for row in self.board)
        if black_count > white_count:
            return "Winner: Black"
        elif white_count > black_count:
            return "Winner: White"
        else:
            return "Draw"

    def next_move(self, x, y):
        if self.is_valid_move(x, y):
            self.board[x][y] = self.turn
            self.flip_stones(x, y)
            self.turn = WHITE if self.turn == BLACK else BLACK
        
        if not self.has_valid_move():
            self.turn = WHITE if self.turn == BLACK else BLACK
            if not self.has_valid_move():
                self.display_result(self.game_end())

    def cpu_move(self):
        valid_moves = [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE) if self.is_valid_move(x, y)]
        if valid_moves:
            x, y = random.choice(valid_moves)
            self.next_move(x, y)

    def display_result(self, result):
        font = pygame.font.Font(None, 74)
        text = font.render(result, True, YELLOW)
        screen.blit(text, text.get_rect(center=(SIZE // 2, SIZE // 2)))
        pygame.display.flip()
        pygame.time.wait(3000)
        self.running = False
        self.ask_restart()

    def ask_restart(self):
        font = pygame.font.Font(None, 50)
        restart_rect = pygame.Rect(SIZE // 4, SIZE // 2, 300, 50)
        quit_rect = pygame.Rect(SIZE // 4, SIZE // 1.5, 300, 50)
        
        while True:
            screen.fill(BLACK)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            color1 = YELLOW if restart_rect.collidepoint(mouse_x, mouse_y) else WHITE
            color2 = YELLOW if quit_rect.collidepoint(mouse_x, mouse_y) else WHITE
            text1 = font.render("Restart", True, color1)
            text2 = font.render("Quit", True, color2)
            screen.blit(text1, restart_rect.topleft)
            screen.blit(text2, quit_rect.topleft)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        main()
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

def select_mode():
    font = pygame.font.Font(None, 50)
    while True:
        screen.fill(BLACK)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        single_rect = pygame.Rect(SIZE // 4, SIZE // 3, 300, 50)
        multi_rect = pygame.Rect(SIZE // 4, SIZE // 2, 300, 50)
        color1 = YELLOW if single_rect.collidepoint(mouse_x, mouse_y) else WHITE
        color2 = YELLOW if multi_rect.collidepoint(mouse_x, mouse_y) else WHITE
        text1 = font.render("Single Player", True, color1)
        text2 = font.render("Two Players", True, color2)
        screen.blit(text1, single_rect.topleft)
        screen.blit(text2, multi_rect.topleft)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_rect.collidepoint(event.pos):
                    return "single"
                if multi_rect.collidepoint(event.pos):
                    return "multi"

def main():
    mode = select_mode()
    game = Othello(mode)
    
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= GRID_SIZE
                y //= GRID_SIZE
                game.next_move(x, y)
        
        if game.mode == "single" and game.turn == WHITE:
            game.cpu_move()
        
        game.draw_board()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
