import pygame, sys, random, os, pickle
from pygame.locals import *

global basicfont
black = (0, 0, 0)
white = (255, 255, 255)
darkgray = (40, 40, 40)
mint = (102, 249, 207)
mint2 = (131,175,155)
skyblue = (38,188,213)


# 猫类
class Cat:
    def __init__(self, cathead=[100, 100], catbody=[[100, 100], [80, 100], [60, 100]]):
        self.cathead = cathead
        self.catbody = catbody
    # 猫头坐标和猫身坐标(包含猫头坐标)


# 鱼类
class Fish:
    def __init__(self, fishbody=[300, 300]):
        self.fishbody = fishbody
    # 鱼身坐标


# 操作类
class Operation:
    def __init__(self, direction="right", change="right", speednum=8, score=0, switch=0):
        self.direction = direction
        self.change = change
        self.speednum = speednum
        self.score = score
        self.switch = switch


    # 游戏结束退出
    def gameover(self):
        pygame.quit()
        sys.exit()

    # 得到一个改变的方向
    def get_change(self):
        for event in pygame.event.get():  # 等待事件
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.change = "up"
                if event.key == K_DOWN:
                    self.change = "down"
                if event.key == K_LEFT:
                    self.change = "left"
                if event.key == K_RIGHT:
                    self.change = "right"
                if event.key == K_ESCAPE:
                    self.gameover()

    # 确定方向
    def confirm_direction(self):
        if (self.change == "left" or self.change == "right") \
                and (self.direction == "up" or self.direction == "down"):
            self.direction = self.change
        if (self.change == "up" or self.change == "down") \
                and (self.direction == "left" or self.direction == "right"):
            self.direction = self.change

    # 根据方向改变猫头坐标
    def change_cathead(self, cat):
        if self.direction == "right":
            cat.cathead[0] += 20
        if self.direction == "left":
            cat.cathead[0] -= 20
        if self.direction == "up":
            cat.cathead[1] -= 20
        if self.direction == "down":
            cat.cathead[1] += 20

    # 猫的移动
    def remove(self, cat):
        cat.catbody.insert(0, list(cat.cathead))
        cat.catbody.pop()

    # 吃到鱼就生成一个新的鱼 并且猫身增长1
    def eat_fish(self, cat, fish):
        if cat.cathead == fish.fishbody:
            cat.catbody.insert(0, list(cat.cathead))
            x = random.randrange(2, 39)
            y = random.randrange(2, 19)
            newfishbody = [int(x * 20), int(y * 20)]
            fish.fishbody = newfishbody
            self.speednum += 0.2
            self.score += 1
        else:
            self.remove(cat)

    # 判断头是否与后面的身子重叠 如果相等则退出游戏
    def eat_myself(self, cat):
        for i in cat.catbody[1:]:
            if cat.cathead == i:
                self.gameover()

    # 给猫身上色并且导入图片
    def darw_color(self, cat, fish, screen, catimage, fishimage,x,y,z):

        for position in cat.catbody:
            if x < 250:
                x += 4
            if y < 250:
                y += 4
            if z < 250:
                z += 4

            color = (x, y, z)
            pygame.draw.rect(screen, color, Rect(position[0], position[1], 20, 20))
            screen.blit(catimage, (cat.cathead[0], cat.cathead[1]))
            screen.blit(fishimage, (fish.fishbody[0], fish.fishbody[1]))
        pygame.display.flip()

    # 判断是否撞到边界
    def collision(self, cat):
        if cat.cathead[0] == 800 or cat.cathead[0] == 0 \
                or cat.cathead[1] == 600 or cat.cathead[1] == 0:
            self.switch = 1

    # 得分显示
    def drawscore(self, screen, basicfont):
        socreSurf = basicfont.render("得分：%s" % (self.score), True, white)
        scoreRect = socreSurf.get_rect()
        scoreRect.topleft = (670, 10)
        screen.blit(socreSurf, scoreRect)

    # 速度显示
    def drawspeed(self, screen, basicfont):
        speedSurf = basicfont.render("速度：%.1f" % (self.speednum), True, white)
        speedRect = speedSurf.get_rect()
        speedRect.topleft = (670, 40)
        screen.blit(speedSurf, speedRect)

    # 历史得分
    def score_load(self):
        #判断文件是否存在
        # os.path.exists(path)	如果路径 path 存在，返回 True；如果路径 path 不存在，返回 False。
        if os.path.exists("history_score.txt"):
            with open("history_score.txt","rb") as f:
                self.history_score = pickle.load(f)
        else:
            self.history_score = [0,0,0]

    # 保存得分
    def score_save(self):
        with open("history_score.txt","wb") as f:
            pickle.dump(self.history_score,f)

    # 结束页面显示
    def showgameoverscreen(self, screen):
        if self.switch == 1:
            self.score_load()
            self.history_score.append(self.score)
            self.history_score.sort(reverse = True)
            del self.history_score[-1]
            self.score_save()

            # 分数显示模块
            historyscoreFont = pygame.font.Font("ziti.ttf",30)
            historysocreSurf = historyscoreFont.render\
                ("Histroy Score：First - %s  Second - %s  Third - %s"%
                 (self.history_score[0],self.history_score[1],self.history_score[2]),True,mint2)
            historyscoreRect = historysocreSurf.get_rect()
            historyscoreRect.topright = (790,20)

            # 游戏结束模块
            gameoverFont = pygame.font.Font("ziti.ttf", 100)
            gameoverSurf = gameoverFont.render("Game Over", True, white)
            gameoverRcet = gameoverSurf.get_rect()
            gameoverRcet.midtop = (400, 250)
            # 提示模块
            reminderFont = pygame.font.Font("ziti.ttf", 40)
            reminderSurf = reminderFont.render("(按Esc退出)", True, white)
            reminderRect = reminderSurf.get_rect()
            reminderRect.midtop = (600, 460)

            screen.blit(historysocreSurf,historyscoreRect)
            screen.blit(gameoverSurf, gameoverRcet)
            screen.blit(reminderSurf, reminderRect)
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == KEYUP:
                        if event.key == K_ESCAPE:
                            self.gameover()


