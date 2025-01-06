import pymssql

conn = pymssql.connect(
    server='dist-6-505.uopnet.plymouth.ac.uk',
    user='NSengupta',
    password='ZwhJ560*',
    database='COMP2001_NSengupta'
)
cursor = conn.cursor()
cursor.execute("SELECT 1")
print(cursor.fetchone())
conn.close()


