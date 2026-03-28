import pygame
import random
import struct
import os

# --- KHỞI TẠO & CẤU HÌNH ---
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)
info = pygame.display.Info()
SW, SH = info.current_w, info.current_h
screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("Point Hunter") # Đặt tiêu đề cửa sổ
clock = pygame.time.Clock()

# --- HỆ THỐNG LƯU TRỮ ---
HS_FILE = "highscore.txt"
def get_hs():
    if not os.path.exists(HS_FILE): return 0
    with open(HS_FILE, "r") as f: 
        try: return int(f.read())
        except: return 0

def set_hs(s):
    if s > get_hs():
        with open(HS_FILE, "w") as f: f.write(str(s))

# --- ÂM THANH (Tự tạo sóng âm) ---
def sound_effect(freq=880):
    duration, rate = 0.1, 44100
    n = int(rate * duration)
    buf = struct.pack('h'*n, *[int(3000 * (1 if (i//(rate//freq//2))%2==0 else -1)) for i in range(n)])
    pygame.mixer.Sound(buffer=buf).play()

# --- ĐỐI TƯỢNG KẺ ĐỊCH ---
class Enemy:
    def __init__(self, speed_mult):
        self.pos = pygame.Vector2(random.randint(50, SW-50), random.randint(50, SH-50))
        self.vel = pygame.Vector2(random.uniform(-4, 4) * speed_mult, random.uniform(-4, 4) * speed_mult)
        self.radius = 40
    def move(self):
        self.pos += self.vel
        if self.pos.x < 0 or self.pos.x > SW: self.vel.x *= -1
        if self.pos.y < 0 or self.pos.y > SH: self.vel.y *= -1
    def draw(self):
        # Vẽ kẻ địch màu xám đậm có viền
        pygame.draw.circle(screen, (60, 60, 60), (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(screen, (100, 100, 100), (int(self.pos.x), int(self.pos.y)), self.radius, 3)

# --- TRẠNG THÁI & FONT ---
state = "MENU"
score = 0
high_score = get_hs()
font_m = pygame.font.SysFont("monospace", 45, bold=True)
font_l = pygame.font.SysFont("monospace", 90, bold=True)

# --- VÒNG LẶP CHÍNH ---
while True:
    screen.fill((10, 10, 10)) # Nền đen sâu
    m_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state != "PLAY":
                state, score, start_t = "PLAY", 0, pygame.time.get_ticks()
                p_pos = pygame.Vector2(SW//2, SH//2)
                t_pos = pygame.Vector2(random.randint(100, SW-100), random.randint(100, SH-200))
                enemies = [Enemy(1) for _ in range(3)]

    if state == "MENU":
        t1 = font_l.render("POINT HUNTER", True, (255, 255, 0))
        t2 = font_m.render(f"BEST: {high_score}", True, (255, 215, 0))
        t3 = font_m.render("TAP TO START", True, (255, 255, 255))
        screen.blit(t1, (SW//2-t1.get_width()//2, SH//3))
        screen.blit(t2, (SW//2-t2.get_width()//2, SH//2))
        screen.blit(t3, (SW//2-t3.get_width()//2, SH//2 + 150))

    elif state == "PLAY":
        remain = 30 - (pygame.time.get_ticks() - start_t)//1000
        if remain <= 0: 
            state = "OVER"; set_hs(score); high_score = get_hs(); sound_effect(220)
        
        if pygame.mouse.get_pressed()[0]: p_pos.update(m_pos)
        
        # Vẽ Mục tiêu (Vàng) và Người chơi (Đỏ)
        pygame.draw.circle(screen, (255, 255, 0), (int(t_pos.x), int(t_pos.y)), 35)
        pygame.draw.circle(screen, (255, 50, 50), (int(p_pos.x), int(p_pos.y)), 50)
        
        # Cập nhật kẻ địch
        for e in enemies:
            e.move(); e.draw()
            if p_pos.distance_to(e.pos) < 90: # Va chạm kẻ địch
                state = "OVER"; set_hs(score); high_score = get_hs(); sound_effect(150)
            
        # Ăn điểm
        if p_pos.distance_to(t_pos) < 85:
            score += 1; sound_effect(1200)
            t_pos.update(random.randint(100, SW-100), random.randint(100, SH-200))
            if score % 5 == 0: enemies.append(Enemy(1 + score/20)) # Tăng dần kẻ địch

        # Hiển thị HUD
        txt = font_m.render(f"SCORE: {score}  TIME: {remain}s", True, (255, 255, 255))
        screen.blit(txt, (50, 80))

    elif state == "OVER":
        t1 = font_l.render("GAME OVER", True, (255, 50, 50))
        t2 = font_m.render(f"YOUR SCORE: {score}", True, (255, 255, 255))
        t3 = font_m.render("TAP TO RESTART", True, (0, 255, 100))
        screen.blit(t1, (SW//2-t1.get_width()//2, SH//3))
        screen.blit(t2, (SW//2-t2.get_width()//2, SH//2))
        screen.blit(t3, (SW//2-t3.get_width()//2, SH//2 + 150))

    pygame.display.flip()
    clock.tick(120)
