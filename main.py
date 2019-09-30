#!/usr/bin/env python3

#Standar modules
from pathlib import Path





#External modules
import tkinter as tk
from tkinter import ttk,filedialog
from PIL import Image,ImageTk


#Internal modules
import Image_scroll
import Image_preview
from utils import _,set_logger,current_os,log_configuration 
import utils

        

import configuration_menu

    



class App(ttk.Frame):
    configuration=None


    def __init__(self,master,folder_rute=None,image_rute=None,
                lang=None,configuration_rute=None):

        self.master=master
        menubar = tk.Menu(master)
        master['menu'] = menubar

        menu_file = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Open...', command=None)
        menu_file.add_command(label='Open folder', command=self.change_dir)


        menu_preferences = tk.Menu(menubar)
        menubar.add_cascade(menu=menu_preferences, label='Preferences')
        menu_preferences.add_command(label="Configuration",command=self.menu_configuration)

        
        self.vconfigure()

        ttk.Frame.__init__(self,master)

        ready_to_go = self.load_configuration(configuration_rute)
        if not ready_to_go:
            self.load_default_configuration(lang)

        
        self.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
        tk.Grid.columnconfigure(self,1,weight=4)
        tk.Grid.columnconfigure(self,0,weight=0)
        tk.Grid.rowconfigure(self,0,weight=1)

        self.image=Image_scroll.Image_Scrollable(self,1,1,image_rute=image_rute,configuration=self.configuration["view"])

        self.preview = Image_preview.Preview(
            self,
            set_image=self.image.set_image_by_rute,
            rute=folder_rute
        )
        self.preview.grid(row=1,column=0,sticky=tk.N+tk.S+tk.W+tk.E)

        tk.Grid.rowconfigure(self,0,weight=0)
        tk.Grid.rowconfigure(self,1,weight=1)
        self.preview.update()
        


    def menu_configuration(self):
        menu = configuration_menu.Configuration(
            self,
            self.vconfigure,
            self.configuration,
        )
        self.master.wait_window(menu)

    def change_dir(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.preview.set_rute(dirname)
            self.preview.load_images_vertical()
            self.preview.set_scroll_y()
            self.preview.show_image(0)
            return True
        return False

    def vconfigure(self,configuration=None):
        if configuration:
            if isinstance(configuration,dict):
                self.configuration=configuration
            else :
                conf = self.load_configuration(configuration)
                if conf:
                    self.configuration=conf
        if not self.configuration:
            log_configuration.debug("Can't configure, empty configuration")
            return False

        self.image.vconfigure(self.configuration["view"])
        self.preview.vconfigure(self.configuration["preview"])
        return True



    def load_configuration(self,rute):
        if rute :
            if isinstance(rute,Path):
                self.configuration_path = rute
            elif isinstance(rute,str):
                self.configuration_path = Path(rute)
            else :
                log_configuration.debug("Configuration must be Path or String")
                return False
        else :
            if current_os == "Linux":
                self.configuration_path = Path.home()/Path(".config")/ \
                                            Path("image_visor")/Path("image_visor.json")
            elif current_os == "Windows":
                self.configuration_default_path = (Path("c:")/"Program Files")/ \
                                            "image_visor"/"image_visor.json"
            #Currently Mac is not supported (I don't have a mac :P)
            else :
                #TODO add Mac support
                raise Exception("Sorry, only supported Linux and Windows")
            

        self.configuration = utils.load_configuration_file(self.configuration_path)
        return self.configuration


        




    def load_default_configuration(self,lang):
        self.configuration=dict()
        if lang :
            #TODO Check for correct language format 
            self.configuration["lang"]=lang
        else :
            self.configuration["lang"]="en"

        self.configuration["view"]=dict()
        self.configuration["preview"]=dict()



def showMyPreferencesDialog():
    pass

if __name__=="__main__":

    root = tk.Tk()
    #root.resizable(True, True)

    tk.Grid.columnconfigure(root,0,weight=1)
    tk.Grid.rowconfigure(root,0,weight=1)

    #app = Image_scroll.Image_Scrollable(root,0,0,image_name="yk.png")

    #disable old TK menu style
    root.option_add('*tearOff', tk.FALSE)

    app = App(root)
    
    root.mainloop()