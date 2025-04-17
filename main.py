from fastapi import background
import pygame, random
import sys
from pygame.locals import K_SPACE, KEYDOWN, QUIT, K_UP
from src.menu import show_menu
from src.pontuacao import Pontuacao

pygame.init()

# Configurações
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

# Função para verificar carregamento de imagens
def load_image(path, scale=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    
    except pygame.error:
        print(f"Erro ao carregar imagem: {path}")
        sys.exit()

# Classes Principais
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        new_size = (60, 60) # Tamanho do pássaro (alt, larg)
        
        self.images = [
            pygame.transform.scale(
                pygame.image.load('./src/img/upbird.png').convert_alpha(), new_size
            ),
            pygame.transform.scale(
                pygame.image.load('./src/img/midbird.png').convert_alpha(), new_size
            ),
            pygame.transform.scale(
                pygame.image.load('./src/img/downbird.png').convert_alpha(), new_size
            ),
        ]
        
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2))
        self.speed = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect.y += self.speed

    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        super().__init__()
        self.image = load_image('./src/img/pipe.png', (PIPE_WIDTH, PIPE_HEIGHT))
        
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(topleft=(xpos, - (self.image.get_height() - ysize)))
        else:
            self.rect = self.image.get_rect(topleft=(xpos, SCREEN_HEIGHT - ysize))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        super().__init__()
        self.image = load_image('./src/img/base.png', (GROUND_WIDTH, GROUND_HEIGHT))
        self.rect = self.image.get_rect(topleft=(xpos, SCREEN_HEIGHT - GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= GAME_SPEED # move a base p a esquerda
        
        # Verifica se a base saiu completamente da tela
        if self.rect.right < 0:
            # Reposiciona a base à direita da tela
            self.rect.x = SCREEN_WIDTH

# Funções auxiliares
def is_off_screen(sprite):
    return sprite.rect.right < 0

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

# Tela Menu
def game_loop():
    
    # Inicialização
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Aerial Odyssey - Prologue')
    background = load_image('./src/img/florest1.jpg', (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    
    bird_group = pygame.sprite.GroupSingle(Bird())
    ground_group = pygame.sprite.Group(Ground(0), Ground(GROUND_WIDTH))
    pipe_group = pygame.sprite.Group(
        get_random_pipes(SCREEN_WIDTH + i * 400)[j]
        for i in range(2) for j in range(2))

    # Inicializando a pontuação
    pontuacao = Pontuacao('./src/fonts/Bangers-Regular.ttf', 25, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    running = True
    game_active = True
    
    show_menu(screen)
    
    # Loop principal
    while running:
        screen.blit(background, (0, 0))
        
        # Verificando eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if game_active:
                    bird_group.sprite.bump()

            # Clique no botão de reiniciar
            if not game_active and event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    # Reiniciar o jogo
                    bird_group = pygame.sprite.GroupSingle(Bird())
                    ground_group = pygame.sprite.Group(Ground(0), Ground(GROUND_WIDTH))
                    pipe_group = pygame.sprite.Group(
                        get_random_pipes(SCREEN_WIDTH + i * 400)[j]
                        for i in range(2) for j in range(2)
                    )
                    pontuacao.reset()
                    game_active = True

    
        if game_active:
            
            # Atualizações
            bird_group.update()
            ground_group.update()
            pipe_group.update()

            if is_off_screen(ground_group.sprites()[0]):
                ground_group.add(Ground(GROUND_WIDTH - 20))

            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[:2])
                pipe_group.add(*get_random_pipes(SCREEN_WIDTH * 2))
                pontuacao.increment() # incrementar a pontuação

            # Verificar colisões
            if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                    pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
                game_active = False  # o jogador perdeu

        # Configurações de estilo
        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)
        pontuacao.draw(screen)
        
        font = pygame.font.Font('./src/fonts/Bangers-Regular.ttf', 50) #Tamanho e tipo de fonte
        
        if not game_active:
            # Cores
            text_color = (255, 255, 255)  # branco
            text_color_button = (0, 0, 0) # preto
            shadow_color = (0, 0, 0)      
            shadow_color_button = (0,0,0)
            button_color = (255, 255, 255)

            # Fontes
            font = pygame.font.Font('./src/fonts/Bangers-Regular.ttf', 50)
            restart_font = pygame.font.Font('./src/fonts/Bangers-Regular.ttf', 30)

            # Game Over - Sombra e Texto
            game_over_shadow = font.render("Game Over", True, shadow_color)
            game_over_text = font.render("Game Over", True, text_color)

            shadow_position = (SCREEN_WIDTH // 2 - game_over_shadow.get_width() // 2 + 2,
                            SCREEN_HEIGHT // 2 - game_over_shadow.get_height() // 2 + 2)
            text_position = (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                            SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2)

            screen.blit(game_over_shadow, shadow_position)
            screen.blit(game_over_text, text_position)

            # Botão de Restart
            restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 50)

            #Desenha a sombra do botão
            shadow_offset = 4
            shadow_rect = restart_button.move(shadow_offset, shadow_offset)
            pygame.draw.rect(screen, shadow_color_button, shadow_rect, border_radius=12)

            # Desenha o botão principal por cima
            pygame.draw.rect(screen, button_color, restart_button, border_radius=12)

            # Texto do botão por cima do botão
            restart_text = restart_font.render("Restart", True, text_color_button)
            screen.blit(restart_text, (
                restart_button.x + (restart_button.width - restart_text.get_width()) // 2,
                restart_button.y + (restart_button.height - restart_text.get_height()) // 2
            ))



        pygame.display.flip()
        clock.tick(30)

# Executando o jogo
game_loop()
