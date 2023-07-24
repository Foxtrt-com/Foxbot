import datetime
import os
import sqlite3
from . import level_helper


def get_database_conn(guild_id):
    conn = None
    try:
        conn = sqlite3.connect(f'./data/{guild_id}.db')
    except Exception as e:
        print(e)

    return conn


def create_guild_database(guild_id):
    open(f'./data/{guild_id}.db', 'a').close()

    conn = get_database_conn(guild_id)

    conn.execute("CREATE TABLE guild_settings(setting_name varchar, setting_value varchar)")

    msg = "Hi {user}, welcome to {server}!"

    conn.execute(f"INSERT INTO guild_settings(setting_name, setting_value) VALUES ('welcome_msg', '{msg}')")

    conn.execute("CREATE TABLE guild_users(uid varchar, last_exp_drop varchar, lvl int, exp int)")

    conn.commit()
    conn.close()


def delete_guild_database(guild_id):
    os.remove(f'./data/{guild_id}.db')


def add_user(guild_id, uid, join_date):
    conn = get_database_conn(guild_id)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO guild_users(uid,last_exp_drop,lvl,exp) VALUES ('{uid}', '{join_date}', 0, 0)")
    conn.commit()
    conn.close()


def delete_user(guild_id, uid):
    conn = get_database_conn(guild_id)
    cur = conn.cursor()

    cur.execute(f"DELETE FROM guild_users WHERE uid = '{uid}'")
    conn.commit()
    conn.close()


def add_exp(guild_id, uid, msg_datetime, exp):
    conn = get_database_conn(guild_id)
    cur = conn.cursor()

    res = cur.execute(f"SELECT * FROM guild_users WHERE uid = '{uid}'")
    user = res.fetchone()

    if datetime.datetime.fromisoformat(user[1]) <= msg_datetime - datetime.timedelta(minutes=1):
        new_exp = user[3] + exp

        if level_helper.has_lvl_up(user[2], new_exp):
            new_lvl = user[2] + 1

            cur.execute(f"UPDATE guild_users SET last_exp_drop = '{msg_datetime}', lvl = {new_lvl}, exp = {new_exp} WHERE uid = '{uid}'")

            conn.commit()
            conn.close()

            return True, new_lvl
        else:
            cur.execute(f"UPDATE guild_users SET last_exp_drop = '{msg_datetime}', exp = {new_exp} WHERE uid = '{uid}'")

            conn.commit()
            conn.close()
            return False, user[2]


def set_welcome_msg(guild_id, msg):
    conn = get_database_conn(guild_id)
    cur = conn.cursor()

    cur.execute(f"UPDATE guild_settings SET setting_value = '{msg}' WHERE setting_name = 'welcome_msg'")
    conn.commit()
    conn.close()


def get_welcome_msg(guild_id):
    conn = get_database_conn(guild_id)
    cur = conn.cursor()

    res = cur.execute("SELECT setting_value FROM guild_settings WHERE setting_name = 'welcome_msg'")
    welcome_msg = res.fetchone()
    conn.close()

    return welcome_msg


def get_top_5(guild_id):
    conn = get_database_conn(guild_id)
    cur = conn.cursor()

    res = cur.execute("SELECT * FROM guild_users ORDER BY exp DESC LIMIT 5")
    top_5 = res.fetchall()
    conn.close()

    return top_5


def get_user(guild_id, uid):
    conn = get_database_conn(guild_id)
    cur = conn.cursor()

    res = cur.execute(f"SELECT * FROM guild_users WHERE uid = '{uid}'")
    user = res.fetchone()
    conn.close()

    return user
