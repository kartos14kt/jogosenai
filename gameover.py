import pygame
import sys

# Inicializa o pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 600, 400
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Game Over")

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
espaco_entre = 30

# Calcula a posição X inicial para centralizar os dois botões juntos
total_largura = largura_botao_tentar + largura_botao_menu + espaco_entre
x_inicial = (LARGURA - total_largura) // 2

botao_tentar = pygame.Rect(x_inicial, ALTURA//2 + 30, largura_botao_tentar, altura_botao)
botao_menu = pygame.Rect(x_inicial + largura_botao_tentar + espaco_entre, ALTURA//2 + 30, largura_botao_menu, altura_botao)

def desenhar_menu():
    tela.fill(CINZA)
    texto_gameover = fonte_grande.render("GAME OVER", True, VERMELHO)
    tela.blit(texto_gameover, (LARGURA//2 - texto_gameover.get_width()//2, ALTURA//2 - 100))

    # Botão Tentar Novamente
    pygame.draw.rect(tela, VERDE, botao_tentar)
    pygame.draw.rect(tela, PRETO, botao_tentar, 2)
    texto_tentar = fonte_media.render("Tentar Novamente", True, BRANCO)
    tela.blit(
        texto_tentar,
        (
            botao_tentar.x + (botao_tentar.width - texto_tentar.get_width()) // 2,
            botao_tentar.y + (botao_tentar.height - texto_tentar.get_height()) // 2
        )
    )

    # Botão Menu
    pygame.draw.rect(tela, VERMELHO, botao_menu)
    pygame.draw.rect(tela, PRETO, botao_menu, 2)
    texto_menu = fonte_media.render("Menu", True, BRANCO)
    tela.blit(
        texto_menu,
        (
            botao_menu.x + (botao_menu.width - texto_menu.get_width()) // 2,
            botao_menu.y + (botao_menu.height - texto_menu.get_height()) // 2
        )
    )

# Exemplo de função principal em gameover.py
def main():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_menu.collidepoint(evento.pos):
                    return "menu"
                if botao_tentar.collidepoint(evento.pos):
                    return "tentar"
        desenhar_menu()
        pygame.display.flip()

if __name__ == "__main__":
    main()