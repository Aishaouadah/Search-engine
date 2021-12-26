import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
import bool_model

class App:


    
    def __init__(self, root):
        #setting title
        root.title("Search Engin")
        #setting window size
        width=550
        height=500
        self.selected = StringVar()
        self.selected.set("B")
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        radioBtn_bool=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        radioBtn_bool["font"] = ft
        radioBtn_bool["fg"] = "#333333"
        radioBtn_bool["justify"] = "center"
        radioBtn_bool["text"] = "Boolean  M."
        radioBtn_bool.place(x=170,y=50,width=85,height=25)
        radioBtn_bool['variable'] = self.selected
        radioBtn_bool['value'] = 'B'
        radioBtn_bool["command"] = self.radioBtn_bool_command

        radioBtn_vect=tk.Radiobutton(root)
        ft = tkFont.Font(family='Times',size=10)
        radioBtn_vect["font"] = ft
        radioBtn_vect["fg"] = "#333333"
        radioBtn_vect["justify"] = "center"
        radioBtn_vect["text"] = "Vectoril M."
        radioBtn_vect['variable'] = self.selected
        radioBtn_vect['value'] = 'V'
        radioBtn_vect.place(x=290,y=50,width=85,height=25)
        radioBtn_vect["command"] = self.radioBtn_vect_command

        self.input_request=tk.Entry(root)
        self.input_request["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.input_request["font"] = ft
        self.input_request["fg"] = "#333333"
        self.input_request["justify"] = "center"
        self.input_request["text"] = "Enter request ..."
        self.input_request.place(x=130,y=90,width=306,height=30)

        btn_search=tk.Button(root)
        btn_search["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        btn_search["font"] = ft
        btn_search["fg"] = "#000000"
        btn_search["justify"] = "center"
        btn_search["text"] = "Search"
        btn_search.place(x=240,y=140,width=91,height=33)
        btn_search["command"] = self.btn_search_command


        # Create text widget and specify size.
        self.textField_results = Text(root, height = 10, width = 52)
        self.textField_results.place(x=110,y=190,width=340,height=250)

    def radioBtn_bool_command(self):
        print('')


    def radioBtn_vect_command(self):
        print('')


    def btn_search_command(self):
        ## call appariment fct to calculate appariment of all docs and render the selected ones 
        selected_docs = bool_model.docs_appariment(self.input_request.get())

        print(selected_docs)
        text = ""
        for doc in selected_docs:
        
            index = bool_model.ids.index(doc)
            title =  bool_model.titles[index]
            text = text +"\n\n "+doc +"\t"+title

        self.textField_results.insert('end',text)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
