import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


import sys
from typing import NoReturn
from const import *
from game.position import Position
from game.person import Person
from game.player import Player
from game.computer import Computer
from solvers.weak_minimax import weak_minimax_find_move
from solvers.minimax import minimax_find_move
from solvers.alpha_beta import alpha_beta_find_move
from game.reset import ResetButton
import pygame


class Game:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2

        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")
        icon_img = pygame.image.load("assets/board.png")
        pygame.display.set_icon(icon_img)
        self.SCREEN = pygame.display.set_mode((600, 400), pygame.RESIZABLE)

        reset_img = pygame.transform.smoothscale(pygame.image.load("assets/reset.png"), [20, 20])
        self.reset_button = ResetButton(
            reset_img,
            lambda: (
                pygame.display.get_surface().get_width() // 2,
                pygame.display.get_surface().get_height() - MARGIN_SIZE_Y // 2,
            ),
        )
        self.ui_group = pygame.sprite.Group()
        self.ui_group.add(self.reset_button)

        self.position = Position()

        self.updated_block_size = (
            lambda: (
                min(
                    self.SCREEN.get_height() - 2 * MARGIN_SIZE_Y,
                    self.SCREEN.get_width() - 2 * MARGIN_SIZE_X,
                )
            )
            // BOARD_SIZE
        )
        self.grid_block_size = self.updated_block_size()
        self.winner = None

    def run_game(self) -> NoReturn:
        do_reset = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.VIDEORESIZE:
                    self.grid_block_size = self.updated_block_size()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        do_reset = self.reset_button.check_mouse_collide()
                        board_value = self.get_board_value(pygame.mouse.get_pos())
                        if (
                            self.winner is not None
                            or board_value is None
                            or not self.position.can_play(board_value)
                        ):
                            continue
                        self.position.add_move(board_value)
                        if (winner := self.position.check_game_ends()) is not None:
                            self.winner = winner
            self.ui_group.update()
            self.draw_display()
            self.play_moves()
            if do_reset:
                do_reset = False
                self.reset()

    def reset(self):
        self.position = Position()
        self.winner = None

    def play_moves(self):
        if self.position.check_game_ends() is not None:
            return
        player = self.player1
        if self.position.move_index % 2 == 1:
            player = self.player2
        if isinstance(player, Computer):
            self.draw_display(waiting=True)
            move = player.play(self.position)
            pygame.event.clear()
            self.position.add_move(move)
            if self.position.check_game_ends() is not None:
                self.winner = self.position.check_game_ends()

    def get_start_coord(self):
        start_x = (self.SCREEN.get_width() - BOARD_SIZE * self.grid_block_size) // 2
        start_y = (self.SCREEN.get_height() - BOARD_SIZE * self.grid_block_size) // 2
        return start_x, start_y

    def draw_x(self, center_pos: tuple[int, int]):
        x, y = center_pos
        offset = self.grid_block_size // 2 - PIECE_MARGIN
        pygame.draw.line(
            self.SCREEN,
            X_COLOR,
            [x - offset, y - offset],
            [x + offset, y + offset],
            PIECE_WIDTH,
        )
        pygame.draw.line(
            self.SCREEN,
            X_COLOR,
            [x + offset, y - offset],
            [x - offset, y + offset],
            PIECE_WIDTH,
        )

    def draw_o(self, center_pos: tuple[int, int]):
        pygame.draw.circle(
            self.SCREEN, O_COLOR, center_pos, self.grid_block_size // 2 - PIECE_MARGIN, PIECE_WIDTH
        )

    def get_screen_value(self, board_val: int):
        start_x, start_y = self.get_start_coord()
        y = (board_val // BOARD_SIZE) * self.grid_block_size + self.grid_block_size // 2 + start_y
        x = (board_val % BOARD_SIZE) * self.grid_block_size + self.grid_block_size // 2 + start_x
        return x, y

    def get_board_value(self, position: tuple[int, int]):
        x, y = position
        start_x, start_y = self.get_start_coord()
        end_x = start_x + BOARD_SIZE * self.grid_block_size
        end_y = start_y + BOARD_SIZE * self.grid_block_size
        if x < start_x or y < start_y:
            return None
        if x >= end_x or y >= end_y:
            return None
        board_x = (x - start_x) // self.grid_block_size
        board_y = (y - start_y) // self.grid_block_size
        return board_y * BOARD_SIZE + board_x

    def blit_top_text(self, text: str):
        font = pygame.font.Font(None, 20)
        img = font.render(text, True, "black")
        center_x = self.SCREEN.get_width() // 2
        center_y = MARGIN_SIZE_Y // 2
        offset_x = center_x - img.get_width() // 2
        self.SCREEN.blit(img, (offset_x, center_y))

    def draw_display(self, waiting=False) -> None:
        self.SCREEN.fill(BG_COLOR)

        # region: draw grid
        start_x, start_y = self.get_start_coord()
        for delta in range(1, BOARD_SIZE):
            delta *= self.grid_block_size
            pygame.draw.line(
                self.SCREEN,
                GRID_COLOR,
                (start_x + delta, start_y),
                (start_x + delta, start_y + BOARD_SIZE * self.grid_block_size),
                width=GRID_SIZE,
            )
        for delta in range(1, BOARD_SIZE):
            delta *= self.grid_block_size
            pygame.draw.line(
                self.SCREEN,
                GRID_COLOR,
                (start_x, start_y + delta),
                (start_x + BOARD_SIZE * self.grid_block_size, start_y + delta),
                width=GRID_SIZE,
            )
        # endregion

        # region: draw the x and o values.
        for i, move in self.position.moves():
            pos = self.get_screen_value(i)
            if move == Cell.PLAYER1:
                self.draw_x(pos)
            else:
                self.draw_o(pos)
        # endregion

        if waiting:
            message = "Waiting for player %s to make a move"
            message %= "1" if self.position.move_index % 2 == 1 else "2"
            self.blit_top_text(message)

        if self.winner is not None:
            message = (
                "It's a draw."
                if self.winner == DRAW
                else "Player %s won." % ("1" if self.winner == Cell.PLAYER1 else "2")
            )
            self.blit_top_text(message)
            self.ui_group.draw(self.SCREEN)

        pygame.display.update()


if __name__ == "__main__":
    p1 = Computer(weak_minimax_find_move)
    p2 = Person()
    Game(p1, p2).run_game()
