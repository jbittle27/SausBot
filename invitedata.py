import sqlite3
import datetime


'''
# Database creation
conn = sqlite3.connect('invites.db')
c = conn.cursor()
c.execute("""CREATE TABLE invites(
            inviter text,
            invitee text,
            time text)""")
            '''


def remove_invite(invitee):
    conn = sqlite3.connect('invites.db')
    c = conn.cursor()
    try:
        c.execute("DELETE from invites WHERE invitee=:invitee",
                  {'invitee': f'{invitee}'})
        conn.commit()
        conn.close()
        return
    except:
        print('Error deleting invite from invites.db')
        conn.close()
        return


def add_invite(inviter, invitee):
    conn = sqlite3.connect('invites.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO invites VALUES (:inviter, :invitee, :time)', {
                  'inviter': inviter, 'invitee': invitee, 'time': datetime.datetime.now()})
        conn.commit()
        conn.close()
        return
    except:
        print('Error saving into invites.db')
        conn.close()
        return


def get_invite(invitee):
    conn = sqlite3.connect('invites.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM invites WHERE invitee=:invitee",
                  {'invitee': f'{invitee}'})
        x = c.fetchone()
        conn.close()
        return (x)
    except:
        print('Error getting invites from invites.db')
        conn.close()
        return
