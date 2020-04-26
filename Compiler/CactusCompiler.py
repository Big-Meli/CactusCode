import tkinter as tk
from tkinter import filedialog
import re

class MenuBar:
    def __init__(self, parent):
        font_specs = ("Consolas", 9)

        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File", command=parent.new_file)
        file_dropdown.add_command(label="Open File", command=parent.open_file)
        file_dropdown.add_command(label="Save File", command=parent.save_file)
        file_dropdown.add_command(label="Save File As", command=parent.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Plant Cactus (Run with CactusCode)", command=parent.run)
        file_dropdown.add_command(label="Exit CactusCompiler")

        menubar.add_cascade(label="File", menu=file_dropdown)
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="Colouring")

        menubar.add_cascade(label="Options", menu=file_dropdown)

class PyText:

    def __init__(self, master):

        master.title("Untitled.cactus - CactusCompiler")
        master.geometry("1200x700")

        font_specs = ("Consolas", 13)

        self.master = master
        self.filename = None

        self.textarea = tk.Text(master, font=font_specs)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = MenuBar(self)
        self.textarea.bind("<Key>", self.syntax)

    def syntax(self, event):

        self.textarea.tag_configure("keyword", foreground="#c3e202")
        self.textarea.tag_configure("root", foreground="#83b301")
        self.textarea.tag_configure("list", foreground="#76ddd7")
        self.textarea.tag_configure("string", foreground="#fdfe80")

        for tag in event.widget.tag_names():
            event.widget.tag_remove(tag, "1.0", "end")

        lines = event.widget.get('1.0', 'end-1c').split('\n')
        for i, line in enumerate(lines):
            self.__applytag__(i, line, 'list', '\[|]|{|}', event.widget) # your tags here
            self.__applytag__(i, line, 'keyword', 'say|wait|set', event.widget)
            self.__applytag__(i, line, 'string', """".*"|'.*'""", event.widget)
            self.__applytag__(i, line, 'root', "@[a-zA-Z0-9]+", event.widget)

    @staticmethod
    def __applytag__ (line, text, tag, regex, widget):
        indexes = [(m.start(), m.end()) for m in re.finditer(regex, text)]
        for x in indexes:
            widget.tag_add(tag, f'{line+1}.{x[0]}', f'{line+1}.{x[1]}')

    def set_window_title(self, name=None):
        if name:
            self.master.title(name + " - CactusCompiler")

    def new_file(self):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self):
        self.filename = filedialog.askopenfilename(defaultextension=".cactus", filetypes=[("Sloppy Cactus Code (*.cactus.txt)", "*.cactus.txt"), ("Cactus Code (*.cactus)", "*.cactus"), ("All Files (*.*)", "*.*"), ("Text Files (*.txt)", "*.txt"), ("Python Scripts (*.py)", "*.py")])

        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as file:
                self.textarea.insert(1.0, file.read())
            self.set_window_title(self.filename)

    def save_file(self):
        pass

    def save_as(self):
        try:
            new_file = filedialog.asksaveasfilename(intialfile="Untitled.cactus", defaultextension=".cactus", filetypes=[("Sloppy Cactus Code (*.cactus.txt)", "*.cactus.txt"), ("Cactus Code (*.cactus)", "*.cactus"), ("All Files (*.*)", "*.*"), ("Text Files (*.txt)", "*.txt"), ("Python Scripts (*.py)", "*.py")])
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as file:
                file.write(textarea_content)
            self.filename = new_file
            self.set_window_title(self.filename)

        except Exception as e:
            print(e)

    def exit(self):
        pass

    def run(self):
        pass

if __name__ == "__main__":
    master = tk.Tk()
    pt = PyText(master)
    master.mainloop()
