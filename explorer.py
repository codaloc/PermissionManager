import tkinter as tk
import os
class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x500")
        self.root.title("File Manager")
        self.root.configure(bg="white")

        self.path = "/home"

        # Path textbox and return button
        self.path_grid = tk.Frame(self.root, background="white")
        self.path_grid.pack(fill=tk.X, padx=30, pady=10)  

        self.path_grid.grid_columnconfigure(0, weight=1)
        self.path_grid.grid_columnconfigure(1, weight=0)  

        self.pathbox = tk.Entry(self.path_grid, font=("Arial",17), border=0,takefocus=True)
        self.pathbox.bind("<KeyPress>", self.shortcut)
        self.pathbox.grid(row=0, column=0, padx=(0,20), ipady=4, sticky='ew')
        self.pathbox.insert(0, self.path)

        self.return_button = tk.Button(
            self.path_grid, 
            text="Back", 
            font=("Arial",17), 
            border=0,
            bg="gainsboro",
            command=self.path_back
        )
        self.return_button.grid(row=0, column=1, padx=(0,30), pady=0)

        # Options
        self.checkbox_frame = tk.Frame(self.root, background="white")
        self.checkbox_frame.pack(fill=tk.X, padx=20, side=tk.TOP, expand=False)

        self.show_hidden_value = tk.IntVar()
        self.show_hidden_checkbox = tk.Checkbutton(self.checkbox_frame, text="Show hidden", font=("Arial",15),background="white", variable=self.show_hidden_value, command=self.draw_files)
        self.show_hidden_checkbox.pack(side=tk.LEFT, padx=10)

        self.show_directories_value = tk.IntVar(value=1)
        self.show_directories_checkbox = tk.Checkbutton(self.checkbox_frame, text="Show directories", font=("Arial", 15),background="white", variable=self.show_directories_value, command=self.draw_files)
        self.show_directories_checkbox.pack(side=tk.LEFT, padx=10)

        # Files
        self.filesframe = tk.Frame(self.root,background="white")
        self.filesframe.pack(fill=tk.X, padx=20, side=tk.TOP, expand=False)


        self.root.bind('<Configure>', self.on_resize)
        self.last_width = self.root.winfo_width()
        self.last_height = self.root.winfo_height()
        self._resize_job = None

        self.draw_files()
        
        self.root.mainloop()
    
    def on_resize(self, event):
        # only root window events and actual size changes
        if (event.widget == self.root and 
            (event.width != self.last_width or event.height != self.last_height)):
            
            # cancel resize job
            if self._resize_job is not None:
                self.root.after_cancel(self._resize_job)
            
            # schedule new resize job
            self._resize_job = self.root.after(100, lambda: self.redraw_right_size(event.width, event.height))
    
    def redraw_right_size(self, new_width, new_height):
        self.last_width = new_width
        self.last_height = new_height
        self.draw_files()



    def get_file_list(self):
        files = []

        for file in os.listdir(self.path):
            if self.show_hidden_value.get() == False:
                if file.startswith('.'):
                    continue
                else:
                    if self.show_directories_value.get():
                        files.append(file)
                    else:
                        if os.path.isfile(file):
                            files.append(file)
            else:
                if self.show_directories_value.get():
                    files.append(file)
                else:
                    if os.path.isfile(file):
                            files.append(file)
        files.sort()

        return files

    def draw_files(self):

        files = self.get_file_list()

        nb=len(files)
        future_frame = tk.Frame(self.root, background="white")
        
        # calculate number of columns
        window_width = self.root.winfo_width()
        button_width = 200  # target width
        collumns_nb = max(1, window_width // button_width)
        
        # expand equally
        future_frame.grid_columnconfigure(tuple(range(collumns_nb)), weight=1, uniform='column')
        
        for i in range((nb + collumns_nb - 1) // collumns_nb):  # finds the right number of rows
            future_frame.grid_rowconfigure(i, weight=0)  #  0 to prevent vertical expansion
            
        allfiles = []
        # draw full rows
        for i in range(nb//collumns_nb):
            for j in range(collumns_nb):
                allfiles.append(File(future_frame, files[i*collumns_nb+j], (i,j), self))  
        # draw last incomplete row
        for k in range(nb%collumns_nb):
                allfiles.append(File(future_frame, files[collumns_nb*(nb//collumns_nb)+k], (nb//collumns_nb,k), self))  

        for file in allfiles:
            file.draw()

        # remove old frame and show new one
        self.filesframe.destroy()
        future_frame.pack(fill=tk.X, padx=20, side=tk.TOP, expand=False)
        self.filesframe = future_frame

    def update_path(self,path):
        #old_path = self.path
        try:
            os.chdir(path)
        except Exception:
            self.pathbox.delete(0, tk.END)
            self.pathbox.insert(0, self.path)
        else:
            self.path = path
            self.pathbox.delete(0, tk.END)
            self.pathbox.insert(0, path)

        self.draw_files()

    def shortcut(self, event):
        if event.keysym == "Return":
            self.update_path(self.pathbox.get().rstrip())
            return "break"

    def path_back(self):
        pathdirs = self.path.split("/")
        pathdirs.pop()
        if len(pathdirs) == 1:
            self.path = "/"
        else:
            self.path = "/".join(pathdirs)
        self.update_path(self.path)

class File:
    def __init__(self, frame, name, location, ui_instance):  
        self.name = name
        self.location = location
        full_path = os.path.join(ui_instance.path, name)

        if os.path.isdir(full_path):
            color = "gainsboro"
        else:
            color = "white"



        self.widget = tk.Button(
            frame, 
            text=f"{name}", 
            font=("Arial",15), 
            bg=color,
            activebackground="gray",
            border=0,
            height=3, 
            wraplength=150, 
            command=lambda: ui_instance.update_path(full_path)
        )

        
    def draw(self):
        self.widget.grid(row=self.location[0], column=self.location[1], padx=10, pady=10, sticky='nsew')  

UI()