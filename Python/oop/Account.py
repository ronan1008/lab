class AbortTransaction(Exception):
    pass


class Account():
    def __init__(self, name, balance, password):
        self.name = name
        self.balance = self.validateAmount(balance)
        self.password = password

    def validateAmount(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            raise AbortTransaction('Amount must be an integer')
        if amount <= 0:
            raise AbortTransaction('Amount must be positive')
        return amount

    def checkPasswordMatch(self, password):
        if password != self.password:
            raise AbortTransaction('Incorrect password for this account')


    def deposit(self, amountToDeposit):
        amountToDeposit = self.validateAmount(amountToDeposit)
        self.balance = self.balance + amountToDeposit
        return self.balance


    def withdraw(self, amountToWithdraw ):
        amountToWithdraw = self.validateAmount(amountToWithdraw)
        if amountToWithdraw > self.balance :
            raise AbortTransaction('You cannot withdraw more than you have in your account')
        self.balance = self.balance - amountToWithdraw
        return self.balance

    def getBalance(self):
        return self.balance

    def show(self):
        print('     Name:', self.name)
        print('     Balance:', self.balance)
        print('     Password:', self.password)
        print()

if __name__ == '__main__':
    accountsList = []
    oAccount = Account('Shock Lee', 1000, 'ShocksPassword')
    accountsList.append(oAccount)

    oAccount = Account('Mary', 12345, 'MarysPassword')
    accountsList.append(oAccount)

    accountsList[0].show()
    accountsList[1].show()

    accountsList[0].deposit(50, 'ShocksPassword')
    accountsList[1].deposit(1, 'MarysPassword')

    accountsList[0].show()
    accountsList[1].show()
