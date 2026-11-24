'''
This python script connects to the postgres container.
Populates the database with random data from the script!
'''
# imports
import random
import psycopg

# Connects to the database
connection_string = "dbname=test_db user=postgres password=password host=localhost port=5432"

# Create lists to random inject data to db
categories = ["Electronics", "Office Supplies", "Furniture", "Tools", "Packaging"]
adjectives = ["Pro", "Compact", "Heavy-Duty", "Wireless", "Standard", "Eco"]
nouns = ["Widget", "Scanner", "Keyboard", "Chair", "Drill", "Box", "Monitor", "Lamp"]
items = []

# Iterate 100 times and adds the random choices to items
for i in range(1, 101):
    sku = f"INV-{i:04d}"
    name = f"{random.choice(adjectives)} {random.choice(nouns)} #{i}"
    category = random.choice(categories)
    quantity = random.randint(0, 250)
    price = round(random.uniform(4.99, 499.99), 2)
    items.append((sku, name, category, quantity, price))


# Create the table if it does not exists
create_table_sql = """
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0)
);
"""

# creating a variable to store the insert statement
insert_sql = """
INSERT INTO inventory (sku, name, category, quantity, price)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (sku) DO NOTHING;
"""

# executes the creation and the data into db
with psycopg.connect(connection_string) as conn:
    with conn.cursor() as cur:
        cur.execute(create_table_sql)
        cur.executemany(insert_sql, items)


        # Shows the number of rows and shows the data in db
        cur.execute("SELECT COUNT(*) FROM inventory;")
        total_rows = cur.fetchone()[0]
        print(f"Total rows in inventory: {total_rows}")

        cur.execute("SELECT id, sku, name, category, quantity, price FROM inventory")
        for row in cur.fetchall():
            print(row)