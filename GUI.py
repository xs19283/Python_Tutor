# import自動修復 程式碼片段Stste
lestModName = ""
while 1:
    try:
        import sys
        import os
        sys.path.append(sys.path[0] + '/mods/')  # 將自己mods的路徑加入倒python lib裡面
        # 要import的東西放這下面
        import time
        import pygame
        import random
        import threading
        from pygame.locals import *
        from pygame import event
        import threading
        from motorContor import StepMotor
        from motorContor import DcStepMotor
        from hx711 import HX711		
    except (ModuleNotFoundError, ImportError):  # python import error
        err = str(sys.exc_info()[1])[17:-1]
        if (lestModName != err):
            print("缺少mod: " + err + " 正在嘗試進行安裝")
            os.system("pip install " + err)
            lestModName = err
        else:
            print("無法修復import問題 請人工檢查", "mod name: " + err)
            sys.exit()
    else:
        del lestModName
        break
    
    
# import自動修復 程式碼片段
RLmotor = StepMotor(26, 20, 19, 16)
FBmotor = DcStepMotor(17,18)
hx =  HX711(dout_pin=22, pd_sck_pin=23, gain_channel_A=128, select_channel='A')

# 馬達速度
moto_speed = 0.00015
# 視窗大小.
canvas_width = 800
canvas_height = 600
#screen = pygame.display.set_mode((800, 600), FULLSCREEN, 32)


# 初始.
pygame.init()
# HX711初始化
result = hx.reset()
hx.set_gain_A(gain=64)
hx.select_channel(channel='A')
result = hx.zero(times=10)
# 顯示Title.
pygame.display.set_caption("釣魚遊戲")
canvas = pygame.display.set_mode((canvas_width, canvas_height))
font = pygame.font.SysFont('楷體', 18)
background = pygame.image.load(sys.path[0] + "/img/normal.jpg").convert()
til_background = pygame.image.load(sys.path[0] + "/img/123.jpg").convert()
fish = pygame.image.load(sys.path[0] + "/img/flash.png").convert_alpha()
buoy = pygame.image.load(sys.path[0] + "/img/buoy.png").convert_alpha()
stay = pygame.image.load(sys.path[0] + "/img/stay.png").convert_alpha()
mouse = pygame.image.load(sys.path[0] + "/img/mouse.png").convert_alpha()
initStrainArray()

# fish= pygame.transform.scale(fish,(200,160))
# 遊戲用變數
powd = 1
point = []
buoypoint = []
movex = 0
movey = 0
strain_data = 0
straincount = 0
StrainArray = []

def PutStrainArray(StrainArray):
    for i in range(4, -1, -1)
        StrainArray[i]=StrainArray[i-1]
    StrainArray.insert(int(hx.get_data_mean(times=1)/1000), 0)
    return StrainArray


def initStrainArray(StrainArray):
    for i in range(0, 5)
        StrainArray.insert(0, 0)

def CalculateByMedian(StrainArray, strain_data)
    StrainArray = PutStrainArray(StrainArray)
    StrainArray.sort()
    median = StrainArray[2]

    straincount = abs(median - strain_data)
    return straincount


def showFont(text, x, y):
    global canvas
    text = font.render(text, 1, (255, 0, 0))
    canvas.blit(text, (x, y))

def blend_color(color1, color2, blend_factor):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = r1 + (r2 - r1) * blend_factor
    g = g1 + (g2 - g1) * blend_factor
    b = b1 + (b2 - b1) * blend_factor

    return int(r), int(g), int(b)


'''def edge_checkge(point, movex, movey):

    if point[0] <= 0 or point[0] >= canvas_width - fish.get_rect()[2]:
        if point[0] <= 0:
            point[0] += 1
        else:
            point[0] -= 1
    else:
        pass
    if point[1] <= 0 or point[1] >= canvas_height - fish.get_rect()[3]:
        if point[1] <= 0:
            point[1] += 1
        else:
            pass
    else:
        point[1] += movey
    return point'''

def edge_checkge2(buoypoint, buoymovex):

    if buoypoint[0] <= 0 or buoypoint[0] >= canvas_width - fish.get_rect()[2]:
        if buoypoint[0] <= 0:
            buoypoint[0] += 1
        else:
            buoypoint[0] -= 1
    else:
        buoypoint[0] += buoymovex

    return buoypoint
  


def powd_checkge(powd, straincount):
    if powd > 599:
          powd = 599
    elif powd < 1:
         powd = 1
    else :
         powd += straincount
    
    return powd


