def add(x:int, y:int):
    return x+y

def sub(x:int, y:int):
    return x - y

def mul(x:int, y:int):
    return x * y

def div(x:int, y:int):
    if y == 0:
        raise ZeroDivisionError("Stupid Why Do would you do that")
    return x / y


class insufficient_Funds(Exception):
    pass

class BankAccount():
    interest = 1.05

    def __init__(self, balance:int) -> int:
        self.balance:int = balance

    def deposit(self, depo:int) -> int:
         self.balance = self.balance + depo

    def withdraw(self, amount:int) -> int:
        if amount > self.balance:
            raise insufficient_Funds("You are Broke!! Get Some Money")
        self.balance = self.balance - amount

    def interest_attained(self) -> int:
        self.balance =  self.balance * self.interest


balance = BankAccount(balance=6000)

balance.interest_attained()

print(balance.balance)

