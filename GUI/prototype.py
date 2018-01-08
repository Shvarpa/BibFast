import tkinter as tk
from tkinter import ttk
from firebase import Firebase
import main
import os

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 8)
SMALL_TEXT = ("Verdana", 5)

try:
    os.remove('.token')
except:
    pass
ref = Firebase(gui=True)



class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="logo.ico")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (Login,MainMenu):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Login(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)
        self.container = container

        self.title_frame = tk.Frame(self)
        l1 = tk.Label(self.title_frame, text="Login:", font=LARGE_FONT)
        l1.pack()

        self.login_frame = tk.Frame(self)
        password = tk.StringVar()
        self.p1 = tk.Label(self.login_frame, text='Password:', font=NORMAL_FONT)
        self.p2 = tk.Entry(self.login_frame, textvariable=password, show='*')
        self.p1.pack(side=tk.LEFT)
        self.p2.pack(padx=5, side=tk.RIGHT)

        self.button_frame = tk.Frame(self)
        self.login = ttk.Button(text='login', command=lambda:self.move_MainMenu(password.get()))
        self.login.pack()

        self.status_frame = tk.Label(self)

        self.title_frame.pack(pady=5)
        self.login_frame.pack(pady=5)
        self.button_frame.pack(pady=2)
        self.status_frame.pack(side=tk.BOTTOM, pady=15)

    def move_MainMenu(self, password):
        main.login(ref, password)
        if ref.token != None:
            self.container.show_frame(MainMenu)
        if ref.token==None:
            self.label=tk.Label(self.status_frame,text="incorrect password")
            self.label.pack()


class MainMenu(tk.Frame):
    def __init__(self, parent, container):
        tk.Frame.__init__(self, parent)


