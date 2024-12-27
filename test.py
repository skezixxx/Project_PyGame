import pygame
import sys

 
pygame.init()
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
width, height = 800, 800
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Главное меню')
font = pygame.font.SysFont(None, 48)
 

def draw_text(text, font, surface, x, y):
   textobj = font.render(text, True, BLUE)
   textrect = textobj.get_rect()
   textrect.topleft = (x, y)
   surface.blit(textobj, textrect)

   
def main():
   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()

    
       screen.fill(WHITE)
       width, height = screen.get_size()
       draw_text('Добро пожаловать!', font, screen, 20, 20)
       start_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 50)
       pygame.draw.rect(screen, WHITE, start_button)
       draw_text('Начать', font, screen, width // 2 - 80, height // 2 - 40)
       exit_button = pygame.Rect(width // 2 - 100, height // 2 + 10, 200, 50)
       pygame.draw.rect(screen, WHITE, exit_button)
       draw_text('Выход', font, screen, width // 2 - 80, height // 2 + 20)
       if event.type == pygame.MOUSEBUTTONDOWN:
           if start_button.collidepoint(event.pos):
               print('Тут будет игра:)')
           if exit_button.collidepoint(event.pos):
               pygame.quit()
               sys.exit()
       pygame.display.flip()
if __name__ == '__main__':
   main()
