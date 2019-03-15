# Imports
from models.budget import Account, Budget
from sqlite3 import connect, OperationalError
from os import path, makedirs
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
    

