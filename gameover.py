import pygame
import sys

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 1580, 865
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
VERDE = (0, 200, 0)
CINZA = (100, 100, 100)

# Fonte
fonte_grande = pygame.font.SysFont(None, 72)
fonte_media = pygame.font.SysFont(None, 40)

# Botões (ajustados para centralizar e caber o texto)
largura_botao_tentar = 255
largura_botao_menu = 120
altura_botao = 50
espaco_entre = 10  # Reduzido para aproximar os botões

# Calcula a posição X inicial para centralizar os botões
x_tentar = (LARGURA - largura_botao_tentar) // 2
x_menu = (LARGURA - largura_botao_menu) // 2

y_tentar = ALTURA//2 + 30
y_menu = y_tentar + altura_botao + espaco_entre

botao_tentar = pygame.Rect(x_tentar, y_tentar, largura_botao_tentar, altura_botao)
botao_menu = pygame.Rect(x_menu, y_menu, largura_botao_menu, altura_botao)

def desenhar_menu(mouse_pos=None, anim_tamanho=1.0):
    tela.fill(PRETO)
    # Animação: aumenta o tamanho da fonte do GAME OVER
    fonte_animada = pygame.font.SysFont(None, int(72 * anim_tamanho))
    texto_gameover = fonte_animada.render("GAME OVER", True, VERMELHO)
    tela.blit(texto_gameover, (LARGURA//2 - texto_gameover.get_width()//2, ALTURA//2 - 100))

    # Botão Tentar Novamente (texto cresce ao passar o mouse)
    if mouse_pos and botao_tentar.collidepoint(mouse_pos):
        fonte_btn = pygame.font.SysFont(None, 48)
    else:
        fonte_btn = fonte_media
    texto_tentar = fonte_btn.render("Tentar Novamente", True, BRANCO)
    tela.blit(
        texto_tentar,
        (
            botao_tentar.x + (botao_tentar.width - texto_tentar.get_width()) // 2,
            botao_tentar.y + (botao_tentar.height - texto_tentar.get_height()) // 2
        )
    )

    # Botão Menu (texto cresce ao passar o mouse)
    if mouse_pos and botao_menu.collidepoint(mouse_pos):
        fonte_btn2 = pygame.font.SysFont(None, 48)
    else:
        fonte_btn2 = fonte_media
    texto_menu = fonte_btn2.render("Menu", True, BRANCO)
    tela.blit(
        texto_menu,
        (
            botao_menu.x + (botao_menu.width - texto_menu.get_width()) // 2,
            botao_menu.y + (botao_menu.height - texto_menu.get_height()) // 2
        )
    )

# Exemplo de função principal em gameover.py
def main():
    anim_tamanho = 1.0
    animando = True
    tempo_anim = 0
    clock = pygame.time.Clock()
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_menu.collidepoint(evento.pos):
                    return "menu"
                if botao_tentar.collidepoint(evento.pos):
                    return "tentar"
        if animando:
            tempo_anim += clock.get_time()
            # anima de 1.0 até 1.15 em 400ms
            if tempo_anim < 400:
                anim_tamanho = 1.0 + 0.15 * (tempo_anim / 400)
            else:
                anim_tamanho = 1.15
                animando = False
        desenhar_menu(mouse_pos, anim_tamanho)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()