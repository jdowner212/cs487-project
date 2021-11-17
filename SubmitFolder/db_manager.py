"""DB transactions module"""
import sqlite3

# import my_config

class appDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        # perm ADMIN(manager)-2, Employee-1, customer-0
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Customers(
        id_customer   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        email         TEXT    NOT NULL,
        password      TEXT    NOT NULL,
        full_name     TEXT    NOT NULL,
        phone         TEXT    DEFAULT (0) NOT NULL,
        perm          INT     NOT NULL DEFAULT (0)
        )""")
        self.conn.commit()

    def add_user_db(self, email, password, full_name, phone):
        self.cur.execute("""
        INSERT INTO Customers
        (email, password, full_name, phone)
        VALUES (?, ?, ?, ?)
        """, (email, password, full_name, phone)
        )
        self.conn.commit()

    def is_customer_exists(self, email):
        # 0 = user email exist in our db
        # 1 = user email does not exist our db
        self.cur.execute("SELECT exists(SELECT 1 FROM Customers WHERE email=?)", (email,))
        if self.cur.fetchone()[0] == 1:
            return 0
        else:
            return 1

    def get_all_customers(self):
        self.cur.execute("SELECT * FROM Customers")
        rows = self.cur.fetchall()
        return rows

    def get_user_perm(self, email, password):
        # if login success returns user id and user perm
        self.cur.execute("""
        SELECT id_customer, perm
        FROM Customers
        WHERE email=? and password=?
        """, (email, password)
        )
        found = self.cur.fetchone()
        if found is None:
            return False, -1
        else:
            return found[0], found[1]

