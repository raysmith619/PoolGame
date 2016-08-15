#!/usr/bin/python
# Simple enough, just import everything from tkinter.
###from tkinter import *
from Tkinter import *

def hello():
    print "hello!"

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class PoolWindow(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self,
                 master=None,
                 gameExit=exit,
                 games=[],          # text, proc pairs
                 actions=[],
                 ):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master
        self.gameExit = gameExit
        self.games = games
        self.actions = actions
        
        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

        
    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("Pool Playing")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # create the file object)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=hello)
        filemenu.add_command(label="Save", command=hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.gameExit)
        menubar.add_cascade(label="File", menu=filemenu)

                                # Game selection coming from text, function pairs from
        gamemenu = Menu(menubar, tearoff=0)
        for namegame in self.games:
            name = namegame[0]
            game = namegame[1]
            if game != None:
                gamemenu.add_command(label=name, command=game)
            else:
                gamemenu.add_separator()
                

        menubar.add_cascade(label="New Game", menu=gamemenu)
                                # Action coming from text, function pairs from
        actionmenu = Menu(menubar, tearoff=0)
        for nameaction in self.actions:
            name = nameaction[0]
            action = nameaction[1]
            if action != None:
                actionmenu.add_command(label=name, command=action)
            else:
                actionmenu.add_separator()
                

        menubar.add_cascade(label="Actions", menu=actionmenu)


#######################################################################
#          Self Test
#######################################################################
if __name__ == "__main__":
    def rack_8ball():
        print("rack_8ball")
        
        
    def rack_9ball():
        print("rack_9ball")
        
        
    def empty_8ball():
        print("empty_8ball")
        
        
    def billiards():
        print("billiards")
        
    def empty_billiards():
        print("empty_billiards")
        
    def run_game():
        print("run_game")
        
    def pause_game():
        print("pause_game")
        
    def aim_next():
        print("aim_next")
        
        
    # root window created. Here, that would be the only window, but
    # you can later have windows within windows.
    mw = Tk()
    def user_exit():
        print("user_exit")
        exit()
        
        
    mw.geometry("400x300")
    
    #creation of an instance
    app = PoolWindow(mw,
                     gameExit=user_exit,
                     games = [
                        ['8-ball', rack_8ball],
                        ['9-ball', rack_9ball],
                        ['empty-8ball', empty_8ball],
                        ['separator', None],
                        ['Billiards', billiards],
                        ['empty-billiards', empty_billiards],
                        ],
                     actions = [
                        ['run', run_game],
                        ['pause', pause_game],
                        ['separator', None],
                        ['Aim Next', aim_next],
                        ],
                    )
    
    
    #mainloop 
    mw.mainloop()  

