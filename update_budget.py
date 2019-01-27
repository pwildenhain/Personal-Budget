# Imports
from models.budget import Account, Budget
from sqlite3 import connect
from pandas import DataFrame, read_sql
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
    Budget.user_exit_program
]

user_action_names = []
for action in user_actions:
    display_name = action.__name__.replace('user_', '').replace('_', ' ').title()
    user_action_names.append(display_name)

while True:
    for num, action in enumerate(user_action_names):
        print(f'{num}) {action}')

    choice = Budget.ensure_positive_integer_from_user('Select an option')

    if choice in range(len(user_action_names)):
        chosen_func = user_actions[choice]
        chosen_func()
    else:
        continue




        

    