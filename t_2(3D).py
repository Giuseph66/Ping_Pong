import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Removido: glutInit()

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, 0.0)

    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

def draw_table():
    glColor3f(0.0, 0.5, 0.0)  # Cor verde para a mesa
    glBegin(GL_QUADS)
    glVertex3f(-2.0, -1.0, -5.0)
    glVertex3f(2.0, -1.0, -5.0)
    glVertex3f(2.0, -1.0, -15.0)
    glVertex3f(-2.0, -1.0, -15.0)
    glEnd()

def draw_cube():
    vertices = [
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, 1],
    ]

    edges = (
        (0,1,2,3),
        (3,2,6,7),
        (7,6,5,4),
        (4,5,1,0),
        (0,3,7,4),
        (1,2,6,5)
    )

    glBegin(GL_QUADS)
    for face in edges:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_paddle(x, z):
    glColor3f(1.0, 0.0, 0.0)  # Cor vermelha para as raquetes
    glPushMatrix()
    glTranslatef(x, -0.9, z)
    glScalef(0.25, 0.05, 0.25)
    draw_cube()
    glPopMatrix()

def draw_ball(x, y, z):
    glColor3f(1.0, 1.0, 1.0)  # Cor branca para a bola
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(0.1, 0.1, 0.1)
    draw_cube()
    glPopMatrix()

def main():
    init()

    # Posições iniciais
    paddle1_x = 0.0
    paddle1_z = -6.0
    paddle2_x = 0.0
    paddle2_z = -14.0

    ball_x = 0.0
    ball_y = -0.7
    ball_z = -10.0
    ball_dx = 0.07
    ball_dz = 0.1

    clock = pygame.time.Clock()
    running = True
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Controles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle1_x -= 0.1
        if keys[pygame.K_RIGHT]:
            paddle1_x += 0.1
        if keys[pygame.K_a]:
            paddle2_x -= 0.1
        if keys[pygame.K_d]:
            paddle2_x += 0.1

        # Limites das raquetes
        paddle1_x = max(-1.5, min(1.5, paddle1_x))
        paddle2_x = max(-1.5, min(1.5, paddle2_x))

        # Movimento da bola
        ball_x += ball_dx
        ball_z += ball_dz

        # Colisões com as paredes laterais
        if ball_x >= 1.9 or ball_x <= -1.9:
            ball_dx *= -1

        # Colisões com as raquetes
        if (paddle1_z - 0.5 <= ball_z <= paddle1_z + 0.5) and (paddle1_x - 0.5 <= ball_x <= paddle1_x + 0.5):
            ball_dz *= -1
        if (paddle2_z - 0.5 <= ball_z <= paddle2_z + 0.5) and (paddle2_x - 0.5 <= ball_x <= paddle2_x + 0.5):
            ball_dz *= -1

        # Pontuação (reiniciar a bola se ultrapassar as raquetes)
        if ball_z <= -15 or ball_z >= -5:
            ball_x = 0.0
            ball_z = -10.0

        # Limpar tela e desenhar objetos
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_table()
        draw_paddle(paddle1_x, paddle1_z)
        draw_paddle(paddle2_x, paddle2_z)
        draw_ball(ball_x, ball_y, ball_z)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
