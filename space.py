                   ###################################
                 #                                #  #     ###########################
               ###################################   #     # Tham khảo:              #
               #                                 #  ########   kienhoc.vn            #
               #    Write by                     #   #     #   pythonprogramming.net #
               #         Diệp Minh Anh Tiến      #   #     #   songho.ca             #
               #                                 #   #     ###########################
               #                                 # #
               ###################################

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random
import cv2

display = (1200,600)
white=(255,255,255)
black=(0,0,0)
green=(0,200,0)
red=(200,0,0)
b_green=(0,255,0)
b_red=(255,0,0)

pygame.init()                                          #set up pygame
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode(display)

vertices = (                                           #Tọa độ các góc
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (                               #Các cạnh
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (                             #CÁc mặt
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

colors = (                                #Màu tô vào các mặt
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
)

def set_vertices(max_distance, min_distance=-20, camera_x=0, camera_y=0):  #Set tọa độ khởi tạo của camera
    camera_x = -1 * int(camera_x)
    camera_y = -1 * int(camera_y)

    x_value_change = random.randrange(camera_x - 30, camera_x + 30)    #Các hộp xuất hiện trong các khoảng tọa độ
    y_value_change = camera_y

    z_value_change = random.randrange(-1 * max_distance, min_distance)

    new_vertices = []

    for vert in vertices:
        new_vert = []

        new_x = vert[0] + x_value_change
        new_y = vert[1] + y_value_change
        new_z = vert[2] + z_value_change

        new_vert.append(new_x)
        new_vert.append(new_y)
        new_vert.append(new_z)

        new_vertices.append(new_vert)


    return new_vertices     #Trả về tất cả tọa độ của các hộp khi khởi động
                            #VD toạ độ một hộp
                            #[[13, -1, -254], [13, 1, -254], [11, 1, -254], [11, -1, -254], [13, -1, -252], [13, 1, -252], [11, -1, -252], [11, 1, -252]]

def Cube(vertices):               #Hàm vẽ Cube
    glBegin(GL_QUADS)

    for surface in surfaces:
        x = 0

        for vertex in surface:


            glVertex3fv(vertices[vertex])
            glColor3fv(colors[x])
            x += 1

    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def textobjects(text,font,colo):    #Xác định đối tượng text trong game intro
    textSurface=font.render(text,True,colo)
    return textSurface,textSurface.get_rect()

def button(msg,colo,fon,siz,x,y,w,h,ic,ac,action):     #Tạo nút bấm và chức năng
    mouse = pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x+w/2 > mouse[0] > x-w/2 and y + h/2 > mouse[1] > y-h/2:
        if click[0]==1:
            if action=='play':
                main()
            elif action=='un_pause':
                unpause()
        pygame.draw.rect(gameDisplay, ac, (x-w/2, y-h/2, w, h))
    else:
        pygame.draw.rect(gameDisplay, ic, (x-w/2, y-h/2, w, h))
    smallText = pygame.font.Font(fon, siz)
    TextSurf, TextRect = textobjects(msg, smallText,colo)
    TextRect.center = (x,y)
    gameDisplay.blit(TextSurf, TextRect)

def Cap(msg,fon,siz,colo):             # Hiển thị thông điệp
    bigText=pygame.font.Font(fon,siz)
    TextSurf, TextRect = textobjects(msg, bigText, colo)
    TextRect.center = (display[0]/2, display[1]/2)
    gameDisplay.blit(TextSurf, TextRect)


def game_win():   #Win game
    pygame.init()
    clock = pygame.time.Clock()
    gameDisplay = pygame.display.set_mode(display)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        bigText = pygame.font.Font('Font\intro.ttf', 80)
        TextSurf, TextRect = textobjects('YOU WIN', bigText, white)
        TextRect.center = (display[0] / 2, display[1] / 2)
        button('AGAIN!', black, 'Font\intro.ttf', 20, 600, 500, 100, 50, (0, 20, 0), white, "play")
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)

def game_intro():       #Mở đầu game
    pygame.init()
    clock = pygame.time.Clock()
    gameDisplay = pygame.display.set_mode(display)
    icon = pygame.image.load('image\iconspace.jpg')
    pygame.display.set_caption('Space')
    pygame.display.set_icon(icon)
    intro=True
    while intro :
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                quit()
        Cap('SPACE','Font\intro.ttf',100,white)
        button('GO',black,'Font\intro.ttf',20,600,500,100,50,(0,20,0),white,"play")
        pygame.display.update()
        clock.tick(15)     # Fps=15(tốc độ khung hình trên giây)


def main():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3, 400)
    cap.set(4, 300)
    global pause
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    max_distance = 90

    gluPerspective(70, (display[0] / display[1]),0, max_distance)
    glTranslatef(0, 0, -40)

    # object_passed = False
    x_move = 0
    y_move = 0

    cur_x = 0
    cur_y = 0

    game_speed = 1.2
    direction_speed = 0.6 # Tốc độ di chuyển máy quay sang trái/phải

    cube_dict = {}
    bien = 0
    coin=-1.47;

    for x in range(60):
        cube_dict[x] = set_vertices(max_distance)    #tọa độ 50 cube khởi điểm
    main_sound=pygame.mixer.Sound('Mr_Tea.wav')
    crash_sound=pygame.mixer.Sound('Debris_Hits.wav')
    lui_sound = pygame.mixer.Sound('Slide_Whistle_to_Drum.wav')
    votay_sound = pygame.mixer.Sound('Battle_Crowd_Celebrate_Stutter.wav')
    pygame.mixer.Sound.set_volume(main_sound, 0.3)
    pygame.mixer.Sound.play(main_sound,-1)

    fgbg = cv2.createBackgroundSubtractorMOG2()
    while True:

        ret, img = cap.read(0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)      #Thông số nhận diện khuôn mặt(x,y,w,h)
        fgmask=fgbg.apply(img)
        #for (x, y, w, h) in faces:
            #cv2.rectangle(fgmask, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('CAM', fgmask)
        if len(faces)!=0:                       #Điều khiển qua tọa độ x (di chuyển của khuôn mặt)
#
            if faces[0][0]>(bien+2):
                x_move=direction_speed
            elif faces[0][0]<(bien-2):
                x_move=-1*direction_speed
            else:
                x_move=0
            bien=faces[0][0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                pygame.quit()
                quit()
            elif event.type== pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        x = glGetDoublev(GL_MODELVIEW_MATRIX)   #Lấy ma trận 4*4 của view,Hàng cuối cùng (x,y,z,w)
        camera_z = x[3][2]
        cur_x += x_move
        cur_y += y_move


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glTranslatef(x_move, y_move, game_speed)

        for each_cube in cube_dict:     #Vẽ các cube trong cube_dict vào tọa độ khởi điểm
            Cube(cube_dict[each_cube])

        for each_cube in    cube_dict:
            #KHi mỗi cube đi qua camera setup lại khoảng xuất hiện của cube
            if camera_z <= cube_dict[each_cube][7][2]-0.1: #Khi nào thì va chạm
                if (-cur_x-0.7< cube_dict[each_cube][6][0] < -cur_x+0.7) or (-cur_x - 0.8 < cube_dict[each_cube][4][0] < -cur_x + 0.8):    # Đoạn này không biết gộp 2 đk thế nào
                    pygame.mixer.Sound.stop(main_sound)
                    pygame.mixer.Sound.play(crash_sound)
                    coin=coin-0.05
                    cv2.waitKey(2000)
                    pygame.mixer.Sound.play(main_sound,-1)
                new_max = int(-1 * (camera_z - (max_distance * 2)))
                #print(new_max)
                cube_dict[each_cube] = set_vertices(new_max, int(camera_z - max_distance), cur_x, cur_y)

        glBegin(GL_QUADS)                                           # Vẽ thanh máu
        glVertex3fv((-cur_x-1.5,-cur_y+1.1, camera_z -3))
        glVertex3fv((-cur_x+coin, -cur_y+1.1, camera_z - 3))
        glVertex3fv((-cur_x+coin, -cur_y+1.2, camera_z - 3))
        glVertex3fv((-cur_x-1.5, -cur_y+1.2, camera_z - 3))
        glEnd()
        coin=coin+0.003
        if coin>=1.4:
            pygame.mixer.Sound.stop(main_sound)
            pygame.mixer.Sound.play(lui_sound,maxtime=1500)
            game_speed=game_speed-0.2
        if coin >=1.6:
            pygame.mixer.Sound.stop(lui_sound)
            pygame.mixer.Sound.play(votay_sound,maxtime=3000)
            game_win()


        pygame.display.flip()
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            pygame.quit()
            quit()
game_intro()
main()
pygame.time.get_ticks(60)
pygame.quit()
quit()
