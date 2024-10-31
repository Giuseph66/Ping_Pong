import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura_tela, altura_tela = 800, 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Ping Pong com pygame.Rect")

# Configurações da bola e da raquete
tamanho_bola = 20
tamanho_raquete = (50, 10)
velocidade_bola = [5, 5]

bola = pygame.Rect(largura_tela // 2, altura_tela // 2, tamanho_bola, tamanho_bola)
raquete = pygame.Rect(largura_tela - 70, altura_tela // 2 - tamanho_raquete[1] // 2, *tamanho_raquete)

# Loop principal
clock = pygame.time.Clock()
rodando = True
while rodando:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Movimento da bola
    bola.x += velocidade_bola[0]
    bola.y += velocidade_bola[1]

    # Verificar colisão com as bordas da tela
    if bola.top <= 0 or bola.bottom >= altura_tela:
        velocidade_bola[1] *= -1  # Inverte a direção vertical
    if bola.left <= 0 or bola.right >= largura_tela:
        velocidade_bola[0] *= -1  # Inverte a direção horizontal

    # Verificar colisão com a raquete
    if bola.colliderect(raquete):
        velocidade_bola[0] *= -1  

    # Atualizar posição da raquete com o mouse
    mouse_y = pygame.mouse.get_pos()[1]
    raquete.centery = mouse_y  # A raquete segue a posição do mouse

    # Limitar a raquete às bordas da tela
    if raquete.top < 0:
        raquete.top = 0
    elif raquete.bottom > altura_tela:
        raquete.bottom = altura_tela

    # Desenhar elementos na tela
    tela.fill((0, 0, 0))  # Preencher o fundo de preto
    pygame.draw.ellipse(tela, (255, 255, 255), bola)  # Desenhar a bola
    pygame.draw.rect(tela, (255, 0, 0), raquete)  # Desenhar a raquete

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
