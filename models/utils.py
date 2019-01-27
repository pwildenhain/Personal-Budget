def ensure_positive_integer_from_user():
    while True:
        try:
            num_input = int(input('How much would you like to transfer: '))
        except ValueError:
            print('Numbers only please :-)')
            continue
        
        if num_input < 0:
            print('Positive numbers only please ;-)')
            continue
        else:
            break
    return num_input
