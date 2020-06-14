from player import *
from network import Network

pygame.mixer.init()
turretsound = pygame.mixer.Sound ( "turrent2.wav" )
turretStoppedsound=pygame.mixer.Sound ( "turrentstopped.wav" )
bulletsound=pygame.mixer.Sound ( "Explosion.wav" )
tanksound=pygame.mixer.Sound ( "tankmovement.wav" )
class Config(object):
    """ a class to hold all game constants that may be modded by the user"""
    fullscreen = False
    width = 1000
    height = 600
    fps = 100


def redraw_window(win,tank1,tank2):
    tank1.drawTank(win)
    tank2.drawTank(win)
    pass
def main():
    n=Network()
    pygame.init()
    screen=pygame.display.set_mode((Config.width,Config.height))
    #creating a background
    background=pygame.Surface(screen.get_size())
    background.fill((241, 174, 245))
    pygame.draw.rect(background, (0, 0, 0), (0, 0, 10,600 ))
    pygame.draw.rect(background, (0, 0, 0), (0, 0, 1000,10 ))
    pygame.draw.rect(background, (0, 0, 0), (0, 590, 1000, 10))
    pygame.draw.rect(background, (0, 0, 0), (990, 0, 10, 600))
    pygame.draw.rect(background, (0, 0, 0), (12, 42, 206, 21))
    pygame.draw.rect(background, (0, 0, 0), (781, 42, 206, 21))
    pygame.draw.rect(background, (255, 255, 255), (15, 45, 200, 15))
    pygame.draw.rect(background, (255, 255, 255), (784, 45, 200, 15))
    background=background.convert()
    screen.blit(background, (0, 0))
    font = pygame.font.Font('freesansbold.ttf', 20)
    controls = font.render("w=> forward/a=>turn left/s=>backward/d=>turn right/down=>fire", True, (0, 0, 0), None)
    controls_rect = controls.get_rect()
    controls_rect.center=(470,30)
    pygame.display.set_caption("Game Of TanKs")
    text1=font.render("Your Health", True , (0,0,250) ,None)
    text_rect1=text1.get_rect()
    text_rect1.center=(80,30)
    text2 = font.render("Opponent Health", True, (255, 0, 0), None)
    text_rect2 =text2.get_rect()
    text_rect2.center=(900,30)
    bulletgroup=pygame.sprite.Group()
    Bullet.groups=bulletgroup
    clock=pygame.time.Clock()
    FPS=Config.fps
    playtime=0
    F=0
    pos=n.getP()
    Tank1=Tank(pos[0],pos[1],pos[2])
    if pos[0][0]==200:
        Tank2=Tank((0,0,200),(650,450),-90)
    else:
        Tank2=Tank((200, 200, 0),(150, 150), 90)
    mainloop=True
    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0  # seconds passed since last frame (float)
        playtime += seconds
        Tank2.tankAngle,Tank2.rect,Tank2.turretAngle,Tank2.firestatus,Tank2.stat,Tank2.health=n.send((Tank1.tankAngle,Tank1.rect,Tank1.turretAngle,Tank1.firestatus,Tank1.stat,Tank1.health))
        Tank2.pos[0],Tank2.pos[1]=Tank2.rect.centerx,Tank2.rect.centery
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame window closed by user
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False  # exit game
                if event.key == pygame.K_RIGHT or event.key==pygame.K_LEFT:
                    turretsound.play(-1)
                if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                    tanksound.play(-1)

            if event.type==pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key==pygame.K_LEFT:
                    turretsound.stop()
                    turretStoppedsound.play()
                if pygame.key.get_pressed()[pygame.K_w]==False and pygame.key.get_pressed()[pygame.K_a]==False and pygame.key.get_pressed()[pygame.K_s]==False and pygame.key.get_pressed()[pygame.K_d]==False:
                    tanksound.stop()



        #Tank1.clear(screen, background)  # funny effect if you outcomment this line
        screen.blit(background, (0, 0))
        screen.blit(text1,text_rect1)
        screen.blit(text2,text_rect2)
        screen.blit(controls, controls_rect)
        pygame.draw.rect(background, (255, 255, 255), (15, 45, 200, 15))
        pygame.draw.rect(background, (255, 255, 255), (784, 45, 200, 15))
        pygame.draw.rect(background, (0, 255, 0), (15, 45, Tank1.health * 2, 15))
        pygame.draw.rect(background, (255, 0, 0), (784, 45, Tank2.health * 2, 15))
        if Tank2.health<=0:
            winText = font.render("YOU WON", True, (0, 0, 0), None)
            winText_rect = winText.get_rect()
            winText_rect.center = (Config.width // 2, Config.height // 2)
            pygame.draw.rect(background, (255, 255, 255), (784, 45, 200, 15))
            screen.blit(background, (0, 0))
            screen.blit(winText,winText_rect)
            pygame.display.flip()
            pygame.time.delay(5000)
            mainloop=False
        elif Tank1.health<=0:
            lostText = font.render("YOU LOST", True, (0, 0, 0), None)
            lostText_rect = lostText.get_rect()
            lostText_rect.center = (Config.width // 2, Config.height // 2)
            pygame.draw.rect(background, (255, 255, 255), (15, 45, 200, 15))
            screen.blit(background, (0, 0))
            screen.blit(lostText,lostText_rect)
            pygame.draw.rect(background, (255, 255, 255), (15, 45, 200, 15))
            pygame.display.flip()
            pygame.time.delay(5000)
            mainloop=False

        #pygame.display.set_caption(f"Your Health : {Tank1.health} Opponent Health : {Tank2.health} ")


        if Tank2.stat==1:
            Bullet(Tank2)
            bulletsound.play()
            Tank2.stat=0
        elif Tank1.stat==1:
            Bullet(Tank1)
            bulletsound.play()
            Tank1.stat=0
        if pygame.sprite.spritecollide(Tank1,bulletgroup,True):
            Tank1.health-=10
        if pygame.sprite.spritecollide(Tank2,bulletgroup,True):
            Tank2.health=-10

        bulletgroup.update(seconds)
        bulletgroup.draw(screen)
        Tank1.update(seconds)
        Tank2.updateOnReceive()
        redraw_window(screen,Tank1,Tank2)
        pygame.display.flip()
    return 0


if __name__ == '__main__':
    main()