from tkinter import *
import attack
import total


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.attacks = AttacksFrame(self)
        self.total = None
        self.init_window()

    def init_window(self):
        self.master.title("DPR Calculator 0.2")

        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        edit.add_command(label="Add attack", command=self.attacks.add_attack)
        edit.add_command(label="Remove attack", command=self.attacks.remove_attack)
        menu.add_cascade(label="Edit", menu=edit)


        self.total = total.Total(self, 1)
        self.total.grid(row=1)

        self.attacks.grid(row=0)
        self.attacks.add_attack()


    def client_exit(self):
        self.master.destroy()




class AttacksFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.attacks = []


    def add_attack(self):
        self.attacks.append(attack.Attack(self))
        self.attacks[-1].grid(row=0, column=len(self.attacks) - 1)

        self.master.total.grid_forget()
        self.master.total.total_edv_label.grid_forget()
        self.master.total = total.Total(self.master, length=len(self.attacks))
        self.master.total.grid(row=1)

    def remove_attack(self):
        if len(self.attacks) == 1:
            return
        target = self.attacks.pop()
        target.grid_forget()

        self.master.total.grid_forget()
        self.master.total.total_edv_label.grid_forget()
        self.master.total = total.Total(self.master, length=len(self.attacks))
        self.master.total.grid(row=1)


root = Tk()

main_window = Window(root)





root.mainloop()
