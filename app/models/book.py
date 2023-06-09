# Class to model Book objects
class Book:
    def __init__(self, title, ISBN, author_lname, author_fname, library_location, status):
        self._title = title
        self._ISBN = ISBN
        self._author_lname = author_lname
        self._author_fname = author_fname
        self._library_location = library_location
        self._status = status

    @property
    def title(self):
       return self._title

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status

# Class to support reading/writing Book objects with the database
class BookDB:
    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._cursor = db_cursor

    def select_all_books(self):
        select_all_query = """
            SELECT * from books;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()    

    def select_book_by_id(self, book_id):
        select_book_by_id = """
                SELECT * from tasks WHERE id = %s;
        """
        self._cursor.execute(select_book_by_id, (book_id,))
        return self._cursor.fetchall()

    def update_book_status(self, book_id, new_status):
        update_query = """
            UPDATE books
            SET status=%s
            WHERE id=%s;
        """
        self._cursor.execute(update_query, (new_status, book_id))
        self._db_conn.commit()