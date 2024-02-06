

import sprites         #sprite loading module
import constants as c  #colour and display constants
import pygame, time    #load Pygame
import copy, random, sys
import pickle

print("Imported")
pygame.init()

gameDisplay = pygame.display.set_mode((c.displayWidth,c.displayHeight))
pygame.display.set_caption("Space Ship")
clock = pygame.time.Clock()

#================================CLASS-CREATION==================================

class player():
    
    def __init__(self, x, y, sprite, width, height, xSpeed, reload, health, collide):
        #x and y are starting coordinates, sprite is the fetched sprite image
        #height and width are the dimensions of the sprite

        self.x         =         x
        self.y         =         y
        self.sprite    =    sprite
        self.width     =     width
        self.height    =    height
        self.xSpeed    =    xSpeed
        self.reload    =    reload
        self.health    =    health
        self.collide   =   collide
  
class projectiles():
    
    def __init__(self, x, y, sprite, width, height, ySpeed, collide):
        #x and y are starting coordinates, sprite is the fetched sprite image
        #height and width are the dimensions of the sprite

        self.x         =         x
        self.y         =         y
        self.sprite    =    sprite
        self.width     =     width
        self.height    =    height
        self.ySpeed    =    ySpeed
        self.collide   =   collide
      

    def drawLaser(self):
        gameDisplay.blit(self.sprite,(self.x,self.y))

class asteroids():

    def __init__(self, x, y ,sprite, width, height, xSpeed, ySpeed, health, anim, collide, timer, size):

        self.x         =         x
        self.y         =         y
        self.sprite    =    sprite
        self.width     =     width
        self.height    =    height
        self.xSpeed    =    xSpeed
        self.ySpeed    =    ySpeed
        self.health    =    health
        self.anim      =      anim
        self.collide   =   collide
        self.timer     =     timer
        self.size     =      size

    def drawAsteroids(self):
        gameDisplay.blit(self.sprite,(self.x, self.y))

#================================FUNCTIONS======================================

def fontRender(text,colour,fontsize):
    font = pygame.font.SysFont(None, fontsize)
    message = font.render(text, True, colour)
    return message

def mainMenu():
    menuQuit = False
    choice = 0

    menuOpt = ["START","HIGH-SCORES","EXIT GAME"]
    optWidths = [c.displayWidth*0.5 - 56, c.displayWidth*0.5 - 120.5, c.displayWidth*0.5 - 98]

    helpMsg = fontRender("Arrow keys to select options, Enter to confirm option", c.Black, 30)
    while not menuQuit:
        gameDisplay.blit(bgImg, (0,0))
        for event in pygame.event.get():
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    choice += 1
                    if choice == 3:
                        choice = 0
                elif event.key == pygame.K_UP:
                    
                    choice += -1
                    if choice == -1:
                        choice = 2
                elif event.key == pygame.K_RETURN:
                    return choice
       

        for i in range(len(menuOpt)):
            if i == choice:
                color = c.Red
            else:
                color = c.Black
            gameDisplay.blit(helpMsg, (c.displayWidth*0.025, c.displayHeight*0.925))
            gameDisplay.blit(fontRender(menuOpt[i], color, 50), (optWidths[i],c.displayHeight*(0.6+(i*0.05))))

        clock.tick(15)
        pygame.display.update(bgSurface)
    

def hiscoreStore():
    picklefile = open("scores.pickle","rb")
    scorelist = pickle.load(picklefile)
    picklefile.close()
    
    for i in range(len(scorelist)):
        if score > scorelist[i][1]:
            name = playerName(i)
            scorelist.insert(i, [name, score])
            if len(scorelist) > 10:
                scorelist.pop(len(scorelist)-1)
            picklefile = open("scores.pickle", "wb")
            pickle.dump(scorelist, picklefile)
            print(scorelist)
            picklefile.close()
            break

