ROLL_PATTERN = '(^\d+d\d+)|([\+\-]\d+d\d+)|([\+\-]\d+(?!d))'
BONUS_PATTERN = '(^[+-]?\d+)|((?<=\/)[+-]?\d+)*'

def concat_lists(list_of_iters):
    output = []
    for sub in list_of_iters:
        for item in sub:
            output.append(item)
    return output

def remove_nulls(origin_list):
    return [item for item in origin_list if item]

def clean_float(f):
    if f == int(f):
        return int(f)
    for i in range(2, 5):
        if f == round(f, i):
            return round(f, i-1)
    return round(f, 4)