from whaaaaat import prompt


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
            'message': "What's your damage dice average?\n >",
            'validate': lambda val: is_num(str(val)),
            'when': lambda answers: answers['system'] == '5e'
        },
        {
            'type': 'input',
            'name': 'flat_damage',
            'message': "What's your flat damage bonus?\n >",
            'validate': lambda val: is_num(str(val)),
            'when': lambda answers: answers['system'] == '5e'
        },
        {
            'type': 'input',
            'name': 'damage',
            'message': "What's your average damage?\n >",
            'validate': lambda val: is_num(str(val)),
            'when': lambda answers: answers['system'] == 'Pathfinder'
        },
        {
            'type': 'input',
            'name': 'multiplier',
            'message': "What's your critical hit multiplier?\n >",
            'validate': lambda val: is_num(str(val)),
            'when': lambda answers: answers['system'] == 'Pathfinder'
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
    for key in ('ac', 'attack', 'base_damage', 'flat_damage', 'damage', 'multiplier'):
        if key in answers.keys():
            answers[key] = float(answers[key])
    if 'crit_range' in answers.keys():
        answers['crit_range'] = int(answers['crit_range'][:-1])/100.
    return answers


def calculate_damage(system, ac, attack, base_damage=0, flat_damage=0, damage=0, multiplier=2, crit_range=0.05):
    if system == '5e':
        chance = 1 - ((ac+1 - attack) / 20.)
        if chance < 0:
            chance = 0
        if chance >= 1:
            chance = 0.95
        return (chance * (base_damage +flat_damage)) + 0.05 * (2*base_damage + flat_damage)

    elif system == 'Pathfinder':
        chance = 1 - ((ac+1 - attack) / 20.)
        chance -= crit_range
        if chance < 0:
            chance = 0
        if chance > 1 - crit_range:
            chance = 1 - crit_range
        return (chance * damage) + (crit_range * multiplier * damage)

    else:
        return 'Something went very wrong here'


def process(answers):
    if answers['system'] == '5e':
        edv = calculate_damage(system='5e',
                               ac=answers['ac'],
                               attack=answers['attack'],
                               base_damage=answers['base_damage'],
                               flat_damage=answers['flat_damage']
                               )
    elif answers['system'] == 'Pathfinder':
        edv = calculate_damage(system='Pathfinder',
                               ac=answers['ac'],
                               attack=answers['attack'],
                               damage=answers['damage'],
                               multiplier=answers['multiplier'],
                               crit_range=answers['crit_range']
                               )
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
            print edv
            first = False
            cont = go()
        except KeyError:
            break
        except ValueError:
            print "\nWhoops, something went wrong. Let's go again from the top."
            continue

if __name__ == '__main__':
    main()
