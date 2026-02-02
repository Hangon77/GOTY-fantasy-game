import pygame
from sys import exit
import os 

pygame.init()

#game variables 
GAME_WIDTH = 512
GAME_HEIGHT = 512

PLAYER_X = GAME_WIDTH//2
PLAYER_Y = GAME_HEIGHT//2
PLAYER_WIDTH = 56
PLAYER_HEIGHT = 56
PLAYER_SHOOT_WIDTH = 70
PLAYER_BULLET_WIDTH = 25
PLAYER_BULLET_HEIGHT = 19
PLAYER_VELOCITY_Y = 8
PLAYER_DISTANCE = 5
BULLET_OFFSET_Y = 18
BULLET_OFFSET_X = 5
TILE_SIZE = 10
GRAVITY = 0.005

HEALTH_WIDTH = 16
HEALTH_HEIGHT = 4

#enemies variables
ATTOR_WIDTH = 56
ATTOR_HEIGHT = 84
ATTOR_BULLET_WIDTH = 20
ATTOR_BULLET_HEIGHT = 20
ATTOR_SHOOT_COOLDOWN = 120  # frames between shots


background_image = pygame.image.load(os.path.join("images", "background.jpg"))
background_image = pygame.transform.scale(background_image, (GAME_WIDTH, GAME_HEIGHT))
player_image_right = pygame.image.load(os.path.join("images", "south.png"))
player_image_shoot = pygame.image.load(os.path.join("images", "shoot.png"))
player_image_bullet = pygame.image.load(os.path.join("images", "wave.png"))
player_image_bullet = pygame.transform.scale(player_image_bullet, (PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT))
attor_image_south = pygame.image.load(os.path.join("images", "betterattor.png"))
attor_image_bullet = pygame.image.load(os.path.join("images", "enemywave.png"))
attor_image_bullet = pygame.transform.scale(attor_image_bullet, (ATTOR_BULLET_WIDTH, ATTOR_BULLET_HEIGHT))
health_image = pygame.image.load(os.path.join("images", "health.png"))
health_image = pygame.transform.scale(health_image, (HEALTH_WIDTH, HEALTH_HEIGHT))
print("cwd:", os.getcwd())

window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("GOTY - ADAM'S GAME OF THE YEAR")
clock = pygame.time.Clock() #frame rate 
pygame.font.init()
#game_font = pygame.font.SysFont('Arial', 24)
game_font = pygame.font.Font("./MaskingRenta-MAxjJ.otf", 24)
game_over = False
wave = 1

#custom event
INVINCIBILITY_END = pygame.USEREVENT + 0
SHOOTING_END = pygame.USEREVENT + 1


