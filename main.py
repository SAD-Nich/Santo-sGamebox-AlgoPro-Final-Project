import pygame, sys
import random
import os
from button import Button
from copy import deepcopy
from random import choice, randrange

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    W, H = 10, 20
    TILE = 34
    GAME_RES = W * TILE, H * TILE
    RES = 1280, 720
    FPS = 60

    pygame.init()
    sc = pygame.display.set_mode(RES)
    game_sc = pygame.Surface(GAME_RES)
    clock = pygame.time.Clock()

    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

    blocks_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                [(0, 0), (0, -1), (0, 1), (-1, -1)],
                [(0, 0), (0, -1), (0, 1), (1, -1)],
                [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    blocks = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in blocks_pos]
    block_rect = pygame.Rect(0, 0, TILE - 3, TILE - 4)
    field = [[0 for i in range(W)] for k in range(H)] #this will be the map of the tetris blocky area

    anim_count, anim_speed, anim_limit = 0, 60, 2000

    bg = pygame.image.load('imgs/blue.png').convert()
    game_bg = pygame.image.load('imgs/black.jpg').convert()

    main_font = pygame.font.Font('font.ttf', 65)
    font = pygame.font.Font('font.ttf', 45)

    maintitle = main_font.render("Santo's TETRIS", True, pygame.Color('darkblue'))
    scoretext = font.render('score:', True, pygame.Color('green'))
    records = font.render('record:', True, pygame.Color('purple'))
    quitbutton = font.render('if you want to quit, press ESC', True, pygame.Color('white'))

    get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

    block, next_block = deepcopy(choice(blocks)), deepcopy(choice(blocks))
    color, next_color = get_color(), get_color()

    score, lines = 0, 0
    scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    #game borders so that the blocks are centered and aligned
    def borders():
        if block[i].x < 0 or block[i].x > W - 1:
            return False
        elif block[i].y > H - 1 or field[block[i].y][block[i].x]:
            return False
        return True

    #accessing fie to get the records and to store them
    def gettingrec():
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    #setting the best records accordint to the database
    def set_record(record, score):
        rec = max(int(record), score)
        with open('record', 'w') as f:
            f.write(str(rec))
    while True:
        record = gettingrec()
        dx, rotate = 0, False
        sc.blit(bg, (0, 0))
        sc.blit(game_sc, (17, 17))
        game_sc.blit(game_bg, (0, 0))
    
    # delay for full lines

        for i in range(lines):
            pygame.time.wait(100)
    
    # controls using arrow keys
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    anim_limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True
                elif event.key == pygame.K_ESCAPE:
                    main_menu()
                    pygame.quit()
        # x-axis movement
        block_old = deepcopy(block)
        for i in range(4):
            block[i].x += dx
            if not borders():
                block = deepcopy(block_old)
                break
        # y-axis movement
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            block_old = deepcopy(block)
            for i in range(4):
                block[i].y += 1
                if not borders():
                    for i in range(4):
                        field[block_old[i].y][block_old[i].x] = color
                    block, color = next_block, next_color
                    next_block, next_color = deepcopy(choice(blocks)), get_color()
                    anim_limit = 2000
                    break
        # rotating the blocks
        center = block[0]
        block_old = deepcopy(block)
        if rotate:
            for i in range(4):
                x = block[i].y - center.y
                y = block[i].x - center.x
                block[i].x = center.x - x
                block[i].y = center.y + y
                if not borders():
                    block = deepcopy(block_old)
                    break
        # check lines for the blocks tht are in the same line as the original tetris game
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
        # score addition
        score += scores[lines]
        # drawing the grid and the colors of the grid
        [pygame.draw.rect(game_sc, (50, 0, 0), i_rect, 2) for i_rect in grid]
        # the blocks
        for i in range(4):
            block_rect.x = block[i].x * TILE
            block_rect.y = block[i].y * TILE
            pygame.draw.rect(game_sc, color, block_rect)
        # drawing the playing field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    block_rect.x, block_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, block_rect)
        # spawning the blocks
        for i in range(4):
            block_rect.x = next_block[i].x * TILE + 400
            block_rect.y = next_block[i].y * TILE + 185
            pygame.draw.rect(sc, next_color, block_rect)
        # drawing the scoreboard and title
        sc.blit(maintitle, (500, 10))
        sc.blit(scoretext, (535, 340))
        sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 400))
        sc.blit(records, (525, 500))
        sc.blit(font.render(record, True, pygame.Color('gold')), (550, 550))
        sc.blit(quitbutton, (450, 650))
        # game over
        for i in range(W):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for i_rect in grid:
                    pygame.draw.rect(game_sc, get_color(), i_rect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)

        pygame.display.flip()
        clock.tick(FPS)
            
