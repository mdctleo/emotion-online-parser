import tkinter as tk
from tkinter import filedialog as fd

from parser import Parser


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Text(self)
        self.text.insert(tk.INSERT, "Emotion Online Parser")
        self.text.pack(side="top")
        # self.text.pack(side="top")

        self.open = tk.Button(self, text="OPEN FILES", fg="green", command=self.open_files)
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        self.open.pack(side="bottom")


    def open_files(self):
        files = tk.filedialog.askopenfilenames(title="Select Files to parse", filetypes=[("csv files","*.csv")])
        parser = Parser(list(files))
        parser.parse()






root = tk.Tk()
app = Application(master=root)
app.mainloop()