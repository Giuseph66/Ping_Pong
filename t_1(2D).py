import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Ping Pong')

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Raquetes
raquete_largura = 10
raquete_altura = 100
raquete_velocidade = 7

# Posição inicial das raquetes
raquete1_x = 50
raquete1_y = altura // 2 - raquete_altura // 2

raquete2_x = largura - 50 - raquete_largura
raquete2_y = altura // 2 - raquete_altura // 2

# Bola
bola_raio = 10
bola_x = largura // 2
bola_y = altura // 2
bola_vel_x = 5
bola_vel_y = 5

# Pontuação
pontuacao1 = 0
pontuacao2 = 0
fonte = pygame.font.SysFont('Arial', 30)

# Loop principal do jogo
clock = pygame.time.Clock()
while True:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimentação das raquetes
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w] and raquete1_y > 0:
        raquete1_y -= raquete_velocidade
    if teclas[pygame.K_s] and raquete1_y < altura - raquete_altura:
        raquete1_y += raquete_velocidade
    if teclas[pygame.K_UP] and raquete2_y > 0:
        raquete2_y -= raquete_velocidade
    if teclas[pygame.K_DOWN] and raquete2_y < altura - raquete_altura:
        raquete2_y += raquete_velocidade

    # Movimentação da bola
    bola_x += bola_vel_x
    bola_y += bola_vel_y

    # Colisão com as bordas superior e inferior
    if bola_y - bola_raio <= 0 or bola_y + bola_raio >= altura:
        bola_vel_y *= -1

    # Colisão com as raquetes
    if (raquete1_x < bola_x - bola_raio < raquete1_x + raquete_largura and
        raquete1_y < bola_y < raquete1_y + raquete_altura):
        bola_vel_x *= -1

    if (raquete2_x < bola_x + bola_raio < raquete2_x + raquete_largura and
        raquete2_y < bola_y < raquete2_y + raquete_altura):
        bola_vel_x *= -1

    # Pontuação
    if bola_x < 0:
        pontuacao2 += 1
        bola_x = largura // 2
        bola_y = altura // 2
        bola_vel_x *= -1
    if bola_x > largura:
        pontuacao1 += 1
        bola_x = largura // 2
        bola_y = altura // 2
        bola_vel_x *= -1

    # Desenho
    tela.fill(preto)
    pygame.draw.rect(tela, branco, (raquete1_x, raquete1_y, raquete_largura, raquete_altura))
    pygame.draw.rect(tela, branco, (raquete2_x, raquete2_y, raquete_largura, raquete_altura))
    pygame.draw.circle(tela, branco, (int(bola_x), int(bola_y)), bola_raio)

    # Exibir pontuação
    texto = fonte.render(f'{pontuacao1} - {pontuacao2}', True, branco)
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, 20))

    # Atualizar tela
    pygame.display.flip()
    clock.tick(60)
