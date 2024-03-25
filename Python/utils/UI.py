# Imports
import sys
import pygame

class Button():
    chose = None
    def __init__(self, x, y, width, height, font, screen, buttonText='Button', onclickFunction=None, onePress=False):
        self.x_pos = x*width
        self.y_pos = y*height
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
            'red': '#ff0000',
        }
        self.font = font
        self.screen = screen
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)

        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False


    def process(self):

        mousePos = pygame.mouse.get_pos()
        
        self.buttonSurface.fill(self.fillColors['normal'])
        if Button.chose == self:
            self.buttonSurface.fill(self.fillColors['red'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction(self.x,self.y)

                elif not self.alreadyPressed:
                    self.onclickFunction(self.x, self.y)
                    self.alreadyPressed = True
                Button.chose = self

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)



class UI:
    def __init__(self, shape, solutions) -> None:
        # Configuration
        pygame.init()
        self.fps = 100
        rows, cols = shape
        self.fpsClock = pygame.time.Clock()
        width, height = 30*cols, 30*rows
        self.screen = pygame.display.set_mode((width, height))

        self.font = pygame.font.SysFont('Arial', 40)

        self.objects = [[Button(i, j, 30, 30, self.font, self.screen, "", self.set_solution) for i in range(cols)] for j in range(rows)]
        self.x = int(shape[0]/2)
        self.y = int(shape[1]/2)
        pass

    def set_solution(self, x,y):
        self.x = x
        self.y = y

    def get_solution(self, t):
        return self.x, self.y

    def run(self):
        # Game loop.
        self.screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for object_row in self.objects:
            for object in object_row:
                object.process()

        pygame.display.flip()
        self.fpsClock.tick(self.fps)