def hiscoreLoad():
    picklefile = open("scores.pickle", "rb")
    try:
        scorelist = pickle.load(picklefile)
        picklefile.close()
    except:
        picklefile.close()
        scorelist = [[]]
        picklefile = open("scores.pickle", "wb")
        scorelist[0].append("Empty")
        scorelist[0].append(0)
        print(scorelist)
        pickle.dump(scorelist, picklefile)
        picklefile.close()
    
    topScore = scorelist[0][1]
    return topScore

def hiscoreList():
    picklefile = open("scores.pickle", "rb")
    scorelist = pickle.load(picklefile)
    picklefile.close()
    msg1 = fontRender("TOP 10 SCORES:", c.Black, 90)
    msg1Width = msg1.get_width()
    msg2 = fontRender("Press Space Bar to continue", c.Black, 60)
    msg2Width = msg2.get_width()
    listQuit = False
    while not listQuit:
        gameDisplay.blit(bgImg, (0,0))
        gameDisplay.blit(msg1, (c.displayWidth*0.5 - (msg1Width*0.5), c.displayHeight*0.1))
        gameDisplay.blit(msg2, (c.displayWidth*0.5 - (msg2Width*0.5), c.displayHeight*0.9))
        for i in range(len(scorelist)):
            topText = fontRender(scorelist[i][0] +": "+ str(scorelist[i][1]), c.Black, 50)
            width = topText.get_width()
            gameDisplay.blit(topText, (c.displayWidth*0.5 - (width*0.5), c.displayHeight*(0.25 + (i*0.05))))
            
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    listQuit = True
        
        pygame.display.update()
    goBack = mainMenu()
    return goBack
    
def gameOver():
    overQuit = False
    overText = fontRender("YOU DIED", c.White, 90)
    hiscoreText = fontRender("Current Hi-score: " + str(hiscore), c.White, 50)
    scoreText = fontRender("Your final score: " + str(score), c.White, 65)
    contText = fontRender("Press Spacebar to go back to the main menu", c.White, 40)
    width = overText.get_width()
    print(width)
    while not overQuit:
        gameDisplay.fill(c.Black)
        gameDisplay.blit(overText, ((c.displayWidth*0.5 - 147.5), c.displayHeight*0.3))
        gameDisplay.blit(hiscoreText, ((c.displayWidth*0.5 - 177), c.displayHeight*0.45))
        gameDisplay.blit(scoreText, ((c.displayWidth*0.5 - 217.5), c.displayHeight*0.5))
        gameDisplay.blit(contText, ((c.displayWidth*0.5 - 299.5),c.displayHeight*0.9))
        pygame.display.update(bgSurface)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    overQuit = True

def playerName(place):
    nameQuit = False
    pName = ""
    if place == 0:
        subtext = "ST"
    elif place == 1:
        subtext = "ND"
    elif place == 2:
        subtext = "RD"
    else:
        subtext = "TH"

    position = fontRender("YOU BEAT " + str(place+1) + subtext, c.White, 90)
    msg = fontRender("Press enter to confirm your choice", c.White, 50)
    print (position.get_width())
    while not nameQuit: 
        gameDisplay.fill(c.Black)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if pName == "":
                        pName == "No Name"
                        nameQuit = True
                    else:
                        nameQuit = True
                elif event.key == pygame.K_BACKSPACE:
                    pName = pName[0:len(pName)-1]
                else:
                    pName += event.unicode
        
        gameDisplay.blit(position, (c.displayWidth*0.5 - 219.5, c.displayHeight*0.5))
        gameDisplay.blit(fontRender("Enter Your Name: " + pName, c.White, 50), (c.displayWidth*0.2,c.displayHeight*0.7))
        gameDisplay.blit(msg, (0, c.displayHeight*0.9))
        pygame.display.update(bgSurface)
    return pName

#==============================START-OF-SETUPS==================================

spritePics = sprites.SpriteSheet("spritesheet.png")
bgObject = sprites.SpriteSheet("background.png")
print("Sprite Sheet Loaded")

