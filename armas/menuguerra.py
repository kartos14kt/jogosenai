import pygame
import sys
import os

# Inicialização do pygame e tela
pygame.init()
LARGURA, ALTURA = 1580, 865  # ajuste conforme necessário
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Menu Principal")
font = pygame.font.SysFont(None, 40)

# Carregamento da imagem de fundo
diretorio_principal = os.path.dirname(__file__)
img_fundo = pygame.image.load(os.path.join(diretorio_principal, 'guerraIMGmenu.png')).convert()
img_fundo = pygame.transform.scale(img_fundo, (LARGURA, ALTURA))
img_arsenal = pygame.image.load(os.path.join(diretorio_principal, 'arsenaldeGUERRA.png')).convert_alpha()
img_arsenal = pygame.transform.scale(img_arsenal, (600, 865))


img_pistola_sheet = pygame.image.load(os.path.join(diretorio_principal, 'armasARSENAL', 'pistola.png')).convert_alpha()
# Extrai a primeira sprite 32x32 do spritesheet
sprite_pistola = pygame.Surface((32, 32), pygame.SRCALPHA)
sprite_pistola.blit(img_pistola_sheet, (0, 0), (0, 0, 32, 32))
sprite_pistola = pygame.transform.scale(sprite_pistola, (100, 100))

def desenha_gradiente_horizontal(surface, largura, altura, pos_x=0, pos_y=0):
    grad = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for x in range(largura):
        alpha = int(255 * (1 - x / (largura - 1)))  # 255 à esquerda, 0 à direita
        pygame.draw.line(grad, (0, 0, 0, alpha), (x, 0), (x, altura))
    surface.blit(grad, (pos_x, pos_y))

# Fonte Comic Sans
fonte_pistola = pygame.font.SysFont("comicsansms", 24, bold=True)
texto_pistola = fonte_pistola.render("PISTOLA", True, (255, 255, 255))
texto_moedas = fonte_pistola.render("20 moedas", True, (255, 255, 0))  # Amarelo

# Botão centralizado no topo (y=10)
botao_largura, botao_altura = 100, 50
botao_x = (LARGURA // 2) - (botao_largura // 2)
botao_y = 10
botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)

# Cor do botão e borda
cor_botao = (50, 50, 200)
cor_borda = (255, 255, 0)

def menu_guerra():
    while True:
        pygame.draw.rect(screen, (255, 0, 0), (0, 0, 600, 865))  # retângulo vermelho
        screen.blit(img_fundo, (0, 0))
        screen.blit(img_arsenal, (0, 0))
        desenha_gradiente_horizontal(screen, 600, 865, 600, 0)
        screen.blit(sprite_pistola, (45, 83))

        # Desenha o botão GUERRA
        pygame.draw.rect(screen, cor_botao, botao_rect)
        pygame.draw.rect(screen, cor_borda, botao_rect, 3)  # borda amarela
        texto_menu = fonte_pistola.render("GUERRA", True, (255,255,255))
        texto_menu_rect = texto_menu.get_rect(center=botao_rect.center)
        screen.blit(texto_menu, texto_menu_rect)

        # Botão VOLTAR (transparente, só texto, logo abaixo do botão guerra)
        botao_voltar_y = botao_y + botao_altura + 10
        texto_voltar = fonte_pistola.render("VOLTAR", True, (255,255,255))
        texto_voltar_rect = texto_voltar.get_rect(center=(botao_x + botao_largura//2, botao_voltar_y + botao_altura//2))
        screen.blit(texto_voltar, texto_voltar_rect)
        botao_voltar_rect = pygame.Rect(botao_x, botao_voltar_y, botao_largura, botao_altura)

        mouse_pos = pygame.mouse.get_pos()
        pistola_rect = pygame.Rect(45, 83, 100, 100)
        if pistola_rect.collidepoint(mouse_pos):
            texto_x = 50 + (100 - texto_pistola.get_width()) // 2
            texto_y = 83 - texto_pistola.get_height() - 5
            screen.blit(texto_pistola, (texto_x, texto_y))
            moedas_x = 50 + (100 - texto_moedas.get_width()) // 2
            moedas_y = 83 + 100 + 5
            screen.blit(texto_moedas, (moedas_x, moedas_y))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botao_rect.collidepoint(event.pos):
                    from armas import menufuturo
                    menufuturo.menu_futuro()
                    return
                if botao_voltar_rect.collidepoint(event.pos):
                    return "voltar"

# Executa o menu guerra se este arquivo for o principal
if __name__ == "__main__":
    while True:
        from menu import menu
        acao_menu = menu()
        if acao_menu == "iniciar":
            # Aqui você pode iniciar o jogo, se desejar
            break
        elif acao_menu == "sair" or acao_menu is None:
            break
        # Se acao_menu == "voltar" ou qualquer outro valor, apenas continua o loop e reabre o menu
