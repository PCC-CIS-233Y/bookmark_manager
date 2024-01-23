
def valid_g_number(n):
    return len(n) == 9 and n[0] == 'G' and n[1:9].isdigit()


def number_in_range(value, ge, gt, le, lt):
    if ge is not None and value < ge:
        return False
    if gt is not None and value <= gt:
        return False
    if le is not None and value > le:
        return False
    if lt is not None and value >= lt:
        return False
    return True


def input_int(prompt="Please enter a whole number: ", error="Input must be a whole number!",
              ge=None, gt=None, le=None, lt=None):
    while True:
        try:
            val_string = input(prompt)
            val_int = int(val_string)
            if number_in_range(val_int, ge, gt, le, lt):
                return val_int
            print(error)
        except ValueError:
            print(error)

def y_or_n(prompt="Please enter yes or no: ", error="Input must be either yes or no!"):
    while True:
        val = input(prompt).lower()
        if val in ["y", "yes", "oui", "ja"]:
            return True
        if val in ["n", "no", "non", "nein"]:
            return False
        print(error)

def is_non_empty(s):
    return len(s) > 0

def input_string(prompt="Please type some text: ", error="Input must be non-empty!", valid=lambda s: len(s) > 0):
    while True:
        try:
            val = input(prompt)
            if valid(val):
                return val
            print(error)
        except ValueError:
            print(error)

def select_item(prompt="Please type yes or no: ", error="Answer must be yes or no!", choices=["Yes", "No"], map=None):
    value_dict = {}
    for choice in choices:
        value_dict[choice.lower()] = choice
    if map is not None:
        for key in map:
            value_dict[key.lower()] = map[key]
    while True:
        val = input(prompt).lower()
        if val in value_dict:
            return value_dict[val]
        print(error)

def input_item(type="int", *args, **kwargs):
    if type == "int":
        return input_int(*args, **kwargs)
    elif type == "y_or_n":
        return y_or_n(*args, **kwargs)
    elif type == "string":
        return input_string(*args, **kwargs)
    elif type == "select":
        return select_item(*args, **kwargs)
    else:
        print("Error! Unknown type", type)
