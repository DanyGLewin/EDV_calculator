from roll import Roll
from PyInquirer import prompt


def is_num(string):
    try:
        float(string)
        return True
    except Exception:
        return False


def get_input():
    questions = [
        {
            'type': 'list',
            'name': 'system',
            'message': 'What system are you using?',
            'choices': ['5e', 'Pathfinder']
        },
        {
            'type': 'input',
            'name': 'ac',
            'message': 'What AC are you attacking against?\n >',
            'validate': lambda val: is_num(val)
        },
        {
            'type': 'input',
            'name': 'attack',
            'message': "What's your to-hit bonus?\n >",
            'validate': lambda val: is_num(str(val).replace('+', ''))
        },
        {
            'type': 'input',
            'name': 'base_damage',
            'message': "What's your regular damage?\n >"
        },
        {
            'type': 'input',
            'name': 'crit_damage',
            'message': "What's your critical hit damage?\n >"
        },
        {
            'type': 'list',
            'name': 'crit_range',
            'message': "What's your critical hit chance?",
            'choices': ['5%', '10%', '15%', '20%', '25%', '30%'],
            'when': lambda answers: answers['system'] == 'Pathfinder'
        }
    ]

    answers = prompt(questions)
    for key in ('ac', 'attack'):
        if key in answers.keys():
            answers[key] = float(answers[key])
    if 'crit_range' in answers.keys():
        if answers['crit_range'][-1] == '%':
            answers['crit_range'] = answers['crit_range'][:-1]
        answers['crit_range'] = int(answers['crit_range']) / 100.
    for key in ('base_damage', 'crit_damage'):
        if key in answers.keys():
            damage_roll = Roll(answers[key])
            answers[key] = damage_roll.average()
    return answers


def calculate_damage(ac, attack, base_damage, crit_damage, crit_range=0.05, **kwargs):
    chance = 1 - ((ac + 1 - attack) / 20.)
    chance -= crit_range
    if chance < 0:
        chance = 0
    if chance > 1 - crit_range:
        chance = 1 - crit_range
    return (chance * base_damage) + (crit_range * crit_damage)



def process(answers):
    edv = calculate_damage(**answers)
    # if answers['system'] == '5e':
    #     edv = calculate_damage(ac=answers['ac'],
    #                            attack=answers['attack'],
    #                            base_damage=answers['base_damage'],
    #                            crit_damage=answers['crit_damage']
    #                            )
    # elif answers['system'] == 'Pathfinder':
    #     edv = calculate_damage(ac=answers['ac'],
    #                            attack=answers['attack'],
    #                            base_damage=answers['base_damage'],
    #                            crit_damage=answers['crit_damage'],
    #                            crit_range=answers['crit_range']
    #                            )
    return edv


def go(first=False):
    question = [
        {
            'type': 'confirm',
            'name': 'continue',
            'message': 'Do you wish to continue?',
            'when': lambda answers: not first
        }
    ]
    return prompt(question)['continue']


def main():
    first = True
    cont = True
    while cont:
        try:
            answers = get_input()
            edv = process(answers)
            print(edv)
            first = False
            cont = go()
        except KeyError:
            break
        except ValueError:
            print("\nWhoops, something went wrong. Let's go again from the top.")
            continue


if __name__ == '__main__':
    main()
