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

# Cores e fontes
preto = (0, 0, 0)
fonte_pontos = pygame.font.SysFont("comicsans", 20, True, True)
fonte_vidas = pygame.font.SysFont("comicsans", 20, True, True)

# Variáveis globais
vidas = 3
pontos = [0]
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
inimigo = Inimigo(50, 50, 64, 64, 1, sprite_inimigo, altura, largura)
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

if __name__ == "__main__":
    acao_menu = menu()
    if acao_menu == "iniciar":
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
        tela.blit(texto_pontos, (largura - 150, 10))
        tela.blit(texto_vidas, (largura - 150, 30))
        fade_in(tela, largura, altura)

        # 4. ANIMAÇÃO do personagem subindo
        destino_y = 400
        animacao_subir_tela(personagem, tela, ruajogo, destino_y, largura, altura)

        escolha = None  # Inicializa a variável escolha

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

            # Verificar colisão com inimigos
            colisoes = pygame.sprite.spritecollide(personagem, grupo_inimigos, False)
            if colisoes:
                vidas -= 1
                for inimigo in colisoes:
                    inimigo.rect.x = randint(493, 1100 - inimigo.rect.width)
                    inimigo.rect.y = 0

            # Game Over
            if vidas == 0:
                escolha = tela_gameover()
                if escolha == "tentar":
                    reinicio()
                    escolha = None  # Limpa a escolha para o próximo game over
                    continue
                elif escolha == "menu":
                    break  # Ou chame sua função de menu, se desejar

            # Criar novo inimigo a cada múltiplo de pontos
            if pontos[0] >= proximo_inimigo:
                novo_inimigo = Inimigo(
                    randint(493, 1100 - 64),  # x
                    -40,                      # y
                    64,                       # largura_frame
                    64,                       # altura_frame
                    randint(2, 5),            # velocidade
                    sprite_inimigo,           # imagem do inimigo
                    altura,                   # altura da tela
                    largura                   # largura da tela
                )
                grupo_inimigos.add(novo_inimigo)
                proximo_inimigo += 10

            # Desenhar sprites
            todassprites.draw(tela)
            grupo_inimigos.draw(tela)

            # Exibir pontuação e vidas
            texto_pontos = fonte_pontos.render(f'Pontos: {pontos[0]}', True, (255, 255, 255))
            texto_vidas = fonte_vidas.render(f'Vidas: {vidas}', True, (255, 255, 255))
            tela.blit(texto_pontos, (largura - 150, 10))
            tela.blit(texto_vidas, (largura - 150, 30))

            pygame.display.flip()