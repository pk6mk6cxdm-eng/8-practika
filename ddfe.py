import sqlite3
import pandas as pd

conn = sqlite3.connect("bookstore.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Authors(
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Books(
    id INTEGER PRIMARY KEY,
    title TEXT,
    author_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers(
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders(
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS OrderDetails(
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    book_id INTEGER,
    quantity INTEGER
)
""")

authors = [
    ("Mukhtar Auezov",),
    ("Abai Kunanbayev",),
    ("Shakarim Qudaiberdiuly",),
    ("Oralxan Bokeihan",)
]
cursor.executemany("INSERT INTO Authors(name) VALUES (?)", authors)

books = [
    ("Abai Zholy",1),
    ("Kara Sozder",2),
    ("Qan men Ter",3),
    ("Aqyl men Bilim",4)
]
cursor.executemany("INSERT INTO Books(title, author_id) VALUES (?,?)", books)

customers = [
    ("Nuraiym",),
    ("Aruzhan",),
    ("Dias",),
    ("Ayazhan",)
]
cursor.executemany("INSERT INTO Customers(name) VALUES (?)", customers)

orders = [
    (1,"2024-01-10"),
    (2,"2024-01-12"),
    (3,"2025-03-25"),
    (4,"2025-02-18")
]
cursor.executemany("INSERT INTO Orders(customer_id, order_date) VALUES (?,?)", orders)

order_details = [
    (1,1,2),
    (2,2,1),
    (3,3,1),
    (4,4,3)
]
cursor.executemany(
    "INSERT INTO OrderDetails(order_id, book_id, quantity) VALUES (?,?,?)",
    order_details
)

conn.commit()

cursor.execute("""
SELECT Books.title
FROM Books
JOIN Authors ON Books.author_id = Authors.id
WHERE Authors.name = 'Mukhtar Auezov'
""")
print("Автордың кітаптары:")
for b in cursor.fetchall():
    print(b[0])

cursor.execute("""
SELECT Customers.name, Books.title, OrderDetails.quantity
FROM Customers
JOIN Orders ON Customers.id = Orders.customer_id
JOIN OrderDetails ON Orders.id = OrderDetails.order_id
JOIN Books ON Books.id = OrderDetails.book_id
JOIN Authors ON Books.author_id = Authors.id
WHERE Authors.name = 'Mukhtar Auezov'
""")
print("Бұл кітаптарды сатып алған клиенттер:")
for c in cursor.fetchall():
    print(c)

cursor.execute("""
DELETE FROM OrderDetails
WHERE quantity = 0
""")
conn.commit()

query = """
SELECT 
    Customers.name AS Customer,
    Books.title AS Book,
    Authors.name AS Author,
    Orders.order_date AS OrderDate,
    OrderDetails.quantity AS Quantity
FROM Customers
JOIN Orders ON Customers.id = Orders.customer_id
JOIN OrderDetails ON Orders.id = OrderDetails.order_id
JOIN Books ON Books.id = OrderDetails.book_id
JOIN Authors ON Books.author_id = Authors.id
ORDER BY Customers.name
"""
df = pd.read_sql_query(query, conn)


df.to_excel("report.xlsx", index=False)
print("Нәтиже report.xlsx файлына сақталды")

conn.close()