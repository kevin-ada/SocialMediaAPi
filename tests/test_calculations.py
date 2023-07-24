import pytest
from calculations import div,sub, BankAccount,add


@pytest.fixture()
def bank_account():
    print("getting the price")
    return BankAccount(balance=5000)

@pytest.mark.parametrize("x, y, result",[
                         (10, 10, 20),
                         (-1, -1, -2),
                         (0, 0, 0),
                         (-3, -3, -6)
                         ])
def test_add(x:int, y:int, result):
    print("testing add function")
    assert add(x, y) == result


@pytest.mark.parametrize(
    "x, y, result",
    [
        (20, 10, 10),
        (10, 5, 5),
        (-1, 4, -5)
    ],
)
def test_sub(x, y, result):
    assert sub(x, y) == result

def test_bank_account(bank_account) :
    assert bank_account.balance == 5000

def test_deposit(bank_account):
    bank_account.deposit(depo=4000)
    assert bank_account.balance == 9000

def test_withdraw(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(4000)
        assert bank_account.balance == 1000

def test_interest_attained(bank_account):
    bank_account.interest_attained()
    assert bank_account.balance == 6500


