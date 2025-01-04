import pygame
from pygame.locals import *
import random
import sys

pygame.init()
clock = pygame.time.Clock()
fps = 60
current_time = pygame.time.get_ticks()
screen_width = 500
screen_height = 650

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Background
bg = pygame.image.load('bg.png')

def draw_bg():
    screen.blit(bg, (0, 0))
# Game state variables
game_over = False
win = False


alien_shoot_timer = 1000  # Initial timer for alien bullets (milliseconds)
last_alien_shot = pygame.time.get_ticks()
class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        try:
            self.image = pygame.image.load("alien_bullet.png")
        except:
            print("Error loading alien bullet image!")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 1  # Bullet speed downward

    def update(self):
        self.rect.y += self.speed  # Move down
        if self.rect.top > screen_height:  # Remove if off-screen
            self.kill()



# Alien Group Movement
global alien_speed, alien_direction
# Alien Movement Variables
alien_speed = 2  # Horizontal speed
alien_direction = 1  # 1 = right, -1 = left
alien_drop = 10  # Distance to drop down when hitting wall

# Alien Class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # List of alien sprite images
        alien_images = [
            pygame.image.load("alien1.png"),
            pygame.image.load("alien2.png"),
            pygame.image.load("alien3.png"),
            pygame.image.load("alien4.png"),
            pygame.image.load("alien5.png")
        ]

        # Randomly select an image for this alien
        self.image = random.choice(alien_images)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        global alien_speed, alien_direction

        # Move horizontally based on direction
        self.rect.x += alien_speed * alien_direction

        # Check for collisions with bullets
        for bullet in bullet_group:
            if self.rect.colliderect(bullet.rect):  # Collision check
                self.kill()  # Remove alien
                bullet.kill()  # Remove bullet too
    
    def shoot(self):
        # Create an alien bullet at the alien's position
        bullet = AlienBullet(self.rect.centerx, self.rect.bottom)
        alien_bullet_group.add(bullet)  # Add to the bullet group



# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 7

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# Spaceship Class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet_group.add(bullet)

# Button Function
def draw_button(text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()  # Get mouse position
    click = pygame.mouse.get_pressed()  # Detect mouse clicks

    # Check if the mouse is over the button
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))  # Hover color
        if click[0] == 1 and action:  # Left mouse click
            action()  # Perform the button's action
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))  # Default color

    # Render text
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, (0, 0, 0))  # Black text
    screen.blit(text_surface, (x + (width // 2 - text_surface.get_width() // 2),
                               y + (height // 2 - text_surface.get_height() // 2)))
# Actions for buttons
def restart_game():
    global game_over, win, alien_group, alien_bullet_group, spaceship
    game_over = False
    win = False
    spaceship.rect.center = (screen_width // 2, screen_height - 100)
    alien_group.empty()
    alien_bullet_group.empty()

    # Recreate aliens
    for pos in alien_pos:
        alien = Alien(pos[0], pos[1])
        alien_group.add(alien)

def quit_game():
    pygame.quit()
    sys.exit()

# Groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

# Create spaceship
spaceship = Spaceship(int(screen_width / 2), screen_height - 100)
spaceship_group.add(spaceship)

# Create aliens
alien_pos = [(50, 200), (125, 200), (200, 200),(275,200),(350,200),(425,200),(50, 125), (125, 125), (200, 125),(275,125),(350,125),(425,125),(50, 275), (125, 275), (200, 275),(275,275),(350,275),(425,275)]  # Alien positions
for pos in alien_pos:  # Only run ONCE, outside the main loop
    alien = Alien(pos[0], pos[1])  # Pass x and y separately
    alien_group.add(alien)



# Game Loop
run = True
while run:
    clock.tick(fps)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Input
    keys = pygame.key.get_pressed()
    spaceship.move(keys)

    # Shoot bullets
    if keys[pygame.K_SPACE] and pygame.time.get_ticks() - current_time > 300:
        spaceship.shoot()
        current_time = pygame.time.get_ticks()

    if len(alien_group) == 0:  # All aliens destroyed
        win = True
        game_over = True
    
    for bullet in alien_bullet_group:
        if bullet.rect.colliderect(spaceship.rect):  # Alien bullet hits player
            game_over = True
    # Lose condition if any alien moves off the screen
    for alien in alien_group:
        if alien.rect.bottom >= spaceship.rect.top:  # Alien reaches player's level
            game_over = True
            win = False  # Mark it as a loss

    if game_over:
        # Set up the font
        font = pygame.font.Font(None, 64)

        if win:
            text = font.render("YOU WIN!", True, (0, 255, 0))  # Green for win
        else:
            text = font.render("GAME OVER!", True, (255, 0, 0))  # Red for loss

        # Display text in the center
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 3))

        # Draw Buttons
        draw_button("Replay", screen_width // 2 - 75, screen_height // 2, 150, 50, (0, 255, 0), (0, 200, 0), restart_game)
        draw_button("Quit", screen_width // 2 - 75, screen_height // 2 + 70, 150, 50, (255, 0, 0), (200, 0, 0), quit_game)

        pygame.display.update()
        continue  # Skip the rest of the loop until the player presses a button





    # Alien Shooting
    if pygame.time.get_ticks() - last_alien_shot > alien_shoot_timer:
        shooter = random.choice(alien_group.sprites())  # Random alien shoots
        shooter.shoot()
        last_alien_shot = pygame.time.get_ticks()

        # Randomize the next shot timing slightly
        alien_shoot_timer = random.randint(500, 1500)  # 0.5s to 1.5s




    # Collision with player
    for bullet in alien_bullet_group:
        if bullet.rect.colliderect(spaceship.rect):  # Alien bullet hits player
            print("Player hit!")  # Replace this with health or game-over logic

        # Update alien bullets
    alien_bullet_group.update()

    
    # Update bullets
    bullet_group.update()



    # Check if any alien hits a wall
    drop_down = False
    for alien in alien_group:
        if alien.rect.right >= screen_width or alien.rect.left <= 0:
            alien_direction *= -1  # Reverse direction
            drop_down = True  # Flag to drop all aliens
            break  # Only need to check one alien to decide

    # Drop all aliens down if needed
    if drop_down:
        for alien in alien_group:
            alien.rect.y += alien_drop

    # Update alien group
    alien_group.update()

    # Draw everything
    draw_bg() 
    alien_bullet_group.draw(screen)
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)

    pygame.display.update()

pygame.quit()
