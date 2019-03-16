# Import modules
from datetime import datetime
from sqlite3 import connect
from pandas import DataFrame, read_sql
from utils.user import ensure_positive_integer_from_user, expect_yes_or_no_answer
# Define classes
class Account():
    """An account within a personal budget

    Attributes:
        name (str): Display name
        category (str): Budget category
        budgeted_amount (int): Bi-weekly allocated amount
        current_balance (int): Current surplus/shortage of allocated amount
    """

    def __init__(self, name, category, budgeted_amount, current_balance):
        self.name = name
        self.category = category
        self.budgeted_amount = budgeted_amount
        self.current_balance = current_balance
    
    def update_budgeted_amount(self, new_budgeted_amount):
        """Update the current budgeted amount for the account"""
        self.budgeted_amount = new_budgeted_amount

        conn = connect('data/budget.db')
        cursor = conn.cursor() 
        cursor.execute('''UPDATE budget_summary SET budgeted_amount = ? WHERE name = ?''',
            (self.budgeted_amount, self.name)) 
        conn.commit()
        conn.close()

    def update_current_balance(self, transaction_type, amount):
        """When a transaction is recorded, update the current balance left on the account"""
        if transaction_type == 'debit':
            self.current_balance -= amount
        elif transaction_type == 'credit':
            self.current_balance += amount
        conn = connect('data/budget.db')
        cursor = conn.cursor() 
        cursor.execute('''UPDATE budget_summary SET current_balance = ? WHERE name = ?''',
            (self.current_balance, self.name)) 
        conn.commit()
        conn.close()

    def add_transaction(self, comment, transaction_type, amount):
        """Record a transaction on the account transaction history and update the current balance"""
        self.update_current_balance(transaction_type, amount)

        date = datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
        transaction = [(date, self.name, comment, transaction_type, amount)]
        labels = ['date', 'name', 'comment', 'transaction_type', 'amount']
        tx_df = DataFrame.from_records(transaction, columns=labels)
        
        conn = connect('data/budget.db')
        tx_df.to_sql("transaction_history", conn, if_exists='append', index=False)
        conn.close()
        
