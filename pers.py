import pygame

class Perssprite(pygame.sprite.Sprite):
    def __init__(self, largura, altura, sprite_sheet):
        super().__init__()
        self.sprite_sheet = sprite_sheet
        self.frame_atual = 0
        self.direcao = "direita"
        self.contador_anim = 0
        self.index_lista = 0
        self.velocidade = 2
        self.pulo = False
        self.velocidade_pulo = 0
        self.pos_y_inicial = 0

        # Carrega todos os frames das animações
        self.carregar_frames(sprite_sheet)

        # Inicializa a imagem e o rect
        self.image = self.frames_direita[0]
        self.rect = self.image.get_rect()
        
    def andar_animacao(self):
        # Escolhe a lista de frames conforme a direção
        if self.direcao == "direita":
            frames = self.frames_direita
        elif self.direcao == "cima":
            frames = self.frames_cima
        elif self.direcao == "baixo":
            frames = self.frames_baixo
        else:
            frames = [self.image]

        # Atualiza o frame da animação
        self.contador_anim += 1
        if self.contador_anim >= 6:  # Troca de frame a cada 6 ticks (ajuste como quiser)
            self.frame_atual = (self.frame_atual + 1) % len(frames)
            self.image = frames[self.frame_atual]
            self.contador_anim = 0

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

def animacao_subir_tela(personagem, tela, fundo, destino_y, largura, altura):
    """
    Faz o personagem surgir de fora da tela (embaixo) e subir até destino_y,
    usando a animação de andar para cima.
    """
    clock = pygame.time.Clock()
    personagem.direcao = "cima"
    personagem.rect.x = largura // 2 - personagem.rect.width // 2  # Centraliza no eixo X
    personagem.rect.y = altura  # Começa fora da tela (embaixo)

    while personagem.rect.y > destino_y:
        personagem.rect.y -= 2  # Ajuste a velocidade aqui (quanto menor, mais devagar)
        personagem.andar_animacao()
        tela.blit(fundo, (0, 0))
        tela.blit(personagem.image, personagem.rect.topleft)
        pygame.display.flip()
        clock.tick(60)
    personagem.rect.y = destino_y