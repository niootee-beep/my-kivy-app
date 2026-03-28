import pygame
import random
import struct
import os
import sys

# --- KHỞI TẠO ---
pygame.init()
# Cố định độ phân giải hoặc lấy theo màn hình Android chuẩn hơn
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SW, SH = screen.get_size()
pygame.mixer.init(frequency=44100, size=-16, channels=1)
clock = pygame.time.Clock()

# --- HỆ THỐNG LƯU TRỮ (Dùng đường dẫn nội bộ Android) ---
HS_FILE = "highscore.txt"

def get_hs():
    try:
        if not os.path.exists(HS_FILE): return 0
        with open(HS_FILE, "r") as f: return int(f.read())
    except: return 0

def set_hs(s):
    if s > get_hs():
        try:
            with open(HS_FILE, "w") as f: f.write(str(s))
        except: pass

def sound_effect(freq=880):
    try:
        duration, rate = 0.1, 44100
        n = int(rate * duration)
        buf = struct.pack('h'*n, *[int(3000 * (1 if (i//(rate//freq//2))%2==0 else -1)) for i in range(n)])
        pygame.mixer.Sound(buffer=buf).play()
    except: pass

class Enemy:
    def __init__(self, speed_mult):
        self.pos = pygame.Vector2(random.randint(50, SW-50), random.randint(50, SH-50))
        self.vel = pygame.Vector2(random.uniform(-4, 4) * speed_mult, random.uniform(-4, 4) * speed_mult)
        self.radius = int(SW * 0.05)
    def move(self):
        self.pos += self.vel
        if self.pos.x < 0 or self.pos.x > SW: self.vel.x *= -1
        if self.pos.y < 0 or self.pos.y > SH: self.vel.y *= -1
    def draw(self):
        pygame.draw.circle(screen, (60, 60, 60), (int(self.pos.x), int(self.pos.y)), self.radius)

state = "MENU"
score = 0
high_score = get_hs()
font_m = pygame.font.SysFont("monospace", int(SW*0.05), bold=True)
font_l = pygame.font.SysFont("monospace", int(SW*0.1), bold=True)

while True:
    screen.fill((10, 10, 10))
    m_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state != "PLAY":
                state, score, start_t = "PLAY", 0, pygame.time.get_ticks()
                p_pos = pygame.Vector2(SW//2, SH//2)
                t_pos = pygame.Vector2(random.randint(100, SW-100), random.randint(100, SH-200))
                enemies = [Enemy(1) for _ in range(3)]

    if state == "MENU":
        t1 = font_l.render("POINT HUNTER", True, (255, 255, 0))
        screen.blit(t1, (SW//2-t1.get_width()//2, SH//3))
        # ... (Các phần vẽ khác giữ nguyên)

    elif state == "PLAY":
        remain = 30 - (pygame.time.get_ticks() - start_t)//1000
        if remain <= 0: state = "OVER"; set_hs(score); high_score = get_hs()
        if pygame.mouse.get_pressed()[0]: p_pos.update(m_pos)
        pygame.draw.circle(screen, (255, 255, 0), (int(t_pos.x), int(t_pos.y)), int(SW*0.04))
        pygame.draw.circle(screen, (255, 50, 50), (int(p_pos.x), int(p_pos.y)), int(SW*0.06))
        for e in enemies:
            e.move(); e.draw()
            if p_pos.distance_to(e.pos) < (SW*0.1): state = "OVER"; set_hs(score)
        if p_pos.distance_to(t_pos) < (SW*0.09):
            score += 1; sound_effect(1200)
            t_pos.update(random.randint(100, SW-100), random.randint(100, SH-200))
            if score % 5 == 0: enemies.append(Enemy(1 + score/20))

    elif state == "OVER":
        t1 = font_l.render("GAME OVER", True, (255, 50, 50))
        screen.blit(t1, (SW//2-t1.get_width()//2, SH//3))

    pygame.display.flip()
    clock.tick(60)
    
