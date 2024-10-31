import pygame
import math

# Inicialização do Pygame
pygame.init()

info = pygame.display.Info()
largura, altura = info.current_w, info.current_h

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Ping Pong 3D - Visão de Cima')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

# Configurações do Eixo Z para a bolinha
z_min = 100  # Distância mínima (mais próxima da tela)
z_max = 250  # Distância máxima (mais distante na tela)
tamanho_inicial_bola = 20  # Tamanho da bolinha para renderização

def calcular_escala(z):
    return max(0.5, 1 - (z - z_min) / (z_max - z_min)) 

def atualizar_posicao_raquete(raquete_rect, x_mouse, y_mouse):
    raquete_rect.center = (x_mouse, y_mouse)

# Função para capturar o scroll do mouse e rotacionar a raquete
def capturar_scroll(event, angulo_raquete):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:  # Scroll para cima
            angulo_raquete = (angulo_raquete + 10) % 360
        elif event.button == 5:  # Scroll para baixo
            angulo_raquete = (angulo_raquete - 10) % 360
    return angulo_raquete

def jogo():
    bola_x, bola_y = largura // 2, altura // 2  # Posição inicial da bola
    bola_z = 150  # Profundidade inicial da bola
    tamanho_raquete = (50, 10)
    velocidade_bola = [5, 5, 1]  # Velocidade no eixo X, Y e Z

    raquete_surface = pygame.Surface(tamanho_raquete, pygame.SRCALPHA)
    raquete_surface.fill((255, 0, 0))  # Vermelho
    raquete_rect = raquete_surface.get_rect(center=(largura // 2, altura // 2))
    angulo_raquete = 0  # Ângulo inicial da raquete

    # Definir um tamanho fixo para o Rect de colisão da bola
    bola_rect_colisao = pygame.Rect(bola_x, bola_y, 20, 20)

    rodando = True
    while rodando:
        tela.fill((0, 0, 0))  # Fundo preto
        pygame.draw.rect(tela, (0, 128, 0), (largura / 4, 0, largura / 2, altura // 1.5))
        
        # Calcular a escala da bola com base no valor de Z
        escala = calcular_escala(bola_z)
        tamanho_bola = int(tamanho_inicial_bola * escala)

        # Atualizar a posição do Rect de colisão sem mudar seu tamanho
        bola_rect_colisao.topleft = (bola_x, bola_y)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
            else:
                angulo_raquete = capturar_scroll(event, angulo_raquete)

        x_mouse, y_mouse = pygame.mouse.get_pos()
        atualizar_posicao_raquete(raquete_rect, x_mouse, y_mouse)

        # Movimento da bola
        bola_x += velocidade_bola[0]
        bola_y += velocidade_bola[1]
        bola_z += velocidade_bola[2]

        # Verificar colisão da bola com as bordas da tela
        if bola_rect_colisao.top <= 0 or bola_rect_colisao.bottom >= altura:
            velocidade_bola[1] *= -1  # Inverte a direção vertical
        if bola_rect_colisao.left <= 0 or bola_rect_colisao.right >= largura:
            velocidade_bola[0] *= -1  # Inverte a direção horizontal
        if bola_z <= z_min or bola_z >= z_max:
            velocidade_bola[2] *= -1  # Inverte a direção de profundidade (Z)
        
        # Rotacionar a raquete
        raquete_rotacionada = pygame.transform.rotate(raquete_surface, angulo_raquete)
        raquete_rotated_rect = raquete_rotacionada.get_rect(center=raquete_rect.center)

        # Verificar colisão da bola com a raquete rotacionada
        if raquete_rotated_rect.colliderect(bola_rect_colisao):
            velocidade_bola[0] *= -1
            velocidade_bola[1] *= -1
            print("Colisão com a raquete")

        # Desenhar a bola com escala (usando tamanho visual)
        bola_desenho = pygame.Rect(bola_x, bola_y, tamanho_bola, tamanho_bola)
        pygame.draw.ellipse(tela, (255, 255, 255), bola_desenho)

        # Desenhar a raquete
        tela.blit(raquete_rotacionada, raquete_rotated_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    jogo()
