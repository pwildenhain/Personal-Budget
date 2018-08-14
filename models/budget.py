# Import modules
from datetime import datetime
# Define classes
class Account():
    """An account within a personal budget with the following properties:

    Attributes:
        name:
        category:
        budgeted_amount:
        current_balance:
        transaction_history:
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
            self.current_balance += -amount
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
        
        

