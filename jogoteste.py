import pygame #22
from pygame.locals import *
from sys import exit
from random import randint
import os
from gameover import main as tela_gameover

from inim import Inimigo
from pers import Perssprite, animacao_subir_tela
from menu import menu

pygame.init()

# Diretórios
diretorio_principal = os.path.dirname(__file__)
diretorioimg = os.path.join(diretorio_principal, 'sprites')

# Configurações da tela
largura = 1580
altura = 865 
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo com Classe Perssprite")

# Cores e fontess
preto = (0, 0, 0)
fonte_pontos = pygame.font.SysFont("comicsans", 20, True, True)
fonte_vidas = pygame.font.SysFont("comicsans", 20, True, True)

# Variáveis globais
vidas = 3
pontos = [0]
moedas_coletadas = [0]
morreu = False

# Relógio
relogio = pygame.time.Clock()

# Carregar sprites
sprite_sheet = pygame.image.load(os.path.join(diretorioimg, 'personagem_sprites.png')).convert_alpha()
sprite_inimigo = pygame.image.load(os.path.join(diretorioimg, 'inimigo_sprite.png')).convert_alpha()
ruajogo = pygame.image.load(os.path.join("sprites", "ruajogo.png")).convert_alpha()
ruajogo = pygame.transform.scale(ruajogo, (largura, altura))

