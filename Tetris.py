import tkinter as tk
import random
import math as m
from PIL import Image, ImageTk
import numpy as np
import time
from socket import *
import threading
import sys,os

SP_X=65
SP_Y=75

point=0
            
def out(now,mode):
    if mode==1:
        for hei in range(0,20):
            for wi in range(0,10):
                root.canvas.create_image(SP_X+wi*40  ,SP_Y+hei*40          , image=pic[now.c[wi,hei]], anchor=tk.NW)
    else:
        now.b1n=root.canvas.create_image(SP_X+now.x*40  ,SP_Y+now.y*40      ,image=pic[now.im], anchor=tk.NW)
        now.b2n=root.canvas.create_image(SP_X+now.b2x*40,SP_Y+now.b2y*40   , image=pic[now.im], anchor=tk.NW)
        now.b3n=root.canvas.create_image(SP_X+now.b3x*40,SP_Y+now.b3y*40   , image=pic[now.im], anchor=tk.NW)
        now.b4n=root.canvas.create_image(SP_X+now.b4x*40,SP_Y+now.b4y*40   , image=pic[now.im], anchor=tk.NW)

def clear(now,mode):
    if mode==1:
        for w in range(0,10):
            root.canvas.delete(field.r[w,now])
            field.r[w,now]=0
    else:
        root.canvas.delete(canvas.delete(now.b1n))
        root.canvas.delete(canvas.delete(now.b2n))
        root.canvas.delete(canvas.delete(now.b3n))
        root.canvas.delete(canvas.delete(now.b4n))
        
def cal_ror(x,y):
    gx=round(m.cos(m.pi/2)*x-m.sin(m.pi/2)*y)
    gy=round(m.sin(m.pi/2)*x+m.cos(m.pi/2)*y)
    return gx,gy


class Now:
    def __init__(self,x,y,im):
        self.b1n=0
        self.b2n=0
        self.b3n=0
        self.b4n=0
        self.im=im
        self.x=x
        self.y=y
        if(im==1):
            self.b2x=x+1
            self.b2y=y
            self.b3x=x+2
            self.b3y=y
            self.b4x=x+3
            self.b4y=y
        elif(im==2):
            self.b2x=x
            self.b2y=y+1
            self.b3x=x+1
            self.b3y=y+1
            self.b4x=x-1
            self.b4y=y+1
        elif(im==3):
            self.b2x=x
            self.b2y=y+1
            self.b3x=x+1
            self.b3y=y+1
            self.b4x=x+2
            self.b4y=y+1
        elif(im==4):
            self.b2x=x
            self.b2y=y+1
            self.b3x=x-1
            self.b3y=y+1
            self.b4x=x-2
            self.b4y=y+1
        elif(im==5):
            self.b2x=x+1
            self.b2y=y
            self.b3x=x
            self.b3y=y+1
            self.b4x=x+1
            self.b4y=y+1
        elif(im==6):
            self.b2x=x+1
            self.b2y=y
            self.b3x=x+1
            self.b3y=y+1
            self.b4x=x+2
            self.b4y=y+1
        elif(im==7):
            self.b2x=x+1
            self.b2y=y
            self.b3x=x
            self.b3y=y+1
            self.b4x=x-1
            self.b4y=y+1
        else:
            self.b2x=x
            self.b2y=y
            self.b3x=x
            self.b3y=y
            self.b4x=x
            self.b4y=y
    def move(self,mov,GS):
        if GS:
            if (mov==38):
                gx=0
                gy=-1
            elif(mov==40):
                gx=0
                gy=1
            elif(mov==37):
                gx=-1
                gy=0
            elif(mov==39):
                gx=1
                gy=0

            if bodyin(self,gx,gy):
                self.x+=gx
                self.y+=gy
                self.b2x+=gx
                self.b2y+=gy
                self.b3x+=gx
                self.b3y+=gy
                self.b4x+=gx
                self.b4y+=gy
                root.canvas.move(self.b1n,gx*40,gy*40)
                root.canvas.move(self.b2n,gx*40,gy*40)
                root.canvas.move(self.b3n,gx*40,gy*40)
                root.canvas.move(self.b4n,gx*40,gy*40)

            elif(mov==40):
                field.settle()
            
    def rotate(self):
        if T.GameState:
            g2x,g2y=cal_ror(self.b2x-self.x,self.b2y-self.y)
            g3x,g3y=cal_ror(self.b3x-self.x,self.b3y-self.y)
            g4x,g4y=cal_ror(self.b4x-self.x,self.b4y-self.y)
            if (ror_bodyin(now.x,now.y,g2x,g2y) and ror_bodyin(now.x,now.y,g3x,g3y) and
            ror_bodyin(self.x,self.y,g4x,g4y) ):
                d2x=self.b2x-self.x
                d2y=self.b2y-self.y
                d3x=self.b3x-self.x
                d3y=self.b3y-self.y
                d4x=self.b4x-self.x
                d4y=self.b4y-self.y
                
                self.b2x=self.x+g2x
                self.b2y=self.y+g2y
                self.b3x=self.x+g3x
                self.b3y=self.y+g3y
                self.b4x=self.x+g4x
                self.b4y=self.y+g4y
                root.canvas.move(self.b2n,40*(g2x-d2x),40*(g2y-d2y))
                root.canvas.move(self.b3n,40*(g3x-d3x),40*(g3y-d3y))
                root.canvas.move(self.b4n,40*(g4x-d4x),40*(g4y-d4y))

