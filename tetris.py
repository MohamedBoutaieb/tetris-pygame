import pygame
import random
import time, copy, math

pygame.init()
offsetY, offsetX = 25, 30
surfaceX, surfaceY = 300, 625
clock = pygame.time.Clock()
win = pygame.display.set_mode((500, 650))
pygame.display.set_caption("Tetris")
screen = pygame.Surface((500 - (surfaceX + offsetX), 650 - (surfaceY + offsetY)))
on = True
# last = time.time()
background1Color, background2Color = (149, 86, 40), (229, 166, 100)
frameRate = 120


def loss():
    for i in range(0, 10):
        if game.board[0][i + 2] is not None:
            return True
    return False


class Block:
    def __init__(self, position: list, sens: int, endLife: bool, color):
        self.position = position
        self.level = 0
        self.sens = sens
        self.endLife = endLife
        self.color = color
        self.movementPeriod = 1
        self.unit = 30


    def draw(self):
        self.col()
        for i in range(0, 4):
            pygame.draw.rect(win, self.color, (self.position[i][0], self.position[i][1], self.unit, self.unit))
            pygame.draw.rect(win, (0, 0, 0), (self.position[i][0], self.position[i][1], self.unit, self.unit), 1)
            if (self.level == 0) and not game.paused:
                self.position[i][1] += self.unit
        if not game.paused:
            if game.shadow:
                self.drawShadow()
            self.level += 1
            self.level %= frameRate - game.level * 10

    def reverseRotate(self):
        if self.color != (240, 255, 0):
            a = self.position[1][0]
            b = self.position[1][1]
            for i in range(0, 4):
                x = self.position[i][0]
                y = self.position[i][1]
                self.position[i][0] = y - b + a
                self.position[i][1] = -x + a + b

    def rotate(self):
        if self.color != (0, 0, 0):
            a = self.position[1][0]
            b = self.position[1][1]
            for i in range(0, 4):
                x = self.position[i][0]
                y = self.position[i][1]
                self.position[i][0] = -y + b + a
                self.position[i][1] = x - a + b

    def verify(self):
        for i in range(0, 4):
            if ((game.board[math.floor((self.position[i][1] - offsetY) / self.unit)][
                     int((self.position[i][0] - offsetX) / self.unit) + 2] is not None) or
                    (game.board[math.ceil((self.position[i][1] - offsetY) / self.unit)][
                         int((self.position[i][0] - offsetX) / self.unit) + 2] is not None)):
                return False

        return True

    def moveRight(self):
        for i in range(0, 4):
            self.position[i][0] += self.unit

    def moveLeft(self):
        for i in range(0, 4):
            self.position[i][0] -= self.unit

    def pause(self):
        if keys[pygame.K_p] and self.movementPeriod % 30 == 0:
            self.movementPeriod += 1
            game.paused = not game.paused
        if game.paused:
            self.movementPeriod += 1
            self.movementPeriod %= 30

    def move(self):
       # self.level %= frameRate - game.level * 10
        if self.movementPeriod % 15 == 0:
            if keys[pygame.K_LEFT]:
                self.moveLeft()
                self.movementPeriod += 1
                if not self.verify():
                    self.moveRight()
                    self.movementPeriod = 0
            if keys[pygame.K_RIGHT]:
                self.moveRight()
                self.movementPeriod += 1
                if not self.verify():
                    self.moveLeft()
                    self.movementPeriod = 0
            if keys[pygame.K_x]:
                self.rotate()
                self.movementPeriod += 1
                if not self.verify():
                    self.reverseRotate()
                    self.movementPeriod = 0
            if keys[pygame.K_h]:
                self.movementPeriod += 1
                game.shadow = not game.shadow
            if keys[pygame.K_UP]:
                self.level=0
                while self.endLife == False:
                    for i in range(0, 4):
                        self.position[i][1] += self.unit
                    self.col()
        if keys[pygame.K_DOWN]:
            self.level %= 10

        self.col()
        if self.movementPeriod != 0:
            self.movementPeriod += 1
            self.movementPeriod %= 15

    def col(self):
        for i in range(0, 4):
            if ((self.position[i][1] >= surfaceY - offsetY) or (
                    game.board[int((self.position[i][1] - offsetY) / self.unit + 1)][
                        int(self.position[i][0] / self.unit) + 1] is not None) ) and self.level==0:
                self.endLife = True
                break

    def drawShadow(self):
        temp = copy.deepcopy(self)
        while temp.endLife == False:
            for i in range(0, 4):
                temp.position[i][1] += temp.unit
            temp.col()
        for i in range(0, 4):
            pygame.draw.rect(win, (0, 0, 0), (temp.position[i][0], temp.position[i][1], temp.unit, temp.unit), 1)


