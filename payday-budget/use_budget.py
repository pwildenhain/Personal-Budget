# Imports
from models.budget import Account, Budget
from utils.user import ensure_positive_integer_from_user, user_exit_program
from sqlite3 import connect, OperationalError
from pandas import DataFrame, read_sql
from os import path, makedirs

def create_budget():
    # Check for existing budget
    if not path.exists('data'):
        makedirs('data')
    conn = connect('data/budget.db')
    cursor = conn.cursor()
    # If a table already exists, take note and ask if they want to overwrite
    try:
        cursor.execute('SELECT * FROM budget_summary')
    except OperationalError:
        budget_already_exists = False
    else:
        budget_already_exists = True

    if budget_already_exists:
        print("Looks like a budget already exists")
        overwrite_existing = ''
        while overwrite_existing not in ['yes', 'no']:
            overwrite_existing = input(
                'Would you like to overwrite the existing budget? Type yes or no: '
            ).lower() 
        if overwrite_existing == 'no':
            conn.close()
            raise SystemExit
    # Initialize tables
    cursor.execute('''
    DROP TABLE IF EXISTS budget_summary 
    ''')
    cursor.execute('''
    CREATE TABLE budget_summary (
    category text
    , name text
    , budgeted_amount integer
    , current_balance integer
    )
    ''')
    cursor.execute('''
    DROP TABLE IF EXISTS transaction_history
    ''')
    cursor.execute('''
    CREATE TABLE transaction_history (
    date real
    , name text
    , transaction_type text
    , comment tex
    , amount integer
    )
    ''')
    conn.commit()
    conn.close()
    # Initialize budget
    budget = Budget()
    print("Let's add some accounts to your personal budget")
    # Add accounts
    while True:
        name = input("Name of this account: ")
        category = input(f"What category does {name} fall under?: ")
        while True:
            try:
                budgeted_amount = int(input(f"How much would you like to budget for {name}: "))
            except ValueError:
                print('Budgeted amount must be an integer')
                continue
            else:
                break
        budget.add_account(name = name, category = category, budgeted_amount = budgeted_amount,
        current_balance = budgeted_amount)
        # Ask for another
        add_another = ''
        while add_another not in ['yes', 'no']:
            add_another = input('Would you like to add another account? Type yes or no: ').lower()
        if add_another == 'yes':
            continue
        else:
            break
    
def update_budget():
    # Load data from SQLite budget_summary table
    conn = connect('data/budget.db')
    accounts = read_sql('SELECT * FROM budget_summary', conn)
    conn.close()
    accounts_dict = dict()
    for account in accounts.itertuples():
        insert_account = Account(
            account.name, account.category,
            account.budgeted_amount, account.current_balance)
        accounts_dict[account.name] = insert_account
    budget = Budget(accounts_dict)
    # Display summary and history before asking for actions
    budget.display_history()
    budget.display_summary()
    # Different actions to update the budget
    user_actions = [
        budget.user_add_transaction,
        budget.user_add_account,
        budget.user_update_budgeted_amount,
        budget.user_transfer_between_accounts,
        budget.user_add_income_to_account,
        budget.user_record_payday,
        budget.user_view_transaction_history,
        budget.user_delete_account,
        user_exit_program
    ]

    user_action_names = []
    for action in user_actions:
        display_name = action.__name__.replace('user_', '').replace('_', ' ').title()
        user_action_names.append(display_name)

    while True:
        for num, action in enumerate(user_action_names):
            print(f'{num}) {action}')

        choice = ensure_positive_integer_from_user('Select an option')

        if choice in range(len(user_action_names)):
            chosen_func = user_actions[choice]
            chosen_func()
        else:
            continue
  