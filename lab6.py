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
EXIT_BUTTON_COLOR = (255, 0, 0)  # цвет кнопки "Выход"
PLAY_BUTTON_COLOR = (0, 255, 0)  # цвет кнопки "Играть"
TEXT_BG_COLOR = (128, 64, 0)  # фон текста информации
TEXT_COLOR = (0, 0, 0)        # цвет текста

# Рассчет размеров игрового поля
BOARD_WIDTH = GRID_WIDTH * CELL_SIZE
BOARD_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Позиция игрового поля (центрирование по горизонтали)
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 0  # в верхней части экрана

# Позиция кнопок
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 40
MENU_BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
PLAY_BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2 - 120
EXIT_BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2 + 120
MENU_BUTTON_Y = BOARD_HEIGHT + 10  # в игровом раунде
PLAY_BUTTON_Y = 420
EXIT_BUTTON_Y = 420

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Крестики-нолики с гравитацией")

# Шрифты
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 48)

class Button:
    """Класс для создания кнопок"""
    def __init__(self, x, y, width, height, text, color, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color or color
        self.is_hovered = False
        
    def draw(self, surface):
        """Отрисовка кнопки"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        """Проверка наведения курсора"""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def check_click(self, pos, event):
        """Проверка клика по кнопке"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

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
            
        # Проверка времени для перемещения фигуры вниз
        current_time = time.time()
        if current_time - self.last_move_time < 1.0:
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

def draw_main_menu(blue_score, red_score, last_winner, play_button, exit_button):
    """Отрисовка главного меню"""
    # Информация о победителе последнего раунда
    winner_text = "Последний раунд: "
    if last_winner == 'blue':
        winner_text += "Победили крестики!"
    elif last_winner == 'red':
        winner_text += "Победили нолики!"
    elif last_winner == 'draw':
        winner_text += "Ничья!"
    else:
        winner_text += "Еще не играли"
    
    winner_surf = font.render(winner_text, True, TEXT_COLOR)
    winner_rect = winner_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
    
    # Фон для текста
    bg_rect = pygame.Rect(
        winner_rect.left - 10, 
        winner_rect.top - 5,
        winner_rect.width + 20,
        winner_rect.height + 10
    )
    pygame.draw.rect(screen, TEXT_BG_COLOR, bg_rect, border_radius=5)
    pygame.draw.rect(screen, TEXT_COLOR, bg_rect, 2, border_radius=5)
    screen.blit(winner_surf, winner_rect)
    
    # Счет игроков
    score_text = font.render("Счёт", True, TEXT_COLOR)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 230))

    score_text2 = font.render(":", True, TEXT_COLOR)
    score_rect2 = score_text2.get_rect(center=(SCREEN_WIDTH // 2, 270))
    
    blue_score_text = font.render(f"{blue_score}", True, X_COLOR)
    blue_score_rect = blue_score_text.get_rect(center=(SCREEN_WIDTH // 2 - 25, 270))
    
    red_score_text = font.render(f"{red_score}", True, O_COLOR)
    red_score_rect = red_score_text.get_rect(center=(SCREEN_WIDTH // 2 + 25, 270))
    
    # Фон для счета
    score_bg_rect = pygame.Rect(
        blue_score_rect.left - 20,
        score_rect.top - 10,
        blue_score_rect.width + 50 + 40,
        score_rect.height + 40 + 20
    )
    pygame.draw.rect(screen, TEXT_BG_COLOR, score_bg_rect, border_radius=5)
    pygame.draw.rect(screen, TEXT_COLOR, score_bg_rect, 2, border_radius=5)
    
    screen.blit(score_text, score_rect)
    screen.blit(score_text2, score_rect2)
    screen.blit(blue_score_text, blue_score_rect)
    screen.blit(red_score_text, red_score_rect)

    # Отрисовка кнопок
    play_button.draw(screen)
    exit_button.draw(screen)

def main():
    # Состояния приложения
    in_game = False
    game = None
    
    # Счет игроков
    blue_score = 0
    red_score = 0
    last_winner = None
    
    # Создание кнопок
    play_button = Button(
        PLAY_BUTTON_X, PLAY_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 
        "Играть", PLAY_BUTTON_COLOR, (100, 255, 100)
    )
    
    exit_button = Button(
        EXIT_BUTTON_X, EXIT_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 
        "Выход", EXIT_BUTTON_COLOR, (255, 100, 100)
    )
    
    menu_button = Button(
        MENU_BUTTON_X, MENU_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 
        "Меню", BUTTON_COLOR, (100, 255, 100)
    )

    # Главный цикл программы
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if in_game:
                # Обработка нажатий клавиш в игровом раунде
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
                
                # Обработка кнопки "Меню" после завершения игры
                if game.game_over and menu_button.check_click(mouse_pos, event):
                    # Обновляем счет
                    if game.winner == 'blue':
                        blue_score += 1
                        last_winner = 'blue'
                    elif game.winner == 'red':
                        red_score += 1
                        last_winner = 'red'
                    elif game.winner == 'draw':
                        last_winner = 'draw'
                    
                    # Возвращаемся в главное меню
                    in_game = False
            else:
                # Обработка кнопок в главном меню
                if play_button.check_click(mouse_pos, event):
                    # Начинаем новую игру
                    game = Game()
                    in_game = True
                
                if exit_button.check_click(mouse_pos, event):
                    pygame.quit()
                    sys.exit()
        
        # Обновление состояния игры
        if in_game:
            game.update()
        
        # Отрисовка
        screen.fill(BACKGROUND)
        
        if in_game:
            # Отрисовка игрового раунда
            draw_game_board()
            draw_pieces(game)
            draw_current_piece(game)
            draw_winning_line(game)
            
            # Отрисовка кнопки "Меню" при завершении игры
            if game.game_over:
                menu_button.check_hover(mouse_pos)
                menu_button.draw(screen)
        else:
            # Отрисовка главного меню
            play_button.check_hover(mouse_pos)
            exit_button.check_hover(mouse_pos)
            draw_main_menu(blue_score, red_score, last_winner, play_button, exit_button)
        
        # Обновление экрана
        pygame.display.flip()

if __name__ == "__main__":
    main()
