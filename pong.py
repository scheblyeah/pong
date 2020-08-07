import pygame
import random

#  To do :
# -zwischenmenu mit esc,
# -pvp, mit dir selber spielen
# -zielpunktezahl in menü einstellen
# -verschiedene ballgeschwindigkeiten für schwierigkeiten
# -zurück zum menü bug
# -ball berührt cpupaddle nicht ganz

pygame.init()
pygame.display.set_caption("Pong")

WIDTH = 600
HEIGHT = 400
BORDER = 20
PADDLESPEED = 4
PADDLESPEEDCPU = 2
DRALLPLAYER = 3
DRALLCPU = 2
POINTSGOAL = 5
CPUPADDLEMOVETOLLERANCE = 10
BALLVELOCITY = 5


BGCOLOR =pygame.Color("black")
FGCOLOR = pygame.Color("white")
fontSmall = pygame.font.Font('freesansbold.ttf', 16)
fontBig = pygame.font.Font('freesansbold.ttf', 64)
boingsound = pygame.mixer.Sound('button.wav')
winsound = pygame.mixer.Sound('win.wav')
losesound = pygame.mixer.Sound('lose.wav')

class Menu:
    menurun = True
    difficulties = [("Easy", 2), ("Normal", 3), ("Hard", 4), ("Impossible", 6)] # list of tuples consisting of the difficulty with their matching cpuPaddleSpeed
    difficulty = 1 #current index of the difficulties list

    
    def printMenus(self,text, color, width, height, fontSize):
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        textInfo = font.render(text, False, color)
        screen.blit(textInfo, (width, height))

    def printDifficulty(self):
        self.printMenus('Difficulty: ' + self.difficulties[self.difficulty % len(self.difficulties)] [0], FGCOLOR, WIDTH // 2 - 70, HEIGHT//2, 16)


    def unprintDifficulty(self):
        self.printMenus('Difficulty: ' + self.difficulties[self.difficulty % len(self.difficulties)] [0], BGCOLOR, WIDTH // 2 - 70, HEIGHT//2, 16)

    def printMenu(self):
        self.printMenus('PONG', FGCOLOR, WIDTH // 2 - 100, HEIGHT//4, 64)
        self.printMenus('Press space to continue', FGCOLOR, WIDTH // 2 - 95, HEIGHT//3*2, 16)
        self.printDifficulty()

    def unprintMenu(self):
        self.printMenus('PONG', BGCOLOR, WIDTH // 2 - 100, HEIGHT//4, 64)
        self.printMenus('Press space to continue', BGCOLOR, WIDTH // 2 - 95, HEIGHT//3*2, 16)
        self.unprintDifficulty()


    def continueToGame(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.menurun = False

    def continueToMenu(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            menu.menurun = True

    def changeDifficulty(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.unprintDifficulty()
            self.difficulty += 1
            self.printDifficulty()
        if keys[pygame.K_LEFT]:
            self.unprintDifficulty()
            self.difficulty -= 1
            self.printDifficulty()

class Score:
    scoreCpu = 0
    scorePlayer = 0
    scoreGoal = POINTSGOAL
    gameIsOver = False

    def printcpu(self):
         scoretextcpu1 = fontSmall.render('CPU: ' + str(self.scoreCpu-1), False, FGCOLOR)
         scoretextcpu2 = fontSmall.render('CPU: ' + str(self.scoreCpu), False, BGCOLOR)
         screen.blit(scoretextcpu1, (WIDTH // 4 - 50, 0))
         screen.blit(scoretextcpu2, (WIDTH // 4 - 50, 0))

    def printplayer(self):
        scoretextplayer1 = fontSmall.render('Player: ' + str(score.scorePlayer-1), False, FGCOLOR)
        scoretextplayer2 = fontSmall.render('Player: ' + str(score.scorePlayer), False, BGCOLOR)
        screen.blit(scoretextplayer1, (WIDTH//4*3, 0))
        screen.blit(scoretextplayer2, (WIDTH//4*3, 0))
    
    def checkForWin(self):
        if self.scoreCpu >= self.scoreGoal or self.scorePlayer >= self.scoreGoal:
            return True
        return False

    def getWinner(self):
        if self.scorePlayer >= self.scoreGoal:
            winsound.play()
            return 'You won the game!'
        if self.scoreCpu >= self.scoreGoal:
            losesound.play()
            return 'You lost the game!'
        return ' '

    def printWinner(self, menu):
        menu.printMenus(self.getWinner(), FGCOLOR, WIDTH // 2-150, HEIGHT //2-50, 32)
        menu.printMenus('Press space to continue', FGCOLOR, WIDTH // 2 - 95, HEIGHT//3*2, 16)

    


class Paddle:
    momentum = 0 #if paddle is standing still = 0 moving up = 1, moving down = -1

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def show(self, color):
        pygame.draw.rect(screen, color , (self.x, self.y, self.width, self.height))

    #function to move ball when up or down key is pushed
    def move(self):
        self.show(BGCOLOR) #paint over the old ball
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.y > BORDER : #checking for wall collision up
            self.y = self.y - PADDLESPEED
            self.momentum = 1
        elif keys[pygame.K_DOWN] and self.y + self.height < HEIGHT-BORDER: #checking for wall collision down
            self.y = self.y + PADDLESPEED
            self.momentum = -1
        else:
            self.momentum = 0
        self.show(FGCOLOR)
    
    #function to move the cpupaddle depending on the balls position
    def moveCPU(self, ball):
        self.show(BGCOLOR)
        if self.calculateMovementForBall(ball) == 1 and self.y - PADDLESPEEDCPU > BORDER:
            self.y = self.y - PADDLESPEEDCPU
            self.momentum = 1
        elif self.calculateMovementForBall(ball) == -1 and self.y + self.height + PADDLESPEEDCPU < HEIGHT-BORDER:
            self.y = self.y + PADDLESPEEDCPU
            self.momentum = -1
        else:
            self.momentum = 0
        self.show(FGCOLOR)

    #returns 1 if paddle has to go up, -1 for down, 0 to not move
    def calculateMovementForBall(self, ball):
        paddlecenter = self.y + self.height // 2
        if paddlecenter - CPUPADDLEMOVETOLLERANCE < ball.y and paddlecenter + CPUPADDLEMOVETOLLERANCE > ball.y:
            return 0
        elif paddlecenter > ball.y:
            return 1
        elif paddlecenter < ball.y:
            return -1
        
class Ball:
    radius = 7
    hitstreak = 0 # saves how many times a paddle was hit since the last time that the ball went out

    def __init__(self, x, y, velocityX, velocityY):
        self.x = x
        self.y = y
        self.velocityX = velocityX 
        self.velocityY = velocityY
    
    def move_ball(self, paddle, paddle2, score, menu):
        self.show(BGCOLOR) #overwrite previous shown ball with background color
        #manage collision with wall left and right
        if self.checkCollision(paddle) or self.checkCollision(paddle2): # for right wall: "self.x + self.velocityX + self.radius > WIDTH-BORDER or " for left wall: "self.x + self.velocityX - self.radius < BORDER or"
            self.velocityX = -self.velocityX #bei collision ändert der ball die richtug
            self.hitstreak += 1 #für jede paddle collision wird der counter erhöht für die ballgeschwindigkeit
            if paddle.momentum == -1:
                self.velocityY -= DRALLPLAYER
            elif paddle.momentum == 1:
                self.velocityY += DRALLPLAYER
            elif paddle2.momentum == -1:
                self.velocityY -= DRALLCPU
            elif paddle2.momentum == 1:
                self.velocityY += DRALLCPU
        #manage collision with wall up and down
        if self.y + self.velocityY + self.radius > HEIGHT-BORDER or self.y + self.velocityY - self.radius < BORDER:
            boingsound.play()
            self.velocityY = -self.velocityY
        #check if ball went out on the right or left side and reset ball if he went out
        if self.x + self.velocityX + self.radius > WIDTH or self.x + self.velocityX - self.radius < 0:
            if self.x > WIDTH//2:
                score.scoreCpu += 1
                score.printcpu()
                self.velocityX = BALLVELOCITY
            else: 
                score.scorePlayer += 1
                score.printplayer()
                self.velocityX = - BALLVELOCITY
            if score.checkForWin():
                score.gameIsOver = True
                score.printWinner(menu)
            else:
                self.x = WIDTH//2
                self.y = HEIGHT//2
                self.velocityY = self.getRandomNumberBetweenExceptZero(-2,2)  # ball kommt jedes mal anders 
                self.hitstreak = 0
        if not score.gameIsOver:
            self.x = self.x + self.velocityX
            self.y = self.y + self.velocityY
            self.show(FGCOLOR)
            self.speedUpBall()

    def show(self, color):
        pygame.draw.circle(screen, color , (self.x, self.y), self.radius)

    #checks if the ball collides with the paddle
    def checkCollision(self, paddle):
        newX = self.x + self.velocityX + self.radius
        newY = self.y + self.velocityY + self.radius
        if newX > paddle.x and newX < paddle.x + paddle.width*3 and newY +self.radius >= paddle.y and newY -self.radius <= paddle.y + paddle.height:
            boingsound.play()
            return True
        return False

    def speedUpBall(self): # every 5 hits the ball gets faster
       if abs(self.velocityX) < 25: # ab xvel = 20 kann paddle den ball nicht mehr spielen, da xvel größer ist als paddle.width*2
            if self.hitstreak % 2 == 1:
                self.hitstreak = 0
                self.velocityX += int( abs(self.velocityX)/self.velocityX ) #wenn positiv = +1, wenn negativ = -1

    def getRandomNumberBetweenExceptZero(self, min, max):
        result = 0
        while result == 0:
            result = random.randint(min, max)
        return result


screen = pygame.display.set_mode((WIDTH, HEIGHT))

#drawing the walls 
pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (0,0), (WIDTH,BORDER))) #north wall
pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (0,HEIGHT-BORDER), (WIDTH,BORDER))) #south wall 
#pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (0,0), (BORDER,HEIGHT))) #left wall 
#pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (WIDTH-BORDER,0), (BORDER,HEIGHT))) #right wall


#initlialize objects
ball = Ball(WIDTH//2, HEIGHT //2, BALLVELOCITY , 0)
paddle = Paddle(WIDTH - 50, HEIGHT //2 -40, 10, 80)
paddlecpu = Paddle(50, HEIGHT //2 - 40, 10, 80)
score = Score()
menu = Menu()

run = True
while run:
    
    while menu.menurun:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu.menurun = False
                run = False
        menu.printMenu()
        menu.continueToGame()
        menu.changeDifficulty()
        pygame.display.flip()
        menu.unprintMenu()

    

    PADDLESPEEDCPU = menu.difficulties[menu.difficulty%len(menu.difficulties)] [1]

    if run:
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not score.gameIsOver:
            score.printcpu()
            score.printplayer()

            ball.move_ball(paddle, paddlecpu, score, menu)
            paddle.move()
            paddlecpu.moveCPU(ball)
        else:
            while not menu.menurun:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                menu.continueToMenu()
                pygame.time.delay(100)
            
            ball = Ball(WIDTH//2, HEIGHT //2, BALLVELOCITY , 0)
            paddle = Paddle(WIDTH - 50, HEIGHT //2 -40, 10, 80)
            paddlecpu = Paddle(50, HEIGHT //2 - 40, 10, 80)
            score = Score()
            menu = Menu()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (0,0), (WIDTH,BORDER))) #north wall
            pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect( (0,HEIGHT-BORDER), (WIDTH,BORDER))) #south wall 
        pygame.display.flip()
        

