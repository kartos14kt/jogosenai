import pygame
from random import randint

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura_frame, altura_frame, velocidade, sprite_inimigo, altura, largura):
        super().__init__()
        self.largura_frame = largura_frame
        self.altura_frame = altura_frame
        self.frame_inimigo = []
        self.carregar_frames(sprite_inimigo)
        self.index_lista = 0
        self.image = self.frame_inimigo[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.topleft = (randint(493, 1100 - self.largura_frame), y)
        self.velocidade = velocidade
        self.altura = altura
        self.largura = largura

    def carregar_frames(self, sprite_inimigo):
        self.frame_inimigo = []
        for i in range(4):  # 4 colunas, 1 linha
            frame = sprite_inimigo.subsurface((i * 48, 0, 48, 48))
            frame = pygame.transform.scale(frame, (60, 60))
            self.frame_inimigo.append(frame)

    def movimento(self, pontos):
        self.rect.y += self.velocidade
        if self.rect.top > self.altura:
            self.rect.y = 0
            self.rect.x = randint(493, 1100 - self.largura_frame)
            pontos[0] += 1
            self.velocidade += 0.1

    def update(self, pontos):
        self.movimento(pontos)
        self.index_lista += 0.08
        if self.index_lista >= len(self.frame_inimigo):
            self.index_lista = 0
        self.image = self.frame_inimigo[int(self.index_lista)]