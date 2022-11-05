import sys, pygame
from constants import *
from snake import Snake
from food import Food


class GameView():

    def __init__(self, window, font, oModel):

        self.window = window
        self.font = font
        self.oModel = oModel

        self.oFood = Food()
        self.oSnake = Snake(self.oFood)
        
        self.STATE = 1

    def checkGameOver(self):
        if (self.oSnake.snakeCoordinates[self.oSnake.HEAD]['x'] == -1 or 
            self.oSnake.snakeCoordinates[self.oSnake.HEAD]['x'] == CELLWIDTH or 
            self.oSnake.snakeCoordinates[self.oSnake.HEAD]['y'] == -1 or 
            self.oSnake.snakeCoordinates[self.oSnake.HEAD]['y'] == CELLHEIGHT):
            return "Reset Game"

        for snakeBody in self.oSnake.snakeCoordinates[1:]:
            if snakeBody['x'] == self.oSnake.snakeCoordinates[self.oSnake.HEAD]['x'] and snakeBody['y'] == self.oSnake.snakeCoordinates[self.oSnake.HEAD]['y']:
                return "Reset Game"

    def handleKeys(self, event):
        if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.oSnake.direction != self.oSnake.RIGHT:
            self.oSnake.direction = self.oSnake.LEFT
        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.oSnake.direction != self.oSnake.LEFT:
            self.oSnake.direction = self.oSnake.RIGHT
        elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.oSnake.direction != self.oSnake.DOWN:
            self.oSnake.direction = self.oSnake.UP
        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.oSnake.direction != self.oSnake.UP:
            self.oSnake.direction = self.oSnake.DOWN
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def update(self):

        if self.oSnake.snakeCoordinates[self.oSnake.HEAD]['x'] == self.oFood.x and self.oSnake.snakeCoordinates[self.oSnake.HEAD]['y'] == self.oFood.y:
            self.oFood.generateNewFoodObject()
        else:
            del self.oSnake.snakeCoordinates[-1]

        if self.oSnake.direction == self.oSnake.UP:
            newHead = {'x': self.oSnake.snakeCoordinates[self.oSnake.HEAD]['x'],'y': self.oSnake.snakeCoordinates[self.oSnake.HEAD]['y'] - 1}
        elif self.oSnake.direction == self.oSnake.DOWN:
            newHead = {'x': self.oSnake.snakeCoordinates[self.oSnake.HEAD]['x'], 'y': self.oSnake.snakeCoordinates[self.oSnake.HEAD]['y'] + 1}
        elif self.oSnake.direction == self.oSnake.LEFT:
            newHead = {'x': self.oSnake.snakeCoordinates[self.oSnake.HEAD]['x'] - 1, 'y': self.oSnake.snakeCoordinates[self.oSnake.HEAD]['y']}
        elif self.oSnake.direction == self.oSnake.RIGHT:
            newHead = {'x': self.oSnake.snakeCoordinates[self.oSnake.HEAD]['x'] + 1, 'y': self.oSnake.snakeCoordinates[self.oSnake.HEAD]['y']}

        self.oSnake.snakeCoordinates.insert(0, newHead)

    def draw(self):

        '''
        Draw game window, snake, food, score
        '''

        self.update()

        # Draw game window
        for x in range(0, WINDOW_WIDTH, CELLSIZE):  # draw vertical lines
            pygame.draw.line(self.window, DARKGRAY, (x, 0), (x, WINDOW_HEIGHT))

        for y in range(0, WINDOW_HEIGHT, CELLSIZE):  # draw horizontal lines
            pygame.draw.line(self.window, DARKGRAY, (0, y), (WINDOW_WIDTH, y))

        # Draw Snake
        for coord in self.oSnake.snakeCoordinates:

            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE

            snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(self.window, DARKGREEN, snakeSegmentRect)

            snakeInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(self.window, GREEN, snakeInnerSegmentRect)

        # Draw Food
        x = self.oSnake.oFood.x * CELLSIZE
        y = self.oSnake.oFood.y * CELLSIZE
        foodRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(self.window, RED, foodRect)


        # Draw Score
        z = len(self.oSnake.snakeCoordinates) - 3
        scoreSurface = self.font.render('Score: %s' % (z), True, WHITE)
        scoreRect = scoreSurface.get_rect()
        scoreRect.topleft = (WINDOW_WIDTH - 120, 10)
        
        self.window.blit(scoreSurface, scoreRect)

        gameStatus = self.checkGameOver()

        if gameStatus == "Reset Game":
            del self.oSnake
            self.oSnake = Snake(self.oFood)
            self.STATE = 2
            return False
        else:
            return True