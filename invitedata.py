import sqlite3
import datetime


# Run invitedata.py to create the invite database
# Only run invitedata.py if a database has not already been created
if __name__ == '__main__':
    try:
        conn = sqlite3.connect('invites.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE invites(
              inviter text,
              invitee text,
              time text)""")
    except:
        print('ERROR: invites.db has already been created')


def remove_invite(invitee):
    # Called from 'on_member_remove' in main.py
    # Removes the member from the invite database
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
    # Called from 'on_member_join' in main.py
    # Adds member, inviter, and time of join
    conn = sqlite3.connect('invites.db')
    c = conn.cursor()
    try:
        time = datetime.datetime.now()
        c.execute('INSERT INTO invites VALUES (:inviter, :invitee, :time)', {
                  'inviter': inviter, 'invitee': invitee, 'time': time.strftime('%a, %b %d, %Y at %I:%M %p')})
        conn.commit()
        conn.close()
        return
    except:
        print('Error saving into invites.db')
        conn.close()
        return


def get_invite(invitee):
    # Called from 'invite' from main.py
    # Gets and returns the member, inviter, and time in a list.
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
