#!/usr/bin/env python3

#Standar modules
from pathlib import Path
import copy
import _tkinter



#External modules
import tkinter as tk
from tkinter import ttk,filedialog
from PIL import Image,ImageTk


#Internal modules
import Image_scroll
import Image_preview
from utils import _,set_logger,current_os,log_configuration ,view_vars
import utils


#The actual class is a modification of : 
# https://www.effbot.org/tkinterbook/tkinter-dialog-windows.htm
class Dialog(tk.Toplevel):

    def __init__(self, parent, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = ttk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid()

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = ttk.Frame(self)

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.grid(row=0,column=0,sticky=tk.S)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.grid(row=0,column=1,sticky=tk.S)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.grid()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override




def python2tkinter(dic_in,dic_out=None):
    if not isinstance(dic_out,dict) :
        dic_out=dict()
    for key,value in dic_in.items():
        if isinstance(value,dict):
            dic_out[key]=python2tkinter(value)
        elif isinstance(value,bool):
            dic_out[key]=tk.BooleanVar()
            dic_out[key].set(value)
        elif isinstance(value,float):
            dic_out[key]=tk.DoubleVar()
            dic_out[key].set(value)
        elif isinstance(value,int):
            dic_out[key]=tk.IntVar()
            dic_out[key].set(value)
        else :
            dic_out[key]=value 

    return dic_out

def tkinter2python(dic_in,dic_out=None):
    if not isinstance(dic_out,dict) :
        dic_out=dict()
    
    for key,value in dic_in.items():
        if isinstance(value,dict):
            dic_out[key]=tkinter2python(value)
        elif isinstance(value,tk.BooleanVar):
            try:
                dic_out[key]=value.get()
            except _tkinter.TclError:
                continue
        elif isinstance(value,tk.DoubleVar):
            try:
                dic_out[key]=value.get()
            except _tkinter.TclError:
                continue
        else :
            dic_out[key]=value 

    return dic_out





class Configuration_tab(ttk.Frame):
    def __init__(self,master,tk_vars=None):
        ttk.Frame.__init__(self,master)
        if isinstance(tk_vars,dict):
            self.tk_vars=tk_vars
        else :
            tk_vars=dict()
           

    def set_default_value(self,name,ptype,default=None):
        if not (name in self.tk_vars):
            if default:
                self.tk_vars[name] = ptype()
                self.tk_vars[name].set(default)
            else :
                self.tk_vars[name] = ptype()
                self.tk_vars[name].set(0)

    def add_bool(self,name,gui_name,default=None,**grid_args):
        self.set_default_value(name,tk.BooleanVar,default)
        out= self.__dict__["arg_"+name]=ttk.Checkbutton(
            self, 
            text=gui_name, 
            variable=self.tk_vars[name],
            command = None
        )
        out.grid(grid_args)
        return out

    def add_float_spinbox(
        self,name,gui_name,from_,to,increment,
        default=None,command=None,**grid_args
    ):
        """self,name,gui_name,default=None,from_=None,to=None,increment=None,
        values=None,wrap=None,format=None,command=None,**grid_args"""
        if default is None:
            self.set_default_value(name,tk.DoubleVar,from_)
        else :
            self.set_default_value(name,tk.DoubleVar,default)

        out=self.__dict__["arg_"+name] = ttk.Frame(self)

        spin = ttk.Spinbox(
            out, 
            from_=from_, 
            to=to,
            increment=increment,
            textvariable=self.tk_vars[name],
            wrap=True,
        )
        spin.grid(row=0,column=1,sticky=tk.E)
        msg = ttk.Label(out,text=gui_name,anchor="w")
        msg.grid(row=0,column=0,sticky=tk.E+tk.W)
        out.grid(grid_args)
        return out




class Configuration(Dialog):
    def __init__(self,master,apply,configuration=None):
        if isinstance(configuration,dict):
            self.real_configuration=configuration
            self.configuration=python2tkinter(configuration)
        else :
            self.configuration=dict()
        self.apply_func=apply
        Dialog.__init__(self,master,_("Configuration"))
        




    def body(self, master): 
        self.tabs = ttk.Notebook(master)

        self.view = Configuration_tab(self.tabs,self.configuration["view"])
        self.tabs.add(self.view,text="View",sticky="nsew")

        self.view.add_bool("zoom_scroll",_("enable zoom with scroll"))
        self.view.add_float_spinbox("zoom_min","min zoom",view_vars["min_user_zoom"],1,0.1)
        self.view.add_float_spinbox("zoom_max","max zoom",1,view_vars["max_user_zoom"],0.1)
        self.view.add_float_spinbox("zoom",_("zoom ratio"),view_vars["user_zoom"],1,0.05)

        self.preview = ttk.Frame(self.tabs)
        self.tabs.add(self.preview,text="Preview")

        self.tabs.grid()

        return self.tabs

    def apply(self):
        tkinter2python(self.configuration,self.real_configuration)
        self.apply_func()



