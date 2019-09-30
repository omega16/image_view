#!/usr/bin/env python3


import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk

import utils
from utils import _,log_configuration,current_os,view_vars

class Image_Scrollable(ttk.Frame):
    image_real = None
    image_rute = None
    image_to_show = None
    zoom = 1.0
    zoom_min = 0.05
    zoom_max = 4
    zoom_change_ratio = 0.1
    zoom_scroll = True

    configuration=None

    def __init__(self,master,row_start,col_start,image_rute=None,
                image_object=None,row_span=1,col_span=1,
                configuration=None):


        ttk.Frame.__init__(self,master)

        self.grid(row=row_start,column=col_start,rowspan=row_span,
                columnspan=col_span,
                sticky=tk.N+tk.S+tk.E+tk.W)


        #self.config(borderwidth=2,relief="sunken")
        self.canvas_view = tk.Canvas(self)
        self.canvas_view.grid(row=0,column=0,sticky=tk.E+tk.W+tk.S+tk.N)

        tk.Grid.columnconfigure(self,0,weight=1)
        tk.Grid.rowconfigure(self,0,weight=1)



        self.canvas_scrolly = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas_view.yview
        )

        self.canvas_view.config(yscrollcommand=self.canvas_scrolly.set)
        self.canvas_scrolly.grid(row=0,column=1,sticky=tk.N+tk.S+tk.E)
        if current_os == "Linux":
            self.canvas_view.bind("<4>",lambda x:self.image_scroll_resize(x))
            self.canvas_view.bind("<5>",lambda x:self.image_scroll_resize(x))
        elif current_os == "Windows":
            #TODO enable windows scroll-resize
            pass 

 

        self.canvas_scrollx = ttk.Scrollbar(self,orient="horizontal",
                                                command=self.canvas_view.xview)

        self.canvas_view.config(xscrollcommand=self.canvas_scrollx.set)
        self.canvas_scrollx.grid(row=1,column=0,sticky=tk.E+tk.W+tk.S)

        if image_object:
            self.set_image_by_object(image_object)
        elif image_rute:
            self.set_image_by_rute(image_rute)


        self.vconfigure(configuration)


    def vconfigure(self,configuration):
        if configuration:
            self.configuration=configuration

        try:
            self.configuration["zoom_max"]=min(self.configuration["zoom_max"],
                                                view_vars["max_user_zoom"])
        except:
            self.configuration["zoom_max"]=view_vars["max_user_zoom"]

        try:
            self.configuration["zoom_min"]=max(self.configuration["zoom_min"],
                                                view_vars["min_user_zoom"])
        except:
            self.configuration["zoom_max"]=view_vars["min_user_zoom"]

        try:
            self.configuration["zoom"]=min(self.configuration["zoom"],
                abs(self.configuration["zoom_max"]-self.configuration["zoom_min"]))
        except:
            self.configuration["zoom"]=abs(self.configuration["zoom_max"]-self.configuration["zoom_min"])/2

        if not ("zoom_scroll" in self.configuration):
            self.configuration["zoom_scroll"] = True

        for key,value in self.configuration.items():
            self.__dict__[key]=value




        



    def set_image_by_rute(self,name):
        self.image_real = Image.open(name)
        if self.image_real:
            self.image_rute=name
            # self.view.update()
            self.image_to_show = ImageTk.PhotoImage(self.image_real)
            self.canvas_view.config(scrollregion=(0,0,*self.image_real.size))
            self.canvas_view.create_image(0,0,image=self.image_to_show,anchor="nw")
            return True
        else :
            return self.image_load_error()

    def set_image_by_object(self,object):
        self.image_real=object
        self.image_to_show = ImageTk.PhotoImage(self.image_real)
        self.canvas_view.config(scrollregion=(0,0,*self.image_real.size))
        self.canvas_view.create_image(0,0,image=self.image_to_show,anchor="nw")
        return True



    def image_load_error(self):
        raise Exception("can't load {}".format(self.image_rute))


    def image_scroll_resize(self,event):
        if not self.zoom_scroll:
            return 
        resize=True
        if not self.image_real:
            return

        if event.num==5 and self.zoom>=self.zoom_min+self.zoom_change_ratio:
            self.zoom -=self.zoom_change_ratio
        elif event.num==5 :
            resize=False
        elif event.num==4 and self.zoom<=self.zoom_max-self.zoom_change_ratio:
            self.zoom +=self.zoom_change_ratio
        elif event.num==4:
            resize=False

        if not resize:
            return

        w,h = self.image_real.size
        w = int(w*self.zoom)
        h = int(h*self.zoom)

        self.image_to_show = ImageTk.PhotoImage(self.image_real.resize((w,h), resample=0))
        self.canvas_view.create_image(0,0,image=self.image_to_show,anchor="nw")
        self.canvas_view.config(scrollregion=(0,0,w,h))
        if w>self.canvas_view.winfo_width():
            self.canvas_scrollx.grid()
        else :
            self.canvas_scrollx.grid_remove()
        if h>self.canvas_view.winfo_height():
            self.canvas_scrolly.grid()
        else :
            self.canvas_scrolly.grid_remove()





if __name__=="__main__":

    root = tk.Tk()
    #root.resizable(True, True)

    tk.Grid.columnconfigure(root,0,weight=1)
    tk.Grid.rowconfigure(root,0,weight=1)

    app = Image_Scrollable(root,0,0,image_rute="yk.png")

    root.mainloop()