import random
import db_engine as db


TERMINATION = False


def luhn():
    temp_number = list('400000' + ''.join(map(str, random.sample(range(10), 9))))
    temp = list(map(int, temp_number))
    temp = [temp[i]*2 if i % 2 == 0 else temp[i] for i in range(len(temp))]
    temp = [d-9 if d > 9 else d for d in temp]
    temp_number.append(str(10 - sum(temp) % 10)[-1])
    number = ''.join(map(str, temp_number))
    return number


def is_luhn(number):
    last_number = int(number[-1])
    temp_number = number[:-1]
    temp = list(map(int, temp_number))
    temp = [temp[i]*2 if i % 2 == 0 else temp[i] for i in range(len(temp))]
    temp = [d-9 if d > 9 else d for d in temp]
    s = sum(temp) + last_number
    if s % 10 == 0:
        return True
    else:
        return False


def transfer(connection, id):
    print("\nTransfer")
    transfer_card_number = input("Enter card number:\n")
    transfer_card = db.get_card_by_number(connection, transfer_card_number)
    if not is_luhn(transfer_card_number):
        print("Probably you made a mistake in the card number. Please try again!\n")
    elif not transfer_card:
        print("Such a card does not exist.\n")
    elif id == transfer_card[0][0]:
        print("You can't transfer money to the same account!\n")
    else:
        transfer_money = int(input("Enter how much money you want to transfer:\n"))
        balance = db.get_card_by_id(connection, id)[0][3]
        if balance - transfer_money < 0:
            print("Not enough money!\n")
        else:
            new_balance = balance - transfer_money
            db.add_income(connection, id, new_balance)
            transfer_id = transfer_card[0][0]
            db.add_income(connection, transfer_id, transfer_card[0][3] + transfer_money)
            print("Success!\n")


def card_operations(connection, id):
    while True:
        # print(db.ger_all_cards(connection))
        choice = int(input("1. Balance\n"
                           "2. Add income\n"
                           "3. Do transfer\n"
                           "4. Close account\n"
                           "5. Log out\n"
                           "0. Exit\n"))
        if choice == 0:
            global TERMINATION
            TERMINATION = True
            break
        if choice == 1:
            print(f"\nBalance: {db.get_card_by_id(connection, id)[0][3]}\n")
        if choice == 2:
            income = int(input("\nEnter income:\n"))
            balance = db.get_card_by_id(connection, id)[0][3]
            db.add_income(connection, id, income+balance)
            print("Income was added!\n")
        if choice == 3:
            transfer(connection, id)
        if choice == 4:
            db.delete_card(connection, id)
            print("The account has been closed!")
            break
        if choice == 5:
            print("\nYou have successfully logged out!\n")
            break


def validation(connection):
    user_card_number_input = input("\nEnter your card number:\n")
    user_PIN_input = input("Enter your PIN:\n")
    db_response = db.get_card_by_number(connection, user_card_number_input)
    if db_response and db_response[0][2] == user_PIN_input:
        print("\nYou have successfully logged in!\n")
        card_operations(connection, db_response[0][0])
    else:
        print("\nWrong card number or PIN!\n")


class Card:
    def __init__(self):
        self.number = luhn()
        self.PIN = ''.join(map(str, random.sample(range(10), 4)))
        self.balance = 0
        print("\nYour card has been created\n"
              f"Your card number:\n{self.number}")
        print(f"Your card PIN:\n{self.PIN}\n")


if __name__ == "__main__":
    conn = db.connect()
    db.create_table(conn)

    while True:
        if TERMINATION:
            print("\nBye!")
            break

        choice = int(input("1. Create an account\n"
                           "2. Log into account\n"
                           "0. Exit\n"))
        if choice == 0:
            print("\nBye!")
            break
        if choice == 1:
            card = Card()
            db.add_card(conn, card)
        if choice == 2:
            validation(conn)
