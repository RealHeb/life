"""
Нажатие левой мыши - добавление жизни на заполненной клетке или удаление её на заполненной,
возможно только когда игра на паузе.

Пробел - остановка игры/запуск игры.

Колесо мыши - регулирует скорость игры, вверх делает игру быстрее, вниз - медленнее.
"""


import pygame
import time
from copy import deepcopy


class Board:
    # Доску взял из старых задач, когда в Яндекс.Лицее pygame проходили.
    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.size = 20

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is None:
            return
        if self.board[cell[0]][cell[1]] == 1:
            self.on_click(cell, 0)
        else:
            self.on_click(cell, 1)

    def get_cell(self, mouse_pos):
        for y in range(self.height):
            for x in range(self.width):
                rect1 = pygame.Rect(x * self.size + self.left, y * self.size + self.top, self.size, self.size)
                if rect1.collidepoint(mouse_pos):
                    return y, x
        return None

    def on_click(self, pos, value):
        self.board[pos[0]][pos[1]] = value

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, 'blue',
                                     (x * self.size + self.left, y * self.size + self.top, self.size, self.size))
                pygame.draw.rect(screen, 'white',
                                 (x * self.size + self.left, y * self.size + self.top, self.size, self.size), 1)


def life(board):
    # Обработчик доски. Вычисляет новое расположение клеток на доске
    new_board = deepcopy(board)
    for row in range(len(board)):
        for col in range(len(board[row])):
            cell_neighbours = 0
            # 8 if, нехорошо, но работает
            if len(board) != row + 1:
                cell_neighbours += board[row + 1][col]  # Снизу
            if len(board[row]) != col + 1:
                cell_neighbours += board[row][col + 1]  # Справа
            if len(board[row]) != col + 1 and len(board) != row + 1:
                cell_neighbours += board[row + 1][col + 1]  # Справа-снизу
            if 0 != col and row != 0:
                cell_neighbours += board[row - 1][col - 1]  # Слева-сверху
            if col != 0:
                cell_neighbours += board[row][col - 1]  # Слева
            if row != 0:
                cell_neighbours += board[row - 1][col]  # Сверху
            if row != 0 and len(board[row]) != col + 1:
                cell_neighbours += board[row - 1][col + 1]  # Справа-сверху
            if col != 0 and len(board) != row + 1:
                cell_neighbours += board[row + 1][col - 1]  # Слева-снизу
            # Вычисление
            if cell_neighbours == 3:
                new_board[row][col] = 1
            if cell_neighbours > 3 or cell_neighbours < 2:
                new_board[row][col] = 0
    return new_board


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

running = True
activated = False
board = Board(24, 24)
speed = 3
last_activation = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not activated:
                board.get_click(event.pos)
            if event.button == 4:
                speed += 0.5
            elif event.button == 5 and speed != 0.5:
                speed -= 0.5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                activated = not activated
    if activated and time.time() - last_activation >= 1 / speed:
        board.board = life(board.board)
        last_activation = time.time()
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
