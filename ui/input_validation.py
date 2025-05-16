def input_int(prompt="Please enter a whole number: ",
              error="Invalid input! Please input a whole number within defined range.",
              ge=None, gt=None, le=None, lt=None):
    while True:
        try:
            val = int(input(prompt))
            if gt is not None and val <= gt:
                print(error)
            elif ge is not None and val < ge:
                print(error)
            elif lt is not None and val >= lt:
                print(error)
            elif le is not None and val > le:
                print(error)
            else:
                return val
        except ValueError:
            print(error)

def input_float(prompt="Please enter a decimal number: ",
                error="Invalid input! Please input a decimal number within defined range.",
                ge=None, gt=None, le=None, lt=None):
    while True:
        try:
            val = float(input(prompt))
            if gt is not None and val <= gt:
                print(error)
            elif ge is not None and val < ge:
                print(error)
            elif lt is not None and val >= lt:
                print(error)
            elif le is not None and val > le:
                print(error)
            else:
                return val
        except ValueError:
            print(error)

def input_string(prompt="Please input any string: ",
                 error="Invalid input! Please input any string.",
                 valid=lambda x: len(x) > 0):
    while True:
        val = str(input(prompt))
        if not valid:
            print(error)
        else:
            return val

def y_or_n(prompt="Please select Yes or No (y/n): ",
           error="Invalid input! Must be some form of yes or no."):
    while True:
        val = str(input(prompt))
        val = val.lower()
        acceptable = ['y', 'n', 'yes', 'no', 'ye', 'nah', 'ya', 'nope', 'yeah', 'naur']
        if val not in acceptable:
            print(error)
        elif val[0] == 'y':
            return True
        elif val[0] == 'n':
            return False
        else:
            print(error)

def select_item(prompt="Please make a selection: ",
                error="Invalid input! Please input a valid selection.",
                options=[],
                map=None):
    value_dict = {}
    for choice in options:
        value_dict[choice.lower()] = choice
    if map is not None:
        for key in map:
            value_dict[key.lower()] = map[key]
    while True:
        val = input(prompt).lower()
        if val in value_dict:
            return value_dict[val]
        print(error)

def input_value(type=None, prompt=None, error=None,
                ge=None, gt=None, le=None, lt=None,
                valid=None, options=None, map=None):
    while True:
        if type == "int":
            input_int(prompt, error, ge, gt, le, lt)
            return
        elif type == "float":
            input_float(prompt, error, ge, gt, le, lt)
            return
        elif type == "str":
            input_string(prompt, error, valid)
            return
        elif type == "yes or no":
            y_or_n(prompt, error)
        elif type == "select":
            select_item(prompt, error, options, map)
            return