class Budget():
    """A bi-weekly personal budget

    Attributes:
        accounts (dict(:obj:)): A dict of Account() objects
    """

    def __init__(self, accounts = {}):
        self.accounts = accounts
      
    def display_summary(self):
        """Display the current balance compared to the budgeted amount for each account"""
        conn = connect('data/budget.db')
        display_df = read_sql('''
        SELECT 
        category as Category
        , name as Account
        , budgeted_amount as Budgeted
        , current_balance as Balance
        FROM 
        budget_summary 
        ORDER BY
        category, budgeted_amount DESC''',
        conn
        )
        conn.close()
        # Add line padding around DataFrame
        print()
        print(display_df)
        print()

    def display_accounts(self):
        return ", ".join(self.accounts.keys())
    
    def display_history(self, by_account="", transactions=10):
        """Display the last n transactions from the transaction_history table"""
        conn = connect('data/budget.db')
        # Add SQL logic for filtering by account only if requested
        if by_account != "":
            filter_account = '''and name in (?)'''
            params = [by_account, transactions]
        else:
            filter_account = ""
            params = [transactions]

        display_sql = f'''
        SELECT 
        date as Date
        , name as Account
        , transaction_type as Type
        , comment as Comment
        , amount as Amount
        FROM 
        transaction_history 
        WHERE
        comment != 'Payday'
        and
        comment NOT LIKE 'Transfer%'
        {filter_account}
        ORDER BY
        date DESC
        LIMIT
        ? '''

        display_df = read_sql(display_sql, conn, params = params)
        conn.close()
        # Add line padding around DataFrame
        print()
        print(display_df)
        print()

    def user_select_account(self):
        """Prompt user to select an account from list of current accounts"""
        account = ''
        while account not in self.accounts.keys():
            print(self.display_accounts())
            account = input('Choose one of the above accounts: ')
        return account
    
    def user_add_transaction(self):
        """Allow user to add a new transaction"""
        account = self.user_select_account()
        amount = ensure_positive_integer_from_user('Transaction amount')
        comment = input('Transaction comment: ')
        self.accounts[account].add_transaction(comment, 'debit', amount)
        self.display_summary()

    def add_account(self, **kwargs):
        """Add an account to the existing budget accounts"""
        new_account = kwargs['name']
        self.accounts[new_account] = Account(**kwargs)
        new_account_obj = self.accounts[new_account]
        insert_account = [( 
            new_account_obj.category,
            new_account_obj.name,
            new_account_obj.budgeted_amount,
            new_account_obj.current_balance
            )]
        labels = ['category', 'name', 'budgeted_amount', 'current_balance']
        insert_df = DataFrame.from_records(insert_account, columns=labels)
        conn = connect('data/budget.db')
        insert_df.to_sql("budget_summary", conn, if_exists='append', index=False)
        conn.close()
    
    def user_add_account(self):
        """Allow user to add account to budget """
        name = input("Name of this account: ")
        category = input(f"What category does {name} fall under?: ")
        budgeted_amount = ensure_positive_integer_from_user('Budgeted amount')
        self.add_account(
            name = name, category = category,
            budgeted_amount = budgeted_amount,
            current_balance = budgeted_amount)
        self.display_summary()

    def user_update_budgeted_amount(self):
        """Allow user to update budgeted amounts"""
        account = self.user_select_account()
        current_budgeted_amount = self.accounts[account].budgeted_amount
        print(f'The current budgeted amount for {account} is {current_budgeted_amount}')
        new_budgeted_amount = ensure_positive_integer_from_user('New budgeted amount')
        self.accounts[account].update_budgeted_amount(new_budgeted_amount)
        self.display_summary()

    def transfer_between_accounts(self, origin, destination, amount):
        """Transfer a part of the balance from one account to another"""
        self.accounts[origin].add_transaction(f'Transfer to {destination}', 'debit', amount)
        self.accounts[destination].add_transaction(f'Transfer from {origin}', 'credit', amount)

    def user_transfer_between_accounts(self):
        """Allow user to transfer between accounts"""
        transfer_amount = ensure_positive_integer_from_user('Transfer amount')
        print('Transfer from:')
        from_account = self.user_select_account()
        print('Transfer to:')
        to_account = self.user_select_account()
        self.transfer_between_accounts(from_account, to_account, transfer_amount)
        self.display_summary()

    def user_add_income_to_account(self):
        account = self.user_select_account()
        amount = ensure_positive_integer_from_user('Income amount')
        comment = input('Income comment: ')
        self.accounts[account].add_transaction(comment, 'credit', amount)
        self.display_summary()

    def record_payday(self):
        """Add the budgeted amount to each account's current balance"""
        for account in self.accounts:
            account_obj = self.accounts[account]
            account_obj.add_transaction('Payday', 'credit', account_obj.budgeted_amount)

    def user_record_payday(self):
        """Allow user to record a payday"""
        user_is_sure = expect_yes_or_no_answer('Are you sure you want to record a payday')
        if user_is_sure:
            print('$$$ *Cha-Ching* $$$')
            self.record_payday()
            self.display_summary()
    
    def delete_account(self, account):
        conn = connect('data/budget.db')
        cursor = conn.cursor() 
        cursor.execute('''DELETE FROM budget_summary WHERE name = ?''',
            (account,)) 
        conn.commit()
        conn.close()

    def user_delete_account(self):
        account = self.user_select_account()
        user_is_sure = expect_yes_or_no_answer(f'Are you sure you want to delete {account}')
        if user_is_sure:
            budgeted_amount = self.accounts[account].budgeted_amount
            current_balance = self.accounts[account].current_balance
            print(f'{account} had ${budgeted_amount} budgeted and ${current_balance} in the balance')
            self.delete_account(account)
            self.display_summary()

    def user_view_transaction_history(self):
        """Allow user to view transaction history"""
        transactions = ensure_positive_integer_from_user('Number of transactions')
        account = self.user_select_account()
        self.display_history(account, transactions)
