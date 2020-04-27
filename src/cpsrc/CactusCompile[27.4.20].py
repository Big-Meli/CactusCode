import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re
import CactusCode

class MenuBar:
    def __init__(self, parent):
        font_specs = ("Arial", 9)

        menubar = tk.Menu(parent.master, font=font_specs)
        parent.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File", command=parent.new_file, accelerator="Ctrl+N")
        file_dropdown.add_command(label="Open File", command=parent.open_file, accelerator="Ctrl+O")
        file_dropdown.add_command(label="Save File", command=parent.save_file, accelerator="Ctrl+S")
        file_dropdown.add_command(label="Save File As", command=parent.save_as, accelerator="Ctrl+Shift+S")
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Plant Cactus (Run with CactusCode)", accelerator="Ctrl+R", command=parent.run)
        file_dropdown.add_command(label="Exit CactusCompiler", accelerator="Ctrl+X")

        menubar.add_cascade(label="File", menu=file_dropdown)
        options_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        options_dropdown.add_command(label="Colouring")

        menubar.add_cascade(label="Options", menu=options_dropdown)

        help_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        help_dropdown.add_command(label="About - Compiler", command=self.show_ab_cp)
        help_dropdown.add_command(label="About - Language", command=self.show_ab_m)
        help_dropdown.add_separator()
        help_dropdown.add_command(label="Release Notes - Compiler", command=self.show_rel_notes_cp)
        help_dropdown.add_command(label="Release Notes - Language", command=self.show_rel_notes_m)

        menubar.add_cascade(label="Help", menu=help_dropdown)

    def show_ab_cp(self):
        box_title = "About: CactusCompiler"
        box_message = "The official Compiler for the 'half baked' programming language known as CactusCode"

        messagebox.showinfo(box_title, box_message)

    def show_ab_m(self):
        box_title = "About: CactusCode"
        box_message = "The official Compiler for the 'half baked' programming language known as CactusCode"

        messagebox.showinfo(box_title, box_message)

    def show_rel_notes_cp(self):
        box_title = "Release Notes: CactusCompiler"
        box_message = "The official Compiler for the 'half baked' programming language known as CactusCode"

        messagebox.showinfo(box_title, box_message)

    def show_rel_notes_m(self):
        box_title = "Release Notes: CactusCode"
        box_message = "The official Compiler for the 'half baked' programming language known as CactusCode"

        messagebox.showinfo(box_title, box_message)


class StatusBar:
    def __init__(self, parent):

        self.status = tk.StringVar()
        self.status.set("CactusCompiler - 1.0")
        font_specs = ("Arial", 10)

        label = tk.Label(parent.textarea, textvariable=self.status, fg="#a9a9a9", bg="lightgrey", anchor="sw", font=font_specs)

        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set("Your file Has Been Saved")
        else:
            self.status.set("CactusCompiler - 1.0")

class CactusCompiler:

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
        self.statusbar = StatusBar(self)
        self.textarea.bind("<Key>", self.syntax)
        self.bind_shortcuts()

    def syntax(self, event):
        self.textarea.tag_configure("list", foreground="#daa520")
        self.textarea.tag_configure("root", foreground="blue")
        self.textarea.tag_configure("keyword", foreground="#ffa500")
        self.textarea.tag_configure("string", foreground="#008b8b")
        self.textarea.tag_configure("variable", foreground="#adff2f")
        self.textarea.tag_configure("integer", foreground="#9370db")
        self.textarea.tag_configure("premaderoot", foreground="red")
        self.textarea.tag_configure("comment", foreground="dark gray", font=("Consolas 13 italic"))

        for tag in event.widget.tag_names():
            event.widget.tag_remove(tag, "1.0", "end")

        lines = event.widget.get('1.0', 'end-1c').split('\n')
        for i, line in enumerate(lines):
            self.__applytag__(i, line, 'list', '\[|]|{|}', event.widget) # your tags here
            self.__applytag__(i, line, 'keyword', 'say|wait|set|to|as|extending|with', event.widget)
            #self.__applytag__(i, line, 'integer', "[0-9]+", event.widget)
            self.__applytag__(i, line, 'root', "@[a-zA-Z0-9]+", event.widget)
            self.__applytag__(i, line, 'variable', "$[a-zA-Z0-9]+", event.widget)
            self.__applytag__(i, line, 'string', """".*"|'.*'""", event.widget)
            self.__applytag__(i, line, 'comment', "//[\s\S]+", event.widget)
            self.__applytag__(i, line, 'premaderoot', "@_[a-zA-Z0-9]+", event.widget)

    @staticmethod
    def __applytag__ (line, text, tag, regex, widget):
        indexes = [(m.start(), m.end()) for m in re.finditer(regex, text)]
        for x in indexes:
            widget.tag_add(tag, f'{line+1}.{x[0]}', f'{line+1}.{x[1]}')

    def set_window_title(self, name=None):
        if name:
            self.master.title(name + " - CactusCompiler")

    def new_file(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.set_window_title()

    def open_file(self, *args):
        self.filename = filedialog.askopenfilename(defaultextension=".cactus", filetypes=[("Sloppy Cactus Code (*.cactus.txt)", "*.cactus.txt"), ("Cactus Code (*.cactus)", "*.cactus"), ("All Files (*.*)", "*.*"), ("Text Files (*.txt)", "*.txt"), ("Python Scripts (*.py)", "*.py")])

        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as file:
                self.textarea.insert(1.0, file.read())
            self.set_window_title(self.filename)

    def save_file(self, *args):
        if self.filename:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as file:
                    file.write(textarea_content)

                self.statusbar.update_status(True)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self, *args):
        try:
            new_file = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".cactus", filetypes=[("Sloppy Cactus Code (*.cactus.txt)", "*.cactus.txt"), ("Cactus Code (*.cactus)", "*.cactus"), ("All Files (*.*)", "*.*"), ("Text Files (*.txt)", "*.txt"), ("Python Scripts (*.py)", "*.py")], initialfile="Untitled.cactus")
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as file:
                file.write(textarea_content)

            self.statusbar.update_status(True)

            self.filename = new_file
            self.set_window_title(self.filename)

        except Exception as e:
            print(e)

    def bind_shortcuts(self):
        self.textarea.bind("<Control-n>", self.new_file)
        self.textarea.bind("<Control-o>", self.open_file)
        self.textarea.bind("<Control-s>", self.save_file)
        self.textarea.bind("<Control-S>", self.save_as)
        self.textarea.bind("<Control-x>", self.exit)
        self.textarea.bind("<Control-r>", self.run)
        self.textarea.bind("<Key>", self.statusbar.update_status, self.syntax)

    def exit(self, *args):
        pass

    def run(self, *args):
        CactusCode.compile(str(self.textarea.get(1.0, tk.END)))

if __name__ == "__main__":
    master = tk.Tk()
    pt = CactusCompiler(master)
    master.mainloop()
