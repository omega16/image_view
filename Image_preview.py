#!/usr/bin/env python3


import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
from pathlib import Path

import itertools

import time

class Preview(ttk.Frame):
    images = None
    rute = None
    width = 128
    height = 128
    canvas = None
    labels = None
    formats_supported = ["*.png","*.jpg","*.jpeg","*.gif"]

    frame=None
    scroll=None
    last_row=0
    last_column=0
    set_image=None
    def __init__(self,master,rute=None,width=128,height=128,
                    visible=True,configuration=None,
                    set_image = None):

        ttk.Frame.__init__(self,master)

        #tk.Grid.columnconfigure(self,1,weight=0)
        tk.Grid.rowconfigure(self,0,weight=1)

        self.width=width
        self.height=height

        self.images=[]
        self.labels=[]
        if not set_image :
            self.set_image=lambda x: x
        else :
            self.set_image=set_image
        if self.set_rute(rute):
            self.load_images_vertical()
            self.set_scroll_y()

        self.vconfigure(configuration)


    def vconfigure(self,configuration):
        pass

    def set_rute(self,rute):
        if rute:
            if isinstance(rute,Path):
                if rute.exists() : 
                    if rute.is_dir():
                        self.rute=rute
                        return True
            elif isinstance(rute,str) :
                rute=Path(rute)
                if rute.exists() : 
                    if rute.is_dir():
                        self.rute=rute
                        return True
        return False                    

    def show_image(self,ind):
        if len(self.images)>ind:
            return self.set_image(self.images[ind][0])
        else :
            return False

    def set_scroll_y(self):
        if not self.canvas:
            return
        if self.scroll :
            self.scroll.grid_forget()

        self.scroll= ttk.Scrollbar(self,orient="vertical",
                                                command=self.canvas.yview)
        self.scroll.grid(row=0,column=1,sticky=tk.N+tk.S+tk.E)

        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.frame.update()
        self.canvas.configure(scrollregion=(0,0,self.frame.winfo_width(),self.frame.winfo_height() ))
        self.canvas.update()
        self.canvas.create_window((0,0), window=self.frame, anchor="nw",
                                  tags="self.frame")
        

    def generate_bind(self,rute):
        def out(event):
            return self.set_image(rute)
        return out

    def load_images_vertical(self):
        self.images=[]
        self.labels=[]
        self.last_row=0
        self.last_column = 0
        if self.frame:
            self.frame.grid_forget()
        if self.canvas:
            self.canvas.grid_forget()
        self.canvas = tk.Canvas(self)
        self.frame = ttk.Frame(self.canvas)
        self.canvas.grid(row=0,column=0,sticky=tk.S+tk.N)

        self.frame.grid(row=0,column=0,sticky=tk.E+tk.W+tk.S+tk.N)
        for img_rutes in (
            self.rute.glob(format) for format in self.formats_supported
        ):
            for img_rute in img_rutes:
                img = Image.open(img_rute)
                img.thumbnail((self.width,self.height))
                self.images.append((img_rute,ImageTk.PhotoImage(img)))
                self.labels.append(ttk.Label(self.frame))
                self.labels[-1]["image"]=self.images[-1][1]
                self.labels[-1].grid(row=self.last_row,column=0)
                self.labels[-1].bind("<Button-1>",self.generate_bind(self.images[-1][0]))
                self.labels.append(ttk.Label(self.frame,wraplength=self.width,justify="center"))
                self.labels[-1]["text"]=self.images[-1][0]
                self.labels[-1].grid(row=self.last_row+1,column=0)
                self.last_row+=2





if __name__=="__main__":

    root = tk.Tk()
    #root.resizable(True, True)

    tk.Grid.columnconfigure(root,0,weight=1)
    tk.Grid.rowconfigure(root,0,weight=1)

    app = Image_Scrollable(root,0,0,image_name="yk.png")

    root.mainloop()