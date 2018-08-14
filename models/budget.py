from datetime import datetime

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

    def add_transaction(self, comment, type, amount):
        date = datetime.now().strftime('%Y-%m-%d')
        transaction = (date, self.name, comment, type, amount)
        return self.transaction_history.append(transaction)

