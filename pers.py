import pygame

class Perssprite(pygame.sprite.Sprite):
    def __init__(self, largura, altura, sprite_sheet):
        super().__init__()
        self.frames_esquerda = []
        self.frames_direita = []
        self.carregar_frames(sprite_sheet)
        self.index_lista = 0
        self.image = self.frames_direita[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (largura // 2, altura // 2)
        self.velocidade = 3
        self.direcao = "direita"
        self.velocidade_pulo = 0
        self.pulo = False
        self.pos_y_inicial = self.rect.y

    def carregar_frames(self, sprite_sheet):
        self.frames_baixo = []
        self.frames_direita = []
        self.frames_esquerda = []
        self.frames_cima = []
        self.frames_parado = []

        for i in range(4):  # 4 colunas
        # Para cada frame, recorta 17x17 e redimensiona para 48x48
            frame_baixo = sprite_sheet.subsurface((i * 17, 0 * 17, 17, 17))
            frame_baixo = pygame.transform.scale(frame_baixo, (48, 48))
            self.frames_baixo.append(frame_baixo)

            frame_direita = sprite_sheet.subsurface((i * 17, 1 * 17, 17, 17))
            frame_direita = pygame.transform.scale(frame_direita, (48, 48))
            self.frames_direita.append(frame_direita)

            frame_esquerda = sprite_sheet.subsurface((i * 17, 2 * 17, 17, 17))
            frame_esquerda = pygame.transform.scale(frame_esquerda, (48, 48))
            self.frames_esquerda.append(frame_esquerda)

            frame_cima = sprite_sheet.subsurface((i * 17, 3 * 17, 17, 17))
            frame_cima = pygame.transform.scale(frame_cima, (48, 48))
            self.frames_cima.append(frame_cima)

            frame_parado = sprite_sheet.subsurface((i * 17, 4 * 17, 17, 17))
            frame_parado = pygame.transform.scale(frame_parado, (48, 48))
            self.frames_parado.append(frame_parado)

    def pular(self):
        if not self.pulo:  # só pula se não estiver pulando
            self.pulo = True
            self.velocidade_pulo = -8
            self.pos_y_inicial = self.rect.y


    def update(self, keys, largura, altura):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.velocidade
            self.direcao = "cima"
        elif keys[pygame.K_s] and self.rect.bottom < altura:
            self.rect.y += self.velocidade
            self.direcao = "baixo"
        elif keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.velocidade
            self.direcao = "esquerda"
        elif keys[pygame.K_d] and self.rect.right < largura:
            self.rect.x += self.velocidade
            self.direcao = "direita"
        else:
            self.direcao = "parado"

        self.index_lista += 0.08
        if self.index_lista >= 4:
            self.index_lista = 0

        if self.direcao == "baixo":
            self.image = self.frames_baixo[int(self.index_lista)]
        elif self.direcao == "cima":
            self.image = self.frames_cima[int(self.index_lista)]
        elif self.direcao == "esquerda":
            self.image = self.frames_esquerda[int(self.index_lista)]
        elif self.direcao == "direita":
            self.image = self.frames_direita[int(self.index_lista)]
        else:
            self.image = self.frames_parado[int(self.index_lista)]

        # Lógica do pulo
        if self.pulo:
            self.rect.y += self.velocidade_pulo
            self.velocidade_pulo += 1  # gravidade
            if self.rect.y >= self.pos_y_inicial:
                self.rect.y = self.pos_y_inicial
                self.pulo = False
                self.velocidade_pulo = 0
