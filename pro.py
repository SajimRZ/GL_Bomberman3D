# Global variables for game state and menu navigation
GAME_STATE = "main_menu"  # Possible states: "main_menu", "playing", "shop", "game_over"
cursor_pos = 0  # Tracks the current menu selection
gold = 0  # Tracks the player's gold

# =================== Main Menu ===================
def draw_main_menu():
    """
    Draws the main menu with options to start the game or access the shop.
    """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw background
    glColor4f(0.1, 0.1, 0.1, 1.0)  # Dark gray
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(SCREEN_WIDTH, 0)
    glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
    glVertex2f(0, SCREEN_HEIGHT)
    glEnd()

    # Title
    draw_text(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100, "3D Bomberman", GLUT_BITMAP_HELVETICA_18)

    # Menu options
    menu_options = ["Start Game", "Shop"]
    for i, option in enumerate(menu_options):
        y_pos = SCREEN_HEIGHT // 2 - i * 50
        glColor3f(1, 1, 0) if i == cursor_pos else glColor3f(1, 1, 1)
        draw_text(SCREEN_WIDTH // 2 - 100, y_pos, option)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def handle_main_menu_input(key):
    """
    Handles input for the main menu.
    """
    global GAME_STATE, cursor_pos

    if key == GLUT_KEY_UP:
        cursor_pos = (cursor_pos - 1) % 2
    elif key == GLUT_KEY_DOWN:
        cursor_pos = (cursor_pos + 1) % 2
    elif key == b'\r':  # Enter key
        if cursor_pos == 0:  # Start Game
            GAME_STATE = "playing"
            initialize_game_map()
        elif cursor_pos == 1:  # Shop
            GAME_STATE = "shop"

# =================== Shop ===================
def draw_shop():
    """
    Draws the shop screen where players can buy upgrades.
    """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw background
    glColor4f(0.2, 0.2, 0.2, 1.0)  # Dark gray
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(SCREEN_WIDTH, 0)
    glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
    glVertex2f(0, SCREEN_HEIGHT)
    glEnd()

    # Shop title
    draw_text(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, "Shop", GLUT_BITMAP_HELVETICA_18)

    # Shop options
    shop_options = ["Increase Max Bombs", "Increase Explosion Radius", "Increase Max Health"]
    for i, option in enumerate(shop_options):
        y_pos = SCREEN_HEIGHT // 2 - i * 50
        glColor3f(1, 1, 0) if i == cursor_pos else glColor3f(1, 1, 1)
        draw_text(SCREEN_WIDTH // 2 - 150, y_pos, option)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def handle_shop_input(key):
    """
    Handles input for the shop.
    """
    global GAME_STATE, cursor_pos, gold

    if key == GLUT_KEY_UP:
        cursor_pos = (cursor_pos - 1) % 3
    elif key == GLUT_KEY_DOWN:
        cursor_pos = (cursor_pos + 1) % 3
    elif key == b'\r':  # Enter key
        selected_option = cursor_pos
        if selected_option == 0 and gold >= 10:  # Increase Max Bombs
            global MAX_NUMBER_OF_PLAYER_BOMBS
            MAX_NUMBER_OF_PLAYER_BOMBS += 1
            gold -= 10
        elif selected_option == 1 and gold >= 10:  # Increase Explosion Radius
            global PLAYER_BOMB_EXPLOTION_RADIUS
            PLAYER_BOMB_EXPLOTION_RADIUS += 1
            gold -= 10
        elif selected_option == 2 and gold >= 10:  # Increase Max Health
            global MAX_HEALTH
            MAX_HEALTH += 10
            gold -= 10
        GAME_STATE = "main_menu"

# =================== Game Over ===================
def draw_game_over():
    """
    Draws the game over screen with the player's progress.
    """
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw background
    glColor4f(0.0, 0.0, 0.0, 1.0)  # Black
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(SCREEN_WIDTH, 0)
    glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
    glVertex2f(0, SCREEN_HEIGHT)
    glEnd()

    # Game over message
    draw_text(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50, "Game Over", GLUT_BITMAP_HELVETICA_18)
    draw_text(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, f"Score: {SCORE}, Waves Cleared: {CURRENT_WAVE}", GLUT_BITMAP_HELVETICA_18)
    draw_text(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50, f"Gold Earned: {CURRENT_WAVE * 10}", GLUT_BITMAP_HELVETICA_18)
    draw_text(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, "Press Enter to Return to Main Menu", GLUT_BITMAP_HELVETICA_18)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def handle_game_over_input(key):
    """
    Handles input for the game over screen.
    """
    global GAME_STATE, gold

    if key == b'\r':  # Enter key
        gold += CURRENT_WAVE * 10  # Add gold based on waves cleared
        GAME_STATE = "main_menu"

# =================== Main Loop Modifications ===================
def showScreen():
    """
    Modified display function to handle different game states.
    """
    if GAME_STATE == "main_menu":
        draw_main_menu()
    elif GAME_STATE == "shop":
        draw_shop()
    elif GAME_STATE == "game_over":
        draw_game_over()
    elif GAME_STATE == "playing":
        # Existing game rendering logic
