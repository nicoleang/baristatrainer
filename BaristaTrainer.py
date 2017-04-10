import pygame

class BaristaGame(PygameGame):
    def init(self):
        self.mode == "intro"
    def intro():
        while (self.mode == "intro"):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    intro = False
            image = pygame.image.load('Screens/StartScreen.png').convert_alpha()

            pygame.display.update()
            clock.tick(15)

