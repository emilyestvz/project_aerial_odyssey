import pygame

class Pontuacao:
    def __init__(self, font_path, font_size, screen_width, screen_height):
        self.score = 0
        self.font = pygame.font.Font(font_path, font_size)
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def reset(self):
        #Reseta a pontuação para 0.
        self.score = 0
        
    def increment(self):
        # Incrementa a pontuação
        self.score += 1
        
    def draw(self, screen):
        # Desenhando a pontuação na tela.
        
        text = self.font.render(f"Points: {self.score}", True, (255, 255, 255))
        
        # Coordenadas para alinhar o texto
        text_x = 10  # 10 pixels da borda esquerda
        text_y = 10 # topo
        
        screen.blit(text, (text_x, text_y))