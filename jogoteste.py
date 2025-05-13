import pygame
from pygame.locals import *
from sys import exit
from random import randint
import os
import time


pygame.init()

# Diretórios
diretorio_principal = os.path.dirname(__file__)
diretorioimg = os.path.join(diretorio_principal, 'sprites')

# Configurações da tela
largura = 1580
altura = 865
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo com Classe Perssprite")

# Cores
preto = (0, 0, 0)
verde = (0, 255, 0)
branco = (255, 255, 255)
# Fonte
fonte_pontos = pygame.font.SysFont("comicsans", 20, True, True)
fonte_vidas = pygame.font.SysFont("comicsans", 20, True, True)

# Variáveis globais
vidas = 3
pontos = 0
morreu = False

# Relógio
relogio = pygame.time.Clock()

# Carregar a sprite sheet
sprite_sheet = pygame.image.load(os.path.join(diretorioimg, 'sprites.png')).convert_alpha()
sprite_inimigo = pygame.image.load(os.path.join(diretorioimg, 'spriteinimigo.png')).convert_alpha()

# Classe Perssprite
# Classe Perssprite


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura_frame, altura_frame, velocidade):
        super().__init__()
        self.largura_frame = largura_frame  # Define largura_frame como um atributo da classe
        self.altura_frame = altura_frame  # Define altura_frame como um atributo da classe
        self.frame_inimigo = []  
        self.carregar_frames()  
        self.index_lista = 0
        self.image = self.frame_inimigo[self.index_lista] 
        self.rect = self.image.get_rect()
        self.rect.topleft = (randint(493, 1100 - self.largura_frame), y)
        self.velocidade = velocidade

    def carregar_frames(self):
        for i in range(5):  # Assume que há 5 frames na sprite sheet
            frame = sprite_inimigo.subsurface((i * 64, 0, 64, 64))  # Recorta cada frame
            self.frame_inimigo.append(frame)  # Adiciona o frame à lista

    def movimento(self):
        global pontos  # Indica que estamos usando a variável global 'pontos'

        # Movimento do inimigo (descendo na tela)
        self.rect.y += self.velocidade
        if self.rect.top > altura:  # Se sair da tela, reinicia no topo
            self.rect.y = 0
            self.rect.x = randint(493, 1100 - self.largura_frame)
            pontos += 1
            self.velocidade += 0.1
        
    def update(self):
        self.movimento()

        # Atualizar animação
        self.index_lista += 0.2
        if self.index_lista >= len(self.frame_inimigo):
            self.index_lista = 0
        self.image = self.frame_inimigo[int(self.index_lista)]





class Perssprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames_esquerda = []
        self.frames_direita = []
        self.carregar_frames()
        self.index_lista = 0
        self.image = self.frames_direita[self.index_lista]  # Começa com a animação para a direita
        self.rect = self.image.get_rect()
        self.rect.center = (largura // 2, altura // 2)  # Centraliza o personagem na tela
        self.velocidade = 3
        self.direcao = "direita"  # Direção inicial

    def carregar_frames(self):
        # Carregar os frames da sprite sheet
        for i in range(3):  # Assume que há 3 frames por linha
            # Primeira linha: frames para a esquerda
            img_esquerda = sprite_sheet.subsurface((i * 64, 0, 64, 64))
            self.frames_esquerda.append(img_esquerda)

            # Segunda linha: frames para a direita
            img_direita = sprite_sheet.subsurface((i * 64, 64, 64, 64))
            self.frames_direita.append(img_direita)

    def update(self, keys):
        # Movimento do personagem
        if keys[K_w] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if keys[K_s] and self.rect.bottom < altura:
            self.rect.y += self.velocidade
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.velocidade
            self.direcao = "esquerda"  # Atualiza a direção
        if keys[K_d] and self.rect.right < largura:
            self.rect.x += self.velocidade
            self.direcao = "direita"  # Atualiza a direção

        # Atualizar animação com base na direção
        self.index_lista += 0.2
        if self.index_lista >= len(self.frames_esquerda):  # Tanto faz frames_esquerda ou frames_direita
            self.index_lista = 0

        if self.direcao == "esquerda":
            self.image = self.frames_esquerda[int(self.index_lista)]
        elif self.direcao == "direita":
            self.image = self.frames_direita[int(self.index_lista)]

# Função para reiniciar o jogo
def reinicio():
    global vidas, pontos, morreu, grupo_inimigos
    personagem.rect.center = (largura // 2, altura // 2)
    vidas = 3
    pontos = 0
    morreu = False

    # Reiniciar o grupo de inimigos
    grupo_inimigos.empty()  # Remove todos os inimigos do grupo
    inimigo = Inimigo(50, 50, 64, 64, 1)  # Cria um novo inimigo com velocidade inicial
    grupo_inimigos.add(inimigo)

    grupo_consumiveis.empty()
    consumivel_vida = Consumivel(randint(493, 1100 - 32), 0, "vida")
    consumivel_velocidade = Consumivel(randint(493, 1100 - 32), 0, "velocidade")
    grupo_consumiveis.add(consumivel_vida, consumivel_velocidade)
    nova_vida = 25
    nova_velocidade = 50
    

# Função para exibir a tela de Game Over
def exibir_game_over():
    global morreu
    overfonte = pygame.font.SysFont("comicsans", 20, True, False)

    textoover = 'Você perdeu! Aperte R para reiniciar'
    texto2 = overfonte.render(textoover, True, (255, 0, 0))
    ret_texto = texto2.get_rect()
    ret_texto.center = (largura // 2, altura // 2)

    texto_pontos = f'Pontos: {pontos}'
    texto_pontos = overfonte.render(texto_pontos, True, (255, 0, 0))
    ret_texto_pontos = texto_pontos.get_rect()
    ret_texto_pontos.center = (largura // 2, altura // 2 + 50)
    morreu = True

    while morreu:
        tela.fill(preto)
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reinicio()
                    '''
                    if event.key == K_e:
                        skills()'''
        tela.blit(texto2, ret_texto)
        tela.blit(texto_pontos, ret_texto_pontos)
        pygame.display.update()



class Consumivel(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo  # Tipo do consumível: "velocidade" ou "vida"
        self.frames = []
        self.carregar_frames()
        self.image = self.frames[0] if tipo == "velocidade" else self.frames[1]
        self.rect = self.image.get_rect()
        self.rect.topleft = (randint(493, 1100), y)
        self.velocidade = 1  # Velocidade inicial do consumível

    def carregar_frames(self):
        # Carregar a sprite sheet "consheet" da pasta "sprites"
        consheet = pygame.image.load(os.path.join(diretorioimg, 'consheet.png')).convert_alpha()
        
        # Assume que a sprite sheet tem os frames dos consumíveis
        for i in range(2):  # Dois tipos de consumíveis
            frame = consheet.subsurface((i * 32, 0, 32, 32))  # Cada frame tem 32x32
            self.frames.append(frame)

    def movimento(self):
        # Movimento do consumível (descendo na tela)
        self.rect.y += self.velocidade
        if self.rect.top > altura:  # Se sair da tela, reinicia no topo
            self.rect.y = 0
            self.rect.x = randint(0, largura - self.rect.width)

    def update(self):
        self.movimento()

    def aplicar_efeito(self, personagem):
        if self.tipo == "vida":
            global vidas
            vidas += 1  # Aumenta a vida do personagem
            print("Vida aumentada!")
        elif self.tipo == "velocidade":
            personagem.velocidade += 0.2  # Aumenta a velocidade do personagem
            print("Velocidade aumentada!")

# Inicialização do personagem
personagem = Perssprite()

# Grupo de sprites
todassprites = pygame.sprite.Group()
todassprites.add(personagem)



# Configurações do inimigo
inimigo = Inimigo(50, 50, 64, 64, 1)
proximo_inimigo = 10

grupo_inimigos = pygame.sprite.Group()
grupo_inimigos.add(inimigo)

imagem_fundo = pygame.image.load('ruajogo.png').convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
# Loop principal do jogo


# Grupo de consumíveis
grupo_consumiveis = pygame.sprite.Group()

# Criar consumíveis
consumivel_vida = Consumivel(randint(493, 1100 - 32), 0, "vida")
consumivel_velocidade = Consumivel(randint(493, 1100 - 32), 0, "velocidade")
grupo_consumiveis.add(consumivel_vida, consumivel_velocidade)

nova_vida = 25
nova_velocidade = 50
while True:
    relogio.tick(60)
    tela.fill(preto)

    # Eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()

    tela.blit(imagem_fundo, (0, 0))

    # Atualizar sprites
    keys = pygame.key.get_pressed()
    todassprites.update(keys)
    grupo_inimigos.update()  # Atualiza o inimigo
    grupo_consumiveis.update()
    

    # Verificar colisão
    colisoes = pygame.sprite.spritecollide(personagem, grupo_inimigos, False)
    if colisoes:
        vidas -= 1
        for inimigo in colisoes:
            # Redefinir a posição do inimigo para uma posição aleatória
            inimigo.rect.x = randint(0, largura - inimigo.rect.width)
            inimigo.rect.y = 0

    pegando_consumivel = pygame.sprite.spritecollide(personagem, grupo_consumiveis, True)
    if pegando_consumivel:
        for consumivel in pegando_consumivel:
            consumivel.aplicar_efeito(personagem)
            # Redefinir a posição do consumível para uma posição aleatória
            

    if vidas == 0:
        exibir_game_over()
    
    if pontos >= proximo_inimigo:
        novo_inimigo = Inimigo(randint(493, 1100 - 64), 0, 64, 64, randint(2, 5))
        grupo_inimigos.add(novo_inimigo)
        proximo_inimigo += 10
    
        # Criar consumível de vida a cada 25 pontos
    if pontos >= nova_vida:
        novo_consumivel_vida = Consumivel(randint(493, 1100 - 32), 0, "vida")
        grupo_consumiveis.add(novo_consumivel_vida)
        nova_vida += 25  # Atualiza para o próximo intervalo

    # Criar consumível de velocidade a cada 50 pontos
    if pontos >= nova_velocidade:
        novo_consumivel_velocidade = Consumivel(randint(493, 1100 - 32), 0, "velocidade")
        grupo_consumiveis.add(novo_consumivel_velocidade)
        nova_velocidade += 50  # Atualiza para o próximo intervalo

    ''' if pontos >= nova_vida:
        nova_vida += 25
        nova_vida = Consumivel(randint(493, 1100 - 32), 0, "vida")
        grupo_consumiveis.add(nova_vida)
    if pontos >= nova_velocidade:
        nova_velocidade += 50
        nova_velocidade = Consumivel(randint(493, 1100 - 32), 0, "velocidade")
        grupo_consumiveis.add(nova_velocidade)'''


    # Desenhar sprites
    todassprites.draw(tela)
    grupo_inimigos.draw(tela)  # Desenha o inimigo
    grupo_consumiveis.draw(tela)

    # Atualizar consumíveis

    # Desenhar consumíveis

    # Exibir pontuação e vidas
    texto_pontos = fonte_pontos.render(f'Pontos: {pontos}', True, (255, 255, 255))
    texto_vidas = fonte_vidas.render(f'Vidas: {vidas}', True, (255, 255, 255))
    tela.blit(texto_pontos, (largura - 150, 10))
    tela.blit(texto_vidas, (largura - 150, 30))

    pygame.display.flip()