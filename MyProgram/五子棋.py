import pygame
from pygame.locals import *
import win32api,win32con
import math
import sys    #导入系统函数

SCREENWIDTH = 1400
SCREENHEIGHT = 1000
FPS = 60
BLACK = True
WRITE = False
ALL_SITE = []
Black_Steps = 0
Write_Steps = 0
yuanxin = []
board = []             #定义棋盘
for i in range(0,19):          #将棋盘升级为二维列表
    board.append([])
    for j in range(0,19):
        board[i].append(0)
pygame.font.init()          #初始化pygame的字体
text = pygame.font.Font("qizi_font.ttf",50)       #初始化字体对象


def main():
    global FPSCLOCK,SCREEN
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    pygame.display.set_caption('五子棋')
    Board()         #进行画棋盘
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        win32api.MessageBox(0, "注意：黑棋先走，白棋其次，横竖斜率先连成一样棋子的即胜利，并没有其他的详细规则和禁手！（仅为2人小游戏，AI在继续研究中。。。。。。）", "规则", win32con.MB_ICONWARNING)
        end = active()
        if end == 1:
            pygame.quit()  # 退出Pygame
            sys.exit()  # 退出sys系统（python系统）

def Board():
    SCREEN.fill((233,204,138))
    #黑方说明
    pygame.draw.circle(SCREEN,(0,0,0),(1100,100),25,0)       #执行说明操作
    text_t = text.render("黑方",1,(0,0,0))
    SCREEN.blit(text_t,(1150,80))
    #白方说明
    pygame.draw.circle(SCREEN, (255, 255, 255), (1100, 175), 25, 0)  # 执行说明操作
    text_t = text.render("白方", 1, (0, 0, 0))
    SCREEN.blit(text_t, (1150, 150))
    for i in range(0,19):                                                       #行
        if i == 0:
            pygame.draw.line(SCREEN,(0,0,0),(100,50),(1000,50),3)
        elif i == 18:
            pygame.draw.line(SCREEN,(0,0,0),(100,950),(1000,950),3)
        else:
            pygame.draw.line(SCREEN,(0,0,0),(100,50*i+50),(1000,50*i+50),1)
    for j in range(0,19):                                                       #列
        if j == 0:
            pygame.draw.line(SCREEN,(0,0,0),(100,50),(100,950),3)
        elif j == 18:
            pygame.draw.line(SCREEN,(0,0,0),(1000,50),(1000,950),3)
        else:
            pygame.draw.line(SCREEN,(0,0,0),(100+50*j,50),(100+50*j,950),1)
    pygame.draw.circle(SCREEN,(0,0,0),(550,500),10,0)                           #绘制中心点
    pygame.display.flip()

