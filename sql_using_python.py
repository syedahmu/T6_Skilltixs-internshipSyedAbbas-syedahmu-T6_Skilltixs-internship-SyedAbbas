# sales_summary.py or Jupyter cell ---
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect to database
conn = sqlite3.connect("SuperStore_sales_dataset.db")

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sales_data.db")
conn = sqlite3.connect(db_path)

cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

conn.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")
conn.commit()

conn.execute("INSERT INTO sales (product, quantity, price) VALUES ('Widget', 10, 2.5)")
conn.commit()

# 2. Run SQL
query = """
SELECT
  product,
  SUM(quantity) AS total_qty,
  SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
"""
df = pd.read_sql_query(query, conn)

print("===== Sales Summary by Product =====")
print(df.to_string(index=False))

# 4. Plot revenue bar chart
plt.figure(figsize=(8, 5))
plt.bar(df['product'], df['revenue'], color='skyblue')
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()


#  Save chart
plt.savefig("sales_chart.png")
plt.show()

# 5. Cleanup
conn.close()
