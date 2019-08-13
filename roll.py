import re
from random import randint
import utils


class Dice:
    def __init__(self, dice_string):
        assert 'd' in dice_string
        self.number = abs(int(dice_string.split('d')[0]))
        self.size = int(dice_string.split('d')[1])
        self.sign = -1 if dice_string[0] == '-' else 1
        assert self.number != 0 and self.size > 0

    def single_die(self):
        return randint(1, self.size)

    def roll(self):
        return self.sign * sum([self.single_die() for i in range(self.number)])

    def average(self):
        a = self.sign * self.number * float(self.size + 1) / 2
        if a == int(a):
            a = int(a)
        return a

    def __str__(self):
        return '{}d{}'.format(self.sign * self.number, self.size)

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)


class Roll:
    def __init__(self, roll_string):
        string_copy = roll_string
        for i in string_copy:
            if i not in ['0123456789d+-']:
                roll_string.replace(i, '')

        if 'd' in roll_string:
            dice_strings, modifier_strings = self.split_roll(roll_string)
            self.dice = [Dice(single_dice) for single_dice in dice_strings]
            self.modifier = sum([int(mod_string) for mod_string in modifier_strings])
        else:
            self.dice = []
            self.modifier = int(roll_string)

    @staticmethod
    def split_roll(roll_str):
        all_matches = re.findall(utils.ROLL_PATTERN, roll_str)
        all_matches = utils.concat_lists(all_matches)
        all_matches = utils.remove_nulls(all_matches)
        if not all_matches:
            return {}
        if '+' not in all_matches[0] and '-' not in all_matches[0]:
            all_matches[0] = '+' + all_matches[0]
        return (
            [item for item in all_matches if 'd' in item],
            [item for item in all_matches if 'd' not in item]
        )

    def roll(self):
        return sum([pool.roll() for pool in self.dice]) + self.modifier

    def average(self):
        average = sum([pool.average() for pool in self.dice]) + self.modifier
        if average == int(average):
            return int(average)
        return average

    def __repr__(self):
        if len(self.dice) == 0:
            return str(self.modifier)
        out = str(self.dice[0])
        for roll in self.dice[1:]:
            if roll.sign > 0:
                out += '+'
            out += roll
        if self.modifier > 0:
            return out + '+' + str(self.modifier)
        elif self.modifier < 0:
            return out + str(self.modifier)
        else:
            return out


def split_bonuses(bonus_string):
    matches = re.findall(utils.BONUS_PATTERN, bonus_string)
    matches = utils.concat_lists(matches)
    matches = utils.remove_nulls(matches)

    out = [int(attack) for attack in matches]
    return out

def get_attack_bonuses(attack_string):
    string_copy = attack_string
    for i in string_copy:
        if i not in '0123456789d+-':
            attack_string.replace('i', '')
    attack_bonus_list = split_bonuses(attack_string)
    return attack_bonus_list