import pygame
import sys

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Função para exibir o menu
def show_menu(screen):
    
    font_title = pygame.font.Font('./src/fonts/Neucha-Regular.ttf', 50)
    font_option = pygame.font.Font(None, 30)
    
    background = pygame.image.load('./src/img/florest1.jpg')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    """Mostra a tela de início."""
    while True:
        screen.blit(background, (0, 0))  # Desenha a imagem de fundo
        
        text_color = (255, 255, 255)  # cor branco
        shadow_color = (0, 0, 0)      # preto
        
        draw_text("Aerial Odyssey", font_title, text_color, shadow_color, screen, screen.get_width() // 2 - font_title.size("Aerial Odyssey")[0] // 2, screen.get_height() // 4)
        draw_text("Pressione ESPAÇO para jogar", font_option, text_color, shadow_color, screen, screen.get_width() // 2 - font_option.size("Pressione ESPAÇO para jogar")[0] // 2, screen.get_height() // 2)
        draw_text("Pressione ESC para sair", font_option, text_color, shadow_color, screen, screen.get_width() // 2 - font_option.size("Pressione ESC para sair")[0] // 2, screen.get_height() // 2 + 50)

        # Atualiza a tela
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Inicia o jogo
                if event.key == pygame.K_ESCAPE:    
                    pygame.quit()
                    sys.exit()

def draw_text(text, font, text_color, shadow_color, screen, x, y):
    
    # Criando a sombra do txt
    shadow = font.render(text, True, shadow_color)
    screen.blit(shadow, (x+2, y+2)) #Sombra deslocada
    
    # Criando o txt
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (x, y)) 
    
