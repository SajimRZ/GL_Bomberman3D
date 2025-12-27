from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

last_time = time.time()

#COLORS
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
YELLOW = (1, 1, 0)
CYAN = (0, 1, 1)
MAGENTA = (1, 0, 1)
WHITE = (1, 1, 1)
BLACK = (0, 0, 0)
GRAY = (0.5, 0.5, 0.5)
AMBER = (1.0, 0.75, 0.0)
WHITE = (1, 1, 1)
BROWN = (0.5, 0.25, 0.0)
SILVER = (0.75, 0.75, 0.75)
GOLD = (1.0, 0.84, 0.0)
PLATINUM = (0.65, 0.65, 0.65)
IRON = (0.5, 0.5, 0.5)
COPPER = (0.85, 0.55, 0.25)
NICKEL = (0.75, 0.75, 0.75)
LEAD = (0.25, 0.25, 0.25)
TIN = (0.5, 0.5, 0.5)
DEEP_GREEN = (0, 0.5, 0)
SKIN = (1.0, 0.84, 0.53)
PINK = (1.0, 0.75, 0.8)
BROWN = (0.6, 0.4, 0.2)


#Screen
SCREEN_WIDTH = 1630
SCREEN_HEIGHT = 955


fovY = 90  # Field of view
GRID_LENGTH = 5000  
rand_var = 423

#walls
EMPTY = 0
INDESTRUCTIBLE_WALL = 1
DESTRUCTIBLE_WALL = 2
BOMB = 3

#grid info
TILE_SIZE = 500  # 500 because it divies 5000 evenly, change tile size if grid changes.
GRID_ROWS = int((2 * GRID_LENGTH) / TILE_SIZE)  + 1
GRID_COLS = int((2 * GRID_LENGTH) / TILE_SIZE)  + 1

GRID_START_X = GRID_LENGTH - (TILE_SIZE / 2)   # starting from middle of the tile
GRID_START_Y = -GRID_LENGTH + (TILE_SIZE / 2)  

#Player info
GAME_MODE = 0 # 0: Wave Survival, 1: Endless, 2: Multiplayer

# player_pos = [GRID_LENGTH - TILE_SIZE, -GRID_LENGTH + TILE_SIZE, 0]
player_pos = [GRID_START_X - TILE_SIZE, GRID_START_Y + TILE_SIZE, 0]
PLAYER_ANGLE = 0

POV = 0  # 0: Third-person, 1: Top-down
if POV == 0:
    PLAYER_SPEED = 50
elif POV == 1 and GAME_MODE == 2:
    PLAYER_SPEED = 200
PLAYER_RADIUS = 100

player_two_pos = [ -GRID_START_X, -GRID_START_Y , 0]
player_two_angle = 180

#Player stats
MAX_HEALTH = 100
CURRENT_HEALTH = MAX_HEALTH

# Camera-related variables - behind player
camera_pos = [player_pos[0], player_pos[1] - 1000, player_pos[2] + 800]
CAMERA_SPEED = 5
CAMERA_THETA = 0

#
#bomb info
PULSE_RATE = 5
EXPLOTION_TIME = 3

MAX_EXPLOSION_RADIUS = 3
EXPLOTION_RADIUS = MAX_EXPLOSION_RADIUS # in tiles  === Upgradable =====

MAX_NUMBER_OF_BOMBS = 1
NUMBER_OF_BOMBS = MAX_NUMBER_OF_BOMBS  #=== Upgradable =====

MAX_BOMB_DAMAGE = 10
BOMB_DAMAGE = MAX_BOMB_DAMAGE  #=== Upgradable =====

target_pos = [player_pos[0], player_pos[1], player_pos[2]]


key_buffer = {
    'up': 0,
    'down': 0,
    'left': 0,
    'right': 0,
    'up2': 0,
    'down2': 0,
    'left2': 0,
    'right2': 0,
}


