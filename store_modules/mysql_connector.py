import mysql.connector as sq


def con_cur_exec(query):
    con = sq.connect(host="localhost", user="root", passwd="root", database="bookstore", port=3306, auth_plugin='caching_sha2_password')
    cur = con.cursor()
    cur.execute(query)
    return con, cur


def con_cur():
    con = sq.connect(host="localhost", user="root", passwd="root", database="bookstore", port=3306, auth_plugin='caching_sha2_password')
    cur = con.cursor()
    return con, cur


def con_cur_exec_commit(query):
    con = sq.connect(host="localhost", user="root", passwd="root", database="bookstore", port=3306, auth_plugin='caching_sha2_password')
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()
    return cur
