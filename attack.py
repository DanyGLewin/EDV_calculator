from tkinter import *

import calc
import roll
import utils


class Attack(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=None, borderwidth=2)
        self.master = master
        self.label_strings = []
        self.labels = []

        self.ac = StringVar()
        self.ac_entry = None

        self.attack = StringVar()
        self.attack_entry = None

        self.base_damage = StringVar()
        self.base_damage_entry = None

        self.crit_damage = StringVar()
        self.crit_damage_entry = None

        self.crit_chance = StringVar(value='5%')
        self.crit_chance_entry = None

        self.edv = StringVar()
        self.edv_label = None

        self.entry_vars = []
        self.entries = []

        self.init_details()

    def init_details(self):
        """
        """
        self.label_strings = ['Enemy AC', 'Attack bonus', 'Damage', 'Crit damage', 'Crit chance', 'EDV']
        self.labels = [Label(self, text=label) for label in self.label_strings]
        for i in range(len(self.labels)):
            self.labels[i].grid(row=i, column=0, sticky=W)

        self.edv_label = Label(self, textvariable=self.edv)
        self.edv_label.grid(row=len(self.labels) - 1, column=1, sticky=W)

        self.ac_entry = Entry(self, textvariable=self.ac)
        self.attack_entry = Entry(self, textvariable=self.attack)
        self.base_damage_entry = Entry(self, textvariable=self.base_damage)
        self.crit_damage_entry = Entry(self, textvariable=self.crit_damage)
        self.crit_chance_entry = Entry(self, textvariable=self.crit_chance)

        self.entries = [self.ac_entry, self.attack_entry, self.base_damage_entry,
                        self.crit_damage_entry, self.crit_chance_entry]

        self.entry_vars = [self.ac, self.attack, self.base_damage, self.crit_damage, self.crit_chance]

        for i in range(len(self.entries)):
            self.entries[i].grid(row=i, column=1, sticky=E)
            self.entry_vars[i].trace('w', lambda name, index, mode, var=self.entry_vars[i]: self.calculate_edv())

        self.edv.trace('w', lambda name, index, mode, var=self.edv: self.master.master.total.update())

    def calculate_edv(self):
        try:
            ac = int(self.ac.get())

            crit_chance_string = self.crit_chance.get()
            crit_chance = 0.05
            if len(crit_chance_string) and crit_chance_string[-1] == '%':
                crit_chance_string = crit_chance_string[:-1]

            try:
                crit_chance = int(crit_chance_string)
                crit_chance = float(crit_chance) / 100
            except ValueError:
                if '.' in crit_chance_string:
                    crit_chance = float(crit_chance_string)
                elif '-20' in crit_chance_string:
                    lower_bound = int(crit_chance_string.split('-')[0])
                    crit_chance = 0.05 * (21-lower_bound)


            attack_string = self.attack.get()
            attack_list = roll.get_attack_bonuses(attack_string)

            damage_string = self.base_damage.get()
            damage_roll = roll.Roll(damage_string)

            crit_damage_string = self.crit_damage.get()
            crit_roll = roll.Roll(crit_damage_string)

            edvs = [calc.calculate_damage(ac, attack, damage_roll.average(), crit_roll.average(), crit_chance)
                    for attack in attack_list]

            for i in range(len(edvs)):
                edvs[i] = str(utils.clean_float(edvs[i]))

            edv_string = ' / '.join(edvs)
            self.edv.set(edv_string)
        except ValueError as e:
            # self.edv.set(e)
            self.edv.set('NaN')
