import pygame
import math

class Config():
    width=1000
    height=600
    fps=100

def radians_to_degrees(radians):
    return (radians / math.pi) * 180.0


def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)


class Bullet(pygame.sprite.Sprite):
    """ a big projectile fired by the tank's main cannon"""
    side = 7  # small side of bullet rectangle
    vel = 180  # velocity
    mass = 50
    maxlifetime = 10.0  # seconds

    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self, self.groups)  # THE most important line !
        self.boss = boss
        self.dx = 0
        self.dy = 0
        self.angle = 0
        self.lifetime = 0.0
        self.color = self.boss.color
        self.calculate_heading()  # !!!!!!!!!!!!!!!!!!!
        self.pos = self.boss.pos[:]  # copy (!!!) of boss position
        self.calculate_origin()
        self.update()

    def calculate_heading(self):
        """ drawing the bullet and rotating it according to it's launcher"""
        self.radius = Bullet.side  # for collision detection
        self.angle += self.boss.turretAngle
        self.mass = Bullet.mass
        self.vel = Bullet.vel

        # Designing a Bullet
        image = pygame.Surface((Bullet.side * 2, Bullet.side))
        image.fill((128, 128, 128))
        pygame.draw.rect(image, (252, 65, 3), (0, 0, int(Bullet.side * 1.5), Bullet.side))
        pygame.draw.circle(image, self.color, (int(self.side * 1.5), self.side // 2), self.side // 2)
        image.set_colorkey((128, 128, 128))

        # Converting bullet surface to image
        self.image0 = image.convert_alpha()
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.rect = self.image.get_rect()

        # Positioning of bullet
        self.dx = math.cos(degrees_to_radians(self.boss.turretAngle)) * self.vel
        self.dy = math.sin(degrees_to_radians(-self.boss.turretAngle)) * self.vel

    def calculate_origin(self):
        # spawn bullet at end of turret barrel instead of tank center
        self.pos[0] += math.cos(degrees_to_radians(self.boss.turretAngle)) * (Tank.side)
        self.pos[1] += math.sin(degrees_to_radians(-self.boss.turretAngle)) * (Tank.side)

    def update(self, seconds=0.0):
        # kill if too old
        self.lifetime += seconds
        if self.lifetime > Bullet.maxlifetime:
            self.kill()

        # calculate movement
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds

        # kill if out of screen
        if self.pos[0] < 0:
            self.kill()
        elif self.pos[0] > Config.width:
            self.kill()
        if self.pos[1] < 0:
            self.kill()
        elif self.pos[1] > Config.height:
            self.kill()
        # move the image of bullet
        self.rect.centerx = self.pos[0]
        self.rect.centery = self.pos[1]


class Turret():
    def __init__(self,tank):
        self.tank=tank
        self.side=self.tank.side
        self.images = {}  # reverse order of apperance for the recoil after shooting bullet
        self.images[0] = self.draw_cannon(0)  # idle position
        self.images[1] = self.draw_cannon(1)
        self.images[2] = self.draw_cannon(2)
        self.images[3] = self.draw_cannon(3)
        self.images[4] = self.draw_cannon(4)
        self.images[5] = self.draw_cannon(5)
        self.images[6] = self.draw_cannon(6)
        self.images[7] = self.draw_cannon(7)
        self.images[8] = self.draw_cannon(8)  # position of max recoil
        self.images[9] = self.draw_cannon(4)
        self.images[10] = self.draw_cannon(0)  # idle position

    def update(self,seconds):

        # painting the correct image of cannon
        if self.tank.firestatus > 0:
            self.image = self.images[int(self.tank.firestatus // (Tank.recoiltime / 10.0))]
        else:
            self.image = self.images[0]

        # rotating Turret
        oldrect = self.image.get_rect()  # store current surface rect
        self.image = pygame.transform.rotate(self.image, self.tank.turretAngle)
        self.rect = self.image.get_rect()

        # Turret moving with a tank
        self.rect = self.image.get_rect()
        self.rect.center = self.tank.rect.center

    def updateOnReceive(self):

        if self.tank.firestatus > 0:
            self.image = self.images[int(self.tank.firestatus // (Tank.recoiltime / 10.0))]
        else:
            self.image = self.images[0]
        oldrect = self.image.get_rect()  # store current surface rect
        self.image = pygame.transform.rotate(self.image, self.tank.turretAngle)
        self.rect = self.image.get_rect()

        # Turret moving with a tank
        self.rect.center = self.tank.rect.center

    def drawCannon(self,win):
        win.blit(self.image, self.rect)

    def draw_cannon(self, offset):
        # painting facing right, offset is the recoil
        image = pygame.Surface((self.tank.side * (2), self.tank.side * (2)))  # created on the fly
        image.fill((128, 128, 128))  # fill grey
        pygame.draw.circle(image, (0, 0, 0), (self.side, self.side), 22, 0)  # red circle
        pygame.draw.circle(image, (0, 255, 0), (self.side, self.side), 18, 0)  # green circle
        pygame.draw.rect(image, (255, 0, 0), (self.side - 10, self.side + 10, 15, 2))  # turret mg rectangle
        pygame.draw.rect(image, (0, 255, 0),(self.side - 20 - offset, self.side - 5, self.side - offset, 10))  # green cannon
        pygame.draw.rect(image, (255, 0, 0), (self.side - 20 - offset, self.side - 5, self.side - offset, 10),1)  # red rect
        image.set_colorkey((128, 128, 128))
        return image

class Tank():
    """ A Tank, controlled by the Player with Keyboard commands.
    This Tank draw it's own Turret"""
    side = 100
    recoiltime = 1.1  # how many seconds  the cannon is busy after firing one time
    turretTurnSpeed = 25  # turret turning speed
    tankTurnSpeed = 20  # tank turning speed
    movespeed = 100
    maxrotate = 360  # maximum amount of degree the turret is allowed to rotate

    # Tank controls are as follows
    firekey = pygame.K_DOWN
    turretLeftkey = pygame.K_LEFT
    turretRightkey = pygame.K_RIGHT
    forwardkey = pygame.K_w
    backwardkey = pygame.K_s
    tankLeftkey = pygame.K_a
    tankRightkey = pygame.K_d

    def __init__(self,color, startpos=(150, 150), angle=0):

        self.pos = [startpos[0], startpos[1]]  # x,y
        self.dx = 0
        self.dy = 0
        self.ammo = 20  # main gun
        self.color = color
        self.turretAngle = angle  # turret facing
        self.tankAngle = angle  # tank facing
        self.firekey = Tank.firekey  # main gun

        self.turretLeftkey = Tank.turretLeftkey  # turret
        self.turretRightkey = Tank.turretRightkey # turret
        self.forwardkey = Tank.forwardkey   # move tank
        self.backwardkey = Tank.backwardkey  # reverse tank
        self.tankLeftkey = Tank.tankLeftkey  # rotate tank
        self.tankRightkey = Tank.tankRightkey  # rotate tank
        # painting facing north, have to rotate 90° later
        image = pygame.Surface((Tank.side, Tank.side))  # created on the fly
        image.fill((128, 128, 128))  # fill grey

        if self.side > 10:
            pygame.draw.rect(image, self.color, (5, 5, self.side - 10, self.side - 10))  # tank body, margin 5
            pygame.draw.rect(image, (90, 90, 90), (0, 0, self.side // 6, self.side))  # Left Margin
            pygame.draw.rect(image, (90, 90, 90), (self.side - self.side // 6, 0, self.side, self.side))  # right Margin
            pygame.draw.rect(image,(255,0,0),(20,10,10,5))
        pygame.draw.circle(image, (255, 0, 0), (self.side // 2, self.side // 2), self.side // 3,2)

        # converting surface to image
        image = pygame.transform.rotate(image, -90)  # rotate so to look east
        self.image0 = image.convert_alpha()
        self.image = image.convert_alpha()
        self.rect = self.image0.get_rect()

        # ---------- turret ------------------
        self.firestatus = 0.0  # time left until cannon can fire again
        self.turndirection = 0  # for turret
        self.tankturndirection = 0
        self.movespeed = Tank.movespeed
        self.turretTurnSpeed = Tank.turretTurnSpeed
        self.tankTurnSpeed = Tank.tankTurnSpeed
        self.turret=Turret(self)  # create a Turret for this tank
        self.stat=0
        self.health=100
    def update(self, seconds):

        # reloading, firestatus
        if self.firestatus > 0:
            self.firestatus -= seconds  # cannon will soon be ready again
            if self.firestatus < 0:
                self.firestatus = 0  # avoid negative numbers

        # getting list pressed keys on keyboard
        pressedkeys = pygame.key.get_pressed()

        # taking direction where turrent will be rotated
        self.turndirection = 0  # left / right turret rotation
        if pressedkeys[self.turretLeftkey]:
            self.turndirection += 1
        if pressedkeys[self.turretRightkey]:
            self.turndirection -= 1

        # taking direction where turrent will be rotated
        self.tankturndirection = 0  # reset left/right rotation
        if pressedkeys[self.tankLeftkey]:
            self.tankturndirection += 1
        if pressedkeys[self.tankRightkey]:
            self.tankturndirection -= 1

        # rotate tank
        self.tankAngle += self.tankturndirection * self.tankTurnSpeed * seconds  # time-based turning of tank

        oldcenter = self.rect.center
        oldrect = self.image.get_rect()  # store current surface rect
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

        # if tank is rotating, turret is also rotating with tank !
        # turret autorotate
        self.turretAngle += self.tankturndirection * self.tankTurnSpeed * seconds + self.turndirection * self.turretTurnSpeed * seconds  # time-based turning

        # fire cannon
        if (self.firestatus == 0) and (self.ammo > 0):
            if pressedkeys[self.firekey]:
                self.firestatus = Tank.recoiltime  # seconds until tank can fire again
                self.stat=1
                self.ammo -= 1


        # movement
        self.dx = 0
        self.dy = 0
        self.forward = 0
        if pressedkeys[self.forwardkey]:
            self.forward += 1
        if pressedkeys[self.backwardkey]:
            self.forward -= 1
        # if both are pressed togehter, self.forward becomes 0

        if self.forward == 1:
            self.dx = math.cos(degrees_to_radians(self.tankAngle)) * self.movespeed
            self.dy = -math.sin(degrees_to_radians(self.tankAngle)) * self.movespeed
        if self.forward == -1:
            self.dx = -math.cos(degrees_to_radians(self.tankAngle)) * self.movespeed
            self.dy = math.sin(degrees_to_radians(self.tankAngle)) * self.movespeed

        # check border collision
        self.pos[0] += self.dx * seconds
        self.pos[1] += self.dy * seconds
        if self.pos[1] + self.side // 2 >= Config.height-10:
            self.pos[1] = Config.height - self.side // 2
            self.dy = 0  # crash into border
        elif self.pos[1] - self.side / 2 <= -10:
            self.pos[1] = 0 + self.side // 2
            self.dy = 0
        if self.pos[0] + self.side // 2 >= Config.width-10:
            self.pos[0] = Config.width - self.side // 2
            self.dy = 0  # crash into border
        elif self.pos[0] - self.side / 2 <= -10:
            self.pos[0] = 0 + self.side // 2
            self.dy = 0

        # Tank will get new position
        self.rect.centerx = round(self.pos[0], 0)  # x
        self.rect.centery = round(self.pos[1], 0)  # y
        self.turret.update(seconds)

    def updateOnReceive(self):
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.tankAngle)
        self.rect = self.image.get_rect()
        self.rect.center=oldcenter
        self.turret.updateOnReceive()


    def drawTank(self,win):
        win.blit(self.image,(self.rect[0],self.rect[1]))
        self.turret.drawCannon(win)
