from Bank import *

oBank = Bank()
joesAccountNumber = oBank.createAccount('Joe', 100, 'joepassword')
print("joe's account number is :", joesAccountNumber)

marysAccountNumber = oBank.createAccount('Mary', 12345, 'marypassword')
print("mary's account number is :", marysAccountNumber)

while True:
    print()
    print('To get an account balance, press b')
    print('To close an account, press c')
    print('To make a deposit, press d')
    print('To get bank information, press 1')
    print('To open a new accounts, press o')
    print('To quit, press q')
    print('To show all accounts, press s')
    print('To make a withdraw, press w')
    print()

    action = input('What do you want to do?')
    action = action.lower()
    action = action[0]
    print()

    if action == 'b':
        oBank.balance()

    elif action == 'c':
        oBank.closeAccount()

    elif action == 'd':
        oBank.deposit()

    elif action == 'i':
        oBank.bankInfo()

    elif action == 'o':
        oBank.openAccount()

    elif action == 's':
        oBank.show()

    elif action == 'q':
        break

    elif action == 'w':
        oBank.withdraw()

    else:
        print('Sorry, that was not a valid action. Please try again.')

print('Done')