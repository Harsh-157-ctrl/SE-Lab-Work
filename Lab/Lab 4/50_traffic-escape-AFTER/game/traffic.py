import pygame
import random

LANE_W = 80
COLORS = [(220, 60, 60), (220, 140, 40), (140, 60, 180), (60, 180, 80), (180, 180, 40), (60, 80, 200)]

class Car:
    def __init__(self, lane_x, y, direction, speed):
        self.rect = pygame.Rect(lane_x + 10, y, 60, 80)
        self.direction = direction  # 1 = down, -1 = up
        self.speed = speed
        self.color = random.choice(COLORS)

    def update(self):
        self.rect.y += self.direction * self.speed

    def off_screen(self, height):
        return self.rect.top > height + 100 or self.rect.bottom < -100

    def draw(self, screen, is_night=False):
        if is_night:
            beam = pygame.Surface((120, 140), pygame.SRCALPHA)
            if self.direction == 1:
                pygame.draw.polygon(beam, (255, 255, 180, 80), [(60, 0), (0, 140), (120, 140)])
                screen.blit(beam, (self.rect.centerx - 60, self.rect.bottom))
            else:
                pygame.draw.polygon(beam, (255, 255, 180, 80), [(60, 140), (0, 0), (120, 0)])
                screen.blit(beam, (self.rect.centerx - 60, self.rect.top - 140))

        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (180, 220, 240), pygame.Rect(self.rect.x + 8, self.rect.y + 10, 44, 22), border_radius=4)
        for wx in [self.rect.x + 6, self.rect.right - 16]:
            for wy in [self.rect.y + 4, self.rect.bottom - 16]:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(wx, wy, 10, 12), border_radius=3)

class Log:
    def __init__(self, x, y, speed, width=110):
        self.rect = pygame.Rect(x, y, width, 50)
        self.speed = speed

    def update(self, max_w):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > max_w:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = max_w

    def draw(self, screen):
        pygame.draw.rect(screen, (139, 69, 19), self.rect, border_radius=6)
        pygame.draw.rect(screen, (100, 50, 15), self.rect, width=2, border_radius=6)

def make_car(lane_idx, height, speed):
    x = lane_idx * LANE_W
    direction = 1 if lane_idx % 2 == 0 else -1
    y = -90 if direction == 1 else height + 10
    return Car(x, y, direction, speed)