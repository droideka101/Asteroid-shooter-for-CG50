import pygame
import sys
import random
import time

pygame.init()
SIZE = (384, 216)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("FARRT BALLS")
display = pygame.Surface((SIZE), pygame.SRCALPHA)
spaceBG = pygame.Surface((SIZE), pygame.SRCALPHA)
overlay = pygame.Surface((SIZE), pygame.SRCALPHA)
menu = pygame.Surface((SIZE), pygame.SRCALPHA)

text_font = pygame.font.SysFont(None, 15)
menu_font = pygame.font.SysFont(None, 20)
title_font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

score = 0

game_state = "start_menu"  # Possible states: start_menu, game, game_over
game_over = False  # To track the game-over state

gun_temp = 100
d_temp = 5

Lives = 5
zero_lives_timer = None

def LivesDisplay(surface, Lives):
    startX = 385
    startY = 5
    parts = [
        pygame.Rect(startX, startY, 4, 10),
        pygame.Rect(startX + 6, startY, 4, 10),
        pygame.Rect(startX - 2, startY + 2, 14, 6),
        pygame.Rect(startX + 2, startY + 8, 6, 4)
    ]
    for i in range(Lives):
        for part in parts:
            part.x -= 20 
            pygame.draw.rect(surface, (204, 24, 31), part)
        

def gunTempDisplay(surface, temp):
    length = temp * 3.84
    #print(temp)
    objectRect = pygame.Rect(0, 212, length, 4)
    pygame.draw.rect(surface, (45, 236, 11), objectRect)

def draw_start_menu():
    menu.fill((0, 0, 0))  # Black background
    title = title_font.render("BALLS GAME", True, pygame.Color("WHITE"))
    start_button = menu_font.render("START >>", True, (255, 255, 255))
    quit_button = menu_font.render("QUIT   <<", True, (255, 255, 255))
    menu.blit(title, (SIZE[0] / 2 - title.get_width() / 2, SIZE[1] / 3 - title.get_height() / 2))
    menu.blit(start_button, (SIZE[0] / 2 - start_button.get_width() / 2, SIZE[1] / 2))
    menu.blit(quit_button, (SIZE[0] / 2 - quit_button.get_width() / 2, SIZE[1] / 2 + quit_button.get_width() / 2))
    screen.blit(menu, (0, 0))
    pygame.display.update()

def draw_game_over_screen(score):
    menu.fill((0, 0, 0))  # Black background
    title = title_font.render("GAME OVER :(", True, pygame.Color("RED"))
    score_text = menu_font.render(f"Score: {score}", True, pygame.Color("WHITE"))
    quit_button = menu_font.render("QUIT    >>", True, (255, 255, 255))
    restart_button = menu_font.render("RESTART (5)", True, (255, 255, 255))
    menu.blit(title, (SIZE[0] / 2 - title.get_width() / 2, SIZE[1] / 3 - title.get_height() / 2))
    menu.blit(score_text, (SIZE[0] / 2 - score_text.get_width() / 2, SIZE[1] / 2 - 20))
    menu.blit(quit_button, (SIZE[0] / 2 - quit_button.get_width() / 2, SIZE[1] / 2 ))
    menu.blit(restart_button, (SIZE[0] / 2 - restart_button.get_width() / 2, SIZE[1] / 2 + 20))
    screen.blit(menu, (0, 0))
    pygame.display.update()

def scoreDisplay(score, font):
    score_count = f"SCORE : {score}"
    img = font.render(score_count, True, pygame.Color("WHITE"))
    #overlay.fill((0, 0, 0, 0))
    overlay.blit(img,(5,5))

def randomGray(start, end):
    random_gray_colour = random.randint(start, end)
    return (random_gray_colour, random_gray_colour, random_gray_colour)

class ScrollingStars():
    def __init__(self, startX, startY):
        self.objectRect = pygame.Rect(startX, startY, 2, 2)

    def updateXY(self, dy, dx):
        self.objectRect.y += dy
        self.objectRect.x += dx
        if self.objectRect.x <= -2:
            self.objectRect.x = 386
            self.objectRect.y = random.randint(0, SIZE[1])

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.objectRect)