class Field:
    def __init__(self):
        self.point=point
        self.now=now
        self.f=np.zeros((10,20),dtype=bool)
        self.c=np.zeros((10,20),dtype=int,)
        self.r=np.zeros((10,20),dtype=int,)

    def settle(self):
        self.f[self.now.x,self.now.y]=True
        self.f[self.now.b2x,self.now.b2y]=True
        self.f[self.now.b3x,self.now.b3y]=True
        self.f[self.now.b4x,self.now.b4y]=True
        
        self.c[self.now.x,self.now.y]=self.now.im
        self.c[self.now.b2x,self.now.b2y]=self.now.im
        self.c[self.now.b3x,self.now.b3y]=self.now.im
        self.c[self.now.b4x,self.now.b4y]=self.now.im
        
        self.r[self.now.x,self.now.y]=self.now.b1n
        self.r[self.now.b2x,self.now.b2y]=self.now.b2n
        self.r[self.now.b3x,self.now.b3y]=self.now.b3n
        self.r[self.now.b4x,self.now.b4y]=self.now.b4n
        self.check_ok()

        spawn()
        
    def check_ok(self):
        match=False
        for height in reversed(range(0,20)): #從19-0 由下而上
            if match:
                height+=1
                match=False
            ok=0
            for i in range(0,10):
                if not self.f[i,height]:
                    break
                elif(ok<10):
                    ok+=1
                    if ok==10:
                        clear(height,1)
                        for h in reversed(range(0,height)):
                            for w in range(0,10):
                                self.f[w,h+1]=self.f[w,h]
                                self.f[w,h]=False
                                self.c[w,h+1]=self.c[w,h]
                                self.c[w,h]=0
                                root.canvas.move(self.r[w,h],0,40)
                                self.r[w,h+1]=self.r[w,h]
                                self.r[w,h]=0
                        self.point+=1
                        T.de_time-=10
                        root.canvas.itemconfigure(root.point, text='line:'+str(self.point))
                        match=True
            
class T:
    GameState=False
    Start=0
    de_time=800
    def __init__(self,rt,now):
        self.root=rt

        self.now=now
        self.update_Time()
        self.update_clock()
        
    def update_clock(self):
        if(T.GameState):
            self.now.move(40,T.GameState)
        self.root.after(self.de_time,self.update_clock)    
            
    def update_Time(self): 
        root.after(1000, self.update_Time)         

