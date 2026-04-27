import sqlite3

def get_db(db_path="store.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path="store.db"):
    conn = get_db(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS aisles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aisle_number TEXT NOT NULL UNIQUE,
            section_name TEXT NOT NULL,
            description TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            aisle_id INTEGER NOT NULL,
            shelf TEXT,
            description TEXT,
            FOREIGN KEY (aisle_id) REFERENCES aisles(id)
        );
    """)

    aisles = [
        ("A1", "Fresh Produce", "Fruits, vegetables, and organic items"),
        ("A2", "Dairy & Eggs", "Milk, cheese, butter, and eggs"),
        ("A3", "Bakery", "Bread, cakes, and baked goods"),
        ("B1", "Beverages", "Juices, sodas, water, and energy drinks"),
        ("B2", "Snacks & Chips", "Biscuits, chips, and namkeen"),
        ("B3", "Breakfast & Cereals", "Oats, cornflakes, and breakfast items"),
        ("C1", "Personal Care", "Shampoo, soap, toothpaste, and skincare"),
        ("C2", "Household Cleaning", "Detergents, cleaners, and mops"),
        ("C3", "Baby Products", "Diapers, baby food, and care items"),
        ("D1", "Rice, Dal & Grains", "All grains, pulses, and flours"),
        ("D2", "Spices & Masala", "All Indian spices and ready masalas"),
        ("D3", "Oils & Ghee", "Cooking oils, ghee, and vanaspati"),
        ("E1", "Frozen Foods", "Ice cream, frozen snacks, and ready meals"),
        ("E2", "Meat & Seafood", "Fresh and frozen meat, fish, and eggs"),
        ("F1", "Stationery", "Pens, notebooks, and office supplies"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO aisles (aisle_number, section_name, description) VALUES (?, ?, ?)",
        aisles
    )

    products = [
        ("Apple", "Fresh Produce", 1, "Top Shelf", "Fresh red and green apples"),
        ("Banana", "Fresh Produce", 1, "Bottom Shelf", "Ripe yellow bananas"),
        ("Tomato", "Fresh Produce", 1, "Middle Shelf", "Fresh tomatoes"),
        ("Spinach", "Fresh Produce", 1, "Middle Shelf", "Fresh green spinach"),
        ("Milk", "Dairy", 2, "Top Shelf", "Full cream and toned milk"),
        ("Curd", "Dairy", 2, "Middle Shelf", "Fresh set curd / yogurt"),
        ("Paneer", "Dairy", 2, "Middle Shelf", "Fresh cottage cheese"),
        ("Butter", "Dairy", 2, "Top Shelf", "Amul and other branded butter"),
        ("Bread", "Bakery", 3, "Middle Shelf", "Whole wheat and white bread"),
        ("Cake", "Bakery", 3, "Top Shelf", "Birthday and celebration cakes"),
        ("Coca Cola", "Beverages", 4, "Bottom Shelf", "Soft drinks and sodas"),
        ("Orange Juice", "Beverages", 4, "Top Shelf", "Fresh and packaged juices"),
        ("Water Bottle", "Beverages", 4, "Bottom Shelf", "Packaged drinking water"),
        ("Lays Chips", "Snacks", 5, "Top Shelf", "Potato chips and wafers"),
        ("Biscuits", "Snacks", 5, "Middle Shelf", "Marie, Parle-G and cream biscuits"),
        ("Cornflakes", "Breakfast", 6, "Top Shelf", "Kellogg's and other cereals"),
        ("Oats", "Breakfast", 6, "Middle Shelf", "Quaker and instant oats"),
        ("Shampoo", "Personal Care", 7, "Top Shelf", "Head & Shoulders, Dove, etc."),
        ("Soap", "Personal Care", 7, "Middle Shelf", "Bathing soaps and body wash"),
        ("Toothpaste", "Personal Care", 7, "Bottom Shelf", "Colgate, Pepsodent, etc."),
        ("Detergent", "Cleaning", 8, "Bottom Shelf", "Surf Excel, Ariel, etc."),
        ("Floor Cleaner", "Cleaning", 8, "Bottom Shelf", "Phenyl and floor cleaners"),
        ("Diapers", "Baby", 9, "Top Shelf", "Pampers and Huggies diapers"),
        ("Baby Food", "Baby", 9, "Middle Shelf", "Cerelac and baby purees"),
        ("Basmati Rice", "Grains", 10, "Bottom Shelf", "Premium basmati and raw rice"),
        ("Toor Dal", "Grains", 10, "Middle Shelf", "All types of dal and pulses"),
        ("Atta", "Grains", 10, "Bottom Shelf", "Wheat flour and multigrain atta"),
        ("Turmeric", "Spices", 11, "Top Shelf", "Haldi and other spice powders"),
        ("Garam Masala", "Spices", 11, "Middle Shelf", "Mixed and ready masalas"),
        ("Sunflower Oil", "Oils", 12, "Bottom Shelf", "Refined and cold-pressed oils"),
        ("Ghee", "Oils", 12, "Top Shelf", "Amul, Patanjali and branded ghee"),
        ("Ice Cream", "Frozen", 13, "Freezer", "Kwality Walls, Amul ice creams"),
        ("Frozen Peas", "Frozen", 13, "Freezer", "McCain and other frozen veggies"),
        ("Chicken", "Meat", 14, "Freezer", "Fresh and frozen chicken cuts"),
        ("Notebook", "Stationery", 15, "Top Shelf", "Ruled and blank notebooks"),
        ("Pen", "Stationery", 15, "Middle Shelf", "Ball pens and gel pens"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO products (name, category, aisle_id, shelf, description) VALUES (?, ?, ?, ?, ?)",
        products
    )

    conn.commit()
    conn.close()
    print("Database initialized with sample data!")

if __name__ == "__main__":
    init_db()