class ScrollilngAsteroids():
    def __init__(self, startX, startY):
        #self.objectRect = pygame.Rect(startX, startY, 20, 20)
        self.parts = [
            pygame.Rect(startX, startY, 20, 20),
            pygame.Rect(startX - 3, startY + 5, 20, 20),
            pygame.Rect(startX + 4, startY + 3, 20, 23),
            pygame.Rect(startX + 7, startY - 2, 20, 20)
        ]
        self.part_colours = [
            randomGray(66, 110),
            randomGray(66, 110),
            randomGray(66, 110),
            randomGray(66, 110)
        ]

    def updateXY(self, dy, dx):
        global score
        self.parts[0].x += dx
        if self.parts[0].x <= -20:
            self.parts[0].x = 400
            self.parts[0].y = random.randint(0, SIZE[1])
            score -= 10

        self.parts[1].x = self.parts[0].x - 3
        self.parts[1].y = self.parts[0].y + 5
        self.parts[2].x = self.parts[0].x + 4
        self.parts[2].y = self.parts[0].y + 3
        self.parts[3].x = self.parts[0].x + 7
        self.parts[3].y = self.parts[0].y - 2

    def draw(self, surface):
        #pygame.draw.rect(surface, (66, 66, 66), self.objectRect)
        for i, part in enumerate(self.parts):
            pygame.draw.rect(surface, self.part_colours[i], part)

class PlayerShip():
    def __init__(self, startX=50, startY=98):
        self.startX = startX
        self.startY = startY
        self.parts = [
            pygame.Rect(startX, startY, 35, 4),  # Main body
            pygame.Rect(startX + 8, startY - 15, 5, 34),  # wing
            pygame.Rect(startX, startY - 3, 20, 10),  # Top part
            pygame.Rect(startX, startY - 5, 5, 14),  # boosters
            pygame.Rect(startX - 2, startY - 5, 3, 14),  # booster fire
            pygame.Rect(startX - 5, startY, 8, 4),  # boosters2
            pygame.Rect(startX + 10, startY, 8, 4),  # cockpit
            pygame.Rect(startX + 6, startY + 17, 10, 2),  # top wing tip
            pygame.Rect(startX + 6, startY - 15, 10, 2)  # bottom wing tip
        ]
        self.part_colours = [
            (145, 145, 145),  # Colour for main body (gray)
            (145, 145, 145),  # Colour for wing (gray)
            (105, 105, 105),  # Colour for top part (gray)
            (105, 105, 105),  # Colour for boosters (gray)
            (186, 62, 0),     # Colour for booster fire (orange)
            (0, 0, 0),        # Colour for boosters2 (black)
            (103, 159, 191),  # Colour for cockpit (blue)
            (145, 145, 145),  # Colour for top wing tip
            (145, 145, 145)   # Colour for bottom wing tip
        ]

        # Speed variables for acceleration
        self.currentSpeed = 0  # Current speed of the ship
        self.accelerationRate = 400  # How quickly the ship accelerates
        self.maxSpeed = 150  # Maximum speed of the ship
        self.decelerationRate = 300  # How quickly the ship decelerates

    def inputHandler(self, keyHeld):
        """Handles input for acceleration or deceleration."""
        if keyHeld[pygame.K_w] and keyHeld[pygame.K_s]:
            return 0  # No change in speed
        if keyHeld[pygame.K_w]:
            return -1  # Move up
        if keyHeld[pygame.K_s]:
            return 1  # Move down
        else:
            return 0  # Gradual deceleration

    def updateXY(self, keyHeld, dt):
        """Updates the position of all ship parts relative to the main body."""
        keyInput = self.inputHandler(keyHeld)
    
        # Adjust current speed with acceleration or deceleration
        if keyInput != 0:
            self.currentSpeed += keyInput * self.accelerationRate * dt
        else:
            # Decelerate towards 0 if no input is held
            if self.currentSpeed > 0:
                self.currentSpeed = max(self.currentSpeed - self.decelerationRate * dt, 0)
            elif self.currentSpeed < 0:
                self.currentSpeed = min(self.currentSpeed + self.decelerationRate * dt, 0)
    
        # Clamp speed to maximum values
        self.currentSpeed = max(min(self.currentSpeed, self.maxSpeed), -self.maxSpeed)
    
        # Calculate the new y position for the main body of the ship
        new_y = self.parts[0].y + (self.currentSpeed * dt)
    
        # Check for collisions with the edges
        if new_y < 0:  # Top edge
            self.parts[0].y = 0
            self.currentSpeed = 0  # Stop movement
        elif new_y > 216 - self.parts[0].height:  # Bottom edge
            self.parts[0].y = 216 - self.parts[0].height
            self.currentSpeed = 0  # Stop movement
        else:
            self.parts[0].y = new_y  # No collision, move normally
    
        # Update the other parts' positions based on their relative offsets
        self.parts[1].y = self.parts[0].y - 15  # Wing offset
        self.parts[2].y = self.parts[0].y - 3   # Top part offset
        self.parts[3].y = self.parts[0].y - 5   # Boosters offset
        self.parts[4].y = self.parts[0].y - 5   # Boosters fire offset
        self.parts[5].y = self.parts[0].y       # Boosters2 offset
        self.parts[6].y = self.parts[0].y       # Cockpit offset
        self.parts[7].y = self.parts[0].y + 17  # Top wing tip offset
        self.parts[8].y = self.parts[0].y - 15  # Bottom wing tip offset
        
    def draw(self, surface):
        for i, part in enumerate(self.parts):
            pygame.draw.rect(surface, self.part_colours[i], part)

