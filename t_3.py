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
z_max = 300  # Distância máxima (mais distante na tela)

# Inicialização da bola com posição Z
bola_pos = [largura // 2, altura // 4]
velocidade_bola = [5, 5, 1]  # Velocidade no eixo X, Y e Z

# Função para calcular a escala com base no valor de Z (mais longe = menor)
def calcular_escala(z):
    return max(0.1, 1 - (z - z_min) / (z_max - z_min))

# Função para capturar o scroll do mouse e rotacionar a raquete
def capturar_scroll(event, angulo_raquete):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 4:  # Scroll para cima
            angulo_raquete = (angulo_raquete + 10) % 360
        elif event.button == 5:  # Scroll para baixo
            angulo_raquete = (angulo_raquete - 10) % 360
    return angulo_raquete

def jogo():
    bola_z = 150  # Valor inicial do eixo Z
    angulo_raquete = 0  # Ângulo inicial da raquete

    # Configurações da raquete
    largura_raquete = 100
    altura_raquete = 15
    raquete_surface = pygame.Surface((largura_raquete, altura_raquete), pygame.SRCALPHA)
    raquete_surface.fill((255, 0, 0))  # Vermelho
    raquete_rect = raquete_surface.get_rect(center=(largura // 2, altura - 50))
    
    rodando = True
    while rodando:
        tela.fill((0, 128, 0))  # Fundo verde da mesa

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
            else:
                # Capturar o scroll do mouse para rotacionar a raquete
                angulo_raquete = capturar_scroll(event, angulo_raquete)

        # Atualizar a posição da raquete com o movimento do mouse no eixo X
        x_mouse, y_mouse = pygame.mouse.get_pos()
        raquete_rect.center = x_mouse,y_mouse

        # Rotacionar a raquete
        raquete_rotacionada = pygame.transform.rotate(raquete_surface, angulo_raquete)
        raquete_rotated_rect = raquete_rotacionada.get_rect(center=raquete_rect.center)

        # Movimento da bolinha
        bola_pos[0] += velocidade_bola[0]
        bola_pos[1] += velocidade_bola[1]
        bola_z += velocidade_bola[2]

        # Verificar limites para manter a bola na área verde e nos limites do Z
        if bola_pos[1] <= 0 or bola_pos[1] >= altura:
            velocidade_bola[1] *= -1  # Inverte a direção vertical
        if bola_pos[0] <= 0 or bola_pos[0] >= largura:
            velocidade_bola[0] *= -1  # Inverte a direção horizontal
        if bola_z <= z_min or bola_z >= z_max:
            velocidade_bola[2] *= -1  # Inverte a direção de profundidade (Z)

        # Calcular escala com base na posição Z
        escala = calcular_escala(bola_z)
        tamanho_bola = int(20 * escala)  # Tamanho da bola ajustado pela escala

        # Desenhar a bolinha com a escala
        bola_rect = pygame.Rect(0, 0, tamanho_bola, tamanho_bola)
        bola_rect.center = (int(bola_pos[0]), int(bola_pos[1]))
        pygame.draw.ellipse(tela, (255, 255, 255), bola_rect)

        # Verificar colisão da bola com a raquete rotacionada
        if raquete_rotated_rect.colliderect(bola_rect) and velocidade_bola[1] > 0:
            velocidade_bola[1] *= -1  # Inverte a direção vertical da bola
            velocidade_bola[0] *= -1  # Inverte a direção vertical da bola
            print("Colisão com a raquete")

        # Desenhar a raquete rotacionada
        tela.blit(raquete_rotacionada, raquete_rotated_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    jogo()
