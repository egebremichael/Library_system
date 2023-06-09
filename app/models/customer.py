class customer:
    def __init__(self, lname, fname):
        self._lname = lname
        self._fname = fname

    @property
    def lname(self):
        return self._lname

    @property
    def fname(self):
        return self._fname

# Class to support reading/writing Customer objects with the database
class CustomerDB:
    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor

    def select_all_customers(self):
        select_all_query = """
            SELECT * from customers;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()   

    def select_customer_by_id(self, customer_id):
        select_customer_by_id = """
                SELECT * from customers WHERE id = %s;
        """
        self._cursor.execute(select_customer_by_id, (customer_id,))
        return self._cursor.fetchall()
