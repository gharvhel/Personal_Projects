#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : snake.py
# Author            : Gharvhel Carre <gc2767@columbia.edu>
# Date              : 02.05.2018
# Last Modified Date: 03.05.2018
# Last Modified By  : Gharvhel Carre <gc2767@columbia.edu>

import curses
from time import sleep
import random


"""
Simple Snake Game
"""


class Snake_game:

    def __init__(self):
        print("[INFO] Loading...")
        self.stdscr = None
        self.__curses_start__()
        self.REFRESH_RATE = 45

    def __del__(self):
        print("[INFO] Snake Terminal Game terminated")
        # Restore terminal Behavior
        self.__curses_end__()

    def __curses_start__(self):
        # Change terminal behavior from game
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        # Clear screen
        self.stdscr.clear()
        
        # Remove blinking server
        curses.curs_set(False)


    def __curses_end__(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def menu(self):
        # Get terminal height and width
        scr_height, scr_width = self.stdscr.getmaxyx()

        # Create window
        window = curses.newwin(scr_height, scr_width, 0, 0)

        # Set snake speed
        window.timeout(self.REFRESH_RATE)

        # For navigation keys
        window.keypad(True)

        # initialize starting values
        snake = [[scr_height//2, scr_width//5]]    # Snake head
        food = [scr_height//2, scr_width//2]        # Food starts in middle
        window.addch(food[0], food[1], ord('O'))    # Draw food on screen
        direction = curses.KEY_RIGHT                # Initial direction is Right
        food_animation = 0
        score = 1
        window.addstr(0, scr_width//2, "SCORE: " +
                      str(score))    # Draw food on screen

        while True:
            # display score
            window.addstr(0, scr_width//2, "SCORE: " +
                          str(score))    # Draw food on screen

            # used to animate food
            food_animation += 20
            if food_animation > 100:
                food_animation = 0

            # Get the next direction from user, and prevent user from going
            # opposite of current d(irection
            next_key = window.getch()
            if next_key == -1:
                direction = direction
            elif direction == curses.KEY_UP and next_key == curses.KEY_DOWN:
                direction = direction
            elif direction == curses.KEY_DOWN and next_key == curses.KEY_UP:
                direction = direction
            elif direction == curses.KEY_LEFT and next_key == curses.KEY_RIGHT:
                direction = direction
            elif direction == curses.KEY_RIGHT and next_key == curses.KEY_LEFT:
                direction = direction
            else:
                direction = next_key

            # Check if snake hit self
            if snake[0] in snake[1:]:
                curses.endwin()
                quit()

            # Snake did not lose, create next head
            new_head = [snake[0][0], snake[0][1]]

            # Check where to add new head and make snake contiue across screen
            if direction == curses.KEY_DOWN:
                new_head[0] += 1
                if new_head[0] == scr_height:   # snake hit edge, continue top
                    new_head[0] = 1
            if direction == curses.KEY_UP:
                new_head[0] -= 1
                if new_head[0] == 0:            # snake hit edge, continue bottom
                    new_head[0] = scr_height-1
            if direction == curses.KEY_LEFT:
                new_head[1] -= 1
                if new_head[1] == 0:
                    # snake hit left edge, continue right
                    new_head[1] = scr_width-1
            if direction == curses.KEY_RIGHT:
                new_head[1] += 1
                if new_head[1] == scr_width:
                    # snake hit right edge, continue left
                    new_head[1] = 1

            snake.insert(0, new_head)

            # check if snake ate food, if so add new food
            if snake[0] == food:
                score += 1
                food = None
                while food is None:
                    new_food = [random.randint(
                        1, scr_height-1), random.randint(1, scr_width-1)]
                    if new_food not in snake or food[0] != 0:
                        food = new_food
                    else:
                        new_food = None
                window.addch(food[0], food[1], ord('O'))
            else:
                tail = snake.pop()
                window.addch(tail[0], tail[1], ' ')

            # animate food
            if food_animation > 50:
                window.addch(food[0], food[1], ord('X'))
            else:
                window.addch(food[0], food[1], ord('O'))

            # animate/move snake
            if direction == curses.KEY_DOWN:
                window.addch(snake[0][0], snake[0][1], ord('v'))
            elif direction == curses.KEY_UP:
                window.addch(snake[0][0], snake[0][1], ord('^'))
            elif direction == curses.KEY_LEFT:
                window.addch(snake[0][0], snake[0][1], ord('<'))
            elif direction == curses.KEY_RIGHT:
                window.addch(snake[0][0], snake[0][1], ord('>'))


if __name__ == '__main__':
    app = Snake_game()
    app.menu()
