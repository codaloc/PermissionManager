import tkinter as tk
import os
import subprocess
import stat
from tkinter import font



class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x500")
        self.root.title("Window")
        self.root.option_add("*Background", "white")
        self.root.configure(bg="white")


        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=0)
        
        self.textbox1 = tk.Entry(self.top_frame, font=("monospace",18))
        self.textbox1.bind("<KeyPress>", self.shortcut)
        self.textbox1.grid(row=0, column=0, padx=5, pady=5, sticky='we')

        self.main_button = tk.Button(self.top_frame, text="Permissions", font=("monospace",14), border=0, bg="gainsboro",activeforeground="grey", command=self.get_perms)
        self.main_button.grid(row=0, column=1, padx=5, pady=5, ipady=1, sticky='e')

        self.file_text = tk.Text(self.root, height=1, font=("monospace",30), state="disabled" , border=0,  highlightthickness = 0)
        self.file_text.pack(side=tk.TOP)

        self.warning_text = tk.Text(self.root, height=1, font=("monospace",12), state="disabled", border=0,  highlightthickness = 0, fg="red")
        self.warning_text.pack(side=tk.TOP)

        self.tip_text = tk.Text(self.root, height=1, font=("monospace",15), state="disabled" , border=0,  highlightthickness = 0)
        self.tip_text.pack(padx=20, side=tk.TOP)
        self.tip_text.tag_configure("center", justify='center')
        self.tip_text.config(state="normal")
        self.tip_text.insert(tk.END, "User   Group   Other     Octal ", "center")
        self.tip_text.config(state="disabled")
        
        self.output_text = tk.Text(self.root, height=1, font=("monospace",30), state="disabled" , border=0,  highlightthickness = 0)
        self.output_text.config(state="normal")
        self.output_text.tag_configure("center", justify='center')
        self.output_text.insert(tk.END, "--- --- --- (---)" , "center")
        self.output_text.config(state="disabled")
        self.output_text.pack(padx=20, side=tk.TOP,ipady=0)


        ###############################################

        self.all_checkboxes = tk.Frame(self.root)
        self.all_checkboxes.pack(side=tk.TOP, padx=5, pady=5)


        ## User checkboxes
        self.user_checkboxes = tk.Frame(self.all_checkboxes)

        self.user_label = tk.Label(self.user_checkboxes, text="User: ", font=("monospace",15))
        self.user_label.pack(side=tk.LEFT, padx=10)

        self.user_read_value = tk.IntVar()
        self.user_checkbox = tk.Checkbutton(self.user_checkboxes, text="Read", font=("monospace",15),variable=self.user_read_value, activeforeground="black")
        self.user_checkbox.pack(side=tk.LEFT, padx=10, pady=1)

        self.user_write_value = tk.IntVar()
        self.user_checkbox = tk.Checkbutton(self.user_checkboxes, text="Write", font=("monospace",15),variable=self.user_write_value, activeforeground="black")
        self.user_checkbox.pack(side=tk.LEFT, padx=10, pady=1)

        self.user_execute_value = tk.IntVar()
        self.user_checkbox = tk.Checkbutton(self.user_checkboxes, text="Execute", font=("monospace",15),variable=self.user_execute_value, activeforeground="black")
        self.user_checkbox.pack(side=tk.LEFT, padx=10, pady=1)

        self.user_checkboxes.pack(side=tk.TOP, fill=tk.X)

        ## Group checkboxes
        self.group_checkboxes = tk.Frame(self.all_checkboxes)

        self.group_label = tk.Label(self.group_checkboxes, text="Group:", font=("monospace",15))
        self.group_label.pack(side=tk.LEFT, padx=10)

        self.group_read_value = tk.IntVar()
        self.group_checkbox = tk.Checkbutton(self.group_checkboxes, text="Read", font=("monospace",15),variable=self.group_read_value, activeforeground="black")
        self.group_checkbox.pack(side=tk.LEFT, padx=10, pady=1)

        self.group_write_value = tk.IntVar()
        self.group_checkbox = tk.Checkbutton(self.group_checkboxes, text="Write", font=("monospace",15),variable=self.group_write_value, activeforeground="black")
        self.group_checkbox.pack(side=tk.LEFT, padx=10, pady=1)

        self.group_execute_value = tk.IntVar()
        self.group_checkbox = tk.Checkbutton(self.group_checkboxes, text="Execute", font=("monospace",15),variable=self.group_execute_value, activeforeground="black")
        self.group_checkbox.pack(side=tk.LEFT, padx=10, pady=1)

        self.group_checkboxes.pack(side=tk.TOP, fill=tk.X)

        ## Other checkboxes
        self.other_checkboxes = tk.Frame(self.all_checkboxes)

        self.other_label = tk.Label(self.other_checkboxes, text="Other:", font=("monospace",15))
        self.other_label.pack(side=tk.LEFT, padx=10)

        self.other_read_value = tk.IntVar()
        self.other_checkbox = tk.Checkbutton(self.other_checkboxes, text="Read", font=("monospace",15),variable=self.other_read_value, activeforeground="black")
        self.other_checkbox.pack(side=tk.LEFT, padx=10, pady=1)

        self.other_write_value = tk.IntVar()
        self.other_checkbox = tk.Checkbutton(self.other_checkboxes, text="Write", font=("monospace",15),variable=self.other_write_value, activeforeground="black")
        self.other_checkbox.pack(side=tk.LEFT, padx=10, pady=1)

        self.other_execute_value = tk.IntVar()
        self.other_checkbox = tk.Checkbutton(self.other_checkboxes, text="Execute", font=("monospace",15),variable=self.other_execute_value, activeforeground="black")
        self.other_checkbox.pack(side=tk.LEFT, padx=10, pady=1)

        self.other_checkboxes.pack(side=tk.TOP, fill=tk.X)

        ###############################################

        self.command_box = tk.Entry(self.root, font=("monospace",15))
        #self.command_box.pack(fill=tk.X, side=tk.TOP, padx=30, pady=5)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, padx=5)

        self.refresh_button = tk.Button(self.button_frame, text="Refresh", font=("monospace",14), border=0, bg="gainsboro", activeforeground="grey", command=self.get_perms)
        self.refresh_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.set_button = tk.Button(self.button_frame, text="Preview", font=("monospace",14), border=0, bg="gainsboro", activeforeground="grey", command=self.preview_perms)
        self.set_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.change_button = tk.Button(self.button_frame, text="Change", font=("monospace",14), border=0, bg="gainsboro", activeforeground="grey", command=self.set_command)
        self.change_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.run_button = tk.Button(self.button_frame, text="Run", border=0, font=("monospace",14), bg="salmon", activeforeground="white", activebackground="red", command=self.run_command)
        #self.run_button.pack(side=tk.LEFT, padx=5, pady=5)


        self.root.mainloop()

    def shortcut(self, event):
        if event.keysym == "Return":
            self.get_perms()
            return "break"
    

    def get_perms(self):
        path = self.textbox1.get().strip()
        if os.path.exists(path):
            command = f"stat {path} -c %a%A"
            result = subprocess.run(command, capture_output=True, check=True, shell=True)
            output = result.stdout.decode().rstrip()

            self.output_text.config(state="normal")
            self.output_text.tag_configure("center", justify='center')
            self.output_text.delete("1.0", tk.END)

            human = output[4:]
            aired_human = ""
            for i, char in enumerate(human):
                if i % 3 == 0 and i != 0:
                    aired_human += " "
                aired_human += char

            oneliner  = f"{aired_human} ({output[:3]})"

            self.output_text.insert(tk.END, oneliner, "center")
            self.output_text.config(state="disabled")

            self.set_checkboxes(output[:3])
            self.file_text.config(state="normal")
            self.file_text.delete("1.0", tk.END)
            self.file_text.tag_configure("center", justify='center')
            cleaned_path = os.path.basename(path.rstrip("/"))
            self.file_text.insert(tk.END, f"{cleaned_path}", "center")
            self.file_text.config(state="disabled")

            if os.path.isdir(path):
                self.warning_text.config(state="normal")
                self.warning_text.delete("1.0", tk.END)
                self.warning_text.tag_configure("center", justify='center')
                self.warning_text.insert(tk.END, f"Warning: Directory", "center")
                self.warning_text.config(state="disabled")
            else:
                self.warning_text.config(state="normal")
                self.warning_text.delete("1.0", tk.END)
                self.warning_text.config(state="disabled")
        else:

            self.warning_text.config(state="normal")
            self.warning_text.delete("1.0", tk.END)
            self.warning_text.tag_configure("center", justify='center')
            self.warning_text.insert(tk.END, "Warning: Invalid Path", "center")
            self.warning_text.config(state="disabled")


    def preview_perms(self):
        permslist = self.get_checkboxes()
        octalperms = self.bool_to_octal(permslist)
        human_readable = self.human_readable_from_octal(octalperms)


        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"{human_readable} ({octalperms})", "center")
        self.output_text.config(state="disabled")

    def set_command(self):
        # /home/coda/Documents/test.txt 
        self.preview_perms()
        permslist = self.get_checkboxes()
        octalperms = self.bool_to_octal(permslist)
        command = f"chmod {octalperms} {self.textbox1.get().strip()}"

        self.command_box.pack(fill=tk.X)
        self.command_box.delete(0, tk.END)
        self.command_box.insert(0, command)
        self.command_box.pack(fill=tk.X, side=tk.TOP, padx=30, pady=5)

        self.run_button.pack(side=tk.LEFT, padx=5, pady=5)

    def run_command(self):

        try:
            command = self.command_box.get()
            result = subprocess.run(command,  capture_output=True, check=True, shell=True)
            self.command_box.pack_forget()
            self.run_button.pack_forget()

            self.file_text.configure(fg="green")
            self.root.after(1000, lambda: self.file_text.configure(fg="black")) 

        except Exception as e:
            self.warning_text.config(state="normal")
            self.warning_text.delete("1.0", tk.END)
            self.warning_text.tag_configure("center", justify='center')
            self.warning_text.insert(tk.END, "Error: Command Failed", "center")
            self.warning_text.config(state="disabled")

            self.file_text.configure(fg="red")
            self.root.after(1000, lambda: self.file_text.configure(fg="black")) 

        else:
            self.get_perms()

        

    def set_checkboxes(self, octalperms):
        permslist = self.perms_to_list(octalperms)

        self.user_read_value.set(permslist[0][0])
        self.user_write_value.set(permslist[0][1])
        self.user_execute_value.set(permslist[0][2])

        self.group_read_value.set(permslist[1][0])
        self.group_write_value.set(permslist[1][1])
        self.group_execute_value.set(permslist[1][2])

        self.other_read_value.set(permslist[2][0])
        self.other_write_value.set(permslist[2][1])
        self.other_execute_value.set(permslist[2][2])
    
    def get_checkboxes(self):
        permslist = []
        permslist.append([self.user_read_value.get(), self.user_write_value.get(), self.user_execute_value.get()])
        permslist.append([self.group_read_value.get(), self.group_write_value.get(), self.group_execute_value.get()])
        permslist.append([self.other_read_value.get(), self.other_write_value.get(), self.other_execute_value.get()])

        permsstring = "|".join([" ".join(str(x)) for x in permslist])
        
        return permslist

    def perms_to_list(self, octalperms):
        # ocal : [read, write, execute]
        self.permdict = {
            0 : [False, False, False],
            1 : [False, False, True],
            2 : [False, True, False],
            3 : [False, True, True],
            4 : [True, False, False],
            5 : [True, False, True],
            6 : [True, True, False],
            7 : [True, True, True]
        }

        allperms = []
        for char in octalperms:
            allperms.append(self.permdict[int(char)])

        return allperms




    def human_readable_from_octal(self, octalperms):
        human_readable_dict = {
            "0" : "---",
            "1" : "--x",
            "2" : "-w-",
            "3" : "-wx",
            "4" : "r--",
            "5" : "r-x",
            "6" : "rw-",
            "7" : "rwx"
        }

        human_readable = []
        for oct in octalperms:
            human_readable.append(human_readable_dict[oct])
        human_readable = " ".join(human_readable)

        return human_readable


    def bool_to_octal(self, permslist):
        bool_dict = {
                "000" : 0,
                "001" : 1,
                "010" : 2,
                "011" : 3,
                "100" : 4,
                "101" : 5,
                "110" : 6,
                "111" : 7
            }

        octalperms = ""
        for subperm in permslist:
            octalperms += str(bool_dict["".join([str(x) for x in subperm])])

        return octalperms

            

UI()