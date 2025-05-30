import pygame
import sys
import time

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 550
CELL_SIZE = 50
GRID_WIDTH = 7  # ширина игрового поля в клетках
GRID_HEIGHT = 10  # высота игрового поля в клетках (4 верхние + 6 нижних)

# Цвета
BACKGROUND = (255, 255, 128)  # фон интерфейса
MOVE_ZONE = (173, 216, 230)   # зона перемещения
PLACE_ZONE = (128, 128, 192)  # зона размещения
GRID_COLOR = (0, 0, 0)        # цвет решётки
X_COLOR = (0, 0, 255)         # цвет крестиков
O_COLOR = (255, 0, 0)         # цвет ноликов
WIN_LINE_COLOR = (0, 255, 0)  # цвет выигрышной линии
BUTTON_COLOR = (0, 255, 0)    # цвет кнопки "Меню"

# Рассчет размеров игрового поля
BOARD_WIDTH = GRID_WIDTH * CELL_SIZE
BOARD_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Позиция игрового поля (центрирование по горизонтали)
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 0  # в верхней части экрана

# Позиция кнопки "Меню"
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40
BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = BOARD_HEIGHT + 10  # под игровым полем с небольшим отступом

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Крестики-нолики с гравитацией")

# Шрифты
font = pygame.font.SysFont(None, 36)

class Game:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        """Сброс состояния игры к начальному"""
        # Игровое поле (10 строк, 7 колонок)
        self.board = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Текущий игрок (синий начинает)
        self.current_player = 'blue'
        
        # Текущая падающая фигура
        self.current_piece = None
        
        # Ожидающее перемещение (влево/вправо)
        self.pending_move = 0
        
        # Состояние игры
        self.game_over = False
        self.winner = None
        self.winning_line = None
        
        # Время последнего перемещения фигуры
        self.last_move_time = time.time()
        
        # Запуск первого хода
        self.start_turn()
    
    def start_turn(self):
        """Начало хода игрока"""
        # Создаем новую падающую фигуру
        piece_type = 'X' if self.current_player == 'blue' else 'O'
        self.current_piece = {
            'type': piece_type,
            'row': 0,
            'col': GRID_WIDTH // 2  # центральная колонка
        }
        self.pending_move = 0  # сброс ожидающего перемещения
        self.last_move_time = time.time()
    
    def request_move(self, direction):
        """Запрос на перемещение фигуры влево/вправо"""
        if not self.current_piece or self.game_over:
            return
            
        # Запоминаем направление для применения при следующем падении
        self.pending_move = direction
    
    def update(self):
        """Обновление состояния игры"""
        if not self.current_piece or self.game_over:
            return
            
        # Проверка времени для перемещения фигуры вниз (каждые 2 секунды)
        current_time = time.time()
        if current_time - self.last_move_time < 2.0:
            return
            
        # Применяем ожидающее перемещение только если фигура в зоне перемещения
        if self.current_piece['row'] < 4:
            new_col = self.current_piece['col'] + self.pending_move
            
            # Проверяем, можно ли переместиться в новую колонку
            if 0 <= new_col < GRID_WIDTH:
                # Проверяем, свободна ли клетка снизу в новой колонке
                next_row = self.current_piece['row'] + 1
                if next_row < GRID_HEIGHT and self.board[next_row][new_col] is None:
                    # Перемещаем фигуру по диагонали
                    self.current_piece['col'] = new_col
                else:
                    # Если клетка снизу занята, перемещаем только вниз
                    pass
            
            # Сбрасываем ожидающее перемещение
            self.pending_move = 0
        
        # Перемещение фигуры вниз
        self.current_piece['row'] += 1
        self.last_move_time = current_time
        
        # Проверка достижения дна или другой фигуры
        row = self.current_piece['row']
        col = self.current_piece['col']
        
        # Если достигли дна
        if row >= GRID_HEIGHT - 1:
            self.place_piece()
            return
            
        # Если под фигурой есть другая фигура
        if self.board[row + 1][col] is not None:
            self.place_piece()
    
    def place_piece(self):
        """Фиксация фигуры на игровом поле"""
        if not self.current_piece:
            return
            
        # Фиксация фигуры на доске
        row = self.current_piece['row']
        col = self.current_piece['col']
        piece_type = self.current_piece['type']
        self.board[row][col] = piece_type
        
        # Проверка условий завершения игры
        self.check_game_over(row, col)
        
        # Если игра не завершена, передаем ход другому игроку
        if not self.game_over:
            self.current_player = 'red' if self.current_player == 'blue' else 'blue'
            self.start_turn()
        else:
            self.current_piece = None
    
    def check_game_over(self, last_row, last_col):
        """Проверка условий завершения игрового раунда"""
        # Условие 3: Фигура в зоне перемещения
        if last_row < 4:  # зона перемещения = верхние 4 строки
            self.game_over = True
            # Проиграл игрок, который поставил фигуру
            self.winner = 'red' if self.current_player == 'blue' else 'blue'
            return
            
        # Условие 1: Проверка 4 в ряд
        self.winning_line = self.check_win(last_row, last_col)
        if self.winning_line:
            self.game_over = True
            self.winner = self.current_player
            return
            
        # Условие 2: Зона размещения заполнена
        if self.is_placement_zone_full():
            self.game_over = True
            self.winner = 'draw'  # ничья
    
    def check_win(self, row, col):
        """Проверка наличия выигрышной комбинации из 4 фигур"""
        piece = self.board[row][col]
        if not piece:
            return None
            
        # Направления для проверки: горизонталь, вертикаль, две диагонали
        directions = [
            (0, 1),   # горизонталь
            (1, 0),   # вертикаль
            (1, 1),   # диагональ
            (1, -1)   # диагональ
        ]
        
        for dr, dc in directions:
            count = 1  # текущая фигура
            
            # Проверка в одном направлении
            r, c = row + dr, col + dc
            while 0 <= r < GRID_HEIGHT and 0 <= c < GRID_WIDTH and self.board[r][c] == piece:
                count += 1
                r += dr
                c += dc
                
            # Проверка в противоположном направлении
            r, c = row - dr, col - dc
            while 0 <= r < GRID_HEIGHT and 0 <= c < GRID_WIDTH and self.board[r][c] == piece:
                count += 1
                r -= dr
                c -= dc
                
            # Если нашли 4 в ряд
            if count >= 4:
                # Рассчитываем координаты линии для отрисовки
                start_row, start_col = row, col
                end_row, end_col = row, col
                
                # Идем в одном направлении
                r, c = row, col
                while 0 <= r < GRID_HEIGHT and 0 <= c < GRID_WIDTH and self.board[r][c] == piece:
                    start_row, start_col = r, c
                    r -= dr
                    c -= dc
                
                # Идем в противоположном направлении
                r, c = row, col
                while 0 <= r < GRID_HEIGHT and 0 <= c < GRID_WIDTH and self.board[r][c] == piece:
                    end_row, end_col = r, c
                    r += dr
                    c += dc
                
                return (start_row, start_col, end_row, end_col)
        
        return None
    
    def is_placement_zone_full(self):
        """Проверка заполненности зоны размещения"""
        for row in range(4, GRID_HEIGHT):  # зона размещения = строки 4-9
            for col in range(GRID_WIDTH):
                if self.board[row][col] is None:
                    return False
        return True