class Laser():
    def __init__(self, startX, startY):
        self.LASER_SPEED = 1000  # Speed of the laser
        self.objectRect = pygame.Rect(startX, startY, 12, 2)

    def update(self, dt):
        self.objectRect.x += self.LASER_SPEED * dt
        if self.objectRect.x > SIZE[0]:  # Remove laser if it goes off screen
            return False
        return True

    def draw(self, surface):
        pygame.draw.rect(surface, (45, 236, 11), self.objectRect)

num_stars = 15  # Number of stars
scrolling_stars_list = []

for _ in range(num_stars):
    startX = random.randint(0, SIZE[0] - 2)  # Random x position
    startY = random.randint(0, SIZE[1])      # Random y position
    star = ScrollingStars(startX, startY)
    scrolling_stars_list.append(star)


num_asteroids = 10
scrolling_asteroid_list = []

for _ in range(num_asteroids):
    startX = random.randint(SIZE[0], SIZE[0] * 2)
    startY = random.randint(0, SIZE[1])
    asteroid = ScrollilngAsteroids(startX, startY)
    scrolling_asteroid_list.append(asteroid)



player_ship = PlayerShip()
lasers = []  # List to hold active lasers


SHIP_SPEED = 150
STAR_SPEED = -60
ASTEROID_SPEED = -120
FPS = 30
laser_timer = 0  # Timer for firing lasers
laser_delay = 100  # Delay in milliseconds between laser shots
next_laser_side = 0  # 0 for left, 1 for right

def restart():
    global lasers
    global score
    global gun_temp
    global Lives
    global zero_lives_timer 
    lasers = []
    player_ship.parts[0].x = 50
    player_ship.parts[0].y = 98
    for asteroid in scrolling_asteroid_list:
        asteroid.parts[0].x = random.randint(SIZE[0], SIZE[0] * 2)
        asteroid.parts[0].y = random.randint(0, SIZE[1])
    gun_temp = 100
    score = 0
    Lives = 3
    zero_lives_timer = None


