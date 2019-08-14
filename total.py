from tkinter import *

import utils


class Total(Frame):
    def __init__(self, master, length):
        Frame.__init__(self, master=None)
        self.master = master
        self.total_edv_string = StringVar(value='')
        self.total_edv_label = Label(textvariable=self.total_edv_string)
        self.total_edv_label.grid(row=1, columnspan=length, sticky=S)
        self.update()

    def get_total_edv(self):
        running_sum = 0
        for attack in self.master.attacks.attacks:
            if str(attack.edv.get()) not in ('NaN', ''):
                for hit in str(attack.edv.get()).split('/'):
                    running_sum += float(hit)
        return utils.clean_float(running_sum)

    def update(self):
        self.total_edv_string.set(self.get_total_edv())