class Player(pygame.Rect):

    class Bullet(pygame.Rect):
        def __init__(self, player_obj):
            pygame.Rect.__init__(self, player_obj.x + BULLET_OFFSET_X, player_obj.y + BULLET_OFFSET_Y,
                                 PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
            self.velocity_y = PLAYER_VELOCITY_Y
            self.image = player_image_bullet
            self.used = False

        def move(self):
            self.y -= self.velocity_y

    def __init__(self):
        pygame.Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.shooting = False
        self.bullets = []
        self.invincible = False
        self.max_health = 30
        self.health = self.max_health
        self.score = 0

    def update_image(self):
        if self.shooting:
            self.image = player_image_shoot
        else:
            self.image = player_image_right

    def set_invincible(self, milliseconds=1000):
        self.invincible = True
        pygame.time.set_timer(INVINCIBILITY_END, milliseconds, 1)

    def shoot(self):
        if not self.shooting:
            self.shooting = True
            self.bullets.append(Player.Bullet(self))
            pygame.time.set_timer(SHOOTING_END, 250, 1)

class Attor(pygame.Rect):
    
    class Bullet(pygame.Rect):
        def __init__(self, attor_obj, target_x, target_y):
            pygame.Rect.__init__(self, attor_obj.x + ATTOR_WIDTH//2, attor_obj.y + ATTOR_HEIGHT,
                                 ATTOR_BULLET_WIDTH, ATTOR_BULLET_HEIGHT)
            self.image = attor_image_bullet
            # Calculate direction towards target
            dx = target_x - self.x
            dy = target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                self.velocity_x = (dx / distance) * 5  # 5 is bullet speed
                self.velocity_y = (dy / distance) * 5
            else:
                self.velocity_x = 0
                self.velocity_y = 5
        
        def move(self):
            self.x += self.velocity_x
            self.y += self.velocity_y
    
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, ATTOR_WIDTH, ATTOR_HEIGHT)
        self.image = attor_image_south  
        self.velocity_y = 0
        self.velocity_x = 2
        self.health = 10
        self.bullets = []
        self.shoot_cooldown = 0


    def move(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y 
        self.x += self.velocity_x

        if self.y + ATTOR_HEIGHT >= GAME_HEIGHT:
            self.y = GAME_HEIGHT - ATTOR_HEIGHT  # Stop at bottom
            self.velocity_y *= -0.8
        if self.x <= 0 or self.x + ATTOR_WIDTH >= GAME_WIDTH:
            self.velocity_x *= -1
    
    def shoot(self, target_x, target_y):
        if self.shoot_cooldown <= 0:
            self.bullets.append(Attor.Bullet(self, target_x, target_y))
            self.shoot_cooldown = ATTOR_SHOOT_COOLDOWN


#start game  
player = Player()
attor = attors = [
    Attor(50, TILE_SIZE*5),
    Attor(150, TILE_SIZE*3),
    Attor(250, TILE_SIZE*5),
    Attor(350, TILE_SIZE*4)
]
attor_shots = []
tiles = []

def draw():
    window.fill("#1f7a24")
    window.blit(background_image, (0, 0))
    window.blit(player.image, (player.x, player.y))
    for attor in attors:  # Draw all attors
        window.blit(attor.image, (attor.x, attor.y))
        for bullet in attor.bullets:
            window.blit(bullet.image, (bullet.x, bullet.y))
    for bullet in attor_shots:  # Draw orphaned attor bullets
        window.blit(bullet.image, (bullet.x, bullet.y))
    for bullet in player.bullets:
        window.blit(bullet.image, (bullet.x, bullet.y))
    
    #health bar
    #pygame.draw.rect(window, "red", (TILE_SIZE, TILE_SIZE, 10 * player.max_health, 10))
    #pygame.draw.rect(window, "green", (TILE_SIZE, TILE_SIZE, 10 * player.health, 10))
    pygame.draw.rect(window, "black", (TILE_SIZE, TILE_SIZE, HEALTH_WIDTH, HEALTH_HEIGHT * player.max_health))
    for i in range(player.max_health - player.health, player.max_health):
        window.blit(health_image, (TILE_SIZE, TILE_SIZE + i * HEALTH_HEIGHT, HEALTH_WIDTH, HEALTH_HEIGHT))    

    #score
    text_score = str(player.score)
    while len(text_score) < 7:
        text_score = "0" + text_score 
    text_surface = game_font.render(text_score, False, "White")
    window.blit(text_surface, (GAME_WIDTH/2, TILE_SIZE/2))

    if game_over:                 
        text_surface = game_font.render("Game Over:", False, "Black")
        window.blit(text_surface, (GAME_WIDTH/8, GAME_HEIGHT/2))
        text_surface = game_font.render("Press [Enter] to Restart", False, "Black")
        window.blit(text_surface, (GAME_WIDTH/8, GAME_HEIGHT/2 + TILE_SIZE *4))

def spawn_wave(wave_num): #AI helped creating
    """Spawn a new wave of attors with increasing difficulty"""
    global attors
    attors = []
    num_attors = 3 + wave_num  # Increase number of attors per wave (wave 1 = 4 attors)
    for i in range(num_attors):
        x = (i % 4) * (GAME_WIDTH // 4) + 50
        y = (i // 4) * 80 + TILE_SIZE * 3
        attors.append(Attor(x, y))

def reset_game():
    global player, attors, attor_shots, game_over, wave
    player = Player()
    attors = []
    attor_shots = []
    game_over = False
    wave = 1
    spawn_wave(wave)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == INVINCIBILITY_END:
            player.invincible = False

        if event.type == SHOOTING_END:
            player.shooting = False

        '''if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                player.y -= 5
            if event.key in (pygame.K_DOWN, pygame.K_s):
                player.y += 5
            if event.key in (pygame.K_LEFT, pygame.K_a):
                player.x -= 5
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                player.x += 5
        '''
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]) and game_over: 
        reset_game()
    if not game_over:
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            player.y = max(player.y - PLAYER_DISTANCE, 0)
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            player.y = min(player.y + PLAYER_DISTANCE, GAME_HEIGHT - PLAYER_HEIGHT)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            player.x = max(player.x - PLAYER_DISTANCE, 0)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            player.x = min(player.x + PLAYER_DISTANCE, GAME_WIDTH - PLAYER_WIDTH)
        if keys[pygame.K_SPACE]:
            player.shoot()
    
    player.update_image()
    
    if not game_over:
        # Update attors
        for attor in attors:
            attor.move()
            attor.shoot_cooldown -= 1
            attor.shoot(player.x + PLAYER_WIDTH//2, player.y + PLAYER_HEIGHT//2)
            
            # Check collision with player
            if not player.invincible and player.colliderect(attor):
                print("Player hit by attor!")
                player.health -= 1 
                player.set_invincible()
                
            
            # Move attor bullets and check collision with player
            for bullet in attor.bullets[:]:
                bullet.move()
                # Remove if off screen
                if bullet.y > GAME_HEIGHT or bullet.x < 0 or bullet.x > GAME_WIDTH:
                    attor.bullets.remove(bullet)
                # Check collision with player
                elif bullet.colliderect(player):
                    attor.bullets.remove(bullet)
                    player.health -= 1
        
        # Update orphaned attor shots
        for bullet in attor_shots[:]:
            bullet.move()
            # Remove if off screen
            if bullet.y > GAME_HEIGHT or bullet.x < 0 or bullet.x > GAME_WIDTH:
                attor_shots.remove(bullet)
            # Check collision with player
            elif bullet.colliderect(player):
                attor_shots.remove(bullet)
                player.health -= 1
        
        # Move and clean up player bullets
        for bullet in player.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                player.bullets.remove(bullet)
            # Check collision - check if bullet center is inside attor
            else:
                for attor in attors[:]:
                    if (attor.x < bullet.x + bullet.width/2 < attor.x + attor.width and
                        attor.y + 40 < bullet.y < attor.y + attor.height): #ai helped creating, not working...
                        player.bullets.remove(bullet)
                        attor.health -= 1
                        if attor.health <= 0:
                            attors.remove(attor)
                            attor_shots.extend(attor.bullets)  # Drop remaining bullets
                            player.score += 500
                            # Check if all attors are defeated
                            if len(attors) == 0:
                                wave += 1
                                spawn_wave(wave)
                        break
        
        if player.health <= 0:
            game_over = True
    
    draw()
    pygame.display.update()
    clock.tick(60) #60 frames per second