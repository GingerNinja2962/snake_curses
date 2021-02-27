import curses
import random
import time
from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT


def setup():

    WIDTH = 150
    HEIGHT = 30
    SPEED = 500
    screen = curses.newwin(HEIGHT, WIDTH, 0, 0)
    screen.keypad(1)
    curses.curs_set(0)
    screen.border(0)
    screen.timeout(SPEED)

    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)

    curses.init_pair(10, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(11, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(13, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(14, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(15, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(16, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

    curses.init_pair(20, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(21, curses.COLOR_CYAN, curses.COLOR_WHITE)

    key_default = KEY_RIGHT
    key_conflict_dict = {
            KEY_DOWN:KEY_UP,
            KEY_UP:KEY_DOWN,
            KEY_LEFT:KEY_RIGHT,
            KEY_RIGHT:KEY_LEFT
            }

    snake = [[10,23],[10,22],[10,21],[10,20]]

    active_fruit, new_fruit = fruit(snake, HEIGHT, WIDTH)

    return snake, key_conflict_dict, key_default, screen, HEIGHT, WIDTH, active_fruit, new_fruit, len(snake), SPEED


def my_raw_input(screen, key_conflict_dict, key_default):

    ch = screen.getch()
    if ch == 27:
        return ch
    elif ch in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
        if key_conflict_dict[ch] != key_default:
            return ch
    return key_default


def logic_processor(snake, key_default, screen, color):

    if key_default == KEY_DOWN:
        if "Fruit" in snake:
            snake.remove("Fruit")
        else:
            screen.addstr(snake[-1][0], snake[-1][1], " ")
            snake.pop()
        snake.insert(0, [int(snake[0][0]) + 1, snake[0][1]])
        screen.addstr(snake[0][0], snake[0][1], "*", curses.color_pair(color[0][1]))

    elif key_default == KEY_UP:
        if "Fruit" in snake:
            snake.remove("Fruit")
        else:
            screen.addstr(snake[-1][0], snake[-1][1], " ")
            snake.pop()
        snake.insert(0, [int(snake[0][0]) - 1, snake[0][1]])
        screen.addstr(snake[0][0], snake[0][1], "*", curses.color_pair(color[0][1]))

    elif key_default == KEY_LEFT:
        if "Fruit" in snake:
            snake.remove("Fruit")
        else:
            screen.addstr(snake[-1][0], snake[-1][1], " ")
            snake.pop()
        snake.insert(0, [snake[0][0], int(snake[0][1]) - 1])
        screen.addstr(snake[0][0], snake[0][1], "*", curses.color_pair(color[0][1]))

    elif key_default == KEY_RIGHT:
        if "Fruit" in snake:
            snake.remove("Fruit")
        else:
            screen.addstr(snake[-1][0], snake[-1][1], " ")
            snake.pop()
        snake.insert(0, [snake[0][0], int(snake[0][1]) + 1])
        screen.addstr(snake[0][0], snake[0][1], "*", curses.color_pair(color[0][1]))
    return snake, color


def out_of_bounds(snake, HEIGHT, WIDTH, screen, color):

    if snake[0][0] > HEIGHT - 2:
        snake[0] = [ 1, snake[0][1] ]
        screen.addstr(snake[0][0], snake[0][1], "*", curses.color_pair(color[0][1]))
        screen.border(0)
    elif snake[0][0] < 1:
        snake[0] = [ 28, snake[0][1] ]
        screen.addstr(snake[0][0], snake[0][1], "*", curses.color_pair(color[0][1]))
        screen.border(0)
    elif snake[0][1] > WIDTH - 2:
        snake[0] = [ snake[0][0], 1 ]
        screen.addstr(snake[0][0], snake[0][1], "*", curses.color_pair(color[0][1]))
        screen.border(0)
    elif snake[0][1] < 1:
        snake[0] = [ snake[0][0], 148 ]
        screen.addstr(snake[0][0], snake[0][1], "*", curses.color_pair(color[0][1]))
        screen.border(0)
    return snake, color


def debugger(screen, snake, active_fruit, new_fruit, key_default, speed, color):

    color_codes = {
            1:"BLUE", 2:"CYAN",
            3:"GREEN", 4:"MAGENTA",
            5:"RED", 6:"WHITE",
            7:"YELLOW", 8:"BLACK",
            10:"BLUE",
            11:"CYAN", 12:"GREEN",
            13:"MAGENTA", 14:"RED",
            15:"WHITE", 16:"YELLOW"
            }

    for X in range(1, 10):
        screen.addstr(X, 2, 33 * " ")
    screen.addstr(1, 2, "====DEBUGGING INFO====")
    screen.addstr(2, 2, f"New_Fruit - {str(new_fruit)}")
    screen.addstr(3, 2, f"Snake - {str(snake[0])}")
    screen.addstr(4, 2, f"Active_Fruit - {str(active_fruit)}")
    screen.addstr(5, 2, f"Key_Default - {str(key_default)}")
    screen.addstr(6, 2, f"Snake Speed - {str(speed)}")
    screen.addstr(7, 2, f"Snake Fruit color - {str(color[0][0])} - {color_codes[color[0][0]]}")
    screen.addstr(8, 2, f"Snake Head color - {str(color[0][1])} - {color_codes[color[0][1]]}")
    screen.addstr(9, 2, f"Snake Body color - {str(color[0][2])} - {color_codes[color[0][2]]}")
    if new_fruit[0] < 10 and new_fruit[1] < 35:
        screen.addstr(new_fruit[0], new_fruit[1], "0", curses.color_pair(color[0][0]))
    for a in range(len(snake)):
        if a == 0:
            if snake[0][0] < 10 and snake[0][1] < 35:
                screen.addstr(snake[0][0], snake[0][1], "*", curses.color_pair(color[0][1]))
        else:
            if snake[a][0] < 10 and snake[a][1] < 35:
                screen.addstr(snake[a][0], snake[a][1], "*", curses.color_pair(color[0][2]))
    return color


def printer(screen, snake, new_fruit, score, color):

    screen.addstr(0, 50, "SCORE - " + str(score), curses.color_pair(21))
    if new_fruit in snake:
        screen.addstr(new_fruit[0], new_fruit[1], "*", curses.color_pair(color[0][1]))
    else:
        screen.addstr(new_fruit[0], new_fruit[1], "O", curses.color_pair(color[0][0]))
    screen.addstr(snake[1][0], snake[1][1], "*", curses.color_pair(color[0][2]))
    screen.refresh()
    return color


def fruit(snake, HEIGHT, WIDTH):

    new_fruit = [random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2)]
    while new_fruit in snake:
        new_fruit = [random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2)]
    return True, new_fruit


def position_change(screen, position, entries):

    ch = screen.getch()
    if ch == KEY_UP:
        if position > 1:
            return position - 1, False
        else:
            return entries, False
    elif ch == KEY_DOWN:
        if position < entries:
            return position + 1, False
        return 1, False
    elif ch == 10:
        return position, True
    else:
        return position, False


def snake_speed(snake, default_speed, last_len):

    if last_len < len(snake):
        default_speed -= int(default_speed * (1/100))
        last_len += 1
    return default_speed, last_len


def random_colors(color):

    if color[1][0]:
        color[0][0] += 1
        if color[0][0] > 7: color[0][0] = 1
    if color[1][1]:
        color[0][1] += 1
        if color[0][1] > 16: color[0][1] = 10
    if color[1][2]:
        color[0][2] += 1
        if color[0][2] > 16: color[0][2] = 10
    return color


def snake_head_color(screen, color):

    position = 1
    enter = False
    while True:
        list_color = [2,2,2,2,2,2,2,2,2]
        list_color[position-1] = 21
        screen.addstr(5, 65, "=====Snake Head Color=====", curses.color_pair(4))
        screen.addstr(7, 75, "Blue", curses.color_pair(list_color[0]))
        screen.addstr(8, 75, "Cyan", curses.color_pair(list_color[1]))
        screen.addstr(9, 75, "Green", curses.color_pair(list_color[2]))
        screen.addstr(10, 75, "Magenta", curses.color_pair(list_color[3]))
        screen.addstr(11, 75, "Red", curses.color_pair(list_color[4]))
        screen.addstr(12, 75, "White", curses.color_pair(list_color[5]))
        screen.addstr(13, 75, "Yellow", curses.color_pair(list_color[6]))
        screen.addstr(14, 75, "Rainbow", curses.color_pair(list_color[7]))
        screen.addstr(15, 75, "Back", curses.color_pair(list_color[8]))
        position, enter = position_change(screen, position, 9)
        screen.refresh()
        if enter == True:
            if position == 8:
                color[1][1] = True
                break
            if position != 9:
                color[1][1] = False
                color[0][1] = (10 + (position - 1))
            break
    screen.clear()
    screen.border(0)
    return color


def snake_body_color(screen, color):

    position = 1
    enter = False
    while True:
        list_color = [2,2,2,2,2,2,2,2,2]
        list_color[position-1] = 21
        screen.addstr(5, 65, "=====Snake Body Color=====", curses.color_pair(4))
        screen.addstr(7, 75, "Blue", curses.color_pair(list_color[0]))
        screen.addstr(8, 75, "Cyan", curses.color_pair(list_color[1]))
        screen.addstr(9, 75, "Green", curses.color_pair(list_color[2]))
        screen.addstr(10, 75, "Magenta", curses.color_pair(list_color[3]))
        screen.addstr(11, 75, "Red", curses.color_pair(list_color[4]))
        screen.addstr(12, 75, "White", curses.color_pair(list_color[5]))
        screen.addstr(13, 75, "Yellow", curses.color_pair(list_color[6]))
        screen.addstr(14, 75, "Rainbow", curses.color_pair(list_color[7]))
        screen.addstr(15, 75, "Back", curses.color_pair(list_color[8]))
        position, enter = position_change(screen, position, 9)
        screen.refresh()
        if enter == True:
            if position == 8:
                color[1][2] = True
                break
            if position != 9:
                color[1][2] = False
                color[0][2] = 10 + (position - 1)
            break
    screen.clear()
    screen.border(0)
    return color



def snake_fruit_color(screen, color):

    position = 1
    enter = False
    while True:
        list_color = [2,2,2,2,2,2,2,2,2]
        list_color[position-1] = 21
        screen.addstr(5, 65, "=====Snake Fruit Color=====", curses.color_pair(4))
        screen.addstr(7, 75, "Blue", curses.color_pair(list_color[0]))
        screen.addstr(8, 75, "Cyan", curses.color_pair(list_color[1]))
        screen.addstr(9, 75, "Green", curses.color_pair(list_color[2]))
        screen.addstr(10, 75, "Magenta", curses.color_pair(list_color[3]))
        screen.addstr(11, 75, "Red", curses.color_pair(list_color[4]))
        screen.addstr(12, 75, "White", curses.color_pair(list_color[5]))
        screen.addstr(13, 75, "Yellow", curses.color_pair(list_color[6]))
        screen.addstr(14, 75, "Rainbow", curses.color_pair(list_color[7]))
        screen.addstr(15, 75, "Back", curses.color_pair(list_color[8]))
        position, enter = position_change(screen, position, 9)
        screen.refresh()
        if enter == True:
            if position == 8:
                color[1][0] = True
                break
            if position != 9:
                color[1][0] = False
                color[0][0] = position
            break
    screen.clear()
    screen.border(0)
    return color


def color_menu(screen, color):

    position = 1
    enter = False
    while True:
        list_color = [2,2,2,2,2]
        list_color[position-1] = 21
        screen.addstr(5, 65, "====COLOR SCHEMS====", curses.color_pair(21))
        screen.addstr(7, 65, "Snake Body Color", curses.color_pair(list_color[0]))
        screen.addstr(8, 65, "Snake Head Color", curses.color_pair(list_color[1]))
        screen.addstr(9, 65, "Snake Fruit Color", curses.color_pair(list_color[2]))
        screen.addstr(10, 71,      "Back", curses.color_pair(list_color[3]))
        position, enter = position_change(screen, position, 4)
        screen.refresh()
        if enter == True:
            screen.clear()
            screen.border(0)
            if position == 1:
                color = snake_body_color(screen, color)
            elif position == 2:
                color = snake_head_color(screen, color)
            elif position == 3:
                color = snake_fruit_color(screen, color)
            elif position == 4:
                break
    screen.clear()
    screen.border(0)
    return color


def menu(screen, color):

    position = 1
    enter = False
    while True:
        list_color = [2,2,2]
        list_color[position-1] = 21
        screen.addstr(5, 66, "====MAIN MENU====", curses.color_pair(21))
        screen.addstr(7, 68, "Color Schems", curses.color_pair(list_color[0]))
        screen.addstr(8, 69, "Play Game", curses.color_pair(list_color[1]))
        screen.addstr(9, 71,      "Quit", curses.color_pair(list_color[2]))
        screen.refresh()
        position, enter = position_change(screen, position, 3)
        if enter == True:
            screen.clear()
            screen.border(0)
            if position == 1:
                color = color_menu(screen, color)
            elif position == 2:
                break
            elif position == 3:
                return False, color
    screen.clear()
    screen.border(0)
    return True, color


def snake_main(snake, key_conflict_dict, key_default, screen, HEIGHT, WIDTH, active_fruit, new_fruit, last_len, speed, color, score):

    for a in range(len(snake)):
        if a == 0:
            screen.addstr(snake[a][0], snake[a][1], "*", curses.color_pair(color[0][1]))
        else:
            screen.addstr(snake[a][0], snake[a][1], "*", curses.color_pair(color[0][2]))

    while True:
        color = random_colors(color)
        speed, last_len = snake_speed(snake, speed, last_len)
        screen.timeout(speed)
        key_default = my_raw_input(screen, key_conflict_dict, key_default)
        if key_default == 27:
            break
        if new_fruit in snake:
            active_fruit = False
            snake.insert(0, "Fruit")
            score += 100
        if not active_fruit:
            active_fruit, new_fruit = fruit(snake, HEIGHT, WIDTH)
        snake, color = logic_processor(snake, key_default, screen, color)
        snake, color = out_of_bounds(snake, HEIGHT, WIDTH, screen, color)
        if snake[0] in snake[1:]:
            break
        # color = debugger(screen, snake, active_fruit, new_fruit, key_default, speed, color) # TODO disable for DEBUGGER
        color = printer(screen, snake, new_fruit, score, color)

    screen.clear()
    screen.border(0)
    screen.addstr(10, 70, "Game Over!")
    screen.addstr(12, 70, "SCORE - " + str(score), curses.color_pair(21))
    screen.refresh()
    time.sleep(3)
    return 


def main(screen):

    close = True
    color= [ [2, 16, 13], [False, False, False] ]
    while close:
        snake, key_conflict_dict, key_default, screen, HEIGHT, WIDTH, active_fruit, new_fruit, last_len, speed = setup()
        close, color = menu(screen, color)
        if close: snake_main(snake, key_conflict_dict, key_default, screen, HEIGHT, WIDTH, active_fruit, new_fruit, last_len, speed, color, 0)
        screen.clear()
        screen.border(0)
    return


if __name__ == "__main__":
    curses.wrapper(main)