import pygame

pygame.init()
win = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

isJump = False
jumpCount, fallCount = 10, 10
x, y, width, height = 200, 300, 20, 20

run = True
while run:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        isJump = True
    if isJump:
        if jumpCount > 0:
            y -= (jumpCount**1.5) / 3
            jumpCount -= 1
            print(jumpCount)
        elif fallCount > 0:
            y += (fallCount**1.5) / 3
            fallCount -= 1
            print(fallCount)
        else:
            isJump = False
            jumpCount, fallCount = 10, 10
            print(jumpCount, fallCount)

    win.fill((53, 81, 92))
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.flip()
