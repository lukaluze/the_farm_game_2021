from tkinter import * 
import time
import pygame 
import random
import pygame

class vestuble_carret :
    def __init__(self,canvas,image,id,x,y):
        self._frame=0
        self.id=id
        self.canvas = canvas
        self.image = image
        self.x=x
        self.y=y
        self.me=self.canvas.create_image(self.x,self.y,image=self.image[0],tags=self.id)
        self.score=100 #기본 점수
        self.desire=0 #욕구
        self.grow=2# 성장정도
        self.endure=20 # 타이머
    def update(self):
        if self.grow==1 :
            self.canvas.itemconfig(self.me, image = self.image[1])
        if self.grow == 0 :
            self.canvas.itemconfig(self.me, image = self.image[2])
        if self.grow == -1:
            self.canvas.itemconfig(self.me, image = self.image[3])
    def getId(self):
        return self.me
    def getScore(self):
        return self.score

class game:
    def __init__(self):
        window = Tk()
        window.title("당근게임")
        window.geometry("800x740")
        window.resizable(0,0)
        self.canvas=Canvas(window, bg="white")
        self.canvas.pack(expand=True, fill=BOTH)
        self.key=set()
        self.step=0 #화면 번호
        self.screen_draw = 0 #화면 불러오기
        self.menu_idx = 0 #화살표 위치
        self.furit_list=[]
        self.check_farm=[]
        self.farm_num=1 #체크박스의 밭 위치
        self.box_x=1 #박스 x 좌표
        self.box_y=1 #박스 Y좌표
        self.score=0
        self.time=0 
        self.s_end_game=0 #소리 반복 안하게
        self.game_play=1 #0일때 화면 꺼지기
        

        window.bind("<KeyRelease>",self.keyReleaseHandler)
        #소리
        
        pygame.init()
        self.sounds = pygame.mixer
        self.sounds.init()
        self.bgm=self.sounds.Sound("sounds/bgm.mp3")
        self.bgm.set_volume(0.1)
        self.s_effect1 = self.sounds.Sound("sounds/tok.mp3")
        self.s_effect2 = self.sounds.Sound("sounds/Coin.mp3")
        self.s_effect3 = self.sounds.Sound("sounds/coming_end.mp3")
        self.s_effect3.set_volume(0.2)
        self.s_effect4 = self.sounds.Sound("sounds/end_game.mp3")
        self.s_effect4.set_volume(0.2)
        
        #이미지
        self.box=PhotoImage(file="image\\check_box.png")
        self.arrowimg = PhotoImage(file="image/arrow.png").subsample(21)
        self.carret_image=[PhotoImage(file='image/carret.gif',format = 'gif -index %i' %(i)) for i in range(4)]
        self.farm_image=PhotoImage(file="image/farm.png").subsample(3)
        self.menu_bgimage=PhotoImage(file="image/menu_bg.png")
        self.farm_bgimage=PhotoImage(file="image/farm_bg.png")
        self.score_bgimage=PhotoImage(file="image/score_bg.png")
        self.water_image=PhotoImage(file="image/want_water.png").subsample(3)
        self.Bacteria_image=PhotoImage(file="image/want_medicine.png").subsample(3)

        self.posstr = "점수 : "
        self.pos_timer="남은 시간 : "

        while True :

            if self.step == 0 and self.screen_draw == 0:
                self.menu_screen()
                self.screen_draw=1
            if self.step==1 :
                if self.screen_draw ==0 :
                    self.stage_one_screen()
                    self.screen_draw=1
                elif self.screen_draw == 1 :
                    self.stage_display()
            if self.step==2 and self.screen_draw==0 :
                self.screen_draw = 1
                self.score_screen()
            if self.game_play==0 :
                break;
            self.canvas.after(33)
            self.canvas.update()

    def menu_screen(self):
        self.canvas.create_image(0,0, image = self.menu_bgimage,anchor = NW,tags="bg")
        self.canvas.create_text(200,280,font="Times 15 italic bold",text="Game_play")
        self.canvas.create_text(200,320,font="Times 15 italic bold",text="Exit")
        self.arrow=self.canvas.create_image(120,280, image = self.arrowimg,tags="arrow")
        
    def stage_one_screen(self):
        self.s_end_game=0
        self.score=0
        self.time=1000
        self.bgm.play()
        self.canvas.create_image(0,0, image = self.farm_bgimage,anchor = NW,tags="bg")
        self.canvas.create_image(250,250,image= self.farm_image)
        self.canvas.create_image(250,375,image= self.farm_image)
        self.canvas.create_image(250,500,image= self.farm_image)
        self.canvas.create_image(400,250,image= self.farm_image)
        self.canvas.create_image(400,375,image= self.farm_image)
        self.canvas.create_image(400,500,image= self.farm_image)
        self.canvas.create_image(550,250,image= self.farm_image)
        self.canvas.create_image(550,375,image= self.farm_image)
        self.canvas.create_image(550,500,image= self.farm_image)
        self.pos_Id=self.canvas.create_text(50,50,font="Times 15 italic bold",text=self.posstr)
        self.pos_time=self.canvas.create_text(650,50,font="Times 15 italic bold",text=self.pos_timer)
        self.check_box=self.canvas.create_image(242,250, image = self.box,tags="box")
    
    def score_screen(self):
        #self.s_effect4.play()
        self.canvas.create_image(0,0, image = self.score_bgimage,anchor = NW,tags="bg")
        self.canvas.create_text(300,350,font=("Times 15 italic bold",30),text=self.score)
        self.canvas.create_text(700,340,font="Times 15 italic bold",text="To Menu")
        self.canvas.create_text(700,380,font="Times 15 italic bold",text="RePlay ?")
        self.arrow=self.canvas.create_image(620,340, image = self.arrowimg,tags="arrow")

    def stage_display(self):
        self.posstr = "점수 : " + str(self.score)
        self.canvas.itemconfigure(self.pos_Id, text=self.posstr)
        self.canvas.itemconfigure(self.pos_time, text=self.pos_timer)
        for e in self.furit_list:
            if e.grow>=1 :
                if e.desire==0 :
                    if(random.randint(0,100)==0):
                        e.desire = random.randint(1,2) 
                        if e.desire == 1 :
                            e.check_desire=self.canvas.create_image(e.x+35,e.y-40, image = self.water_image)
                        elif e.desire == 2 :
                            e.check_desire=self.canvas.create_image(e.x+35,e.y-40, image = self.Bacteria_image)
                if e.desire!=0 and e.grow<=2:
                    if e.endure > 0 :
                        e.endure = e.endure-1
                    else :
                        e.score=e.score-1
                if e.score <=0 :
                    e.grow = -1
                    e.desire = 0
                    self.canvas.delete(e.check_desire)
            e.update()

        self.time=self.time-1
        self.pos_timer="남은 시간 : "+str(self.time)
        if self.time<= 120 :
            if self.s_end_game==0 :
                self.bgm.stop()
                self.s_effect3.play()
                self.s_end_game=1
        if self.time<=0 :
            self.s_effect3.stop()
            self.screen_draw=0
            self.step=2
            

    def keyReleaseHandler(self, event):
        if self.step==0: #메뉴에서
            if event.keycode == 38 and self.menu_idx > 0 :
                self.menu_idx = self.menu_idx - 1
                self.canvas.move(self.arrow, 0, -40)
                self.s_effect1.play()
            if event.keycode == 40 and self.menu_idx < 1 :
                self.menu_idx = self.menu_idx + 1
                self.canvas.move(self.arrow, 0, 40)
                self.s_effect1.play()
            if event.keycode == 32:
                if self.menu_idx ==0 :
                    self.step=1
                    self.screen_draw = 0 
                if self.menu_idx ==1 :
                    self.game_play=0

        if self.step==1 : #게임화면에서
            if event.keycode == 37 and self.box_x>1 : #왼쪽
                self.canvas.move(self.check_box,-150,0)
                self.farm_num=self.farm_num-1
                self.box_x=self.box_x-1
            if event.keycode == 39 and self.box_x<3 : #오른쪽
                self.canvas.move(self.check_box,150,0)
                self.farm_num=self.farm_num+1
                self.box_x=self.box_x+1
            if event.keycode == 38 and self.box_y>1 : #위쪽
                self.canvas.move(self.check_box,0,-125)
                self.farm_num=self.farm_num+3
                self.box_y=self.box_y-1
            if event.keycode == 40 and self.box_y<3: #아래쪽
                self.canvas.move(self.check_box,0,125)
                self.farm_num=self.farm_num-3
                self.box_y=self.box_y+1
                   
            if event.keycode==81 : #q 심기
                if self.farm_num not in self.check_farm :
                    box_pos = self.canvas.coords(self.check_box)
                    self.furit_list.append(vestuble_carret(self.canvas,self.carret_image,self.farm_num,box_pos[0],box_pos[1]))
                    self.check_farm.append(self.farm_num)
                    self.s_effect1.play()
            if event.keycode==87 : #w 물주기
                for e in self.furit_list:
                    if e.id == self.farm_num and e.desire == 1 and e.grow >= 1:
                        self.canvas.delete(e.check_desire)
                        e.desire =0
                        e.grow=e.grow-1
                        e.endure=20
                        self.s_effect1.play()
            if event.keycode == 69 : #e 병치료
                for e in self.furit_list:
                    if e.id == self.farm_num and e.desire == 2 and e.grow >=1 :
                        self.canvas.delete(e.check_desire)
                        e.desire =0
                        e.grow=e.grow-1
                        e.endure=20
                        self.s_effect1.play()
            if event.keycode == 82 : #r 수확
                for e in self.furit_list:
                    if e.id == self.farm_num and e.grow<=0 :
                        if e.grow == 0 :
                            self.s_effect2.play()
                        else :
                            self.s_effect1.play()
                        self.score=self.score + e.getScore()
                        self.canvas.delete(e.getId())
                        self.furit_list.pop(self.furit_list.index(e))
                        self.check_farm.remove(self.farm_num)
                        

        if self.step==2: #메뉴에서
            if event.keycode == 38 and self.menu_idx > 0 :
                self.menu_idx = self.menu_idx - 1
                self.canvas.move(self.arrow, 0, -40)
                self.s_effect1.play()
            if event.keycode == 40 and self.menu_idx < 1 :
                self.menu_idx = self.menu_idx + 1
                self.canvas.move(self.arrow, 0, 40)
                self.s_effect1.play()
            if event.keycode == 32:
                if self.menu_idx ==0 :
                    self.canvas.delete("all")
                    self.step=0
                    self.screen_draw=0
                if self.menu_idx ==1 :
                    self.canvas.delete("all")
                    self.step=1
                    self.screen_draw=0
                self.canvas.delete("all")
                    



game()
        