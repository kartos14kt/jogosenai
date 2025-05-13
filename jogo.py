class Consumivel(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo):
        super().__init__()
        self.tipo = tipo  # Tipo do consumível: "velocidade" ou "vida"
        self.frames = []
        self.carregar_frames()
        self.image = self.frames[0] if tipo == "vida" else self.frames[1]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def carregar_frames(self):
    # Carregar a sprite sheet "consheet" da pasta "sprites"
    consheet = pygame.image.load(os.path.join(diretorioimg, 'sprites', 'consheet.png')).convert_alpha()
    
    # Assume que a sprite sheet tem os frames dos consumíveis
    for i in range(2):  # Dois tipos de consumíveis
        frame = consheet.subsurface((i * 32, 0, 32, 32))  # Cada frame tem 32x32
        self.frames.append(frame)

    def aplicar_efeito(self, personagem):
        if self.tipo == "vida":
            global vidas
            vidas += 1  # Aumenta a vida do personagem
            print("Vida aumentada!")
        elif self.tipo == "velocidade":
            personagem.velocidade += 1  # Aumenta a velocidade do personagem
            print("Velocidade aumentada!")