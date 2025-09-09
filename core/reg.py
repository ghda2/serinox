from .db import get_connection

def register_submission(landpage, name, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO submissions (landpage, name, email) VALUES (%s, %s, %s)", (landpage, name, email))
    conn.commit()
    cur.close()
    conn.close()
