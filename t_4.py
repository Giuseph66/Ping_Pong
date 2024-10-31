import pygame
import sys
import math
import socket
import threading

# Configurações do jogo
LARGURA, ALTURA = 800, 600
FPS = 60

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Ping Pong 3D - Visão de Cima')
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
VERDE = (0, 128, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Classe Bola com Física Realista
class Bola:
    def __init__(self, x, y, raio):
        self.x = x
        self.y = y
        self.raio = raio
        self.vel_x = 0
        self.vel_y = -5
        self.acel_gravidade = 0.1  # Simular gravidade

    def atualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.acel_gravidade  # Aplicar gravidade

        # Colisão com as bordas da tela
        if self.x - self.raio <= 0 or self.x + self.raio >= LARGURA:
            self.vel_x *= -1
        if self.y - self.raio <= 0:
            self.vel_y *= -1

    def desenhar(self, tela):
        pygame.draw.circle(tela, BRANCO, (int(self.x), int(self.y)), self.raio)

# Classe Raquete controlada pelo mouse
class Raquete:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.x = LARGURA / 2 - self.largura / 2
        self.y = ALTURA - self.altura - 10
        self.vel_x = 0

    def atualizar(self):
        pos_mouse = pygame.mouse.get_pos()
        self.x = pos_mouse[0] - self.largura / 2

        # Limites da raquete
        if self.x <= 0:
            self.x = 0
        elif self.x + self.largura >= LARGURA:
            self.x = LARGURA - self.largura

    def desenhar(self, tela):
        pygame.draw.rect(tela, VERMELHO, (self.x, self.y, self.largura, self.altura))

# Funções de rede
def iniciar_servidor(host, porta, jogo):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, porta))
    server_socket.listen()
    print(f"Servidor iniciado em {host}:{porta}")
    conn, addr = server_socket.accept()
    print(f"Conectado por {addr}")
    jogo.conn = conn

    threading.Thread(target=receber_dados, args=(conn, jogo)).start()

def conectar_servidor(host, porta, jogo):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, porta))
    print(f"Conectado ao servidor {host}:{porta}")
    jogo.conn = client_socket

    threading.Thread(target=receber_dados, args=(client_socket, jogo)).start()

def receber_dados(conn, jogo):
    while True:
        try:
            data = conn.recv(1024)
            if data:
                mensagem = data.decode()
                x, y = map(float, mensagem.split(','))
                jogo.raquete_oponente.x = x
                jogo.raquete_oponente.y = y
            else:
                break
        except:
            break

# Classe principal do jogo
class Jogo:
    def __init__(self):
        self.bola = Bola(LARGURA / 2, ALTURA / 2, 10)
        self.raquete = Raquete(100, 10)
        self.raquete_oponente = Raquete(100, 10)
        self.raquete_oponente.y = 10  # Raquete do oponente na parte superior
        self.conn = None
        self.pontuacao = 0
        self.pontuacao_oponente = 0
        self.fonte = pygame.font.SysFont('Arial', 30)
        self.menu_inicial()

    def menu_inicial(self):
        executando = True
        while executando:
            tela.fill(VERDE)
            titulo = self.fonte.render('Ping Pong 3D', True, BRANCO)
            instrucoes = self.fonte.render('Pressione S para hospedar ou C para conectar', True, BRANCO)
            tela.blit(titulo, (LARGURA / 2 - titulo.get_width() / 2, ALTURA / 2 - 50))
            tela.blit(instrucoes, (LARGURA / 2 - instrucoes.get_width() / 2, ALTURA / 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    executando = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        threading.Thread(target=iniciar_servidor, args=('0.0.0.0', 5555, self)).start()
                        executando = False
                    elif event.key == pygame.K_c:
                        threading.Thread(target=conectar_servidor, args=('localhost', 5555, self)).start()
                        executando = False

            clock.tick(FPS)

    def enviar_dados(self):
        if self.conn:
            mensagem = f"{self.raquete.x},{self.raquete.y}"
            try:
                self.conn.sendall(mensagem.encode())
            except:
                pass

    def atualizar(self):
        self.bola.atualizar()
        self.raquete.atualizar()
        self.enviar_dados()

        # Colisão da bola com a raquete do jogador
        if (self.bola.y + self.bola.raio >= self.raquete.y and
            self.raquete.x <= self.bola.x <= self.raquete.x + self.raquete.largura):
            self.bola.vel_y *= -1
            self.bola.vel_x += (self.bola.x - (self.raquete.x + self.raquete.largura / 2)) * 0.05

        # Colisão da bola com a raquete do oponente
        if (self.bola.y - self.bola.raio <= self.raquete_oponente.y + self.raquete_oponente.altura and
            self.raquete_oponente.x <= self.bola.x <= self.raquete_oponente.x + self.raquete_oponente.largura):
            self.bola.vel_y *= -1
            self.bola.vel_x += (self.bola.x - (self.raquete_oponente.x + self.raquete_oponente.largura / 2)) * 0.05

        # Pontuação
        if self.bola.y - self.bola.raio >= ALTURA:
            self.pontuacao_oponente += 1
            self.resetar_bola()
        elif self.bola.y + self.bola.raio <= 0:
            self.pontuacao += 1
            self.resetar_bola()

    def resetar_bola(self):
        self.bola.x = LARGURA / 2
        self.bola.y = ALTURA / 2
        self.bola.vel_x = 0
        self.bola.vel_y *= -1

    def desenhar(self):
        tela.fill(VERDE)
        self.bola.desenhar(tela)
        self.raquete.desenhar(tela)
        self.raquete_oponente.desenhar(tela)

        # Desenhar a pontuação
        pontuacao_texto = self.fonte.render(f'Você: {self.pontuacao}', True, BRANCO)
        pontuacao_oponente_texto = self.fonte.render(f'Oponente: {self.pontuacao_oponente}', True, BRANCO)
        tela.blit(pontuacao_texto, (10, ALTURA - 40))
        tela.blit(pontuacao_oponente_texto, (10, 10))

        pygame.display.flip()

    def executar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.conn:
                        self.conn.close()
                    pygame.quit()
                    sys.exit()

            self.atualizar()
            self.desenhar()
            clock.tick(FPS)

if __name__ == '__main__':
    jogo = Jogo()
    jogo.executar()