#initialisation of objects here
ship =   player(0, 0, spritePics.getImage(0,0,110,110), 110, 110, 0, 500, 3, False)
pLaser = projectiles(0, 0, spritePics.getImage(220, 47, 6, 47), 6, 47, -25, False)
enemyship =  player(0, 0, spritePics.getImage(1,110,110,110), 110, 110, 5, 1200, 5, False)
obstacle = asteroids(0, 0, pygame.transform.scale((spritePics.getImage(248, 0, 25, 25)),(100,100)), 100, 100, 0, 3, 2, 0, False, 1850, 0)
eLaser = projectiles(0, 0, spritePics.getImage(220, 0, 6, 47), 6, 47, 10, False)
#lists of animation frames
obstDestroy = [spritePics.getImage(273,0,25,25), spritePics.getImage(298,0,25,25), spritePics.getImage(323,0,25,25)]
obstCrack = [spritePics.getImage(298,25,25,25), spritePics.getImage(273,25,25,25), spritePics.getImage(248,25,25,25)]
shipAnim = [spritePics.getImage(0,0,110,110), spritePics.getImage(110,0,110,110)]
enemyshipAnim = [spritePics.getImage(1,110,110,110), spritePics.getImage(112,110,110,110)]
livesImg = pygame.transform.scale(spritePics.getImage(226,43,22,22), (50,50))

#surface that is drawn
bgSurface = pygame.Rect(0,0,1366,768)
bgImg = bgObject.getImage(0,0,1366,768)

print("Objects created")

#list for object copies
laserList       = []
enemyList       = []
enemyLimit      = []
enemyDest       = []
enemylaserList  = []
enemylaserDest  = []
astList         = []
astMasks        = []
astDest         = []
laserDest       = []

#masks creation
enemy_mask = pygame.mask.from_surface(enemyship.sprite)
obstacle_mask = pygame.mask.from_surface(obstacle.sprite)
pLaser_mask = pygame.mask.from_surface(pLaser.sprite)
ship_mask = pygame.mask.from_surface(ship.sprite)
eLaser_mask = pygame.mask.from_surface(eLaser.sprite)
#timers
rel = pygame.time.get_ticks()
enemyrel = pygame.time.get_ticks()
spawn = pygame.time.get_ticks()
scoreTimer = pygame.time.get_ticks()
diffTimer = pygame.time.get_ticks()

#initial player coordinates
ship.x = ((c.displayWidth * 0.5) - 110)
ship.y = (c.displayHeight * 0.8)

score = 0
hiscore = hiscoreLoad()
scorediff = 0
scorediff2 = 1000

#=================================GAME-START====================================
#game starts here

gameQuit = False
menuChoice = mainMenu()