def spawn():
    im=random.randint(1,7)
    po=random.randint(2,6)
    now.__init__(po,0,im)
    if T.GameState:
        T.de_time=800
        if bodyin(now,0,0):
            out(now,0)
        else:
            root.canvas.itemconfig(root.game,text='YOU LOSE',font="Times 50 italic bold")
            print('GAME OVER!!!!')
            T.GameState=False    
    else:
        pass
        
# pressed 38 上
# pressed 40 下
# pressed 37 左
# pressed 39 右

def key(event):
    if(event.keycode in range(37,41) and not event.keycode==38 ):
        now.move(event.keycode,T.GameState)
    elif(event.keycode==38):#上
        now.rotate()
    elif(event.keycode==32):#空白鍵
        T.de_time=1
    elif(event.keycode==13 and T.GameState==False):
        Gamestart()
    else:
        pass

def ror_bodyin(bx,by,gx,gy):
    ror_OK=False
    if((bx+gx in range(0,10)) and (by+gy in range(0,20))):
        if(not(field.f[bx+gx,by+gy] or field.f[bx+gx,by+gy])):
            ror_OK=True
    return ror_OK

def bodyin(now,gx,gy):
    move_OK=False
    if (((now.x+gx in range(0,10)) and (now.y+gy in range(0,20)) and (now.b2x+gx in range(0,10)) and
        (now.b2y+gy in range(0,20)) and (now.b3x+gx in range(0,10)) and (now.b3y+gy in range(0,20)) and
        (now.b4x+gx in range(0,10)) and (now.b4y+gy in range(0,20))) and (not(field.f[now.x+gx,now.y+gy]or
        field.f[now.b2x+gx,now.b2y+gy]or  field.f[now.b3x+gx,now.b3y+gy] or field.f[now.b4x+gx,now.b4y+gy]))):
        move_OK=True
    return move_OK

root=tk.Tk()
root.title('Tetris!!!')
root.label=tk.Label(root,text='Press Enter to Start the Game!!')

root.resizable(0,0)
root.canvas=tk.Canvas(root,height=925,width=600)

root.canvas.create_text(300,30,fill="darkblue",font="Times 35 italic bold",
                        text="Time to Tetris!!!!")

root.point=root.canvas.create_text(475,455,fill="black", anchor=tk.NW,font="Times 30 italic bold",
                        text='line:'+str(point))


root.bind("<Key>",key)
root.canvas.pack(expand=tk.YES,fill=tk.BOTH)

background=tk.PhotoImage(file='background.png')

source = Image.open('tiles.png')
slice_lightblue=source.crop((0,0,40,40))
slice_blue=source.crop((40,0,80,40))
slice_orange=source.crop((80,0,120,40))
slice_yellow=source.crop((120,0,160,40))
slice_red=source.crop((160,0,200,40))
slice_green=source.crop((200,0,240,40))
slice_purple=source.crop((240,0,280,40))
slice_back=source.crop((280,0,320,40))

pic=[]
pic.append(ImageTk.PhotoImage(slice_back))     #0=back
pic.append(ImageTk.PhotoImage(slice_lightblue))#1=lightblue
pic.append(ImageTk.PhotoImage(slice_purple))   #2=purple
pic.append(ImageTk.PhotoImage(slice_blue))     #3=blue
pic.append(ImageTk.PhotoImage(slice_orange))   #4=orange
pic.append(ImageTk.PhotoImage(slice_yellow))   #5=yellow
pic.append(ImageTk.PhotoImage(slice_red))      #6=red
pic.append(ImageTk.PhotoImage(slice_green))    #7=green

bg=root.canvas.create_image(SP_X, SP_Y, image=background, anchor=tk.NW)    #40-440 0-800    

now=Now(0,0,0)
field=Field()
t=T(root,now)

root.game=root.canvas.create_text(300,300,fill="black", anchor=tk.CENTER,font="Times 30 italic bold",
                        text='Press Enter to Start The Game!!')

def Gamestart():
    root.canvas.itemconfig(root.game,text='')
    T.Start+=1
    T.GameState=True
    spawn()

root.mainloop()