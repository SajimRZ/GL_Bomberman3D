from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
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

# Camera-related variables - behind player
camera_pos = [player_pos[0], player_pos[1] + 1500, player_pos[2] + 1500]
CAMERA_SPEED = 5
CAMERA_THETA = 0

target_pos = [player_pos[0], player_pos[1], player_pos[2]]



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


#=================== Player Model =========================
def drawPlayer():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2] + 75)  # Move to player position
    #feet
    glPushMatrix()
    glColor3f(*PINK)
    glTranslatef(10,0,0)
    glutSolidSphere(20,20,20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(*PINK)
    glTranslatef(-10,0,0)
    glutSolidSphere(20,20,20)
    glPopMatrix()
    glPopMatrix()


def keyboardListener(key, x, y):
   ...


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, CAMERA_THETA, CAMERA_SPEED
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        z += CAMERA_SPEED * 10  # Small angle decrement for smooth movement
        camera_pos = (x, y, z)
    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        z -= CAMERA_SPEED * 10  # Small angle decrement for smooth movement
        camera_pos = (x, y, z)

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        CAMERA_THETA += CAMERA_SPEED
        # Calculate radius from current position
        radius = math.sqrt(x*x + y*y)
        # Convert angle to radians and calculate new position
        theta_rad = math.radians(CAMERA_THETA)
        x = radius * math.sin(theta_rad)
        y = radius * math.cos(theta_rad)
        
        camera_pos = (x, y, z)
        

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        CAMERA_THETA -= CAMERA_SPEED
        # Calculate radius from current position
        radius = math.sqrt(x*x + y*y)
        # Convert angle to radians and calculate new position
        theta_rad = math.radians(CAMERA_THETA)
        x = radius * math.sin(theta_rad)
        y = radius * math.cos(theta_rad)
        camera_pos = (x, y, z)
    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    ...


def setupCamera():
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
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              a, b, c,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()
    
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
    
    # Draw the walls (uncomment when you're ready to see them)
    draw_tiles()

    #Draw the player
    drawPlayer()



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
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()