while True:
    dt = clock.tick(FPS) / 1000.0
    keyHeld = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keyHeld[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    if game_state == "start_menu":
        draw_start_menu()
        if keyHeld[pygame.K_RIGHT]:  # Start game on >
            game_state = "game"
            player_ship = PlayerShip()  # Reset player ship
            score = 0  # Reset score
            game_over = False
        if keyHeld[pygame.K_LEFT]:  # exit game on <
            pygame.quit()
            sys.exit()

    elif game_state == "game_over":
        draw_game_over_screen(score)
        if keyHeld[pygame.K_RIGHT]:  # Quit game on >
            pygame.quit()
            sys.exit()
        if keyHeld[pygame.K_5]:
            pygame.time.wait(500)
            restart()
            game_state = "start_menu"

    elif game_state == "game":
        # Game logic
        spaceBG.fill((0, 0, 0))
        display.fill((0, 0, 0, 0))
        overlay.fill((0, 0, 0, 0))
        

        # Update and draw stars
        for star in scrolling_stars_list:
            star.updateXY(0, STAR_SPEED * dt)

        for asteroid in scrolling_asteroid_list:
            asteroid.updateXY(0, ASTEROID_SPEED * dt)

        # Update and draw player ship
        player_ship.updateXY(keyHeld, dt)

        if gun_temp == 0:
            guns_Overheated = True
        if gun_temp > 100:
            guns_Overheated = False

        # Laser firing logic
        laser_timer += dt * 1000  # Convert dt to milliseconds
        if keyHeld[pygame.K_0] and laser_timer >= laser_delay and gun_temp >= 2 and not guns_Overheated:
            if next_laser_side == 0:
                lasers.append(Laser(player_ship.parts[7].x, player_ship.parts[7].y - 2))  # Top wing tip
                next_laser_side = 1
            else:
                lasers.append(Laser(player_ship.parts[8].x, player_ship.parts[8].y + 2))  # Bottom wing tip
                next_laser_side = 0
            laser_timer = 0  # Reset timer
            gun_temp -= 2
            #gunTempDisplay(overlay, gun_temp)

        if laser_timer >= laser_delay and gun_temp <= 100:
            gun_temp += 1
            
        gunTempDisplay(overlay, gun_temp)

        # Update lasers
        lasers = [laser for laser in lasers if laser.update(dt)]

        for laser in lasers[:]:
            for asteroid in scrolling_asteroid_list[:]:
                for asteroid_parts in asteroid.parts:
                    if laser.objectRect.colliderect(asteroid_parts):
                        try:
                            lasers.remove(laser)
                            asteroid.parts[0].x = random.randint(SIZE[0], SIZE[0] * 2)
                            asteroid.parts[0].y = random.randint(0, SIZE[1])
                            score += 5
                            break
                        except:
                            break

        scoreDisplay(score, text_font)

        LivesDisplay(overlay, Lives) 

        for asteroid in scrolling_asteroid_list:
            collision_detected = False
            for ship_part in player_ship.parts:
                for asteroid_part in asteroid.parts:
                    if asteroid_part.colliderect(ship_part):  # Collision
                        collision_detected = True
                        Lives -= 1
                        asteroid.parts[0].x = random.randint(SIZE[0], SIZE[0] * 2)
                        asteroid.parts[0].y = random.randint(0, SIZE[1])
                        print(f"Remaining Lives {Lives}")
                        break
                if collision_detected:
                    break

        # if Lives <= 0:
        #     pygame.time.wait(1000)
        #     game_state = "game_over"
        #     game_over = True

        if Lives <= 0:
            # Display 0 hearts
            Lives = 0
            LivesDisplay(overlay, Lives)  # Update the overlay with 0 lives
            screen.blit(overlay, (0, 0))  # Redraw overlay (with 0 hearts)
            pygame.display.update()  # Force a screen update to show 0 hearts

            # Add a short pause to let the player see the 0 hearts
            pygame.time.wait(1000)  # Wait for 1 second (non-blocking)

            # Now transition to the game over state
            game_state = "game_over"
            game_over = True

        # Add a new variable to track the "pause" when lives reach 0

        

        # if Lives <= 0 and zero_lives_timer is None:
        #     print("timer started")
        #     # Start the timer when lives reach 0
        #     zero_lives_timer = pygame.time.get_ticks()
        #     Lives = 0
        #     LivesDisplay(overlay, Lives)  # Display 0 hearts
        #     screen.blit(overlay, (0, 0))
        #     pygame.display.update()  # Show the update immediately

        # if zero_lives_timer is not None:
        #     print("timer check")
        #     # Check if 1 second has passed since the timer started
        #     if pygame.time.get_ticks() - zero_lives_timer >= 1000:  # 1000 ms = 1 second
        #         print("timer reached one second")
        #         # End the pause and switch to the game-over state
        #         zero_lives_timer = None  # Reset the timer
        #         game_state = "game_over"
        #         game_over = True
                

        # Draw everything
        for star in scrolling_stars_list:
            star.draw(spaceBG)
        for laser in lasers:
            laser.draw(display)
        for asteroid in scrolling_asteroid_list:
            asteroid.draw(display)
        player_ship.draw(display)


        # Blit everything to the screen
        screen.blit(spaceBG, (0, 0))
        screen.blit(display, (0, 0))
        screen.blit(overlay, (0, 0))
        pygame.display.update()
        #clock.tick(FPS)

#Current test - 3 lives before game over, trying to make 0 hearts show for a second between losing last life and gameover screen showing
