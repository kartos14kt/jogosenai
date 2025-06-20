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

while True:
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, 600, 865))  # retângulo vermelho
    screen.blit(img_fundo, (0, 0))
    screen.blit(img_arsenal, (0, 0))
    desenha_gradiente_horizontal(screen, 600, 865, 600, 0)
    screen.blit(sprite_pistola, (45, 83))  # desenha a primeira sprite do spritesheet na posição (45, 83)

    mouse_pos = pygame.mouse.get_pos()
    pistola_rect = pygame.Rect(45, 83, 100, 100)
    if pistola_rect.collidepoint(mouse_pos):
        texto_x = 55 + (100 - texto_pistola.get_width()) // 2
        texto_y = 83 + 100  # 10 pixels abaixo da imagem
        screen.blit(texto_pistola, (texto_x, texto_y))

        
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # Pressionar ESC para sair
                pygame.quit()
                sys.exit()