def fish_true(fish, movex, movey):

    if movex > 0:
        if movey < 0:
            fish = pygame.transform.rotate(fish, 315)
        elif movey > 0:
            fish = pygame.transform.rotate(fish, 225)
        else:
            fish = pygame.transform.rotate(fish, 270)
    if movex < 0:
        if movey < 0:
            fish = pygame.transform.rotate(fish, 45)
        elif movey > 0:
            fish = pygame.transform.rotate(fish, 135)
        else:
            fish = pygame.transform.rotate(fish, 90)
    if movex == 0:
        if movey > 0:
            fish = pygame.transform.rotate(fish, 180)

    return fish

def buoy_true(buoy, buoymovex):
    
    if movex > 0:
        buoy = pygame.transform.rotate(buoy, 350)
    elif movex <0:
        buoy = pygame.transform.rotate(buoy, 10)
    else:
        buoy = pygame.transform.rotate(buoy, 0)

    return buoy


def fish_motor(point):
    global RLmotor,canvas_width
    x = (point[0]/(canvas_width-60)*100)
    #print(point)
    RLmotor.run_degree(x)

def fish_pull(point,movey):
    global FBmotor
    y = ((point[1])/(canvas_height-60)*100)
    FBmotor.run_fast(1)
    if movey>0:
        FBmotor.AT()
        FBmotor.run_fast(1)
    elif movey<0:
        FBmotor.FW()
        FBmotor.run_fast(1)
       

#def fish_mode(point):
    #global FBmotor
    #S

def fish_size(fish, point):
    if point[1] == 300:
        x = 1
    else:
        x = point[1]/300
    fish = pygame.transform.scale(fish, (int(65*x), int(116*x)))
    return fish

def win_check(powd):
    win_time = 10
    count = 0
    while True:
        if powd > 500 and powd < 600:
            count += 1
            if count >= win_time:
                print("you win")
        else:
            count = 0


    
        
def fish_Game(point, buoypoint, buoy, fish, powd, movex, movey, canvas, strain_data, straincount, StrainArray):
    # 遊戲用的變數
    temp_fish = fish_true(fish, movex, movey)
    temp_buoy = (buoy, movex)
    point = [400, 300]
    flagX = 0      # 0:Left 1:Right
    buoypoint = [400, 0]
    wincount = 0
    buoyx = 0
    strain = 0
    mLeft = 0
    mRight = 1
    bgGap = 20
    mStep = 40
    strain_data = int(hx.get_data_mean(times=1)/1000)
    print(strain_data)
    #swing = 0
    #tour = 0
    # 硬體 變數處始畫
    global RLmotor
    RLmotor.run_Zone()
    while True:
        for event in pygame.event.get(): 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                    
        straincount = CalculateByMedian(StrainArray, strain_data)
        
        '''# Ex. 20 (Gap) 
        if point[0] <= bgGap:
           flagX = mLeft
        # Ex. 800 (Canvas)- 60 (Fish) - 20 (Gap) 
        if point[0] >= canvas_width - 60 - bgGap :
           flagX = mRight
               
        # 魚 座標
        if point[0] >= (mStep +bgGap) and flagX == mRight:
            point[0] -= mStep
        else:
            point[0] += mStep
        if point[0] <= (canvas_width - 60 - bgGap) and flagX == mLeft:
            point[0] += mStep
        else:
            point[0] -= mStep'''
        # 拉力條
        powd = powd_checkge(powd, straincount-1) #影響拉力條長度
        my_rect3 = Rect(50, 0, powd, 20) #拉力條
        factor = powd/600 #拉力條顏色變化量
        powdcolr = blend_color([0, 255, 0], [255, 60, 20], factor) #拉力條顏色變化
        # 硬體區
        fish_motor(point) #
        # 繪圖區
        canvas.blit(background, (0, 0)) #
        canvas.blit(temp_fish, point) #
        pygame.draw.rect(canvas, powdcolr, my_rect3) # 
        pygame.display.update() #
        
      #  endTime = time.time()
        
      #  print ("Interval:", endTime-startTime)
        
 #############################################################     
        
        
        
def mainWindows():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                # 接收到退出事件后退出程序
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if mouse.get_rect() <stay.get_rect():
                    fish_Game(point, buoypoint, buoy, fish, powd, movex, movey, canvas, strain_data, straincount, StrainArray)
            if event.type == MOUSEMOTION :
                x, y = pygame.mouse.get_pos()
                x-= mouse.get_width() / 2
                y-= mouse.get_height() / 2
                canvas.blit(mouse, (x, y))
                pygame.display.update()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
            canvas.blit(til_background, (0, 0))
            canvas.blit(stay, (50, 400))
            #showFont("案任意鍵開始遊戲", 300, 300)
            #if event.type == MOUSEMOTION:
         
        
            

if __name__ == '__main__':
    mainWindows()
"""
if powd >= 600:
            showFont("掉魚線斷了，本次遊戲結束", 350, 300)
            pygame.display.update()
            time.sleep(3)
            break
"""
