import sqlite3

with sqlite3.connect('/tmp/python_adv.db') as conn:
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS stocksN \n (date text, trans text, symbol text, qty real, price real)')

    # Insert a row of data
    c.execute("INSERT INTO stocks VALUES ('2020-04-05', 'sell', 'UBU|NTU', 100, 35.14)")

    # Save (commit) the changes
    conn.commit()

    c.execute('select * FROM stocks')

    print('-' * 30)
    # load one row
    print(c.fetchone())

    print('-' * 30)
    for row in c:
        print(row)

    print('-' * 30)
    # alternative way: load rows into list
    print(c.fetchall())
