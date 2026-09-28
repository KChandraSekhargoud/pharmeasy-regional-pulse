import sqlite3

conn = sqlite3.connect('pharmeasy.db')
c = conn.cursor()

print("--- 1. Row-Count Check ---")
print("LEFT JOIN:", c.execute("SELECT COUNT(*) FROM regions_master r LEFT JOIN orders_clean o ON r.region = o.region").fetchone()[0])
print("INNER JOIN:", c.execute("SELECT COUNT(*) FROM regions_master r INNER JOIN orders_clean o ON r.region = o.region").fetchone()[0])

print("\n--- 2. Duplicate-Key Check ---")
dupes = c.execute("SELECT order_id FROM orders_clean GROUP BY order_id HAVING COUNT(*) > 1").fetchall()
print("Duplicates found:", len(dupes))

print("\n--- 3. Null Check (Kurnool COUNT(*) vs COUNT(fk)) ---")
query = """
SELECT r.region, COUNT(*) as count_star, COUNT(o.order_id) as count_fk 
FROM regions_master r LEFT JOIN orders_clean o ON r.region = o.region 
WHERE r.region = 'Kurnool' GROUP BY r.region
"""
print(c.execute(query).fetchall())

print("\n--- 4. Per-Region Order Counts ---")
counts = c.execute("SELECT r.region, COUNT(o.order_id) as orders FROM regions_master r LEFT JOIN orders_clean o ON r.region = o.region GROUP BY r.region ORDER BY orders ASC").fetchall()
for row in counts:
    print(row)