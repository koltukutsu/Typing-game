from audioop import mul
import os
import time
import curses
import threading

import multiprocessing
# import signal
import psutil # use it instead of signal
from playsound import playsound as playmusic
from curses import wrapper
from curses.textpad import rectangle

from utils import wpm_calculator, read_words
from glob import glob
from sys import exit as sys_exit

# stop = threading.Event()
current_system_pid = os.getpid()
ThisSystem = psutil.Process(current_system_pid)

# def handler(signum, frame):
#     y = input("Are you sure you want to quit? (y/n):").lower()
#     if y == "y":
#         stop.set()

go_on_global = True

def play_music(music_path="./waggle_dance.mp3") -> None:
    # while not stop.isSet():
    while go_on_global:
        print(go_on_global)
        playmusic(music_path)
        print(go_on_global)

    
    
def menu() -> None:
    global _choice
    global _file_name
    global go_on_global
    _choice = None
    _file_name = None
    
    

    def sub_normal(screen) -> None:
        global _choice
        global middle_row
        global middle_col
        global num_rows
        global num_cols

        curses.echo()        
        curses.curs_set(0)
        screen.clear()
        num_rows, num_cols = screen.getmaxyx()
        
        messages = ["1-Start", "2-Choose the file", "q-Quit"]

        middle_row = int(num_rows / 2)
        middle_col = int(num_cols / 2)
        x_position_rectangle = 100
        
        for i, message in enumerate(messages):
            # curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK, curses.A_BOLD)
            half_length_of_message = int(len(message) / 2)
            x_position = middle_col - half_length_of_message
            x_position_rectangle = x_position if x_position_rectangle > x_position else x_position_rectangle
            # x_position = middle_col
            y_position = middle_row + i
            screen.addstr(y_position - len(messages), x_position, message, curses.A_BOLD)

        max_character_length = max([len(msg) for msg in messages])
        rectangle(screen, middle_row - 1 - len(messages), x_position_rectangle - 1, middle_row + 1,  x_position_rectangle + max_character_length) # uy, ux, ly, lx
        rectangle(screen, 0, 0, num_rows-1, num_cols-2)
        rectangle(screen, 1, 2, num_rows-2, num_cols-4)
        rectangle(screen, 2, 4, num_rows-3, num_cols-6)
        
        screen.addstr(middle_row, x_position, "Choice: ")
        screen.refresh()
        
        _choice = screen.getch()
        
        
    def start_typing_game(screen) -> None:
        global _len_words
        global _measured_time

        screen.nodelay(1)

        def print_user_word(screen, user_word:str) -> None:
            if user_word:
                user_word_len = len(user_word)
                x_pos_user = middle_col - user_word_len
                            # screen.clear()
                for j in range(middle_row + 4, middle_row + 7):
                    screen.move(j, 0)
                    screen.clrtoeol()
                    
                screen.addstr(middle_row + 5, x_pos_user, user_word)
                rectangle(screen, middle_row + 4, x_pos_user - 1, middle_row + 6, x_pos_user + user_word_len)
                rectangle(screen, 0, 0, num_rows-1, num_cols-2)
                screen.refresh()
            else:
                for j in range(middle_row + 4, middle_row + 7):
                    screen.move(j, 0)
                    screen.clrtoeol()
                    rectangle(screen, 0, 0, num_rows-1, num_cols-2)
                    screen.refresh()
                    
        words = read_words(_file_name)
        _len_words = len(words)
        flag = None
        i = 0
        _measured_time = 0
        # start = time.time()
        while i < _len_words:
            screen.clear()
            word_len = len(words[i])
            x_pos = middle_col - word_len
            
            screen.addstr(middle_row, x_pos, words[i])
            rectangle(screen, middle_row - 1, x_pos - 1, middle_row + 1, x_pos + word_len)
            rectangle(screen, 0, 0, num_rows-1, num_cols-2)
            
            # screen.addstr(middle_row, x_pos - 3 - len(str(i)), str(i + 1)) # show the counter
            # rectangle(screen, middle_row - 1, x_pos - 4 - len(str(i)), middle_row + 1, x_pos - 3)
            display_something(screen, f"Number: {str(i)}/{_len_words}", middle_row=middle_row - 7, middle_col=middle_col - 9) ## display the word related numbers

            display_something(screen, "Cometh Word:", middle_row=middle_row - 2, middle_col=middle_col - 5, dp_rectangle=False)
            display_something(screen, "Yours:", middle_row=middle_row + 3, middle_col=middle_col - 5, dp_rectangle=False)
            screen.refresh()
            
            user_word = ""
            flag = 0

            while flag == 0:
                start_inner = time.time()
                key = ""
                try:
                    key = screen.getkey()
                except:
                    pass

                end_inner = time.time()
                _measured_time += (end_inner - start_inner)
                # display_something(screen, f"Time: {round(_measured_time * 100, 3)}", middle_row=middle_row - 7, middle_col=middle_col + 8, dp_rectangle=True) ## time diplay
                # screen.refresh()

                if key != "":
                    if key == " " or key == "\n": # TODO and deleting the character
                            if user_word == words[i]:
                                i += 1
                                flag = 1    
                            else:
                                flag = 1
                        
                    elif key in ("\b", "^", "^?", "\x7f", "KEY_BACKSPACE"):
                    # elif key == "\b" or key == "^?" or key == "^":
                        user_word = user_word[:-1] if len(user_word) != 0 else ""
                        print_user_word(screen, user_word)

                    else:
                        user_word += key
                        print_user_word(screen, user_word)
                
        
    def scoring_screen(screen) -> None:
        flag: int
        output: str

        flag = 0
        screen.clear()
        output = f"Your score: {round(_wpm_score, 2)} words per minute"
        
        screen.addstr(middle_row, middle_col - int(len(output) / 2) , output)
        rectangle(screen, middle_row - 1, middle_col - len(output) - 1, middle_row + 1, middle_col + len(output) + 1)
        screen.addstr(middle_row + 2, middle_col - int(len("Pres -q- for Quit!") / 2), "Press -q- for Quit!")
        rectangle(screen, middle_row + 1, middle_col - len("Pres -q- for Quit!") - 1, middle_row + 3, middle_col + len("Pres -q- for Quit!") + 1)
        screen.refresh()
        curses.napms(3000)
        key = screen.getch()
     
        
    def sub_start(screen) -> None:
        global _len_words; _len_words = None
        global _measured_time; _measured_time = None
        global _wpm_score

        
        if _file_name == None:
            screen.clear()
            message_to_show = "Choose an existing file, turning back!!!" 
            screen.addstr(middle_row, middle_col - int(len(message_to_show) / 2), message_to_show)
            screen.refresh()
            curses.napms(750)
        else:
            screen.clear()
            message_to_show = "Typing is starting!!!"
            screen.addstr(middle_row, middle_col - int(len(message_to_show) / 2), message_to_show)
            screen.refresh()
            curses.napms(750)
            # start(_file_name)
            try:
                wrapper(start_typing_game)
                _wpm_score = wpm_calculator(_len_words, _measured_time)
                print(_wpm_score)
                print(_measured_time)
                screen.nodelay(-1)
                wrapper(scoring_screen)
            except KeyboardInterrupt:
                # ThisSystem.terminate()        
                pass    
                

    def display_something(screen, message, middle_row, middle_col, dp_rectangle=True) -> None:
        screen.addstr(middle_row, middle_col - int(len(message) / 2), message)
        if dp_rectangle:
            rectangle(screen, middle_row - 1, middle_col - int(len(message) / 2) - 1, middle_row + 1, middle_col + int(len(message) / 2) + 1)
        # screen.refresh()

                 
    def sub_file(screen) -> None:
        global _file_name
        
        curses.echo()
        curses.curs_set(0)
        
        while True:
            screen.clear()
            show_files = "-l- to list the file names"
            screen.addstr(middle_row - 1, middle_col - int(len(show_files) / 2), show_files)
            message_to_show = "Name of the File:"
            screen.addstr(middle_row, middle_col - int(len(message_to_show) / 2), message_to_show)
            screen.addstr(middle_row + 1, middle_col, "> ")
            _file_name = screen.getstr().decode("utf-8")
            
            if not os.path.isfile(_file_name) and _file_name != "l":
                _file_name = None
                
                screen.clear()
                message_to_show = "Invalid file name, turning back!!!"
                screen.addstr(middle_row, middle_col - int(len(message_to_show) / 2), message_to_show)
                # screen.addstr(middle_row, middle_row, message_to_show)
                
                screen.refresh()
                curses.napms(750)
                break
            elif _file_name == "l":
                _file_name = None
                max_file_length = 0
                screen.clear()
                
                for i, txt_file_name in enumerate(glob("*.txt")):
                    if len(txt_file_name) > max_file_length:
                        max_file_length = len(txt_file_name)
                        
                    screen.addstr(middle_row + i, middle_col - int(len(txt_file_name) / 2), txt_file_name)
                else:    
                    try:        
                        rectangle(screen, middle_row - 1, middle_col - 1 - int(max_file_length / 2), middle_row + i + 1, middle_col + int(max_file_length / 2))
                        screen.refresh()
                    except UnboundLocalError:
                        message_to_show = "Probably there is no file to show"
                        screen.addstr(middle_row, middle_col - int(len(message_to_show) / 2), message_to_show)
                        display_something(screen, message_to_show, middle_row, middle_col)
                    finally:
                        screen.refresh()
                        curses.napms(1500)
            else:
                break
                
                    
    while _choice != ord("q"):
        wrapper(sub_normal)    

        if _choice == ord("1"):
            wrapper(sub_start)
                
        elif _choice == ord("2"):
            wrapper(sub_file)
    else:
        go_on_global = False
        with open("tmp.txt", "w+") as close_file:
            os.system('ps aux | grep "/usr/bin/python3 /packages/home/.semih/local/lib.python3/8-site/playsound.py ./waggle_dance.mp3" >> tmp.txt')
            for el in close_file:
                process_id = el.split()[1].replace(" ", "")
                os.system(f"kill -9 {process_id}")

if __name__ == "__main__":
    #musicthread = threading.Thread(target=play_music)
    mainthread = threading.Thread(target=menu)

    #musicthread.daemon = True
    #musicthread.start()
    mainthread.start()

    go_on_global = False

    sys_exit(0)