def Black_Walk():
    global BLACK,WRITE
    global ALL_SITE,board
    if BLACK == True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if 100 <= x <= 1000 and 50 <= y <= 950:
                if event.type == MOUSEBUTTONDOWN:
                    yuanxin1 = CircleCenter()
                    for weizhi in yuanxin1:
                        x1 = weizhi[0]
                        y1 = weizhi[1]
                        if x1 - 15 <= x <= x1 + 15 and y1 - 15 <= y <= y1 + 15:
                            if (x1, y1) in ALL_SITE:
                                win32api.MessageBox(0, "不要下在已有的棋子上！", "提醒", win32con.MB_ICONWARNING)
                                break
                            pygame.draw.circle(SCREEN, (0, 0, 0), (x1, y1), 20, 0)
                            ALL_SITE.append((x1, y1))
                            hang = (y1 // 50) -1                 #定义二维列表中的行标
                            lie = (x1 // 50) -2                  #定义二维列表中的列标
                            board[hang][lie] = 1                  #将指定的位置赋予数字1，便于规则判断
                            pygame.display.flip()
                            BLACK = None
                            WRITE = True
                            break
                    break

def Write_Walk():
    global WRITE,BLACK
    global ALL_SITE,board
    if WRITE == True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if 100 <= x <= 1000 and 50 <= y <= 950:
                if event.type == MOUSEBUTTONDOWN:
                    yuanxin1 = CircleCenter()
                    for weizhi in yuanxin1:
                        x1 = weizhi[0]
                        y1 = weizhi[1]
                        if x1 - 15 <= x <= x1 + 15 and y1 - 15 <= y <= y1 + 15:
                            if (x1,y1) in ALL_SITE:
                                win32api.MessageBox(0,"不要下在已有的棋子上！","提醒",win32con.MB_ICONWARNING)
                                break
                            pygame.draw.circle(SCREEN, (255, 255, 255), (x1, y1), 20, 0)
                            ALL_SITE.append((x1,y1))
                            hang = (y1 // 50) -1                   #定义二维列表中的列标
                            lie = (x1 // 50) -2             #定义二维列表中的行标
                            board[hang][lie] = -1            #将指定的位置赋予数字-1，便于规则判断
                            pygame.display.flip()
                            BLACK = True
                            WRITE = None
                            break
                    break

def CircleCenter():
    global yuanxin
    for i in range(0,19):
        for j in range(0,19):
            x = 100+50*i
            y = 50+50*j
            yuanxin.append((x,y))
    return yuanxin


def Rule():
    global ALL_SITE,board
    for i in range(0,19):       #进行行列判断
        for j in range(0,19):
            if j <= 14 and i <= 14:                  #列判断and行判断
                if board[i][j] + board[i][j+1] + board[i][j+2] + board[i][j+3] + board[i][j+4] == 5:    #黑棋列判断
                    win32api.MessageBox(0,"黑棋胜！","结果",win32con.MB_ICONWARNING)
                    return 1
                elif board[i][j] + board[i][j+1] + board[i][j+2] + board[i][j+3] + board[i][j+4] == -5:  #白旗列判断
                    win32api.MessageBox(0, "白棋胜！", "结果", win32con.MB_ICONWARNING)
                    return -1
                elif board[i][j] + board[i+1][j] + board[i+2][j] + board[i+3][j] + board[i+4][j] == 5:  #黑棋行判断
                    win32api.MessageBox(0, "黑棋胜！", "结果", win32con.MB_ICONWARNING)
                    return 1
                elif board[i][j] + board[i+1][j] + board[i+2][j] + board[i+3][j] + board[i+4][j] == -5:  #白棋行判断
                    win32api.MessageBox(0, "白棋胜！", "结果", win32con.MB_ICONWARNING)
                    return -1

    for i in range(0,19):      #进行左对角线判断
        for j in range(0,19):
            if j <= 14 and i <= 14:
                if board[i][j] + board[i + 1][j + 1] + board[i + 2][j + 2] + board[i + 3][j + 3] + board[i + 4][j + 4] == 5:  # 黑棋左对角线判断
                    win32api.MessageBox(0, "黑棋胜！", "结果", win32con.MB_ICONWARNING)
                    return 1
                elif board[i][j] + board[i + 1][j + 1] + board[i + 2][j + 2] + board[i + 3][j + 3] + board[i + 4][j + 4] == -5:  # 白棋左对角线判断
                    win32api.MessageBox(0, "白棋胜！", "结果", win32con.MB_ICONWARNING)
                    return -1
    for i in range(0,19):      #进行右对角线判断
        for j in range(18,1,-1):
            if j >= 5 and i <= 14:
                if board[i][j] + board[i+1][j-1] + board[i+2][j-2] + board[i+3][j-3] + board[i+4][j-4] == 5:
                    win32api.MessageBox(0, "黑棋胜！", "结果", win32con.MB_ICONWARNING)
                    return 1
                elif board[i][j] + board[i+1][j-1] + board[i+2][j-2] + board[i+3][j-3] + board[i+4][j-4] == -5:
                    win32api.MessageBox(0, "白棋胜！", "结果", win32con.MB_ICONWARNING)
                    return -1
    if len(ALL_SITE) == 361:   #进行平局判断
        win32api.MessageBox(0,"平局！","提醒",win32con.MB_ICONWARNING)
        return 2

def active():
    while True:
        Black_Walk()  # 黑棋走
        jieguo = Rule()
        if jieguo == 1 or jieguo == -1 or jieguo == 2:
            return 1
        else:
            Write_Walk()  # 白棋走
            jieguo1 = Rule()
            if jieguo1 == 1 or jieguo1 == -1 or jieguo1 == 2:
                return 1

if __name__ == '__main__':
    main()
