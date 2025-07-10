import sqlite3

conn = sqlite3.connect('perf.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS perf_data')
cursor.execute('CREATE TABLE perf_data(stack TEXT, count INT)')

with open('perf.folded', 'r') as f:
    for line in f:
        # 分割 stack 和 count，确保去除多余字符
        parts = line.strip().split(' ')
        if len(parts) == 2:
            stack, count = parts
            cursor.execute('INSERT INTO perf_data (stack, count) VALUES (?, ?)', (stack, int(count)))

conn.commit()
conn.close()
