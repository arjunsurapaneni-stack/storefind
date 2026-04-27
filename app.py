from flask import *
import sqlite3
from database import init_db
import os

# Initialize database when app starts
os.makedirs("instance", exist_ok=True)
init_db()
app=Flask(__name__)
app.secret_key = "store_admin_secret_2024"  # Change this in production!

@app.route('/')
def index():
    return render_template('index.html')





@app.route("/search")
def search():
    import os
    print("Looking for db at:", os.getcwd())
    query = request.args.get("q", "").strip()
    print("Searching for:", query)
    if not query:
        return redirect("/")

    with sqlite3.connect("store.db") as conn:
        conn.row_factory = sqlite3.Row
        results = conn.execute("""
            SELECT p.*, a.aisle_number, a.section_name
            FROM products p JOIN aisles a ON p.aisle_id = a.id
            WHERE p.name LIKE ? OR p.category LIKE ?
        """, (f"%{query}%", f"%{query}%")).fetchall()

    print(len(results), "results found")
    for r in results:
        print(dict(r))

    return render_template("results.html", query=query, results=results)



@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "admin123":
            return redirect("/admin")
        else:
            return render_template("admin_login.html", error="Wrong password! Try again.")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("index"))


# @app.route("/admin")
# def admin_dashboard():
#     conn = sqlite3.connect("store.db")
#     conn.row_factory = sqlite3.Row
#     products = conn.execute("""
#         SELECT p.*, a.aisle_number, a.section_name
#         FROM products p JOIN aisles a ON p.aisle_id = a.id
#     """).fetchall()
#     aisles = conn.execute("SELECT * FROM aisles").fetchall()
#     product_count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
#     aisle_count = conn.execute("SELECT COUNT(*) FROM aisles").fetchone()[0]
#     conn.close()
#     return render_template("admin.html", products=products, aisles=aisles,product_count=product_count,
#         aisle_count=aisle_count)

@app.route("/admin")
def admin_dashboard():
    with sqlite3.connect("store.db") as conn:
        conn.row_factory = sqlite3.Row
        products = conn.execute("""
            SELECT p.*, a.aisle_number, a.section_name
            FROM products p JOIN aisles a ON p.aisle_id = a.id
        """).fetchall()
        aisles = conn.execute("SELECT * FROM aisles").fetchall()
        product_count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        aisle_count = conn.execute("SELECT COUNT(*) FROM aisles").fetchone()[0]

    return render_template("admin.html",
        products=products,
        aisles=aisles,
        product_count=product_count,
        aisle_count=aisle_count
    )

@app.route("/admin/add_product", methods=["POST"])
def add_product():
    name = request.form.get("name")
    category = request.form.get("category")
    aisle_id = request.form.get("aisle_id")
    shelf = request.form.get("shelf")
    conn = sqlite3.connect("store.db")
    conn.execute(
        "INSERT INTO products (name, category, aisle_id, shelf) VALUES (?, ?, ?, ?)",
        (name, category, aisle_id, shelf)
    )
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route('/admin/add_aisle',methods=['POST'])
def add_aisle():
    conn=sqlite3.connect("store.db")
    aisle_code=request.form.get("aisle_code").strip().upper()
    section=request.form.get('section')
    conn.execute(
        "INSERT INTO aisles(aisle_number,section_name) VALUES(?,?)",
        (aisle_code,section)
    )

    conn.commit()
    conn.close()
    return redirect('/admin')
@app.route('/admin/delete_aisle',methods=['POST'])
def delete_aisle():
    aisle_code=request.form.get('aisle_code').strip().upper()
    conn=sqlite3.connect('store.db')
    conn.row_factory = sqlite3.Row
    aisle=conn.execute("SELECT * FROM aisles WHERE aisle_number=?",(aisle_code,)).fetchone()
    if aisle:
        conn.execute("DELETE FROM aisles WHERE aisle_number=?",(aisle_code,))
        conn.commit()
        return redirect('/admin')
    else:
        products = conn.execute("""
        SELECT p.*, a.aisle_number, a.section_name
        FROM products p JOIN aisles a ON p.aisle_id = a.id
    """).fetchall()
    aisles = conn.execute("SELECT * FROM aisles").fetchall()
    conn.close()
    return render_template("admin.html",error="Aisle Not Found!", products=products, aisles=aisles)

@app.route('/admin/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn=sqlite3.connect('store.db')
    conn.row_factory=sqlite3.Row
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))



  

if __name__=='__main__':
    app.run(debug=True)

