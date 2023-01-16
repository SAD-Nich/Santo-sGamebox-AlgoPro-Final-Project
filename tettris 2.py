import pygame
from copy import deepcopy
from random import choice, randrange

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

#the actual game loop
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
                pygame.quit()
                exit()
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