#map info
game_map = [[EMPTY for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]


#bomb info
ALL_BOMBS = [] # list of all bombs, [x, y, time_to_explode], the x and y will follow game_map


#Upgrade Screen info 
show_upgrade_menu = False

upgrade_options = {
    "Bomb Number": NUMBER_OF_BOMBS,
    "Explosion Radius": EXPLOTION_RADIUS,
    "Bomb Damage": BOMB_DAMAGE,
    "Heal up": CURRENT_HEALTH,
}
cursor_pos = 0



def initialize_game_map():
    global game_map
    
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            game_map[row][col] = EMPTY # everything empty first
    
    # Place indestructible walls on the OUTER BORDER (row 0, row 19, col 0, col 19)
    for row in range(GRID_ROWS):
        game_map[row][0] = INDESTRUCTIBLE_WALL              # Left edge
        game_map[row][GRID_COLS - 1] = INDESTRUCTIBLE_WALL  # Right edge
    for col in range(GRID_COLS):
        game_map[0][col] = INDESTRUCTIBLE_WALL              # Top edge
        game_map[GRID_ROWS - 1][col] = INDESTRUCTIBLE_WALL  # Bottom edge
    
    # Place inner indestructible walls in grid pattern
    for row in range(2, GRID_ROWS - 1, 2):
        for col in range(2, GRID_COLS - 1, 2):  
            game_map[row][col] = INDESTRUCTIBLE_WALL
    

    # generating destructible walls
    for row in range(1, GRID_ROWS - 1):
        for col in range(1, GRID_COLS - 1):
            
            if game_map[row][col] == INDESTRUCTIBLE_WALL:
                continue
            
            if row <= 2 and col <= 2:
                continue
            if row <= 2 and col >= GRID_COLS - 3:  # Top-right
                continue
            if row >= GRID_ROWS - 3 and col <= 2:  # Bottom-left
                continue
            if row >= GRID_ROWS - 3 and col >= GRID_COLS - 3:  # Bottom-right
                continue
            
            # generate wall with changes
            if random.random() < 0.25:
                game_map[row][col] = DESTRUCTIBLE_WALL


def grid_to_world(grid_row, grid_col):

    world_x = GRID_START_X - (grid_col * TILE_SIZE) # X decreases as col increases
    world_y = GRID_START_Y + (grid_row * TILE_SIZE) # Y increases as row increases
    return world_x, world_y


def world_to_grid(world_x, world_y):
    grid_col = round((GRID_START_X - world_x) / TILE_SIZE)
    grid_row = round((world_y - GRID_START_Y) / TILE_SIZE)
    return grid_row, grid_col


def get_tile_at_position(world_x, world_y):

    grid_row, grid_col = world_to_grid(world_x, world_y)
    
    # Check bounds
    if 0 <= grid_row < GRID_ROWS and 0 <= grid_col < GRID_COLS:
        return game_map[grid_row][grid_col]
    return None

def get_tile_type(world_x, world_y):

    tile = get_tile_at_position(world_x, world_y)
    return tile

def print_game_map():

    print("\n=== GAME MAP ===")
    # print(f"Grid size: {GRID_ROWS}x{GRID_COLS}")
    # print(f"GRID_START: ({GRID_START_X}, {GRID_START_Y})")
    # print(f"Tile (0,0) at world: {grid_to_world(0, 0)}")
    # print(f"Tile (0,{GRID_COLS-1}) at world: {grid_to_world(0, GRID_COLS-1)}")
    # print(f"Tile ({GRID_ROWS-1},0) at world: {grid_to_world(GRID_ROWS-1, 0)}")
    # print(f"Tile ({GRID_ROWS-1},{GRID_COLS-1}) at world: {grid_to_world(GRID_ROWS-1, GRID_COLS-1)}")
    # print(f"Boundary walls at: ±{GRID_LENGTH}")
    # print(f"Edge tile coverage: {GRID_START_X - TILE_SIZE/2} to {GRID_START_X + TILE_SIZE/2}")
    # print()
    for row in range(GRID_ROWS):
        line = ""
        for col in range(GRID_COLS):
            tile = game_map[row][col]
            if tile == EMPTY:
                line += ". "
            elif tile == INDESTRUCTIBLE_WALL:
                line += "# "
            elif tile == DESTRUCTIBLE_WALL:
                line += "X "
        print(line)
    print("================\n")


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

#===================== Ortho Upgrade Menu ===============================
def draw_upgrade_menu():
    global upgrade_options, cursor_pos
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    panel_w = 600
    panel_h = 400
    panel_x = (SCREEN_WIDTH - panel_w) // 2
    panel_y = (SCREEN_HEIGHT - panel_h) // 2

    #Panel
    glColor4f(0.3, 0.3, 0.3, 0.9)  # gray
    glBegin(GL_QUADS)
    glVertex2f(panel_x, panel_y)
    glVertex2f(panel_x + panel_w, panel_y)
    glVertex2f(panel_x + panel_w, panel_y + panel_h)
    glVertex2f(panel_x, panel_y + panel_h)
    glEnd()

    #Title
    draw_text(panel_x, panel_y + panel_h - 50, "Select an Upgrade")
    
    #Options
    start_y = panel_y + panel_h - 120
    for i, [option, value] in enumerate(upgrade_options.items()):
        if i == cursor_pos: #where cursor currently is
            glColor3f(1,1,0)
            prefix  = "> "
        else:
            glColor3f(1,1,1)
            prefix = "  "
        
        draw_text(panel_x, start_y - i * 40, f"{prefix}{option}: {value} + 1") #the option text

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)



