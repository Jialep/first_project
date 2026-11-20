import pprint
import sqlite3
import calendar_core as core
data=[
    ('2026-11-23','MA1521 Finals','9am to 11am'),
    ('2026-11-23','IS2238 Finals','1pm to 3pm'),
    ('2026-11-25','CS1010A Finals','9am to 11am'),
    ('2026-11-28','IS1108 Finals','1pm to 3pm'),
    ('2026-11-20','QET','10am to 12pm')
]
rubbish=[
    ('2030-13-32','Rubbish data','hehehehe'),
    ('6767-67-67','67-virus','676767'),
    ('2026-10-18','Loser','hahaloser')]
def create_table(database,name):
    con=None
    try:
        con=sqlite3.connect(database)
        cur=con.cursor()
        #cur.execute('DROP TABLE IF EXISTS Calendar')
        cur.execute(
            f'CREATE TABLE IF NOT EXISTS {name}('
            'event_id INTEGER PRIMARY KEY AUTOINCREMENT,' \
            'date TEXT ,' \
            'title TEXT,' \
            'details TEXT'
            ')')
        con.commit()
    except Exception as e:
        return f'An error occurred: {e}'
    finally:
        if con is not None:
            con.close()
def add_event(database,name,data):
    error=[]
    valid=[]
    for line in data:
        date=line[0]
        try:
            date=core.format_date(date)
            valid.append(line)
        except ValueError:
            error.append(line)
    for line in error:
        print(f'{line[0]} in {line} is invalid')
    con=None
    try:
        con=sqlite3.connect(database)
        cur=con.cursor()
        cur.executemany(f'INSERT INTO {name} (date, title, details) VALUES (?,?,?)',valid)
        con.commit()
    except Exception as e:
        return f'An error occurred: {e}'
    finally:
        if con is not None:
            con.close()
def view_table(database,name):
    con=None
    try:
        con=sqlite3.connect(database)
        cur=con.cursor()
        pprint.pprint(cur.execute(f'SELECT * FROM {name}').fetchall())
        con.commit()
    except Exception as e:
        return f'An error occurred: {e}'
    finally:
        if con is not None:
            con.close()
def delete_event(database,name,e_id):
    con=None
    try:
        con=sqlite3.connect(database)
        cur=con.cursor()
        selected=cur.execute(
            f'SELECT * FROM {name} WHERE event_id=?',(e_id,),
        ).fetchone()
        if selected is None:
            return 'No such events exists'
        cur.execute(f'DELETE FROM {name} WHERE event_id=?',(e_id,))
        con.commit()
        return(f'{selected} has been removed')
    except Exception as e:
        return f'An error occurred: {e}'
    finally:
        if con is not None:
            con.close()
def get_events_by_dates(database,name,date_key):
    con=None
    try:
        con=sqlite3.connect(database)
        cur=con.cursor()
        try:
            date_key=core.format_date(date_key)
        except ValueError as e:
            return(e)
        selected=cur.execute(
            f'SELECT * FROM {name} WHERE DATE=?',(date_key,)
        ).fetchall()
        if not selected:
            return(f'No events are found on {date_key}')
        return pprint.pformat(selected)
        con.commit()
    except Exception as e:
        return f'An error occurred: {e}'
    finally:
        if con is not None:
            con.close()
def get_by_date_range(database,name,start,end):
    con=None
    try:
        con=sqlite3.connect(database)
        cur=con.cursor()
        try:
            start=core.format_date(start)
            end=core.format_date(end)
        except ValueError:
            return f'Invalid date range'
        query=(
            f'SELECT * FROM {name} WHERE date BETWEEN ? AND ? ORDER BY date,event_id'
        )
        selected=cur.execute(query,(start,end)).fetchall()
        if selected==[]:
            return f'No events from {start} to {end}'
        pprint.pprint(selected)
        con.commit()
    except Exception as e:
        return f'An error ocurred:{e}'
    finally:
        if con is not None:
            con.close()
def get_by_id(database,name,e_id):
    con = None
    try:
        con=sqlite3.connect(database)
        cur=con.cursor()
        query=f'SELECT * FROM {name} WHERE event_id=?'
        selected=cur.execute(query,(e_id,)).fetchone()
        if selected is None:
            return f'No events with event ID: {e_id}'
        return(selected)
        con.commit()
    except Exception as e:
        return f'An error occurred: {e}'
    finally:
        if con is not None:
            con.close()   
def delete_by_id(database,name,e_id):
    con=None
    try:
        con=sqlite3.connect(database)
        cur=con.cursor()
        query=f'SELECT * FROM {name} WHERE event_id=?'
        selected=cur.execute(query,(e_id,)).fetchone()
        if selected is None:
            return f'No events with index: {e_id}'
        query2=(
            f'DELETE FROM {name} WHERE event_id=?'
        )
        cur.execute(query2,(e_id,))
        con.commit()
        return(f'{selected} has been deleted')
    except Exception as e:
        return f'An error occurred: {e}'
    finally:
        if con is not None:
            con.close()
if __name__ == '__main__':
    db='My_events_db'
    name='Calendar'
    create_table(db,name)
    add_event(db,name,rubbish)
    view_table(db,name)
    print(
        delete_event(db,name,1),
        get_events_by_dates(db,name,'2026-11-23'),
        get_by_id(db,name,3)
    )