while not gameQuit and menuChoice < 2:

    if menuChoice == 1:
        menuChoice = hiscoreList()
        
    else:
        pygame.display.update(bgSurface) 
        #game content starts here
        gameDisplay.blit(bgImg,(0,0))
        #gameDisplay.fill(c.White)
        
        ship.x += ship.xSpeed
        Held = pygame.key.get_pressed()

        #ship controls
        if Held[pygame.K_LEFT] == 1 and ship.x > 0:
            ship.xSpeed = -15
        elif Held[pygame.K_RIGHT] == 1 and ship.x < c.displayWidth - ship.width:
            ship.xSpeed = 15
        else:
            ship.xSpeed = 0

        #timers
        rel2 = pygame.time.get_ticks()
        enemyrel2 = pygame.time.get_ticks()
        spawn2 = pygame.time.get_ticks()
        scoreTimer2 = pygame.time.get_ticks()
        diffTimer2 = pygame.time.get_ticks()
        #drawing of player ship
        gameDisplay.blit(shipAnim[int(rel2/120)%(len(shipAnim))],(ship.x,ship.y))
        enemyship.sprite = enemyshipAnim[int(rel2/120)%(len(enemyshipAnim))]
        
        #spawn obstacles here
    ##    if (spawn2 - spawn) >= obstacle.timer:
    ##        astList.append(copy.copy(obstacle))
    ##        astList[len(astList)-1].x = random.randint(0,(c.displayWidth - obstacle.width))
    ##        astList[len(astList)-1].y = -obstacle.height
    ##        astList[len(astList)-1].xSpeed = random.uniform(-1,1)
    ##        spawn = int(spawn2)
    ##    
    ##    for i in range(len(astList)):
    ##        astList[i].y += obstacle.ySpeed
    ##        astList[i].x += astList[i].xSpeed
    ##        astList[i].drawAsteroids()
    ##        if (astList[i].x < 0) or (astList[i].x > c.displayWidth - obstacle.width):
    ##            astList[i].xSpeed = -astList[i].xSpeed
    ##
    ##    #asteroid to ship collision handling
    ##        offset = (int(astList[i].x - ship.x), int(astList[i].y - ship.y))
    ##        astList[i].collide = obstacle_mask.overlap(obstacle_mask, offset)
    ##        if astList[i].collide:
    ##            astList.pop(i)
    ##            ship.health += -1
    ##            time.sleep(0.1)
    ##            print("SHIP HIT")
    ##            
    ##        elif astList[i].y > c.displayHeight:
    ##                astList[i].collide = True
        
        if enemyrel2 - enemyrel > enemyship.reload:
            for i in range(len(enemyList)):
                enemylaserList.append(copy.copy(eLaser))
                enemylaserList[len(enemylaserList)-1].x = enemyList[i].x + (enemyList[i].width / 2) - (eLaser.width / 2)
                enemylaserList[len(enemylaserList)-1].y = enemyList[i].y - eLaser.height + ship.height + 10
            enemyrel = int(enemyrel2)

        for i in range(len(enemylaserList)):
            offset = (int(enemylaserList[i].x - ship.x), int(enemylaserList[i].y - ship.y))
            enemylaserList[i].collide = ship_mask.overlap(eLaser_mask, offset)
            if enemylaserList[i].collide:
                enemylaserDest.append(i)
                ship.health += -1
                time.sleep(0.1)

        for i in range(len(enemylaserDest)):
            if enemylaserList[i].collide:
                enemylaserDest.append(i)
        try:
            for i in range(len(enemylaserDest)):
                enemylaserList.pop(enemylaserDest[i])
        except: pass
        enemylaserDest = []
        for i in range(len(enemylaserList)):
            if enemylaserList[i].y > c.displayHeight:
                enemylaserList[i].collide = True
            enemylaserList[i].y += enemylaserList[i].ySpeed
            enemylaserList[i].drawLaser()

        for i in range(len(enemylaserDest)):
            if enemylaserList[i].collide:
                enemylaserList.append(i)
        try:
            for i in range(len(enemylaserDest)):
                enemylaserList.pop(enemylaserDest[i])
        except: pass
        enemylaserDest = []
        
        if scorediff - score < 0:
            enemyList.append(copy.copy(enemyship))
            enemyList[len(enemyList)-1].x = random.randint(0,int((c.displayWidth - enemyship.width)))
            enemyList[len(enemyList)-1].y = -enemyship.height
            enemyLimit.append(random.uniform(c.displayHeight*0.05, c.displayHeight*0.35))
            scorediff += 500
        if scorediff2 - score < 0:
            ship.health += 1
            scorediff2 += 1000
        for i in range(len(enemyList)):
            if enemyList[i].y < enemyLimit[i]:
                
                enemyList[i].y += 1.25
                gameDisplay.blit(enemyshipAnim[int(enemyrel2/120)%(len(enemyshipAnim))], (enemyList[i].x,enemyList[i].y))
            else:
                if enemyList[i].x < 0 or enemyList[i].x > c.displayWidth - enemyship.width:
                    enemyList[i].xSpeed = -enemyList[i].xSpeed
                enemyList[i].x += enemyList[i].xSpeed
                gameDisplay.blit(enemyshipAnim[int(enemyrel2/120)%(len(enemyshipAnim))], (enemyList[i].x,enemyList[i].y))

        if (spawn2 - spawn) >= obstacle.timer:
            size = random.randint(1,100)
            multiplier = 1
            diffVar = 2000
            faster = fontRender("FASTER!", c.Red, 90)
            faster_width = faster.get_width()
            if diffTimer2 - diffTimer >= 25000 and obstacle.ySpeed < 12.5:
                obstacle.ySpeed     += 2
                obstacle.timer      += -300
                ship.reload         += -75
                enemyship.reload    += -150
                eLaser.ySpeed       += 1
                diffVar             += -450
                gameDisplay.blit(faster,(c.displayWidth*0.5 - (faster_width*0.5),c.displayHeight*0.5))
                pygame.display.update(bgSurface)
                time.sleep(0.5)
                diffTimer = diffTimer2 - diffVar

            if size <= 60: 
                astList.append(copy.copy(obstacle))
                astList[len(astList)-1].x = random.randint(0,(c.displayWidth - obstacle.width))
                astList[len(astList)-1].y = -obstacle.height
                spawn = int(spawn2)
                astList[len(astList)-1].size = 2
                astList[len(astList)-1].health = 3
                astMasks.append(pygame.mask.from_surface(astList[len(astList)-1].sprite))

            elif size > 60 and size <= 75: 
                astList.append(copy.copy(obstacle))
                multiplier = 1.5
                astList[len(astList)-1].width = int(astList[len(astList)-1].width * multiplier)
                astList[len(astList)-1].height = int(astList[len(astList)-1].height * multiplier)
                astList[len(astList)-1].sprite = pygame.transform.scale((astList[len(astList)-1].sprite), ((astList[len(astList)-1].width),(astList[len(astList)-1].height)))
                astList[len(astList)-1].x = random.randint(0,(c.displayWidth - obstacle.width))
                astList[len(astList)-1].y = -astList[len(astList)-1].height
                astList[len(astList)-1].ySpeed =  astList[len(astList)-1].ySpeed * 0.5
                spawn = int(spawn2)
                astList[len(astList)-1].size = 3
                astList[len(astList)-1].health = 4
                astMasks.append(pygame.mask.from_surface(astList[len(astList)-1].sprite))
                
            elif size > 75 and size <= 100:
                astList.append(copy.copy(obstacle))
                multiplier = 0.5
                astList[len(astList)-1].width = int(astList[len(astList)-1].width * multiplier)
                astList[len(astList)-1].height = int(astList[len(astList)-1].height * multiplier)
                astList[len(astList)-1].sprite = pygame.transform.scale((astList[len(astList)-1].sprite), ((astList[len(astList)-1].width),(astList[len(astList)-1].height)))
                astList[len(astList)-1].x = random.randint(0,(c.displayWidth - obstacle.width))
                astList[len(astList)-1].y = -astList[len(astList)-1].height
                astList[len(astList)-1].ySpeed =  astList[len(astList)-1].ySpeed * 1.5
                spawn = int(spawn2)
                astList[len(astList)-1].size = 1
                astList[len(astList)-1].health = 2
                astMasks.append(pygame.mask.from_surface(astList[len(astList)-1].sprite))
                

        #asteroid to ship collision handling
        for i in range(len(astList)):
            offset = (int(astList[i].x - ship.x), int(astList[i].y - ship.y))
            astList[i].collide = ship_mask.overlap(astMasks[i], offset)
            if astList[i].collide:
                astDest.append(i)
                ship.health += -1
                time.sleep(0.1)
                print("SHIP HIT")

        for i in range(len(astDest)):
            astList.pop(astDest[i])
            astMasks.pop(astDest[i])
        astDest = []

        for i in range(len(astList)):
            astList[i].y += astList[i].ySpeed
            astList[i].drawAsteroids()
            if (astList[i].x < 0) or (astList[i].x > c.displayWidth - astList[i].width):
                astList[i].xSpeed = -astList[i].xSpeed

        
            elif astList[i].y > c.displayHeight:
                    astList[i].collide = True
        #score
        if scoreTimer2 - scoreTimer >= 1000:
            score += 10
            scoreTimer = scoreTimer2

        if score > hiscore:
            hiscore = score

        #score printing
        scoreText = fontRender("SCORE: " + str(score), c.Black, 35)
        hiscoreText = fontRender("HIGH-SCORES: " + str(hiscore), c.Black, 35)

        gameDisplay.blit(scoreText, ((c.displayWidth*0.9 - 64), (c.displayHeight*0.05)))
        gameDisplay.blit(hiscoreText,((c.displayWidth*0.1 - 99), (c.displayHeight*0.05)))
        
        if ship.health <= 0:
                    hiscoreStore()
                    gameOver()
                    menuChoice      = mainMenu()
                    ship.health     = 3
                    ship.reload     = 500
                    laserList       = []
                    enemyList       = []
                    enemyLimit      = []
                    enemylaserList  = []
                    enemylaserDest  = []
                    astList         = []
                    astMasks        = []
                    astDest         = []
                    laserDest       = []
                    enemyDest       = []
                    score           = 0
                    ship.x          = ((c.displayWidth * 0.5) - 110)
                    ship.y          = (c.displayHeight * 0.8)
                    diffVar         = 2000
                    obstacle.ySpeed = 3
                    obstacle.timer  = 1700
                    enemyship.reload= 1200
                    eLaser.ySpeed   = 10
                    rel             = rel2
                    enemyrel        = enemyrel2
                    spawn           = spawn2
                    scoreTimer      = scoreTimer2
                    diffTimer       = diffTimer2

        #lives and lives images
        for i in range(ship.health):
                gameDisplay.blit(livesImg,((( 20) +(i*51)),(c.displayHeight *0.9)))

        #shooting
        if Held[pygame.K_SPACE] == 1 and rel2-rel >= ship.reload:
            laserList.append(copy.copy(pLaser))
            laserList[len(laserList)-1].x = ship.x + (ship.width / 2) - (pLaser.width / 2)
            laserList[len(laserList)-1].y = ship.y - pLaser.height + 25
            rel = int(rel2)

        #collisions handling
        
        for i in range(len(laserList)):
            for a in range(len(astList)):
                offset = (int(laserList[i].x - astList[a].x), int(laserList[i].y - astList[a].y))
                laserList[i].collide = astMasks[a].overlap(pLaser_mask, offset)
                if laserList[i].collide:
                    astList[a].health += -1
                    if astList[a].health <= 0:
                        if astList[a].size == 1:
                            score += 25
                        elif astList[a].size == 2:
                            score += 50
                        elif astList[a].size == 3:
                            score += 100
                        laserList[i].collide = True
                        astList.pop(a)
                        astMasks.pop(a)
                    else:
                        astList[a].sprite = pygame.transform.scale(obstCrack[astList[a].health - 1], (astList[a].width, astList[a].height))               
                    break
            
            laserList[i].y += pLaser.ySpeed
            laserList[i].drawLaser()
            for b in range(len(enemyList)):
                offset = (int(laserList[i].x - enemyList[b].x), int(laserList[i].y - enemyList[b].y))
                hitconfirm = enemy_mask.overlap(pLaser_mask, offset)
                if hitconfirm and enemyList[b].y > enemyLimit[b]:
                    enemyList[b].health += -1
                    laserList[i].collide = True
                    if enemyList[b].health <= 0:
                        enemyDest.append(b)
                        score += 200
        try:
            for i in range(len(enemyDest)):
                enemyList.pop(enemyDest[i])
        except: pass
        enemyDest = []
        #collide is true when offscreen
        for i in range(len(laserList)):
            if laserList[i].y <= - pLaser.height:
                laserList[i].collide = True
            
        #removes laser
        for i in range(len(laserList)):
            if laserList[i].collide:
                laserDest.append(i)
        try:
            for i in range(len(laserDest)):
                laserList.pop(laserDest[i])
        except: pass
        laserDest = []
        
        print(len(laserList), len(astList), len(astMasks), obstacle.timer, obstacle.ySpeed)
        
        clock.tick(60)
        
        for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   gameQuit = True

sys.exit()
quit()

#=========================================================================
