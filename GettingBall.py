import pygame
import random

# Color
Black = (0, 0, 0)
BallColor = (255, 255, 255)
PlayerColor = (160, 82, 45)

pygame.init()
screen = pygame.display.set_mode((640, 480))
myclock = pygame.time.Clock()

flag = 0
GameStart = 0
count = 5
Player_X = 280
Ball_X = random.randrange(15,625)
Ball_Y = 10
BallRadius = 10
SpeedVector_X = random.randint(0, 10) - 5
SpeedVector_Y = random.randint(3, 5)

while flag == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = 1
    #GameStart描画
    while GameStart == 0:
        screen.fill(Black)
        font = pygame.font.SysFont(None, 80)
        Title_text = font.render("Getting Ball", True, BallColor)
        screen.blit(Title_text, (160, 100))
        font = pygame.font.SysFont(None, 40)
        Start_text = font.render("Please wait " + str(count) + "seconds", True, PlayerColor)
        screen.blit(Start_text, (200, 300))
        pygame.display.flip()
        pygame.time.delay(1000)
        count -= 1
        if count == 0: GameStart = 1

    press = pygame.key.get_pressed()
    if press[pygame.K_LEFT] and Player_X > 0: Player_X -= 5
    if press[pygame.K_RIGHT] and Player_X < 560: Player_X += 5
    screen.fill(Black)
    # Player描画
    Player = pygame.Rect(Player_X, 440, 80, 10)
    pygame.draw.rect(screen, PlayerColor, Player)
    # Ball描画
    Ball_X += SpeedVector_X
    Ball_Y += SpeedVector_Y
    pygame.draw.circle(screen, BallColor, (Ball_X, Ball_Y), BallRadius)
    #Ball反射＆当たり判定
    if Ball_X < 10 or Ball_X > 630:SpeedVector_X *= -1  # X反射
    if Ball_Y > 500:                                    # GameOver
        screen.fill(Black)
        font = pygame.font.SysFont(None, 80)
        End_text = font.render("Game Over", True, BallColor)
        screen.blit(End_text, (160, 100))
        pygame.time.delay(1000)
        flag = 1
    if Ball_Y == 430:
        if Ball_X > Player_X and Ball_X < Player_X + 80:
            Ball_X = random.randrange(15,625)
            Ball_Y = 10
            SpeedVector_X = random.randint(0, 10) - 5
            SpeedVector_Y = random.randint(3, 5)
    pygame.display.flip()
    myclock.tick(60)

pygame.quit()
