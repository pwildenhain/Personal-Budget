# CLeanly dealing with user inputs
def ensure_positive_integer_from_user(prompt):
    while True:
        try:
            num_input = int(input(f'{prompt}: '))
        except ValueError:
            print('Numbers only please :-)')
            continue
        
        if num_input < 0:
            print('Positive numbers only please ;-)')
            continue
        else:
            break
    return num_input

def expect_yes_or_no_answer(question):
    """Ask user a yes or no question, return a boolean value"""
    yes_or_no = ''
    yn_bool_dict = {'yes' : True, 'no' : False}
    while yes_or_no not in ['yes', 'no']:
        yes_or_no = input(f'{question}?: ').lower()
        bool_yn = yn_bool_dict[yes_or_no]
    return bool_yn

def user_exit_program():
    raise SystemExit