def draw_game_board():
    """Отрисовка игровой доски с зонами"""
    # Отрисовка зон
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            # Определение цвета зоны
            if row < 4:  # верхние 4 строки - зона перемещения
                color = MOVE_ZONE
            else:  # нижние 6 строк - зона размещения
                color = PLACE_ZONE
            
            # Расчет координат клетки
            x = BOARD_X + col * CELL_SIZE
            y = BOARD_Y + row * CELL_SIZE
            
            # Отрисовка клетки
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            
            # Отрисовка границ клетки
            pygame.draw.rect(screen, GRID_COLOR, (x, y, CELL_SIZE, CELL_SIZE), 1)

def draw_pieces(game):
    """Отрисовка фигур на игровом поле"""
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            piece = game.board[row][col]
            if piece:
                x = BOARD_X + col * CELL_SIZE
                y = BOARD_Y + row * CELL_SIZE
                
                if piece == 'X':
                    draw_x(x, y)
                else:  # 'O'
                    draw_o(x, y)

def draw_current_piece(game):
    """Отрисовка текущей падающей фигуры"""
    if not game.current_piece:
        return
        
    piece = game.current_piece
    row = piece['row']
    col = piece['col']
    
    # Проверка, что фигура в пределах поля
    if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
        x = BOARD_X + col * CELL_SIZE
        y = BOARD_Y + row * CELL_SIZE
        
        if piece['type'] == 'X':
            draw_x(x, y)
        else:  # 'O'
            draw_o(x, y)

def draw_x(x, y):
    """Отрисовка крестика"""
    offset = 10
    pygame.draw.line(screen, X_COLOR, 
                    (x + offset, y + offset), 
                    (x + CELL_SIZE - offset, y + CELL_SIZE - offset), 3)
    pygame.draw.line(screen, X_COLOR, 
                    (x + offset, y + CELL_SIZE - offset), 
                    (x + CELL_SIZE - offset, y + offset), 3)

def draw_o(x, y):
    """Отрисовка нолика"""
    center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
    radius = CELL_SIZE // 2 - 10
    pygame.draw.circle(screen, O_COLOR, center, radius, 3)

def draw_winning_line(game):
    """Отрисовка выигрышной линии"""
    if not game.winning_line:
        return
        
    start_row, start_col, end_row, end_col = game.winning_line
    
    # Расчет координат центров клеток
    start_x = BOARD_X + start_col * CELL_SIZE + CELL_SIZE // 2
    start_y = BOARD_Y + start_row * CELL_SIZE + CELL_SIZE // 2
    end_x = BOARD_X + end_col * CELL_SIZE + CELL_SIZE // 2
    end_y = BOARD_Y + end_row * CELL_SIZE + CELL_SIZE // 2
    
    # Отрисовка линии
    pygame.draw.line(screen, WIN_LINE_COLOR, (start_x, start_y), (end_x, end_y), 5)

def draw_menu_button(game):
    """Отрисовка кнопки 'Меню' при завершении игры"""
    if not game.game_over:
        return
        
    # Отрисовка прямоугольника кнопки
    pygame.draw.rect(screen, BUTTON_COLOR, 
                    (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    
    # Отрисовка текста кнопки
    text = font.render("Меню", True, GRID_COLOR)
    text_rect = text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, 
                                     BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

def main():
    """Главный цикл программы"""
    game = Game()
    
    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                if game.current_player == 'blue':
                    if event.key == pygame.K_a:  # A - влево
                        game.request_move(-1)
                    elif event.key == pygame.K_d:  # D - вправо
                        game.request_move(1)
                else:  # red player
                    if event.key == pygame.K_LEFT:  # Стрелка влево
                        game.request_move(-1)
                    elif event.key == pygame.K_RIGHT:  # Стрелка вправо
                        game.request_move(1)
        
        # Обновление состояния игры
        game.update()
        
        # Отрисовка
        screen.fill(BACKGROUND)
        draw_game_board()
        draw_pieces(game)
        draw_current_piece(game)
        draw_winning_line(game)
        draw_menu_button(game)
        
        # Обновление экрана
        pygame.display.flip()

if __name__ == "__main__":
    main()
