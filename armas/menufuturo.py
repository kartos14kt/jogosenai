import pygame
import sys
import os

pygame.init()
LARGURA, ALTURA = 1580, 865
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Menu Futuro")

# Carregar imagem de fundo
img_fundo = pygame.image.load(os.path.join(os.path.dirname(__file__), 'futuroIMGmenu.png')).convert()
img_fundo = pygame.transform.scale(img_fundo, (LARGURA-500, ALTURA))

diretorio_principal = os.path.dirname(__file__)
img_arsenal = pygame.image.load(os.path.join(diretorio_principal, 'arsenaldoFUTURO.png')).convert_alpha()
img_arsenal = pygame.transform.scale(img_arsenal, (500, 865))

# Carregar imagem do botão
img_botao = pygame.image.load(os.path.join(diretorio_principal, 'botaoFUTURO.png')).convert_alpha()
img_botao = pygame.transform.scale(img_botao, (100, 50))

# Posição centralizada
botao_x = (LARGURA // 2) - 50
botao_y = 10  # Agora o botão fica no topo da tela

def desenha_gradiente_horizontal(surface, largura, altura, pos_x=0, pos_y=0):
    grad = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for x in range(largura):
        alpha = int(255 * (x / (largura - 1)))  # 0 à esquerda, 255 à direita
        pygame.draw.line(grad, (0, 0, 0, alpha), (x, 0), (x, altura))
    surface.blit(grad, (pos_x, pos_y))

def menu_futuro():
    while True:
        screen.blit(img_fundo, (0, 0))
        # Desenha o arsenal do futuro no lado direito da tela
        screen.blit(img_arsenal, (LARGURA - 500, 0))
        desenha_gradiente_horizontal(screen, 500, ALTURA, LARGURA-1000, 0)
        # Desenha o botão no topo centralizado
        screen.blit(img_botao, (botao_x, botao_y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pressionar ESC para sair
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(botao_x, botao_y, 100, 50).collidepoint(event.pos):
                    # Importa e chama o menu guerra sem abrir nova janela
                    from armas import menuguerra
                    menuguerra.menu_guerra()
                    return

if __name__ == "__main__":
    menu_futuro()