# 画网格
def grid(screen):
    for x in range(0, 800, 20):
        pygame.draw.line(screen, darkgray, (x, 0), (x, 600))
    for y in range(0, 600, 20):
        pygame.draw.line(screen, darkgray, (0, y), (800, y))

# 制作者窗口
def myname(screen):
    mynameFont = pygame.font.Font("ziti.ttf", 18)
    mynameSurf = mynameFont.render("制作者:胖胖", True, skyblue)
    mynameRect = mynameSurf.get_rect()
    mynameRect.topleft = (12, 570)
    screen.blit(mynameSurf, mynameRect)

# 主程序
def main():
    pygame.init()
    cat = Cat()
    fish = Fish()
    o = Operation()
    screen = pygame.display.set_mode((800, 600))
    speed = pygame.time.Clock()
    pygame.display.set_caption("贪吃猫")
    catimage = pygame.image.load("mm.png")
    fishimage = pygame.image.load("yu.png")
    basicfont = pygame.font.Font('ziti.ttf', 25)
    x = random.randint(20, 120)
    y = random.randint(20, 120)
    z = random.randint(20, 120)

    while True:
        screen.fill(black)  # 填充背景
        grid(screen)  # 画网格
        myname(screen)  # 制作人模块
        o.get_change()  # 得到一个改变的方向
        o.confirm_direction()  # 确定一个方向
        o.change_cathead(cat)  # 改变猫头的方向(坐标)
        o.eat_fish(cat, fish)  # 判断吃鱼
        # o.eat_myself(cat) # 删减吃自己会死
        o.collision(cat)  # 判断是否碰撞边界 碰撞改变属性switch——>1
        o.showgameoverscreen(screen)  # 判断switch为1时候结束游戏,展示结束窗口
        o.darw_color(cat, fish, screen, catimage, fishimage,x,y,z)  # 填充猫身颜色和填入猫头和鱼的图片
        o.drawscore(screen, basicfont)  # 分数模块
        o.drawspeed(screen, basicfont)  # 速度模块
        pygame.display.flip()
        speed.tick(o.speednum)


if __name__ == '__main__':
    main()


