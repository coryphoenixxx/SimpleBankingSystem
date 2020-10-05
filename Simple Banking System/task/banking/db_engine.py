import sqlite3

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS card (" \
               "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
               "number TEXT, " \
               "pin TEXT, " \
               "balance INTEGER);"

INSERT_CARD = "INSERT INTO card(number, pin, balance) VALUES (?, ?, ?);"
GET_CARD_BY_NUMBER = "SELECT * FROM card WHERE number = ?;"
GET_CARD_BY_ID = "SELECT * FROM card WHERE id = ?;"
ADD_INCOME = "UPDATE card SET balance = ? WHERE id = ?;"
DELETE_CARD = "DELETE FROM card WHERE id = ?;"
GET_CARDS = "SELECT * FROM card;"


def connect():
    return sqlite3.connect('card.s3db')


def create_table(connection):
    with connection:
        connection.execute(CREATE_TABLE)
        connection.commit()


def add_card(connection, card):
    with connection:
        connection.execute(INSERT_CARD, (card.number, card.PIN, 0))
        connection.commit()


def get_card_by_number(connection, number):
    with connection:
        result = connection.execute(GET_CARD_BY_NUMBER, (number,)).fetchall()
        connection.commit()
        return result


def get_card_by_id(connection, id):
    with connection:
        result = connection.execute(GET_CARD_BY_ID, (id,)).fetchall()
        connection.commit()
        return result


def add_income(connection, id, income):
    with connection:
        result = connection.execute(ADD_INCOME, (income, id))
        connection.commit()
        return result


def delete_card(connection, id):
    with connection:
        result = connection.execute(DELETE_CARD, (id,))
        connection.commit()
        return result


def ger_all_cards(connection):
    with connection:
        result = connection.execute(GET_CARDS).fetchall()
        connection.commit()
        return result
