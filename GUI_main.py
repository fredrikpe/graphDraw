

from Tkinter import *
from ttk import *
import tkFileDialog

import graph_class
import graph_draw


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)
        
        lbl = Label(self, text="Windows")
        lbl.grid(sticky=W, pady=4, padx=5)
        
        self.area = Text(self)
        self.area.grid(row=1, column=0, columnspan=2, rowspan=4, 
            padx=5, sticky=E+W+S+N)
        
        abtn = Button(self, text="Activate", command=self.onActivate)
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text="Close")
        cbtn.grid(row=2, column=3, pady=4)
        
        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu)

    def onActivate(self):
        text = self.area.get(1.0, END)
        if text != "":
            self.textToGraph(text)

    def textToGraph(self, text):
        words = text.split()
        length = int(words[0])
        edges = [[int(s[0]), int(s[1])] for s in words[1:]]
        new_graph = graph_class.Graph(edges, length)

        tmp_g = graph_draw.graph_draw(new_graph)


        root2 = Tk()
        ex = Drawing(root2, tmp_g)
        root2.geometry("330x220+300+300")
        root2.mainloop()



    def onOpen(self):
      
        ftypes = [('Text files', '*.txt'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        
        if fl != '':
            text = self.readFile(fl)
            self.area.insert(END, text)

    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        return text
              

def main():
  
    root = Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()  




class Drawing(Frame):
  
    def __init__(self, parent, graph):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.graph = graph       
        self.initUI()
        
        
    def initUI(self):
      
        self.parent.title("Shapes")        
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)

        for v in self.graph.vertices:
            self.createNode(v)

        self.canvas.pack(fill=BOTH, expand=1)

    def createNode(self, v):
        print v.x, v.y, v.index
        self.canvas.create_oval(10+v.x, 10+v.y, 40+v.x, 40+v.y, outline="#f11", 
        fill="#1f1", width=2)
        self.canvas.create_text(15+v.x, 45+v.y, text=str(v.index))


if __name__ == '__main__':
    main()