app = App()
app.geometry("400x200")
app.mainloop()
#
# # class for frame
# class simpleapp_tk(tkinter.Tk):
#     def __init__(self, parent):
#         tkinter.Tk.__init__(self, parent)
#         self.parent = parent
#         self.initialize()
#
#     def initialize(self):
#         self.grid()
#
#         # window config
#         self.resizable(False, False)
#
#         # login button
#         self.button1 = tkinter.Button(self, text="Log in", anchor="center", command=self.LogInClick)
#         self.button1.grid(column=0, row=1, columnspan=2, sticky="EW")
#
#         # password label
#         self.label1 = tkinter.Label(self, text="password:", anchor="w")
#         self.label1.grid(column=0, row=0, sticky="W")
#
#         # password entry
#         self.entry1Var = tkinter.StringVar()
#         self.entry1Var.set("Password")
#         self.entry1 = tkinter.Entry(self, textvariable=self.entry1Var)
#         self.entry1.grid(column=1, row=0, sticky="E")
#
#     def LogInClick(self):
#         # clean window
#         self.entry1.destroy()
#         self.entry1.destroy()
#         self.entry1.destroy()
#         self.label1.destroy()
#         self.button1.destroy()
#
#         # menu label
#         self.label1 = tkinter.Label(self, text="Chose article option:", anchor="w")
#         self.label1.grid(column=0, row=0, columnspan=1, sticky="EW")
#
#         # Buttons
#         self.button1 = tkinter.Button(self, text="New Article", anchor="w", command=self.MakeNewArticle)
#         self.button1.grid(column=0, row=1, sticky="EW")
#
#         self.button2 = tkinter.Button(self, text="Excisting article", anchor="w", command=self.ChoseExcistArticle)
#         self.button2.grid(column=1, row=1, sticky="EW")
#
#         self.button3 = tkinter.Button(self, text="Delete article", anchor="w", command=self.DeleteArticle)
#         self.button3.grid(column=2, row=1, sticky="EW")
#
#         self.button4 = tkinter.Button(self, text="Edit article status", anchor="w", command=self.EditArticle)
#         self.button4.grid(column=3, row=1, sticky="EW")
#
#     #
#     def MakeNewArticle(self):
#         # clean window
#         self.label1.destroy()
#         self.button1.destroy()
#         self.button2.destroy()
#         self.button3.destroy()
#         self.button4.destroy()
#
#         # menu label
#         self.label1 = tkinter.Label(self, text="insert info for article:", anchor="center")
#         self.label1.grid(column=0, row=0, columnspan=2, sticky="EW")
#
#         # name label
#         self.label2 = tkinter.Label(self, text="Article name:", anchor="w")
#         self.label2.grid(column=0, row=1, sticky="W")
#
#         # name entry
#         self.entry1Var = tkinter.StringVar()
#         self.entry1Var.set("Name here")
#         self.entry1 = tkinter.Entry(self, textvariable=self.entry1Var)
#         self.entry1.grid(column=1, row=1, sticky="E")
#
#         # status label
#         self.label3 = tkinter.Label(self, text="Article status:", anchor="w")
#         self.label3.grid(column=0, row=2, sticky="W")
#
#         # status entry
#         self.entry2Var = tkinter.StringVar()
#         self.entry2Var.set("status here")
#         self.entry2 = tkinter.Entry(self, textvariable=self.entry2Var)
#         self.entry2.grid(column=1, row=2, sticky="E")
#
#         # Button
#         self.button1 = tkinter.Button(self, text="Next", anchor="center", command=self.NextSourceClear1)
#         self.button1.grid(column=0, row=3, columnspan=2, sticky="EW")
#
#     #
#     def ChoseExcistArticle(self):
#         # clean window
#         self.label1.destroy()
#         self.button1.destroy()
#         self.button2.destroy()
#         self.button3.destroy()
#         self.button4.destroy()
#
#         # menu label
#         self.label1 = tkinter.Label(self, text="chose article:", anchor="center")
#         self.label1.grid(column=0, row=0, columnspan=2, sticky="EW")
#
#         # option list
#         self.option1Var = tkinter.StringVar()
#         self.option1 = tkinter.OptionMenu(self, self.option1Var, "Article 1", "Article 2", "Article 3", "...")
#         self.option1.grid(column=0, row=1, columnspan=2, sticky="EW")
#
#         # Buttons
#         self.button1 = tkinter.Button(self, text="Next", anchor="center", command=self.NextSourceClear2)
#         self.button1.grid(column=0, row=2, columnspan=2, sticky="EW")
#
#     #
#     def DeleteArticle(self):
#         pass
#
#     def EditArticle(self):
#         pass
#
#     #
#     def NextSourceClear1(self):
#         self.label1.destroy()
#         self.label2.destroy()
#         self.label3.destroy()
#         self.entry1.destroy()
#         self.entry2.destroy()
#         self.button1.destroy()
#         self.NextSource()
#
#     #
#     def NextSourceClear2(self):
#         self.label1.destroy()
#         self.button1.destroy()
#         self.option1.destroy()
#         self.NextSource()
#
#     #
#     def NextSource(self):
#         # menu label
#         self.label1 = tkinter.Label(self, text="Chose source option:", anchor="w")
#         self.label1.grid(column=0, row=0, sticky="EW")
#
#         # Buttons
#         self.button1 = tkinter.Button(self, text="Add New Source", anchor="w", command=self.MakeNewSource)
#         self.button1.grid(column=0, row=1, sticky="EW")
#
#         self.button2 = tkinter.Button(self, text="Add Excisting Source", anchor="w", command=self.ChoseExcistSource)
#         self.button2.grid(column=1, row=1, sticky="EW")
#
#         self.button2 = tkinter.Button(self, text="Edit Source", anchor="w", command=self.EditSource)
#         self.button2.grid(column=2, row=1, sticky="EW")
#
#         # source list
#         self.label2 = tkinter.Label(self, text="Source 1", anchor="w")
#         self.label2.grid(column=0, row=2, columnspan=3, sticky="EW")
#
#         self.label3 = tkinter.Label(self, text="Source 2", anchor="w")
#         self.label3.grid(column=0, row=3, columnspan=3, sticky="EW")
#
#         # buttons continue
#         self.button3 = tkinter.Button(self, text="Save article", anchor="center", command=self.SaveArticle)
#         self.button3.grid(column=0, row=4, columnspan=3, sticky="EW")
#
#         self.button4 = tkinter.Button(self, text="Next", anchor="center", command=self.ChoseFormatType)
#         self.button4.grid(column=0, row=5, columnspan=3, sticky="EW")
#
#     #
#     def MakeNewSource(self):
#         pass
#
#     def SaveArticle(self):
#         pass
#
#     # Option 4
#     def ChoseExcistSource(self):
#         pass
#
#     def EditSource(self):
#         pass
#
#     #
#     def ChoseFormatType(self):
#         # clean window
#         self.label1.destroy()
#         self.label2.destroy()
#         self.label3.destroy()
#         self.button1.destroy()
#         self.button2.destroy()
#         self.button3.destroy()
#         self.button4.destroy()
#
#         # Menu label
#         self.label1 = tkinter.Label(self, text="Chose format type:", anchor="center")
#         self.label1.grid(column=0, row=0, columnspan=2, sticky="EW")
#
#         # type list
#         self.option1Var = tkinter.StringVar()
#         self.option1 = tkinter.OptionMenu(self, self.option1Var, "IEEE", "MILA", "Harvard", "APA")
#         self.option1.grid(column=0, row=1, columnspan=2, sticky="EW")
#
#         # button
#         self.button1 = tkinter.Button(self, text="Export Text File", anchor="center", command=self.OpenTextFile)
#         self.button1.grid(column=0, row=2, columnspan=2, sticky="EW")
#
#     def OpenTextFile(self):
#         # open text file
#         os.startfile('ExportList.txt')
#
#
# if __name__ == "__main__":
#     app = simpleapp_tk(None)
#     app.title("My App!")  # giving title to window
#     app.mainloop()  # used for events to  work