# Função para reiniciar o jogo
def reinicio():
    global vidas, pontos, morreu, grupo_inimigos
    personagem.rect.center = (largura // 2, altura // 2)
    vidas = 3
    pontos[0] = 0
    morreu = False
    grupo_inimigos.empty()
    inimigo = Inimigo(50, 50, 64, 64, 1, sprite_inimigo, altura, largura)
    grupo_inimigos.add(inimigo)

# Inicialização do personagem
personagem = Perssprite(largura, altura, sprite_sheet)

# Grupos de sprites
todassprites = pygame.sprite.Group()
todassprites.add(personagem)
grupo_inimigos = pygame.sprite.Group()

# Inimigo inicial
inimigo = Inimigo(50, 50, 64, 64, 3, sprite_inimigo, altura, largura)  # velocidade aumentada para 3
grupo_inimigos.add(inimigo)
proximo_inimigo = 10

# Fade (opcional)
def fade_in(tela, largura, altura, cor="black", velocidade=2, delay=30):
    fade_img = pygame.Surface((largura, altura)).convert_alpha()
    fade_img.fill(cor)
    for alpha in range(255, -1, -velocidade):
        tela.blit(ruajogo, (0, 0))
        todassprites.draw(tela)
        grupo_inimigos.draw(tela)
        texto_pontos = fonte_pontos.render(f'Pontos: {pontos[0]}', True, (255, 255, 255))
        texto_vidas = fonte_vidas.render(f'Vidas: {vidas}', True, (255, 255, 255))
        tela.blit(texto_pontos, (largura - 150, 10))
        tela.blit(texto_vidas, (largura - 150, 30))
        fade_img.set_alpha(alpha)
        tela.blit(fade_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(delay)

def fade_out(tela, largura, altura, cor="black", velocidade=2, delay=30):
    fade_img = pygame.Surface((largura, altura)).convert_alpha()
    fade_img.fill(cor)
    for alpha in range(0, 256, velocidade):
        tela.blit(ruajogo, (0, 0))
        todassprites.draw(tela)
        grupo_inimigos.draw(tela)
        texto_pontos = fonte_pontos.render(f'Pontos: {pontos[0]}', True, (255, 255, 255))
        texto_vidas = fonte_vidas.render(f'Vidas: {vidas}', True, (255, 255, 255))
        tela.blit(texto_pontos, (largura - 150, 10))
        tela.blit(texto_vidas, (largura - 150, 30))
        fade_img.set_alpha(alpha)
        tela.blit(fade_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(delay)

def carregar_spritesheet_moeda():
    diretorio_principal = os.path.dirname(__file__)
    spritesheet = pygame.image.load(os.path.join(diretorio_principal, 'sprites', 'MonedaD.png')).convert_alpha()
    return spritesheet

def get_sprite_moeda(spritesheet, indice, largura=16, altura=16):
    sprite = pygame.Surface((largura, altura), pygame.SRCALPHA)
    sprite.blit(spritesheet, (0, 0), (indice * largura, 0, largura, altura))
    return sprite

class Moeda(pygame.sprite.Sprite):
    def __init__(self, spritesheet, altura_tela, largura_tela):
        super().__init__()
        self.spritesheet = spritesheet
        self.indice_sprite = 0
        self.num_sprites = self.spritesheet.get_width() // 16
        self.image = get_sprite_moeda(self.spritesheet, self.indice_sprite)
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = randint(493, 1100 - 32)
        self.rect.y = -32
        self.velocidade = randint(1, 2)  # velocidade menor
        self.altura_tela = altura_tela
        self.anim_timer = 0
        self.anim_interval = 100  # ms entre frames
    def update(self):
        self.rect.y += self.velocidade
        # Animação
        self.anim_timer += relogio.get_time()
        if self.anim_timer >= self.anim_interval:
            self.anim_timer = 0
            self.indice_sprite = (self.indice_sprite + 1) % self.num_sprites
            self.image = get_sprite_moeda(self.spritesheet, self.indice_sprite)
            self.image = pygame.transform.scale(self.image, (32, 32))
        if self.rect.y > self.altura_tela:
            self.kill()

if __name__ == "__main__":
    while True:
        acao_menu = menu()
        if acao_menu == "iniciar":
            # Recarrega sprites e reinicializa personagem e inimigos ao voltar do menu
            sprite_sheet = pygame.image.load(os.path.join(diretorioimg, 'personagem_sprites.png')).convert_alpha()
            sprite_inimigo = pygame.image.load(os.path.join(diretorioimg, 'inimigo_sprite.png')).convert_alpha()
            ruajogo = pygame.image.load(os.path.join("sprites", "ruajogo.png")).convert_alpha()
            ruajogo = pygame.transform.scale(ruajogo, (largura, altura))

            personagem = Perssprite(largura, altura, sprite_sheet)
            personagem.rect.center = (largura // 2, altura // 2)  # Garante centralização
            todassprites = pygame.sprite.Group()
            todassprites.add(personagem)
            grupo_inimigos = pygame.sprite.Group()
            inimigo = Inimigo(50, 50, 64, 64, 1, sprite_inimigo, altura, largura)
            grupo_inimigos.add(inimigo)
            proximo_inimigo = 10
            vidas = 3
            pontos[0] = 0
            # moedas_coletadas NÃO é zerada aqui!
            morreu = False

            # 1. FADE OUT do menu (escurece tudo)
            fade_out(tela, largura, altura)

            # 2. Reposiciona o personagem fora da tela, centralizado no X
            personagem.rect.x = largura // 2 - personagem.rect.width // 2
            personagem.rect.y = altura

            # 3. FADE IN da tela do jogo (revela o cenário, ainda sem o personagem subindo)
            tela.blit(ruajogo, (0, 0))
            grupo_inimigos.draw(tela)
            todassprites.draw(tela)  # personagem ainda fora da tela
            texto_pontos = fonte_pontos.render(f'Pontos: {pontos[0]}', True, (255, 255, 255))
            texto_vidas = fonte_vidas.render(f'Vidas: {vidas}', True, (255, 255, 255))
            fade_in(tela, largura, altura)

            # 4. ANIMAÇÃO do personagem subindo
            destino_y = 400
            animacao_subir_tela(personagem, tela, ruajogo, destino_y, largura, altura)

            escolha = None  # Inicializa a variável escolha

            # Carregar spritesheet da moeda
            spritesheet_moeda = carregar_spritesheet_moeda()
            # Grupo de moedas
            grupo_moedas = pygame.sprite.Group()

            while True:
                relogio.tick(60)
                tela.blit(ruajogo, (0, 0))

                # Eventos
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            exit()

                # Atualizar sprites
                keys = pygame.key.get_pressed()
                todassprites.update(keys, largura, altura)
                grupo_inimigos.update(pontos)
                grupo_moedas.update()

                # Verificar colisão com inimigos
                colisoes = pygame.sprite.spritecollide(personagem, grupo_inimigos, False)
                if colisoes:
                    vidas -= 1
                    for inimigo in colisoes:
                        inimigo.rect.x = randint(493, 1100 - inimigo.rect.width)
                        inimigo.rect.y = 0

                # Verificar colisão com moedas
                colisoes_moedas = pygame.sprite.spritecollide(personagem, grupo_moedas, True)
                for moeda in colisoes_moedas:
                    moedas_coletadas[0] += 1  # Conta moedas coletadas

                # Game Over
                if vidas == 0:
                    escolha = tela_gameover()
                    if escolha == "tentar":
                        reinicio()
                        escolha = None  # Limpa a escolha para o próximo game over
                        continue
                    elif escolha == "menu":
                        break  # Sai do loop do jogo e volta ao menu

                # Criar novo inimigo a cada múltiplo de pontos
                if pontos[0] >= proximo_inimigo:
                    novo_inimigo = Inimigo(
                        randint(493, 1100 - 64),  # x
                        -40,                      # y
                        64,                       # largura_frame
                        64,                       # altura_frame
                        randint(4, 7),            # velocidade aumentada
                        sprite_inimigo,           # imagem do inimigo
                        altura,                   # altura da tela
                        largura                   # largura da tela
                    )
                    grupo_inimigos.add(novo_inimigo)
                    proximo_inimigo += 10

                # Gerar moeda aleatoriamente (exemplo: 1% de chance por frame)
                if randint(1, 100) == 1:
                    moeda = Moeda(spritesheet_moeda, altura, largura)
                    grupo_moedas.add(moeda)

                # Desenhar sprites
                todassprites.draw(tela)
                grupo_inimigos.draw(tela)
                grupo_moedas.draw(tela)

                # Exibir pontuação, vidas e moedas
                texto_pontos = fonte_pontos.render(f'Pontos: {pontos[0]}', True, (255, 255, 255))
                texto_vidas = fonte_vidas.render(f'Vidas: {vidas}', True, (255, 255, 255))
                texto_moedas = fonte_pontos.render(f'Moedas: {moedas_coletadas[0]}', True, (255, 255, 0))
                tela.blit(texto_pontos, (largura - 150, 10))
                tela.blit(texto_vidas, (largura - 150, 30))
                tela.blit(texto_moedas, (largura - 150, 50))

                pygame.display.flip()
        else:
            break