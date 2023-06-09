from datetime import date, timedelta

from app.models.book import Book
from app.models.customer import customer

#Class to model Transaction objects
class Transaction:
    def __init__(self, book_fk, customer_fk):
        self._book_fk = book_fk
        self._customer_fk = customer_fk
        self._check_out_date = date.today()
        self._return_date = date.today() + timedelta(days=14)

    @property
    def book_fk(self):
        return self._book_fk

    @property
    def customer_fk(self):
        return self._customer_fk

    @property
    def check_out_date(self):
        return self._check_out_date

    @property
    def return_date(self):
        return self._return_date

# Class to support reading/writing Transaction objects with the database
class TransactionDB:
    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor

    def select_all_transactions(self):
        select_all_query = """
            SELECT * from ledger;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()

    def select_all_transactions_by_customer(self, customer_fk):
        select_transactions_by_customer = """
            SELECT * from ledger WHERE customer_fk LIKE %s;
        """
        self._cursor.execute(select_transactions_by_customer, (f"%{customer_fk}%",))
        return self._cursor.fetchall()

    def select_transaction_by_id(self, transaction_id):
        select_transaction_by_id = """
                SELECT * from ledger WHERE transaction_id = %s;
        """
        self._cursor.execute(select_transaction_by_id, (transaction_id,))
        return self._cursor.fetchall()

    def insert_transaction(self, transaction):
        insert_query = """
            INSERT INTO ledger (book_fk, customer_fk)
            VALUES (%s, %s);
        """

        self._cursor.execute(insert_query, (transaction.book_fk, transaction.customer_fk))
        self._cursor.execute("SELECT LAST_INSERT_ID() transaction_id")
        transaction_id = self._cursor.fetchone()
        self._db_conn.commit()
        return transaction_id

    def delete_transaction_by_id(self, transaction_id):
        delete_query = """
            DELETE from ledger
            WHERE id=%s;
        """
        self._cursor.execute(delete_query, (transaction_id,))
        self._db_conn.commit()