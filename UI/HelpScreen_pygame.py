import pygame
import sys

class HelpScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Help Screen")
        self.clock = pygame.time.Clock()

    def build_background(self):
        background = pygame.image.load("../assets/fondo_sin_cosas.png")
        self.screen.blit(background, (0, 0))

    def build_sections(self):
        help_title = pygame.image.load("../assets/HELP_title.png")
        self.screen.blit(help_title, (325, 50))

        font = pygame.font.Font(None, 36)
        text = font.render("Movimiento del águila", True, (255, 255, 255))
        self.screen.blit(text, (50, 120))

        aguila_foto = pygame.image.load("../assets/ss_aguila.png")
        self.screen.blit(aguila_foto, (100, 150))

        tuto_eagle = font.render("Usar flechas para mover águila", True, (255, 255, 255))
        self.screen.blit(tuto_eagle, (50, 280))

        label_info_blocks = font.render("Bloques", True, (255, 255, 255))
        self.screen.blit(label_info_blocks, (100, 360))

        bloque_foto = pygame.image.load("../assets/ss_blocks.png")
        self.screen.blit(bloque_foto, (65, 390))

        tuto_blocks = font.render("Para elegir tipo presionar 1, 2 y 3", True, (255, 255, 255))
        self.screen.blit(tuto_blocks, (50, 520))

        tuto_blocks2 = font.render("Para colocar usar mouse", True, (255, 255, 255))
        self.screen.blit(tuto_blocks2, (50, 550))

        label_info_tank = font.render("Movimiento del tanque", True, (255, 255, 255))
        self.screen.blit(label_info_tank, (500, 120))

        tanque_foto = pygame.image.load("../assets/ss_tanque.png")
        self.screen.blit(tanque_foto, (580, 150))

        tuto_tank = font.render("Usar WASD para mover tanque", True, (255, 255, 255))
        self.screen.blit(tuto_tank, (450, 300))

        label_info_shoot = font.render("Disparos", True, (255, 255, 255))
        self.screen.blit(label_info_shoot, (580, 360))

        balas_foto = pygame.image.load("../assets/ss_bala.png")
        self.screen.blit(balas_foto, (570, 390))

        tuto_shoot = font.render("Para disparar presione espacio", True, (255, 255, 255))
        self.screen.blit(tuto_shoot, (500, 540))

    def build_buttons(self):
        pygame.draw.rect(self.screen, (0, 128, 255), (300, 400, 200, 50))
        font = pygame.font.Font(None, 36)
        text = font.render("Back", True, (255, 255, 255))
        self.screen.blit(text, (400, 415))

    def back(self):
        pygame.quit()
        sys.exit()

def main():
    help_screen = HelpScreen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Placeholder code for button click handling
                if 300 <= event.pos[0] <= 500 and 400 <= event.pos[1] <= 450:
                    print("Button clicked!")

        help_screen.build_background()
        help_screen.build_sections()
        help_screen.build_buttons()

        pygame.display.flip()
        help_screen.clock.tick(60)

if __name__ == "__main__":
    main()
