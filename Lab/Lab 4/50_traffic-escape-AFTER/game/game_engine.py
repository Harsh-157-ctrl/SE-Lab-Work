import pygame
import random
import json
import os
from game.player import Player, LANE_W
from game.traffic import Car, Log, make_car

LANES = 8
WIDTH = LANES * LANE_W
HEIGHT = 600
FPS = 60
DAY_BG = (60, 60, 60)
NIGHT_BG = (20, 20, 35)
RIVER_Y = 260
RIVER_HEIGHT = 80
HIGH_SCORE_FILE = "high_scores.json"

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Traffic Escape")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 16, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 38, bold=True)
        self.high_scores = self.load_high_scores()
        self.reset()

    def load_high_scores(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_high_score(self, new_score):
        if new_score <= 0:
            return
        self.high_scores.append(new_score)
        self.high_scores = sorted(list(set(self.high_scores)), reverse=True)[:5]
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(self.high_scores, f)

    def reset(self):
        self.player = Player(WIDTH // 2, HEIGHT - 80)
        self.cars = []
        self.logs = [
            Log(20, RIVER_Y + 15, 3, 110),
            Log(260, RIVER_Y + 15, 3, 110),
            Log(500, RIVER_Y + 15, 3, 110),
            Log(120, RIVER_Y + 15, -2.5, 100),
            Log(380, RIVER_Y + 15, -2.5, 100)
        ]
        self.timer = 0
        self.spawn_interval = 50
        self.speed = 3
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.won = False
        self.ticks = 0
        self.is_night = False
        self.score_saved = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                if event.key == pygame.K_n:  # Press N to manually toggle Day/Night
                    self.is_night = not self.is_night
        return True

    def update(self):
        if self.game_over or self.won:
            if not self.score_saved:
                self.save_high_score(self.score // 10)
                self.score_saved = True
            return

        # Automatic Day/Night Cycle (switches every 30 seconds / 1800 ticks at 60 FPS)
        self.ticks += 1
        if self.ticks % (30 * FPS) == 0:
            self.is_night = not self.is_night

        keys = pygame.key.get_pressed()
        self.player.move(keys, 0, WIDTH, 30, HEIGHT)

        # Log hopping check
        player_on_log = False
        river_rect = pygame.Rect(0, RIVER_Y, WIDTH, RIVER_HEIGHT)
        for log in self.logs:
            log.update(WIDTH)
            if log.rect.colliderect(self.player.rect):
                player_on_log = True
                self.player.rect.x += log.speed

        # Drowning check
        if river_rect.colliderect(self.player.rect) and not player_on_log:
            self.handle_hit()

        # Car collision check
        self.timer += 1
        if self.timer >= self.spawn_interval:
            lane = random.randint(0, LANES - 1)
            self.cars.append(make_car(lane, HEIGHT, self.speed))
            self.timer = 0
            self.spawn_interval = max(22, self.spawn_interval - 0.2)

        for c in self.cars:
            c.update()
            if c.rect.colliderect(self.player.rect):
                self.handle_hit()

        self.cars = [c for c in self.cars if not c.off_screen(HEIGHT)]
        self.score += 1
        if self.score % 300 == 0:
            self.speed = min(10, self.speed + 0.5)

        if self.player.rect.top <= 35:
            self.won = True

    def handle_hit(self):
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            self.player.reset_position()

    def draw(self):
        bg_color = NIGHT_BG if self.is_night else DAY_BG
        self.screen.fill(bg_color)

        # River lane
        pygame.draw.rect(self.screen, (30, 90, 180), pygame.Rect(0, RIVER_Y, WIDTH, RIVER_HEIGHT))
        for log in self.logs:
            log.draw(self.screen)

        # Road lines
        for i in range(LANES + 1):
            pygame.draw.line(self.screen, (100, 100, 100), (i * LANE_W, 0), (i * LANE_W, HEIGHT), 2)
        for y in range(0, HEIGHT, 60):
            if not (RIVER_Y <= y <= RIVER_Y + RIVER_HEIGHT):
                for i in range(LANES):
                    pygame.draw.rect(self.screen, (200, 200, 100), pygame.Rect(i * LANE_W + LANE_W // 2 - 3, y, 6, 30))

        # Sidewalks
        pygame.draw.rect(self.screen, (150, 130, 110), pygame.Rect(0, HEIGHT - 50, WIDTH, 50))
        pygame.draw.rect(self.screen, (150, 130, 110), pygame.Rect(0, 30, WIDTH, 25))

        for c in self.cars:
            c.draw(self.screen, is_night=self.is_night)
        self.player.draw(self.screen)

        # HUD bar
        hud = pygame.Rect(0, 0, WIDTH, 30)
        pygame.draw.rect(self.screen, (20, 20, 20), hud)
        cycle_str = "NIGHT" if self.is_night else "DAY"
        lives_str = "♥ " * self.lives
        s = self.font.render(f"Lives: {lives_str} | Score: {self.score // 10} | Mode: {cycle_str} (N=Toggle)", True, (220, 220, 220))
        self.screen.blit(s, (6, 6))

        if self.game_over:
            self._msg("GAME OVER", (220, 60, 60))
        if self.won:
            self._msg("YOU MADE IT!", (80, 220, 80))

        pygame.display.flip()

    def _msg(self, text, color):
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        self.screen.blit(ov, (0, 0))

        m = self.big_font.render(text, True, color)
        sub = self.font.render("Press R to Restart", True, (200, 200, 200))
        self.screen.blit(m, (WIDTH // 2 - m.get_width() // 2, HEIGHT // 2 - 100))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 - 50))

        hs_title = self.font.render("--- TOP 5 HIGH SCORES ---", True, (255, 215, 0))
        self.screen.blit(hs_title, (WIDTH // 2 - hs_title.get_width() // 2, HEIGHT // 2 + 10))

        for idx, sc in enumerate(self.high_scores[:5]):
            hs_item = self.font.render(f"#{idx + 1}: {sc} pts", True, (240, 240, 240))
            self.screen.blit(hs_item, (WIDTH // 2 - hs_item.get_width() // 2, HEIGHT // 2 + 40 + (idx * 24)))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()