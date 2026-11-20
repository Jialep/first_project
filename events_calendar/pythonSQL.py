import sqlite3
#cur=cursor,con=connection
con = sqlite3.connect('tutorial.db') #connects to db
cur=con.cursor() #creates and connects cursor to database
cur.execute('CREATE TABLE IF NOT EXISTS movie(title,year,score)') #creating table with col names in ()
# cur.execute('DROP TABLE IF EXISTS movie')
# res = cur.execute('SELECT name FROM sqlite_master WHERE name="table";') #->return (table_name,) 
# res=cur.execute('SELECT name FROM sqlite_master WHERE name="spam";') #-> return None
# print(res.fetchone())
# cur.execute('''
#    INSERT INTO movie VALUES
#    ('movie1',2026,8.1),
#    ('movie2',2025,9.4)
# ''')
# data = [
#    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
#    ("Monty Python's The Meaning of Life", 1983, 7.5),
#    ("Monty Python's Life of Brian", 1979, 8.0),
# ]
# cur.executemany('INSERT INTO movie VALUES(?,?,?)',data)
# con.commit()
# res=cur.execute('SELECT score FROM movie')
# print(res.fetchall())
# for row in cur.execute('SELECT year,title FROM movie ORDER BY year'):
#    print(row)
#con.close()
# new_con=sqlite3.connect('tutorial.db')
# new_cur=new_con.cursor()
# res=new_cur.execute('SELECT title, year FROM movie ORDER by score DESC')
# row=res.fetchone()
# if row is not None:
#     print(f'The highest scoring Monty Python movie is {title!r}, relased in {year}')
# new_con.close()