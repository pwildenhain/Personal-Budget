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
# Display summary before asking for actions
budget.display_summary()
# Different actions to update the budget
while True:
    print('What would you like to do?')
    print('a) Add a transaction')
    print('b) Add an account')
    print('c) Update account budgeted amount')
    print('d) Tranfer between accounts')
    print('e) Add income to an account')
    print('f) Record a payday')
    print('g) View transaction history')
    print('h) Exit the program')
    action = input('Type a, b, c, d, e, f, g or h: ').lower()
    if action == 'a':
        account = ''
        while account not in budget.accounts.keys():
            print(budget.display_accounts())
            account = input('Choose one of the above accounts: ')
        while True:
            try:
                amount = int(input('Transaction amount: '))
            except ValueError:
                print('Transaction amount must be an integer')
                continue
            else:
                break
        comment = input('Transaction comment: ')
        budget.accounts[account].add_transaction(comment, 'debit', amount)
        budget.display_summary()
        continue
    if action == 'b':
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
        budget.add_account(
            name = name, category = category,
            budgeted_amount = budgeted_amount,
            current_balance = budgeted_amount)
        budget.display_summary()
        continue
    if action == 'c':
        account = ''
        while account not in budget.accounts.keys():
            print(budget.display_accounts())
            account = input('Choose one of the above accounts: ')
        current_budgeted_amount = budget.accounts[account].budgeted_amount
        print(f'The current budgeted amount for {account} is {current_budgeted_amount}')
        while True:
            try:
                new_budgeted_amount = int(input('Enter the new budgeted amount: '))
            except ValueError:
                print('New budgeted amount must be an integer')
                continue
            else:
                budget.accounts[account].update_budgeted_amount(new_budgeted_amount)
                update_comment = 'Update budgeted amount'
                if new_budgeted_amount > current_budgeted_amount:
                    budget.accounts[account].add_transaction(
                        comment = update_comment,
                        transaction_type = 'credit',
                        amount = new_budgeted_amount - current_budgeted_amount
                    )
                elif current_budgeted_amount > new_budgeted_amount:
                    budget.accounts[account].add_transaction(
                        comment = update_comment,
                        transaction_type = 'debit',
                        amount = current_budgeted_amount - new_budgeted_amount
                    )
                else:
                    print("You silly goose, those are the same numbers")
                    continue
                budget.display_summary()
                break
        continue
    if action == 'd':
        while True:
            try:
                transfer_amount = int(input('How much would you like to transfer: '))
                break
            except ValueError:
                print('Numbers only please :-)')
                continue
            print()
        from_account = ''
        while from_account not in budget.accounts.keys():
            print(budget.display_accounts())
            from_account = input(f'Choose one of the above accounts to transfer ${transfer_amount} from: ')
        to_account = ''
        while to_account not in budget.accounts.keys():
            print(budget.display_accounts())
            to_account = input(f'Choose one of the above accounts to transfer ${transfer_amount} to: ')
        budget.transfer_money(from_account, to_account, transfer_amount)
        budget.display_summary()
    if action == 'e':
        account = ''
        while account not in budget.accounts.keys():
            print(budget.display_accounts())
            account = input('Choose one of the above accounts: ')
        while True:
            try:
                amount = int(input('Income amount: '))
            except ValueError:
                print('Income amount must be an integer')
                continue
            else:
                break
        comment = input('Income comment: ')
        budget.accounts[account].add_transaction(comment, 'credit', amount)
        budget.display_summary()
    if action == 'f':
        confirm = ''
        while confirm not in ['yes', 'no']:
            confirm = input(
                'Are you sure you want to record a payday? Type yes or no: '
            ).lower()
        if confirm == 'yes':
            print('$$$ *Cha-Ching* $$$')
            budget.payday()
            budget.display_summary()
            continue
        elif confirm == 'no':
            continue
    if action == 'g':
        while True:
            try:
                transactions = int(input('Number of transactions to view: '))
            except ValueError:
                print('Number of transactions must be an integer')
                continue
            else:
                break
        account = ''
        while account not in budget.accounts.keys():
            print(budget.display_accounts())
            account = input('Choose one of the above accounts: ')
        budget.display_history(account, transactions)
    if action == 'h':
        raise SystemExit
    else:
        continue



        

    