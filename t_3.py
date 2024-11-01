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

fonte = pygame.font.Font(None, 36)

# Configurações do Eixo Z para a bolinha
z_min = 100  # Distância mínima (mais próxima da tela)
z_max = 300  # Distância máxima (mais distante na tela)

# Inicialização da bola com posição Z
bola_pos = [largura // 2, altura // 4]
velocidade_bola = [5, 5, 1]  # Velocidade no eixo X, Y e Z

# Limites de velocidade
velocidade_minima = 3
velocidade_maxima = 15

# Função para calcular a escala com base no valor de Z
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

# Reset da bola
def resetar_bola():
    global bola_pos, velocidade_bola, bola_z, cor_bola
    bola_pos = [largura // 2, altura // 4]
    velocidade_bola = [5, 5, 1]
    bola_z = 200
    cor_bola = (255, 0, 0)

def jogo():
    global bola_pos, velocidade_bola
    bola_z = 150
    angulo_raquete = 0

    largura_raquete = 100
    altura_raquete = 15
    raquete_surface = pygame.Surface((largura_raquete, altura_raquete), pygame.SRCALPHA)
    raquete_surface.fill((255, 0, 0))
    raquete_rect = raquete_surface.get_rect(center=(largura // 2, altura - 50))
    
    largura_mesa = largura / 2
    altura_mesa = altura // 1.5
    mesa = pygame.Rect(largura / 4, 0, largura_mesa, altura_mesa)
    
    x_mouse_anterior, y_mouse_anterior = pygame.mouse.get_pos()
    velocidade_raquete_x = 0
    velocidade_raquete_y = 0
    rodando = True
    while rodando:
        cor_bola = (255, 255, 255)
        tela.fill((0, 0, 0))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
            else:
                angulo_raquete = capturar_scroll(event, angulo_raquete)

        # Atualizar a posição da raquete com o movimento do mouse no eixo X
        x_mouse, y_mouse = pygame.mouse.get_pos()
        raquete_rect.center = x_mouse, y_mouse

        delta_x = x_mouse - x_mouse_anterior
        delta_y = y_mouse - y_mouse_anterior
        delta_tempo = clock.get_time() / 1000

        if delta_tempo > 0:
            velocidade_raquete_x = abs(delta_x / delta_tempo)
            velocidade_raquete_y = abs(delta_y / delta_tempo)

        # Atualizar posição anterior do mouse
        x_mouse_anterior, y_mouse_anterior = x_mouse, y_mouse

        # Rotacionar a raquete
        raquete_rotacionada = pygame.transform.rotate(raquete_surface, angulo_raquete)
        raquete_rotated_rect = raquete_rotacionada.get_rect(center=raquete_rect.center)

        # Movimento da bolinha
        bola_pos[0] += velocidade_bola[0]
        bola_pos[1] += velocidade_bola[1]
        bola_z += velocidade_bola[2]

        # Verificar limites para manter a bola na área verde e nos limites do Z
        if bola_pos[1] <= 0 or bola_pos[1] >= altura:
            velocidade_bola[1] *= -1
        if bola_pos[0] <= 0 or bola_pos[0] >= largura:
            velocidade_bola[0] *= -1
        if bola_z <= z_min or bola_z >= z_max:
            velocidade_bola[2] *= -1

        # Limitar a velocidade da bola
        velocidade_total = math.hypot(velocidade_bola[0], velocidade_bola[1])
        if velocidade_total > velocidade_maxima:
            fator = velocidade_maxima / velocidade_total
            velocidade_bola[0] *= fator
            velocidade_bola[1] *= fator

        # Calcular escala com base na posição Z
        escala = calcular_escala(bola_z)
        tamanho_bola = int(20 * escala)

        pygame.draw.rect(tela, (0, 128, 0), mesa)
        bola_rect = pygame.Rect(0, 0, tamanho_bola, tamanho_bola)
        bola_rect.center = (int(bola_pos[0]), int(bola_pos[1]))

        angulo_bola = math.degrees(math.atan2(velocidade_bola[1], velocidade_bola[0]))
        angulo_saida = 2 * angulo_raquete - angulo_bola
        # Verificar colisão com a raquete
        if raquete_rotated_rect.colliderect(bola_rect):
            # Cálculo do ângulo de rebote
            
            # Manter a direção horizontal ao aplicar o ângulo de saída
            direcao_original_x = 1 if velocidade_bola[0] > 0 else -1
            
            # Aplicar spin com base no movimento da raquete
            spin = velocidade_raquete_x / 100
            velocidade_total = min(velocidade_maxima, velocidade_total + spin)
            
            # Novo vetor de velocidade com ângulo de saída ajustado e mantendo a direção original
            velocidade_bola[0] = velocidade_total * math.cos(math.radians(angulo_saida)) * direcao_original_x
            velocidade_bola[1] = -abs(velocidade_total * math.sin(math.radians(angulo_saida)))

        # Desenhar a bolinha e a raquete
        pygame.draw.ellipse(tela, cor_bola, bola_rect)
        tela.blit(raquete_rotacionada, raquete_rotated_rect.topleft)

        # Exibir dados na tela
        linhas_texto = [
            f"Raquete - Vel X: {velocidade_raquete_x:.2f} px/s, Vel Y: {velocidade_raquete_y:.2f} px/s",
            f"Bola - X: {bola_pos[0]:.2f}, Y: {bola_pos[1]:.2f}, Z: {bola_z:.2f}",
            f"Ângulo Raquete: {angulo_raquete}°",
            f"Ângulo Bola: {angulo_bola}°, Saída: {angulo_saida}°"
        ]
        y_ini = 600
        for linha in linhas_texto:
            superficie_texto = fonte.render(linha, True, (255, 255, 255))
            tela.blit(superficie_texto, (10, y_ini))
            y_ini += 30

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    jogo()