#=================== Player Model ========================================

def drawPlayer(num=1):

    glPushMatrix()
    if num == 1:
        glTranslatef(player_pos[0], player_pos[1], player_pos[2] + 23)
        glRotatef(-PLAYER_ANGLE,0,0,1)  
    else:
        glTranslatef(player_two_pos[0], player_two_pos[1], player_two_pos[2] + 23)
        glRotatef(-player_two_angle,0,0,1)

    glScalef(1.5,1.5,1.5)
    #feet
    glPushMatrix()
    glColor3f(*PINK)
    glTranslatef(30,0,0)
    glutSolidSphere(20,20,20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(*PINK)
    glTranslatef(-30,0,0)
    glutSolidSphere(20,20,20)
    glPopMatrix()
    
    #Legs
    glPushMatrix()
    if num == 1:
        glColor3f(*WHITE)
    else:
        glColor3f(*GRAY)
    glTranslatef(30,0,20)
    glScalef(1,1,2)
    gluCylinder(gluNewQuadric(), 15, 15, 60, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-30,0,20)
    glScalef(1,1,2)
    gluCylinder(gluNewQuadric(), 15, 15, 60, 10, 10)
    glPopMatrix()

    #Body
    glPushMatrix()
    if num == 1:
        glColor3f(0.3, 0.3, 1)
    else:
        glColor3f(1, 0.3, 0.3)
    glTranslatef(0,0,130)
    glScalef(1.3,0.8,1.5)
    gluSphere(gluNewQuadric(), 40, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()

    #Arms
    glPushMatrix()
    glColor3f(*SKIN)
    glTranslatef(40,0,150)
    glRotatef(45+90,0,1,0)
    glScalef(1,1,1)
    gluCylinder(gluNewQuadric(), 12, 8, 90, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(*SKIN)
    glTranslatef(-40,0,150)
    glRotatef(-45-90,0,1,0)
    glScalef(1,1,1)
    gluCylinder(gluNewQuadric(), 12, 12, 90, 10, 10)
    glPopMatrix()

    #Hands
    glPushMatrix()
    glColor3f(*PINK)
    glTranslatef(100,0,90)
    gluSphere(gluNewQuadric(), 15, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()

    glPushMatrix()
    glColor3f(*PINK)
    glTranslatef(-100,0,90)
    gluSphere(gluNewQuadric(), 15, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()

    #Head
    glPushMatrix()
    if num == 1:
        glColor3f(*WHITE)
    else:
        glColor3f(*GRAY)
    glTranslatef(0,0,220)
    glScalef(1.5,1,1.5)
    gluSphere(gluNewQuadric(), 30, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()

    glPushMatrix()
    glColor3f(*SKIN)
    glTranslatef(0,8,220)
    glScalef(1.2,1,1)
    gluSphere(gluNewQuadric(), 30, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()

    #head thing
    glPushMatrix()
    glColor3f(*DEEP_GREEN)
    glTranslatef(0,0,250)
    glRotatef(45,1,0,0)
    gluCylinder(gluNewQuadric(), 5, 5, 40, 10, 10)
    glPopMatrix()

    glPushMatrix()
    if num == 1:
        glColor3f(*YELLOW)
    else:
        glColor3f(*AMBER)
    glTranslatef(0,-30,280)
    gluSphere(gluNewQuadric(), 15, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()


    glPopMatrix()

#=================== Bomb Model ========================================
def drawBomb(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(math.sin(time.time()*PULSE_RATE)*0.1 + 1, math.sin(time.time()*PULSE_RATE)*0.1 + 1, math.sin(time.time()*PULSE_RATE)*0.1 + 1)
    
    glPushMatrix()
    #glColor3f(0.5, 0.4, 1)
    glColor3f(math.sin(time.time())*0.5 +0.5,  math.cos(time.time())*0.5 +0.5, math.cos(time.time())*0.5 +0.5)
    glTranslatef(0,0,100)
    gluSphere(gluNewQuadric(), 100, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()

    glPushMatrix()
    glColor3f(*BLACK)
    glTranslatef(0,0,190)
    glutSolidCube(50)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(0,0,210)
    glRotatef(45,1,0,0)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 10)
    glPopMatrix()

    #fuse
    glPushMatrix()
    glColor3f(1, 0.5, 0)
    glTranslatef(0,-40,255)
    gluSphere(gluNewQuadric(), 20, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()


    glPopMatrix()



#=================   Player Movement ===============================
def PlayerMovementThirdPerson(pspeed):
    global key_buffer,player_pos, camera_pos,PLAYER_ANGLE,PLAYER_SPEED, CAMERA_THETA, target_pos

    rot_speed = 80
    px, py, pz = player_pos
    cx, cy, cz = camera_pos

    dx = cx - px
    dy = cy - py
    radius = math.sqrt(dx*dx + dy*dy)

    nx, ny = 0, 0

    nx += pspeed * math.sin(math.radians(PLAYER_ANGLE))
    ny += pspeed * math.cos(math.radians(PLAYER_ANGLE))

    #check if next step hits a wall
    if not collides_with_wall(px+nx, py):
        px += nx
    if not collides_with_wall(px, py+ny):
        py += ny

    #check if current position is outside and clamp it
    px, py = clamp_to_map(px, py)

    CAMERA_THETA = 0
    theta_rad = math.radians(PLAYER_ANGLE+180)
    cx = px + radius * math.sin(theta_rad)
    cy = py + radius * math.cos(theta_rad)

    player_pos = [px, py, pz]
    camera_pos = [cx, cy, cz]
    target_pos = [px, py, pz]
    

def PlayerMovementTopDown(pxspd, pyspd, pangle, num=1):
    global key_buffer,player_pos, camera_pos,PLAYER_ANGLE,PLAYER_SPEED, CAMERA_THETA, target_pos
    global player_two_pos, player_two_angle
    
    if num == 1:
        px, py, pz = player_pos
        nx, ny = 0, 0
        nx += pxspd
        ny += pyspd

        PLAYER_ANGLE = pangle
        
        #check if next step hits a wall
        if not collides_with_wall(px+nx, py):
            px += nx
        if not collides_with_wall(px, py+ny):
            py += ny

        #check if current position is outside and clamp it
        px, py = clamp_to_map(px, py)

        player_pos = [px, py, pz]
    elif GAME_MODE == 2 and num == 2:
        px, py, pz = player_two_pos
        nx, ny = 0, 0
        nx += pxspd
        ny += pyspd

        player_two_angle = pangle
        
        #check if next step hits a wall
        if not collides_with_wall(px+nx, py):
            px += nx
        if not collides_with_wall(px, py+ny):
            py += ny

        #check if current position is outside and clamp it
        px, py = clamp_to_map(px, py)

        player_two_pos = [px, py, pz]
    
    
    #center of grid
    target_pos = [0, 500, 0]
    camera_pos = [0, 500, 6500]

def player_turn3P(cam_speed):
    global key_buffer,player_pos, camera_pos,PLAYER_ANGLE,PLAYER_SPEED, CAMERA_THETA, target_pos
    
    px, py, pz = player_pos
    cx, cy, cz = camera_pos
    dx = cx - px
    dy = cy - py
    radius = math.sqrt(dx*dx + dy*dy)
    
    PLAYER_ANGLE += cam_speed * 5

    CAMERA_THETA = 0
    theta_rad = math.radians(PLAYER_ANGLE+180)
    cx = px + radius * math.sin(theta_rad)
    cy = py + radius * math.cos(theta_rad)

    camera_pos = [cx, cy, cz]

#==============  Collosion Detection ===========================
def collides_with_wall(x, y):
    global PLAYER_RADIUS

    row, col = world_to_grid(x, y)

    wall_half = TILE_SIZE / 2

    # Check nearby tiles only
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
                if game_map[r][c] in (INDESTRUCTIBLE_WALL, DESTRUCTIBLE_WALL):

                    wx, wy = grid_to_world(r, c)

                    # Wall BBOX
                    minx = wx - wall_half
                    maxx = wx + wall_half
                    miny = wy - wall_half
                    maxy = wy + wall_half

                    # Closest point on wall to player center
                    closest_x = max(minx, min(x, maxx))
                    closest_y = max(miny, min(y, maxy))

                    dx = x - closest_x
                    dy = y - closest_y

                    if (dx * dx + dy * dy) <= (PLAYER_RADIUS * PLAYER_RADIUS):
                        return True

    return False
def clamp_to_map(x, y):
    global PLAYER_RADIUS
    min_x = -GRID_LENGTH + PLAYER_RADIUS
    max_x =  GRID_LENGTH - PLAYER_RADIUS
    min_y = -GRID_LENGTH + PLAYER_RADIUS
    max_y =  GRID_LENGTH - PLAYER_RADIUS

    x = max(min_x, min(x, max_x))
    y = max(min_y, min(y, max_y))
    return x, y

#
#============= Bomb Placement ==============================

def draw_allBombs():
    global ALL_BOMBS
    for bomb in ALL_BOMBS:
        gridx, gridy = bomb[0], bomb[1]
        world_x, world_y = grid_to_world(gridx, gridy)
        drawBomb(world_x, world_y, 0)

#============= Delta Time ==================================
def delta_time():
    global last_time
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    return dt

def keyboardListener(key, x, y):
    global key_buffer,player_pos, camera_pos,PLAYER_ANGLE,PLAYER_SPEED, CAMERA_THETA, target_pos, POV, GAME_MODE
    global show_upgrade_menu

    if key == b'w':
        if POV == 0:
            PlayerMovementThirdPerson(PLAYER_SPEED)
        elif POV == 1:
            PlayerMovementTopDown(0, PLAYER_SPEED, 0)


    if key == b's':
        if POV == 0:
            PlayerMovementThirdPerson(-PLAYER_SPEED)
        elif POV == 1:
            PlayerMovementTopDown(0, -PLAYER_SPEED, 180)

    if key == b'a':
        if POV == 0:
            player_turn3P(-CAMERA_SPEED)
        elif POV == 1:
            PlayerMovementTopDown(-PLAYER_SPEED, 0, 270)

    if key == b'd':
        if POV == 0:
            player_turn3P(CAMERA_SPEED)
        elif POV == 1:
            PlayerMovementTopDown(PLAYER_SPEED, 0, 90)

    if key == b'e':
        if GAME_MODE == 0:
            if POV == 1:
                camera_pos = [player_pos[0], player_pos[1] - 1000, player_pos[2] + 800]
            else:
                camera_pos = [0, 500, 6500]
                target_pos = [0, 500, 0]
            POV = (POV + 1) % 2  # Toggle between 0 and 1

    if key == b' ':
        px, py, pz = player_pos
        grid_row, grid_col = world_to_grid(px, py)

        # Check bounds
        if 0 <= grid_row < GRID_ROWS and 0 <= grid_col < GRID_COLS:
            tile_type = game_map[grid_row][grid_col]
            print(f"Tile type at ({grid_row}, {grid_col}): {tile_type}")
            print(f"  (0=EMPTY, 1=INDESTRUCTIBLE, 2=DESTRUCTIBLE, 3=BOMB)")
                

            if tile_type == EMPTY:
                game_map[grid_row][grid_col] = BOMB
                ALL_BOMBS.append([grid_row, grid_col, time.time() + EXPLOTION_TIME])
                print(f"✅ Bomb placed at grid ({grid_row}, {grid_col})")
            else:
                print(f"❌ Cannot place bomb - tile occupied (type: {tile_type})")
        else:
            print(f"❌ Out of bounds: ({grid_row}, {grid_col})")
            print("===========================\n")

    #temporary
    if key == b'm':
        show_upgrade_menu = not show_upgrade_menu

# def keyboardUpListener(key, x, y):
#     if key == b'w':
#          key_buffer['up'] = False
#     if key == b's':
#         key_buffer['down'] = False
#     if key == b'a':
#         key_buffer['left'] = False
#     if key == b'd':
#         key_buffer['right'] = False



def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, CAMERA_THETA, CAMERA_SPEED, player_pos
    x, y, z = camera_pos
    px, py, pz = player_pos
    #calculate radius from player to camera
    dx = x - px
    dy = y - py
    radius = math.sqrt(dx*dx + dy*dy)
    if GAME_MODE != 2:
        if POV == 0:
            if key == GLUT_KEY_LEFT:
                CAMERA_THETA -= 12
                final_angle = PLAYER_ANGLE + CAMERA_THETA

                theta_rad = math.radians(final_angle + 180)

                x = px + radius * math.sin(theta_rad)
                y = py + radius * math.cos(theta_rad)

                camera_pos = [x, y, z]
                
            if key == GLUT_KEY_RIGHT:
                CAMERA_THETA += 12
                final_angle = PLAYER_ANGLE + CAMERA_THETA

                theta_rad = math.radians(final_angle + 180)

                x = px + radius * math.sin(theta_rad)
                y = py + radius * math.cos(theta_rad)

                camera_pos = [x, y, z]
    else:
        if key == GLUT_KEY_LEFT:
            PlayerMovementTopDown(-PLAYER_SPEED, 0, 270, num=2)
        if key == GLUT_KEY_RIGHT:
            PlayerMovementTopDown(PLAYER_SPEED, 0, 90, num=2)
        if key == GLUT_KEY_UP:
            PlayerMovementTopDown(0, PLAYER_SPEED, 0, num=2)
        if key == GLUT_KEY_DOWN:
            PlayerMovementTopDown(0, -PLAYER_SPEED, 180, num=2)


# def SpecialKeyUpListener(key, x, y):
#     if key == GLUT_KEY_LEFT:
#         key_buffer['left2'] = False
#     if key == GLUT_KEY_RIGHT:
#         key_buffer['right2'] = False
#     if key == GLUT_KEY_UP:
#         key_buffer['up2'] = False
#     if key == GLUT_KEY_DOWN:
#         key_buffer['down2'] = False

def mouseListener(button, state, x, y):
    ...


def setupCamera():
    global POV, camera_pos, target_pos
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, SCREEN_WIDTH / SCREEN_HEIGHT, 0.1, 9000) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x, y, z = camera_pos
    a, b, c = target_pos
    
    if POV == 1:  # top-down
        gluLookAt(x, y, z,
                a, b, c,
                0, 1, 0)  
    else:         # third-person
        gluLookAt(x, y, z,
                a, b, c,
                0, 0, 1)
    
def draw_tiles():
    
    scale = 1.2

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            tile = game_map[row][col]
            if tile == EMPTY or tile == BOMB:
                continue

            world_x, world_y = grid_to_world(row, col)
            
            # Draw the wall cube
            glPushMatrix()
            glTranslatef(world_x, world_y, TILE_SIZE / 2)  
            glColor3f(*BLACK)
            glutSolidCube(TILE_SIZE * 0.9)
            glPopMatrix()
            
    
            glPushMatrix()
            glTranslatef(world_x, world_y, TILE_SIZE / 2)
            glScalef(scale, 1, 1)
            if tile == INDESTRUCTIBLE_WALL:
                glColor3f(*GRAY)  
            elif tile == DESTRUCTIBLE_WALL:
                glColor3f(*BROWN) 
            glutSolidCube(TILE_SIZE * 0.8)
            glPopMatrix()
            
            
            glPushMatrix()
            glTranslatef(world_x, world_y, TILE_SIZE / 2)
            glScalef(1, scale, 1)
            
            # Different colors for different wall types
            if tile == INDESTRUCTIBLE_WALL:
                glColor3f(*GRAY)  
            elif tile == DESTRUCTIBLE_WALL:
                glColor3f(*BROWN) 
            glutSolidCube(TILE_SIZE * 0.8)
            glPopMatrix()
            
            glPushMatrix()
            glTranslatef(world_x, world_y, TILE_SIZE / 2)
            glScalef(1, 1, scale)
            
            # Different colors for different wall types
            if tile == INDESTRUCTIBLE_WALL:
                glColor3f(*GRAY)  
            elif tile == DESTRUCTIBLE_WALL:
                glColor3f(*BROWN) 
            glutSolidCube(TILE_SIZE * 0.8)
            glPopMatrix()

def draw_walls():
    # it's brokem right now
    wall_cords = {
        "front": [[-GRID_LENGTH, GRID_LENGTH, 0], [GRID_LENGTH, GRID_LENGTH, 0], [GRID_LENGTH, GRID_LENGTH, 700], [-GRID_LENGTH, GRID_LENGTH, 700]],
        "left": [[-GRID_LENGTH, GRID_LENGTH, 0], [-GRID_LENGTH, -GRID_LENGTH, 0], [-GRID_LENGTH, -GRID_LENGTH, 700], [-GRID_LENGTH, GRID_LENGTH, 700]],
        "back": [[-GRID_LENGTH, -GRID_LENGTH, 0], [GRID_LENGTH, -GRID_LENGTH, 0], [GRID_LENGTH, -GRID_LENGTH, 700], [-GRID_LENGTH, -GRID_LENGTH, 700]],
        "right": [[GRID_LENGTH, GRID_LENGTH, 0], [GRID_LENGTH, -GRID_LENGTH, 0], [GRID_LENGTH, -GRID_LENGTH, 700], [GRID_LENGTH, GRID_LENGTH, 700]],
    }
    colors = {
        "front": WHITE,
        "right": GREEN,
        "back": BLUE,
        "left": CYAN,
    }
    for wall in wall_cords:
        glBegin(GL_QUADS)
        glColor3f(*colors[wall])
        for cord in wall_cords[wall]:
            glVertex3f(cord[0], cord[1], cord[2])
        glEnd()

def draw_ground(n):
    # Draw the grid (game floor)

    glBegin(GL_QUADS)
    col1 = [0.3,0.4,0.6]
    col2 = [0.7, 0.5, 0.9]

    for i in range(-n//2, n//2):
        for j in range(-n//2 + 1, n//2 + 1):
            if (i+j)%2==0:
                glColor3f(col1[0], col1[1], col1[2])
            else:
                glColor3f(col2[0], col2[1], col2[2])
            glVertex3f(i*TILE_SIZE, j*TILE_SIZE, 0)
            glVertex3f((i+1)*TILE_SIZE, j*TILE_SIZE, 0)
            glVertex3f((i+1)*TILE_SIZE, (j+1)*TILE_SIZE, 0)
            glVertex3f(i*TILE_SIZE, (j+1)*TILE_SIZE, 0)
    glEnd()



def idle():
    global POV, GAME_MODE
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    dt = delta_time()
    if GAME_MODE == 2:
        POV = 1


    glutPostRedisplay()

def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClearColor(*BLACK, 1.0)
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)  # Set viewport size

    setupCamera()  # Configure camera perspective
    
    draw_ground(GRID_COLS)
    
    # Draw the walls 
    draw_tiles()

    #Draw the player
    # drawBomb(GRID_LENGTH - TILE_SIZE, -GRID_LENGTH + TILE_SIZE, 0, )
    draw_allBombs()
    drawPlayer(1)
    if GAME_MODE == 2:
        drawPlayer(2)
    #drawBomb(GRID_LENGTH - TILE_SIZE, -GRID_LENGTH + TILE_SIZE, 0, )


    # ============= All ortho things after here ================

    #glClear(GL_DEPTH_BUFFER_BIT) #remove the depth before drawing ortho stufff
    if show_upgrade_menu:
        draw_upgrade_menu()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D Bomberman 3D")  # Create the window
    
    # Initialize the game map
    initialize_game_map()
    print_game_map()  # Print map to console for debugging
    draw_walls()

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    
    # glutKeyboardUpFunc(keyboardUpListener)
    # glutSpecialUpFunc(SpecialKeyUpListener)
    
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