class Game:
    def __init__(self, score, level, paused, shadow):
        self.score = score
        self.level = level
        self.paused = paused
        self.initBoard()
        self.current = self.initBlocks()
        self.shadow = shadow
    def initBoard(self):
        t = [[j for i in range(0, 14)] for j in range(0, 21)]
        for i in range(0, 20):
            for j in range(2, 12):
                t[i][j] = None
        self.board = t

    def initBlocks(self):
        blue1 = Block([[180, -5], [180, 25], [180, 55], [180, 85]], 1, False, (30, 30, 220))
        b = Block([[180, -5], [180, 25], [150, 25], [150, 55]], 1, False, (255, 20, 20))
        blockr = Block([[150, -5], [150, 25], [180, 25], [180, 55]], 1, False, (15, 200, 15))
        Lr = Block([[150, -5], [150, 25], [180, 25], [210, 25]], 1, False, (255, 94, 19))
        Ll = Block([[180, -5], [180, 25], [150, 25], [120, 25]], 1, False, (19, 94, 255))
        T = Block([[180, -5], [180, 25], [150, 25], [210, 25]], 1, False, (212, 0, 212))
        box = Block([[150, -5], [180, -5], [150, 25], [180, 25]], 1, False, (240, 255, 0))
        self.sac = [blue1, b, blockr, Lr, Ll, T, box]
        self.bag = [0, 0, 0, 0, 0, 0, 0]
        p = random.randint(0, 6)
        self.bag[p] = self.sac[p]
        return self.sac[p]

    def switchPiece(self):
        for i in range(0, len(self.current.position)):
            self.board[int((self.current.position[i][1] - 25) / 30)][
                int((self.current.position[i][0] - 30) / 30) + 2] = self.current.color
        p = random.randint(0, 6)
        if 0 in self.bag:
            while (self.bag[p] != 0):
                p = random.randint(0, 6)
        else:
            self.bag = [0, 0, 0, 0, 0, 0, 0]
        self.current = copy.deepcopy(self.sac[p])
        self.bag[p] = self.sac[p]

    def verifyLine(self):
        n = 0
        for i in range(19, 0, -1):
            while not (None in self.board[i]):
                self.board[i] = self.board[i - 1]
                n += 1
                for j in range(i - 1, 0, -1):
                    if j - 1 > 0:
                        self.board[j] = self.board[j - 1]
                    else:
                        self.board[j] = [0, 0, None, None, None, None, None, None, None, None, None, None, 0, 0]

        if not (None in game.board[0]):
            for j in range(2, 12):
                self.board[0][j] = None
            n += 1
        if n == 1:
            self.score[0] += 40 * min((1 + int(self.score[1] / 10)), 10)
        elif n == 2:
            self.score[0] += 100 * min((1 + int(self.score[1] / 10)), 10)
        elif n == 3:
            self.score[0] += 300 * min((1 + int(self.score[1] / 10)), 10)
        elif n == 4:
            self.score[0] += 400 * min((1 + int(self.score[1] / 10)), 10)
        self.score[1] += n
        if self.score[1] < 100:
            self.level = 1 + int(self.score[1] / 10)
        else:
            self.level = 10


game = Game([0, 0], 1, False, False)
game.initBoard()


def message(s, color, y):
    font = pygame.font.SysFont("Cambria", 35)
    text = font.render(s, True, color)
    win.blit(text, [screen.get_width() / 4 + surfaceX + offsetX, y])


def lossText(s, color, x, y):
    font = pygame.font.SysFont("Cambria", 35)
    text = font.render(s, True, color)
    win.blit(text, [x, y])


def draw():
    if loss():
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 500, 650))
        lossText("game over , your score was:", (255, 255, 255), 45, 200)
        lossText(str(int(game.score[0])), (255, 255, 255), 250 - (int(len(str(int(game.score[0]))) / 2)) * 12, 250)
        lossText("Lines:", (255, 255, 255), 220, 300)
        lossText(str(int(game.score[1])), (255, 255, 255), 250 - (int(len(str(int(game.score[1]))) / 2)) * 12, 350)
        lossText("press R to restart", (255, 255, 255), 120, 400)
    else:
        win.fill(background1Color)
        pygame.draw.rect(win, background2Color, (30, 0, surfaceX, surfaceY))
        pygame.draw.rect(win, (0, 0, 0), (30, 0, surfaceX, surfaceY), 1)
        message("SCORE", (255, 255, 255), 110)
        message(str(int(game.score[0])), (255, 255, 255), 155)
        message("LINES", (255, 255, 255), 220)
        message(str(int(game.score[1])), (255, 255, 255), 265)
        message("LEVEL", (255, 255, 255), 315)
        message(str(int(game.level)), (255, 255, 255), 365)
        message("FPS:", (0, 0, 0), 20)
        message(fps, (0, 0, 0), 55)
        for i in range(0, 20):
            for j in range(2, 12):
                if game.board[i][j] is not None:
                    pygame.draw.rect(win, game.board[i][j], (j * 30 - 30, i * 30 + 25, 30, 30))
                    pygame.draw.rect(win, (0, 0, 0), (j * 30 - 30, i * 30 + 25, 30, 30), 1)
        game.current.draw()
        if game.paused:
            message("PAUSED", (0, 0, 0), 415)


def restart():
    game.level = 1
    game.initBoard()
    game.initBlocks()
    game.score[0] = 0
    game.score[1] = 0


while on:
    clock.tick(frameRate)
    #  pygame.time.get_ticks()
    # dt = time.time() - last
    #  last = time.time()
    #  dt *= 2
    fps = str(int(clock.get_fps()))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
    game.current.pause()

    if not loss() and not game.paused:
        game.current.move()
        game.verifyLine()
        if game.current.endLife:
            game.switchPiece()
    else:
        if keys[pygame.K_r]:
            restart()
    draw()
    pygame.display.update()
pygame.quit()