def Dinorun():
    pygame.init()
    # Global Constants
    SCREEN_HEIGHT = 720
    SCREEN_WIDTH = 1280
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #Movement
    RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
            pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
    JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
    DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
            pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
    #Obstacle
    SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
    LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

    BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
            pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

    CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

    BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

    #Hitboxes and Image calls
    class Dinosaur:
        X_POS = 80
        Y_POS = 310
        Y_POS_DUCK = 340
        JUMP_VEL = 8.5

        def __init__(self):
            self.duck_img = DUCKING
            self.run_img = RUNNING
            self.jump_img = JUMPING

            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

            self.step_index = 0
            self.jump_vel = self.JUMP_VEL
            self.image = self.run_img[0]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS

        def update(self, userInput):
            if self.dino_duck:
                self.duck()
            if self.dino_run:
                self.run()
            if self.dino_jump:
                self.jump()

            if self.step_index >= 10:
                self.step_index = 0

            if userInput[pygame.K_UP] and not self.dino_jump:
                self.dino_duck = False
                self.dino_run = False
                self.dino_jump = True
            elif userInput[pygame.K_DOWN] and not self.dino_jump:
                self.dino_duck = True
                self.dino_run = False
                self.dino_jump = False
            elif not (self.dino_jump or userInput[pygame.K_DOWN]):
                self.dino_duck = False
                self.dino_run = True
                self.dino_jump = False

        def duck(self):
            self.image = self.duck_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS_DUCK
            self.step_index += 1

        def run(self):
            self.image = self.run_img[self.step_index // 5]
            self.dino_rect = self.image.get_rect()
            self.dino_rect.x = self.X_POS
            self.dino_rect.y = self.Y_POS
            self.step_index += 1

        def jump(self):
            self.image = self.jump_img
            if self.dino_jump:
                self.dino_rect.y -= self.jump_vel * 4
                self.jump_vel -= 0.8
            if self.jump_vel < - self.JUMP_VEL:
                self.dino_jump = False
                self.jump_vel = self.JUMP_VEL

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    #Cloud image generation functions
    class Cloud:
        def __init__(self):
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)
            self.image = CLOUD
            self.width = self.image.get_width()

        def update(self):
            self.x -= game_speed
            if self.x < -self.width:
                self.x = SCREEN_WIDTH + random.randint(2500, 3000)
                self.y = random.randint(50, 100)

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.x, self.y))

    #Obstacle Hitboxes and Generators
    class Obstacle:
        def __init__(self, image, type):
            self.image = image
            self.type = type
            self.rect = self.image[self.type].get_rect()
            self.rect.x = SCREEN_WIDTH

        def update(self):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                obstacles.pop()

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.type], self.rect)


    class SmallCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 325


    class LargeCactus(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 300


    class Bird(Obstacle):
        def __init__(self, image):
            self.type = 0
            super().__init__(image, self.type)
            self.rect.y = 250
            self.index = 0

        def draw(self, SCREEN):
            if self.index >= 9:
                self.index = 0
            SCREEN.blit(self.image[self.index//5], self.rect)
            self.index += 1

    #main function to run the game
    def main():
        global game_speed, x_pos_bg, y_pos_bg, points, obstacles
        run = True
        clock = pygame.time.Clock()
        player = Dinosaur()
        cloud = Cloud()
        game_speed = 20
        x_pos_bg = 0
        y_pos_bg = 380
        points = 0
        font = pygame.font.Font('freesansbold.ttf', 20)
        obstacles = []
        death_count = 0

        def score():
            global points, game_speed
            points += 1
            if points % 100 == 0:
                game_speed += 1/5

            text = font.render("Points: " + str(points), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            SCREEN.blit(text, textRect)

        def background():
            global x_pos_bg, y_pos_bg
            image_width = BG.get_width()
            SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            if x_pos_bg <= -image_width:
                SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= game_speed

        while run:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    run = False

            SCREEN.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()

            player.draw(SCREEN)
            player.update(userInput)

            if len(obstacles) == 0:
                if random.randint(0, 2) == 0:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 2) == 1:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 2) == 2:
                    obstacles.append(Bird(BIRD))

            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(100)
                    death_count += 1
                    menu(death_count)

            background()
            cloud.draw(SCREEN)
            cloud.update()
            score()
            clock.tick(30)
            pygame.display.update()

    #Menu and after Death or when the Dinosaur is destroyed
    def menu(death_count):
        global points
        run = True
        while run:
            SCREEN.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 30)
            userInput = pygame.key.get_pressed()

            if death_count == 0:
                text = font.render("Press SPACE to Start", True, (0, 0, 0))
            elif death_count > 0:
                text = font.render("Press SPACE to Restart or ESC to Stop", True, (0, 0, 0))
                score = font.render("Your Score: " + str(points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                SCREEN.blit(score, scoreRect)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if userInput[pygame.K_SPACE]:
                    main()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_menu()


    menu(death_count=0)

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(70).render("Santo's Gamebox", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 250), 
                            text_input="Tetris", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        DINO_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="Dino Run", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, DINO_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if DINO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Dinorun()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()