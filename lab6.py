import pygame
import sys

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
MOVE_ZONE = (173, 216, 230)  # зона перемещения
PLACE_ZONE = (128, 128, 192)  # зона размещения
GRID_COLOR = (0, 0, 0)  # цвет решётки

# Рассчет размеров игрового поля
BOARD_WIDTH = GRID_WIDTH * CELL_SIZE
BOARD_HEIGHT = GRID_HEIGHT * CELL_SIZE

# Позиция игрового поля (центрирование по горизонтали)
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 0  # в верхней части экрана

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Крестики-нолики с гравитацией")

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

def main():
    """Главный цикл программы"""
    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Заливка фона
        screen.fill(BACKGROUND)
        
        # Отрисовка игровой доски
        draw_game_board()
        
        # Обновление экрана
        pygame.display.flip()

if __name__ == "__main__":
    main()
