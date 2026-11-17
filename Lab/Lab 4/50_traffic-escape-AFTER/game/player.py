import pygame

SPEED = 4
LANE_W = 80

class Player:
    def __init__(self, x, y):
        self.start_x = x - 20
        self.start_y = y - 30
        self.rect = pygame.Rect(self.start_x, self.start_y, 40, 60)
        self.color = (60, 160, 220)
        self.move_cooldown = 0

    def reset_position(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y

    def move(self, keys, min_x, max_x, min_y, max_y):
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -LANE_W
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = LANE_W
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -25
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = 25

        nx = max(min_x, min(max_x - self.rect.width, self.rect.x + dx))
        ny = max(min_y, min(max_y - self.rect.height, self.rect.y + dy))

        if dx or dy:
            self.rect.x = nx
            self.rect.y = ny
            self.move_cooldown = 8

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (180, 220, 240), pygame.Rect(self.rect.x + 6, self.rect.y + 8, 28, 18), border_radius=4)
        for wx in [self.rect.x + 4, self.rect.right - 12]:
            for wy in [self.rect.y + 4, self.rect.bottom - 14]:
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(wx, wy, 8, 10), border_radius=3)