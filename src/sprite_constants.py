# ASSETS
ASSETS = "assets"

# SPRITES
ICON = f"{ASSETS}/icon.PNG"
GRASS_SPRITE = f"{ASSETS}/grass.png"
OBSTACLE_SPRITE = f"{ASSETS}/obstacle.png"
BALDUR_ADVENTURE = f"{ASSETS}/TheBaldur_Adventure"
PLAYER_SPRITE_SHEETS = f"{BALDUR_ADVENTURE}/Adventurer/Spritesheets"
PLAYER_IDLE = f"{PLAYER_SPRITE_SHEETS}/Adventurer_Idle.png"
PLAYER_RUN = f"{PLAYER_SPRITE_SHEETS}/Adventurer_Running.png"
PLAYER_JUMP = f"{PLAYER_SPRITE_SHEETS}/Adventurer_Flying.png"
RANDOM_IMAGE = f"{ASSETS}/lol.png"
BACKGROUND_IMAGE = f"{ASSETS}/bg_gpt.png"
# MUSIC
GAME_LOOP_MUSIC = f"{ASSETS}/loop_music.mp3"
GAME_OVER_MUSIC = f"{ASSETS}/pwned.mp3"
PAUSE_SOUND = f"{ASSETS}/pause.mp3"

# SPRITE CONFIGURATION
PLAYER_IDLE_FRAMES_NUMBER = 5
PLAYER_RUN_FRAMES_NUMBER = 6
PLAYER_JUMP_FRAMES_NUMBER = 2

# SPRITE DIMENSIONS
PLAYER_RUN_FRAMES_DIMENSIONS = (32, 32)
RANDOM_IMAGE_DIMENSIONS = (128, 128)
BACKGROUND_DIMENSIONS = (1408, 772)

# DIMENSIONS
STAR_SIZE = 8
CLOUD_SIZE = 32
GRASS_SIZE = 64
PLAYER_SIZE = 64
PLAYER_SPRITE_W = 32
PLAYER_SPRITE_H = PLAYER_SIZE
OBSTACLE_SIZE = 64

# COLORS
WHITE = [255, 255, 255]
GRAY = [150, 150, 150]
DAY = [120, 154, 241]  # 515
NIGHT = [36, 43, 61]  # 140 => 140 / 515 = 27
RED = [165, 22, 22]
BLACK = [0, 0, 0]

# PHYSICS
PLAYER_JUMP_FORCE = 25