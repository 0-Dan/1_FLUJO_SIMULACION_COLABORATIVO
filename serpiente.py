import curses
import random

def query_start(stdscr):
    stdscr.addstr("¿Estás listo para empezar? (y/n): ")
    while True:
        k = stdscr.getch()
        if k in (ord('y'), ord('Y')):
            stdscr.clear()  # Limpia la pantalla después de la selección
            return True
        elif k in (ord('n'), ord('N')):
            return False

def main(stdscr):
    curses.curs_set(0)  # Cursor invisible
    if not query_start(stdscr):
        return  # Si el usuario no está listo, termina

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)  # Refresca cada 100 ms
    w.border(0)  # Dibuja borde

    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    food = [sh // 2, sw // 2]
    w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

    key = curses.KEY_RIGHT  # Dirección inicial hacia la derecha

    while True:
        next_key = w.getch()
        if next_key != -1:
            key = next_key

        new_head = [snake[0][0], snake[0][1]]

        # Actualiza la dirección basada en la tecla presionada
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1

        # Verifica si la serpiente choca con el borde o consigo misma
        if (new_head[0] in [0, sh] or
                new_head[1] in [0, sw] or
                new_head in snake):
            curses.endwin()
            quit()

        snake.insert(0, new_head)

        if snake[0] == food:
            food = None
            while food is None:
                nf = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(int(tail[0]), int(tail[1]), ' ')

        w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_BLOCK)

def start_game():
    curses.wrapper(main)
    
start_game()

# clonado, modificado total y a ver si lo logro


    