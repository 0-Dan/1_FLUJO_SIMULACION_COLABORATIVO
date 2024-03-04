
# pip install windows-curses

import curses
import random


# preparamos la terminal para una aplicación interactiva, configurando la visualización y
# controlando cómo se manejan las entradas del usuario.

#  Inicializa la librería curses y crea un objeto de ventana para toda la pantalla.
s = curses.initscr()

# Hace el cursor invisible de la terminal.
curses.curs_set(0)

# Obtiene las dimensiones de la ventana, asignando la altura (sh) y la anchura (sw)
sh, sw = s.getmaxyx()

# Crea una nueva ventana con las dimensiones de toda la pantalla.
w = curses.newwin(sh, sw, 0, 0)

# Permite que la ventana capture teclas especiales, como las flechas de dirección.
w.keypad(1)

# Establece un límite de tiempo de espera de 100 milisegundos para la entrada 
w.timeout(100)



# /// 

# posiciona la serpiente en la pantalla de manera que comience en el centro (verticalmente), 
# un cuarto del camino desde el lado izquierdo (horizontalmente), 
# orientada horizontalmente hacia la izquierda con una longitud inicial de tres segmentos.

snk_x = sw/4
snk_y = sh/2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]


# colocamos comida en el centro y ponemos como comida el caracter pi (π)
food = [sh/2, sw/2]
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)

key = curses.KEY_RIGHT #  la serpiente se moverá automáticamente hacia la derecha

# normas de la serpiente

while True:
    next_key = w.getch() # proximo movimiento. si no hay movimiento getch() devuelve -1 debido al timeout configurado anteriormente.
    key = key if next_key == -1 else next_key # mantiene la direccion que le demos con la flecha

    # si esta en la lista de los bordes o en su lista de posicion y choca con ella, pierde
    if snake[0][0] in [0, sh] or \
        snake[0][1]  in [0, sw] or \
        snake[0] in snake[1:]:
        curses.endwin()
        quit()

    new_head = [snake[0][0], snake[0][1]] # copia la posicion de la cabeza
    
    # dependiendo de key si arriba, abajo...actualizaremos new_head, la cabeza

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    snake.insert(0, new_head) # cabeza y cuerpo
    
    # si la babeza come o no come 

    if snake[0] == food:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')
        
    # w es la ventana y tenemos añadiendo ( 1  posicion x, posicion y la representacion de la cabeza curses.ACS_CKBOARD )

    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)


    