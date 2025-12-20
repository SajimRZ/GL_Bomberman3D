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

#grid info
TILE_SIZE = 500  # 500 because it divies 5000 evenly, change tile size if grid changes.
GRID_ROWS = int((2 * GRID_LENGTH) / TILE_SIZE) 
GRID_COLS = int((2 * GRID_LENGTH) / TILE_SIZE)  
GRID_START_X = GRID_LENGTH
GRID_START_Y = -GRID_LENGTH

#Player info
player_pos = [GRID_LENGTH - TILE_SIZE, -GRID_LENGTH + TILE_SIZE, 0]
PLAYER_ANGLE = 0
PLAYER_SPEED = 10
PLAYER_RADIUS = 100

# Camera-related variables - behind player
camera_pos = [player_pos[0], player_pos[1] - 1000, player_pos[2] + 800]
CAMERA_SPEED = 5
CAMERA_THETA = 0
POV = 0  # 0: Third-person, 1: Top-down

target_pos = [player_pos[0], player_pos[1], player_pos[2]]

key_buffer = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}



#map info
game_map = [[EMPTY for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]


def initialize_game_map():
    global game_map
    
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            game_map[row][col] = EMPTY # everything empty first
    
    for row in range(2, GRID_ROWS - 1, 2):  #placing default walls
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

    world_x = GRID_START_X - (grid_col * TILE_SIZE)  # X decreases as col increases
    world_y = GRID_START_Y + (grid_row * TILE_SIZE)  # Y increases as row increases
    return world_x, world_y


def world_to_grid(world_x, world_y):

    grid_col = int((GRID_START_X - world_x) / TILE_SIZE)
    grid_row = int((world_y - GRID_START_Y) / TILE_SIZE)
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
    print("Top-left is (0,0), Bottom-right is ({},{})".format(GRID_ROWS-1, GRID_COLS-1))
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
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
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




#=================== Player Model ========================================

def drawPlayer():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2] + 23)
    glRotatef(-PLAYER_ANGLE,0,0,1)  
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
    glColor3f(*WHITE)
    glTranslatef(30,0,20)
    glScalef(1,1,2)
    gluCylinder(gluNewQuadric(), 15, 15, 60, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(*WHITE)
    glTranslatef(-30,0,20)
    glScalef(1,1,2)
    gluCylinder(gluNewQuadric(), 15, 15, 60, 10, 10)
    glPopMatrix()

    #Body
    glPushMatrix()
    glColor3f(0.3, 0.3, 1)
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
    glColor3f(*WHITE)
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
    glColor3f(*YELLOW)
    glTranslatef(0,-30,280)
    gluSphere(gluNewQuadric(), 15, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glPopMatrix()


    glPopMatrix()

#=================== Bomb Model ========================================
def drawBomb(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(math.sin(time.time()*5)*0.1 + 1, math.sin(time.time()*5)*0.1 + 1, math.sin(time.time()*5)*0.1 + 1)
    
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
def PlayerMovementThirdPerson(dt):
    global key_buffer,player_pos, camera_pos,PLAYER_ANGLE,PLAYER_SPEED, CAMERA_THETA, target_pos
    
    rot_speed = 80
    px, py, pz = player_pos
    cx, cy, cz = camera_pos

    pspeed = PLAYER_SPEED* 200 * dt

    dx = cx - px
    dy = cy - py
    radius = math.sqrt(dx*dx + dy*dy)
    nx, ny = 0, 0

    if key_buffer['up']:
        nx += pspeed * math.sin(math.radians(PLAYER_ANGLE))
        ny += pspeed * math.cos(math.radians(PLAYER_ANGLE))

    if key_buffer['down']:
        nx -= pspeed * math.sin(math.radians(PLAYER_ANGLE))
        ny -= pspeed * math.cos(math.radians(PLAYER_ANGLE))
    
    #check if next step hits a wall
    if not collides_with_wall(px+nx, py):
        px += nx
    if not collides_with_wall(px, py+ny):
        py += ny

    #check if current position is outside and clamp it
    px, py = clamp_to_map(px, py)
        
    if key_buffer['left']:
        PLAYER_ANGLE -= CAMERA_SPEED * rot_speed * dt
    if key_buffer['right']:
        PLAYER_ANGLE += CAMERA_SPEED * rot_speed * dt
  
    if key_buffer['left'] or key_buffer['right'] or key_buffer['up'] or key_buffer['down']:
        CAMERA_THETA = 0
        theta_rad = math.radians(PLAYER_ANGLE+180)
        cx = px + radius * math.sin(theta_rad)
        cy = py + radius * math.cos(theta_rad)

    player_pos = [px, py, pz]
    camera_pos = [cx, cy, cz]
    target_pos = [px, py, pz]

def PlayerMovementTopDown(dt):
    global key_buffer,player_pos, camera_pos,PLAYER_ANGLE,PLAYER_SPEED, CAMERA_THETA, target_pos
    
    pspeed = PLAYER_SPEED* 200 * dt
    px, py, pz = player_pos

    nx, ny = 0, 0

    if key_buffer['up']:
        PLAYER_ANGLE = 0
        ny += pspeed

    if key_buffer['down']:
        PLAYER_ANGLE = 180
        ny -= pspeed
    if key_buffer['left']:
        PLAYER_ANGLE = 270
        nx -= pspeed
    if key_buffer['right']:
        PLAYER_ANGLE = 90
        nx += pspeed
    
    #check if next step hits a wall
    if not collides_with_wall(px+nx, py):
        px += nx
    if not collides_with_wall(px, py+ny):
        py += ny

    #check if current position is outside and clamp it
    px, py = clamp_to_map(px, py)
        
    player_pos = [px, py, pz]
    #center of grid
    target_pos = [0, 0, 0]
    camera_pos = [0, 0, 6000]

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


#============= Delta Time ==================================
def delta_time():
    global last_time
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    return dt

def keyboardListener(key, x, y):
    global key_buffer, POV, camera_pos, player_pos

    if key == b'w':
         key_buffer['up'] = True
    if key == b's':
        key_buffer['down'] = True
    if key == b'a':
        key_buffer['left'] = True
    if key == b'd':
        key_buffer['right'] = True
    if key == b'e':
        camera_pos = [player_pos[0], player_pos[1] - 1000, player_pos[2] + 800]
        POV = (POV + 1) % 2  # Toggle between 0 and 1

def keyboardUpListener(key, x, y):
    if key == b'w':
         key_buffer['up'] = False
    if key == b's':
        key_buffer['down'] = False
    if key == b'a':
        key_buffer['left'] = False
    if key == b'd':
        key_buffer['right'] = False


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
            if tile == EMPTY:
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

def draw_ground():
        # Draw the grid (game floor)
    glBegin(GL_QUADS)
    
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)


    glColor3f(0.7, 0.5, 0.95)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -GRID_LENGTH, 0)

    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glEnd()



def idle():
    global POV
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    dt = delta_time()
    if POV == 0:
        PlayerMovementThirdPerson(dt)
    elif POV == 1:
        PlayerMovementTopDown(dt)


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

    # Draw a random points
    # glPointSize(20)
    # glBegin(GL_POINTS)
    # glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    # glEnd()
    
    draw_ground()
    
    # Draw the walls 
    draw_tiles()

    #Draw the player
    drawPlayer()
    drawBomb(GRID_LENGTH - TILE_SIZE, -GRID_LENGTH + TILE_SIZE, 0, )



    # Display game info text at a fixed screen position
    draw_text(10, 770, f"A Random Fixed Position Text")
    draw_text(10, 740, f"See how the position and variable change?: {rand_var}")


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
    glutKeyboardUpFunc(keyboardUpListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()