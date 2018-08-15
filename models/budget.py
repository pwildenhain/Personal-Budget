# Import modules
from datetime import datetime
# Define classes
class Account():
    """An account within a personal budget

    Attributes:
        name (str): Display name
        category (str): Budget category
        budgeted_amount (int): Bi-weekly allocated amount
        current_balance (int): Current surplus/shortage of allocated amount
        transaction_history (list(tuple)): Every transaction recorded on this account
    """

    def __init__(self, name, category, budgeted_amount, current_balance, transaction_history):
        self.name = name
        self.category = category
        self.budgeted_amount = budgeted_amount
        self.current_balance = current_balance
        self.transaction_history = transaction_history

    def update_budgeted_amount(self, new_budgeted_amount):
        """Update the current budgeted amount for the account"""
        try:
            if new_budgeted_amount > 0:
                self.budgeted_amount = new_budgeted_amount
            else:
                return print('Amount must be greater than zero')
        except TypeError:
            print('Amount must be a number')

    def update_current_balance(self, transaction_type, amount):
        """When a transaction is recorded, update the current balance left on the account"""
        if transaction_type == 'debit':
            self.current_balance -= amount
        elif transaction_type == 'credit':
            self.current_balance += amount

    def add_transaction(self, comment, transaction_type, amount):
        """Record a transaction on the account transaction history and update the current balance"""
        try:
            self.update_current_balance(transaction_type, amount)
        except TypeError:
            print('Amount must be a number')
        else:
            date = datetime.now().strftime('%Y-%m-%d')
            transaction = (date, self.name, comment, transaction_type, amount)
            self.transaction_history.append(transaction)
        
class Budget():
    """A bi-weekly personal budget

    Attributes:
        categories (list(str)): A list of categories that belong to one or more accounts
        accounts (dict(:obj:)): A dict of Account() objects
    """

    def __init__(self, accounts = {}, categories = []):
        self.accounts = accounts
        self.categories = categories

    def add_category(self, name):
        if name in self.categories:
            raise Exception('That category already exists')
        self.categories.append(name)

    def add_account(self, category, **kwargs):
        """Add an account to the existing budget accounts"""
        if kwargs['category'] not in self.categories:
            self.add_category(kwargs['category'])
        self.accounts[kwargs['name']] = Account(**kwargs)
 
    def transfer_money(self, origin, destination, amount):
        try:
            self.accounts[origin].add_transaction(f'Transfer to {destination}', 'debit', amount)
        except KeyError:
            print(f'{origin} is not an account in the budget')
        try:
            self.accounts[destination].add_transaction(f'Transfer from {origin}', 'credit', amount)
        except KeyError:
            print(f'{destination} is not an account in the budget')
  
    def display_summary(self):
        """Display the current balance compared to the budgeted amount for each account"""
        print('category: account: budgeted amount: current balance')
        for account in self.accounts:
            account_obj = self.accounts[account]
            category = account_obj.category
            budgeted_amount = account_obj.budgeted_amount
            balance = account_obj.current_balance
            name = account_obj.name.title()
            print(f'{category}: {name}: {budgeted_amount}: {balance}')   

