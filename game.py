
import random
import sys

import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HUD_HEIGHT = 60
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - HUD_HEIGHT) // CELL_SIZE
FPS = 60

BACKGROUND = (18, 20, 30)
BOARD_COLOR = (27, 31, 44)
GRID_COLOR = (37, 42, 56)
WHITE = (240, 242, 248)
MUTED = (170, 177, 194)
PURPLE = (170, 90, 235)
PURPLE_LIGHT = (204, 150, 250)
GREEN = (103, 220, 135)
RED = (245, 91, 105)
ORANGE = (255, 157, 76)
OBSTACLE_COLOR = (105, 113, 132)

KEY_DIRECTIONS = {
    pygame.K_UP: (0, -1),
    pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_d: (1, 0),
}


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("arial", 54, bold=True)
        self.font = pygame.font.SysFont("arial", 27)
        self.small_font = pygame.font.SysFont("arial", 19)
        self.state = "welcome"
        self.running = True
        self.reset_board()

    def reset_board(self):
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = [center, (center[0] - 1, center[1]), (center[0] - 2, center[1])]
        self.direction = (1, 0)
        self.score = 0
        self.food_eaten = 0
        self.obstacles = []
        self.enemy = None
        self.food = None
        self.snake_timer = 0
        self.enemy_timer = 0
        self.won = False

        self.enemy = self.random_empty_cell()
        self.food = self.random_empty_cell()
        for _ in range(3):
            self.add_obstacle()

    def random_empty_cell(self):
        occupied = set(self.snake) | set(self.obstacles)
        if self.enemy is not None:
            occupied.add(self.enemy)
        if getattr(self, "food", None) is not None:
            occupied.add(self.food)

        available = [
            (x, y)
            for y in range(GRID_HEIGHT)
            for x in range(GRID_WIDTH)
            if (x, y) not in occupied
        ]
        return random.choice(available) if available else None

    def add_obstacle(self):
        position = self.random_empty_cell()
        if position is not None:
            self.obstacles.append(position)

    def start_game(self):
        self.reset_board()
        self.state = "playing"

    def set_direction(self, new_direction):
        if new_direction != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction

    def handle_key(self, key):
        if key == pygame.K_ESCAPE or key == pygame.K_q:
            self.running = False
            return

        if self.state == "welcome":
            self.start_game()
        elif self.state == "playing":
            if key == pygame.K_SPACE:
                self.state = "paused"
            elif key in KEY_DIRECTIONS:
                self.set_direction(KEY_DIRECTIONS[key])
        elif self.state == "paused":
            if key == pygame.K_SPACE:
                self.state = "playing"
        elif self.state == "gameover":
            if key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                self.start_game()

    def snake_interval(self):
        level = self.score // 30
        return max(75, 150 - level * 8)

    def enemy_interval(self):
        level = self.score // 30
        return max(100, 520 - level * 45)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        next_head = (head_x + self.direction[0], head_y + self.direction[1])
        x, y = next_head
        growing = next_head == self.food

        outside_board = not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT)
        body_to_check = self.snake if growing else self.snake[:-1]
        if (
            outside_board
            or next_head in body_to_check
            or next_head in self.obstacles
            or next_head == self.enemy
        ):
            self.state = "gameover"
            return

        self.snake.insert(0, next_head)
        if growing:
            self.score += 10
            self.food_eaten += 1
            if self.food_eaten % 3 == 0:
                self.add_obstacle()
            self.food = self.random_empty_cell()
            if self.food is None:
                self.won = True
                self.state = "gameover"
        else:
            self.snake.pop()

    def move_enemy(self):
        x, y = self.enemy
        candidates = [
            (x + dx, y + dy)
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0))
        ]
        candidates = [
            position
            for position in candidates
            if 0 <= position[0] < GRID_WIDTH
            and 0 <= position[1] < GRID_HEIGHT
            and position not in self.obstacles
            and position != self.food
        ]
        if not candidates:
            return

        self.enemy = random.choice(candidates)
        if self.enemy in self.snake:
            self.state = "gameover"

    def update(self, elapsed_ms):
        self.snake_timer += elapsed_ms
        self.enemy_timer += elapsed_ms

        while self.state == "playing" and self.snake_timer >= self.snake_interval():
            self.snake_timer -= self.snake_interval()
            self.move_snake()

        while self.state == "playing" and self.enemy_timer >= self.enemy_interval():
            self.enemy_timer -= self.enemy_interval()
            self.move_enemy()

    def draw_text(self, text, font, color, center):
        image = font.render(text, True, color)
        self.screen.blit(image, image.get_rect(center=center))

    def cell_rect(self, cell, inset=2):
        x, y = cell
        return pygame.Rect(
            x * CELL_SIZE + inset,
            HUD_HEIGHT + y * CELL_SIZE + inset,
            CELL_SIZE - inset * 2,
            CELL_SIZE - inset * 2,
        )

    def draw_board(self):
        self.screen.fill(BACKGROUND)
        pygame.draw.rect(
            self.screen,
            BOARD_COLOR,
            (0, HUD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - HUD_HEIGHT),
        )

        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(
                self.screen, GRID_COLOR, (x, HUD_HEIGHT), (x, SCREEN_HEIGHT)
            )
        for y in range(HUD_HEIGHT, SCREEN_HEIGHT + 1, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

        score_image = self.small_font.render(f"Puntos: {self.score}", True, WHITE)
        level_image = self.small_font.render(
            f"Nivel: {self.score // 30 + 1}", True, WHITE
        )
        controls_image = self.small_font.render(
            "Flechas/WASD: mover    Espacio: pausa", True, MUTED
        )
        self.screen.blit(score_image, (18, 18))
        self.screen.blit(level_image, (175, 18))
        self.screen.blit(
            controls_image,
            controls_image.get_rect(midright=(SCREEN_WIDTH - 18, 30)),
        )

        for obstacle in self.obstacles:
            pygame.draw.rect(
                self.screen, OBSTACLE_COLOR, self.cell_rect(obstacle), border_radius=4
            )
        if self.food is not None:
            pygame.draw.circle(
                self.screen,
                GREEN,
                self.cell_rect(self.food, 3).center,
                CELL_SIZE // 2 - 3,
            )
        if self.enemy is not None:
            pygame.draw.rect(
                self.screen, ORANGE, self.cell_rect(self.enemy), border_radius=5
            )
            enemy_pixel_x = self.enemy[0] * CELL_SIZE
            enemy_pixel_y = HUD_HEIGHT + self.enemy[1] * CELL_SIZE
            pygame.draw.circle(
                self.screen, WHITE, (enemy_pixel_x + 7, enemy_pixel_y + 7), 2
            )
            pygame.draw.circle(
                self.screen, WHITE, (enemy_pixel_x + 13, enemy_pixel_y + 7), 2
            )

        for index, segment in enumerate(self.snake):
            color = PURPLE_LIGHT if index == 0 else PURPLE
            pygame.draw.rect(
                self.screen, color, self.cell_rect(segment), border_radius=5
            )

    def draw_overlay(self, title, lines, title_color=WHITE):
        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((8, 10, 18, 205))
        self.screen.blit(shade, (0, 0))
        self.draw_text(title, self.title_font, title_color, (SCREEN_WIDTH // 2, 205))
        for index, line in enumerate(lines):
            self.draw_text(
                line,
                self.font if index == 0 else self.small_font,
                WHITE if index == 0 else MUTED,
                (SCREEN_WIDTH // 2, 290 + index * 42),
            )

    def draw(self):
        self.draw_board()
        if self.state == "welcome":
            self.draw_overlay(
                "SNAKE",
                [
                    "Pulsa cualquier tecla para empezar",
                    "Flechas o WASD: mover    Espacio: pausa",
                    "Come la comida y evita al enemigo, los obstáculos y tu cola",
                    "Pulsa Q o Esc para salir",
                ],
                PURPLE_LIGHT,
            )
        elif self.state == "paused":
            self.draw_overlay(
                "PAUSA",
                ["Pulsa espacio para continuar", "Pulsa Q o Esc para salir"],
                PURPLE_LIGHT,
            )
        elif self.state == "gameover":
            title = "¡Has ganado!" if self.won else "Fin del juego"
            self.draw_overlay(
                title,
                [
                    f"Puntuación final: {self.score}",
                    "Pulsa R, Enter o espacio para jugar otra vez",
                    "Pulsa Q o Esc para salir",
                ],
                GREEN if self.won else RED,
            )

        pygame.display.flip()

    def run(self):
        while self.running:
            elapsed_ms = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            if self.state == "playing":
                self.update(elapsed_ms)
            self.draw()

        pygame.quit()
        return 0


def main():
    return SnakeGame().run()


if __name__ == "__main__":
    sys.exit(main())
