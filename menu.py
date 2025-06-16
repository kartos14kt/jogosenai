import pygame
import os
from pers import Perssprite

pygame.init()
largura, altura = 1580, 865
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Menu do Jogo")

fonte = pygame.font.SysFont("comicsans", 40)
branco = (255, 255, 255)
cinza = (100, 100, 100)
azul = (0, 120, 255)
preto = (0, 0, 0)

def desenhar_botao(texto, x, y, w, h, ativo):
    cor = azul if ativo else cinza
    pygame.draw.rect(tela, cor, (x, y, w, h))
    label = fonte.render(texto, True, branco)
    tela.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))

fundo_menu = pygame.image.load(os.path.join("sprites", "rua_animacao.png")).convert_alpha()
fundo_menu = pygame.transform.scale(fundo_menu, (largura, altura))
sprite_sheet = pygame.image.load(os.path.join("sprites", "personagem_sprites.png")).convert_alpha()
personagem_menu = Perssprite(largura, altura, sprite_sheet)
personagem_menu.rect.x = largura // 2 - 34
personagem_menu.rect.y = 30

relogio = pygame.time.Clock()

def animar_saida_personagem(personagem_menu, largura, altura):
    meio_y = altura // 2 - personagem_menu.rect.height // 2
    clock = pygame.time.Clock()

    # Decide direção vertical
    if personagem_menu.rect.y < meio_y:
        direcao_y = 1  # Andar para baixo
        personagem_menu.direcao = "baixo"
    elif personagem_menu.rect.y > meio_y:
        direcao_y = -1  # Andar para cima
        personagem_menu.direcao = "cima"
    else:
        direcao_y = 0

    # Anda verticalmente até o centro do eixo Y (sem teleporte)
    while personagem_menu.rect.y != meio_y:
        personagem_menu.rect.y += direcao_y * 2  # Ajuste a velocidade aqui
        if (direcao_y == 1 and personagem_menu.rect.y > meio_y) or (direcao_y == -1 and personagem_menu.rect.y < meio_y):
            personagem_menu.rect.y = meio_y  # Corrige ultrapassagem

        personagem_menu.andar_animacao()
        tela.blit(fundo_menu, (0, 0))
        desenhar_botao("Iniciar", 100, 120, 200, 60, False)
        desenhar_botao("Saves", 100, 250, 200, 60, False)
        desenhar_botao("Skills", 100, 380, 200, 60, False)
        tela.blit(personagem_menu.image, personagem_menu.rect.topleft)
        pygame.display.flip()
        clock.tick(60)

    # Agora anda para a direita usando sprite de andar para a direita
    personagem_menu.direcao = "direita"
    while personagem_menu.rect.x < largura:
        personagem_menu.rect.x += 4  # Ajuste a velocidade aqui
        personagem_menu.andar_animacao()
        tela.blit(fundo_menu, (0, 0))
        desenhar_botao("Iniciar", 100, 120, 200, 60, False)
        desenhar_botao("Saves", 100, 250, 200, 60, False)
        desenhar_botao("Skills", 100, 380, 200, 60, False)
        tela.blit(personagem_menu.image, personagem_menu.rect.topleft)
        pygame.display.flip()
        clock.tick(60)

def menu():
    rodando = True
    save_existe = os.path.exists("save.txt")
    pulo_anterior = False

    while rodando:
        relogio.tick(60)
        tela.blit(fundo_menu, (0, 0))
        mx, my = pygame.mouse.get_pos()

        texto_jogo = "Continuar" if save_existe else "Iniciar"
        botao_jogo = pygame.Rect(100, 120, 200, 60)
        botao_saves = pygame.Rect(100, 250, 200, 60)
        botao_skills = pygame.Rect(100, 380, 200, 60)

        personagem_sobre_jogo = personagem_menu.rect.colliderect(botao_jogo)
        personagem_sobre_saves = personagem_menu.rect.colliderect(botao_saves)
        personagem_sobre_skills = personagem_menu.rect.colliderect(botao_skills)

        mouse_sobre_jogo = botao_jogo.collidepoint(mx, my)
        mouse_sobre_saves = botao_saves.collidepoint(mx, my)
        mouse_sobre_skills = botao_skills.collidepoint(mx, my)

        desenhar_botao(texto_jogo, *botao_jogo, mouse_sobre_jogo or personagem_sobre_jogo)
        desenhar_botao("Saves", *botao_saves, mouse_sobre_saves or personagem_sobre_saves)
        desenhar_botao("Skills", *botao_skills, mouse_sobre_skills or personagem_sobre_skills)

        keys = pygame.key.get_pressed()
        personagem_menu.update(keys, largura, altura)
        tela.blit(personagem_menu.image, personagem_menu.rect.topleft)

        if pulo_anterior and not personagem_menu.pulo:
            if personagem_menu.rect.colliderect(botao_jogo):
                print("Iniciar/Continuar selecionado (pulo)")
                animar_saida_personagem(personagem_menu, largura, altura)
                return "iniciar"
            if personagem_menu.rect.colliderect(botao_saves):
                print("Saves selecionado (pulo)")
            if personagem_menu.rect.colliderect(botao_skills):
                print("Skills selecionado (pulo)")
        pulo_anterior = personagem_menu.pulo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botao_jogo.collidepoint(mx, my):
                    print("Iniciar/Continuar selecionado")
                    return "iniciar"
                if botao_saves.collidepoint(mx, my):
                    print("Saves selecionado")
                if botao_skills.collidepoint(mx, my):
                    print("Skills selecionado")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
                if event.key == pygame.K_SPACE:
                    personagem_menu.pular()

        pygame.display.flip()

if __name__ == "__main__":
    menu()
    pygame.quit()