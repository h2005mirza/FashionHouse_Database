import sqlite3

# Connecting to the database
conn = sqlite3.connect('fashion_powerhouses.db')
cur = conn.cursor()

# Dropping tables if they already exist
cur.execute('DROP TABLE IF EXISTS PRODUCT')
cur.execute('DROP TABLE IF EXISTS COLLECTION')
cur.execute('DROP TABLE IF EXISTS CATEGORY')
cur.execute('DROP TABLE IF EXISTS DESIGNER')

# Creating the tables
cur.execute('''
    CREATE TABLE DESIGNER (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        country TEXT NOT NULL
    );
''')

cur.execute('''
    CREATE TABLE COLLECTION (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        year INTEGER NOT NULL,
        designer_id INTEGER,
        FOREIGN KEY(designer_id) REFERENCES DESIGNER(id)
    );
''')

cur.execute('''
    CREATE TABLE CATEGORY (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
''')

cur.execute('''
    CREATE TABLE PRODUCT (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        price REAL NOT NULL,
        collection_id INTEGER,
        category_id INTEGER,
        FOREIGN KEY(collection_id) REFERENCES COLLECTION(id),
        FOREIGN KEY(category_id) REFERENCES CATEGORY(id)
    );
''')

# Inserting data into DESIGNER
designers = [
    ('Louis Vuitton', 'France'),
    ('Chanel', 'France'),
    ('Prada', 'Italy'),
    ('Tommy Hilfiger', 'USA'),
    ('Ralph Lauren', 'USA'),
    ('Marc Jacobs', 'USA'),
    ('Yves Saint Laurent', 'France'),
    ('Burberry', 'United Kingdom'),
    ('Calvin Klein', 'USA'),
    ('Alexander McQueen', 'United Kingdom'),
    ('Tom Ford', 'USA'),
    ('Gucci', 'Italy'),
    ('Versace', 'Italy'),
    ('Balenciaga', 'Spain'),
    ('Dolce & Gabbana', 'Italy'),
    ('Hermes', 'Italy'),
    ('Fendi', 'Italy'),
    ('Givenchy', 'France'),
    ('Christian Dior', 'France'),
    ('Giorgio Armani', 'Italy'),
    ('Valentino', 'Italy'),
    ('Michael Kors', 'USA'),
    ('Vivienne Westwood', 'United Kingdom'),
    ('Jean Paul Gaultier', 'France')
]
for designer in designers:
    cur.execute('INSERT INTO DESIGNER (name, country) VALUES (?, ?)', designer)

# Inserting data into CATEGORY
categories = ['Bags', 'Outerwear', 'Dresses', 'Apparel', 'Suits', 'Knitwear', 'Perfumes', 'Footwear', 'Accessories']
for category in categories:
    cur.execute('INSERT INTO CATEGORY (name) VALUES (?)', (category,))

# Inserting data into COLLECTION
collections = [
    ('Spring/Summer 2024', 2024, 1),
    ('Fall/Winter 2023', 2023, 2),
    ('Couture 2023', 2023, 3),
    ('Rive Gauche 2022', 2022, 4),
    ('Heritage Collection', 2021, 5),
    ('Purple Label 2023', 2023, 6),
    ('Spring Collection', 2022, 7),
    ('Runway 2022', 2022, 8),
    ('Resort Collection', 2022, 9),
    ('Signature 2023', 2023, 10),
    ('Classic Revival', 2021, 11)
]
for collection in collections:
    cur.execute('INSERT INTO COLLECTION (name, year, designer_id) VALUES (?, ?, ?)', collection)

# Mapping CATEGORY names to IDs
cur.execute('SELECT id, name FROM CATEGORY')
category_map = {name: id for id, name in cur.fetchall()}

# Inserting data into PRODUCT
products = [
    ('Leather Handbag', 2500.00, 1, category_map['Bags']),
    ('Wool Coat', 1800.00, 2, category_map['Outerwear']),
    ('Silk Gown', 5000.00, 3, category_map['Dresses']),
    ('Logo T-Shirt', 700.00, 4, category_map['Apparel']),
    ('Trench Coat', 2200.00, 5, category_map['Outerwear']),
    ('Cashmere Sweater', 1500.00, 6, category_map['Knitwear']),
    ('Fragrance Set', 300.00, 8, category_map['Perfumes']),
    ('Sunglasses', 450.00, 11, category_map['Accessories']),
    ('Fur Coat', 6000.00, 13, category_map['Outerwear'])
]
for product in products:
    cur.execute('INSERT INTO PRODUCT (name, price, collection_id, category_id) VALUES (?, ?, ?, ?)', product)

# Retrieving and displaying combined data
print('!PRODUCTS IN GLOBAL FASHION POWERHOUSES!')
cur.execute('''
    SELECT PRODUCT.name, PRODUCT.price, COLLECTION.name AS collection, CATEGORY.name AS category, DESIGNER.name AS designer
    FROM PRODUCT
    JOIN COLLECTION ON PRODUCT.collection_id = COLLECTION.id
    JOIN CATEGORY ON PRODUCT.category_id = CATEGORY.id
    JOIN DESIGNER ON COLLECTION.designer_id = DESIGNER.id
''')

for row in cur.fetchall():
    print(f"Product: {row[0]}, Price: ${row[1]:,.2f}, Collection: {row[2]}, Category: {row[3]}, Designer: {row[4]}")

# Closing the connection
conn.commit()
conn.close()
