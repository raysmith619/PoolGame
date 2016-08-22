#!/usr/bin/env python
"""
Handle 2.x and 3.x
"""
try:
    import Tkinter as tk
except ImportError:
    print("No Tkinter (2.x) - try tkinter (3.x)")
    import tkinter as tk
    
class PoolTk:           # 2.x or 3.x Tk
    def __init__(self):
        self.tk = tk.Tk
                
class PoolTk:           # 2.x or 3.x Tk
    def __init__(self):
        self.tk = tk.Tk            
            
    def Tk(self):
        return self.tk()
    
    def Frame(self, mw, **args):
        return tk.Frame(mw, **args)
        