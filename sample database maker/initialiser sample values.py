from random import *
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


def database():
    con = sq.connect(host="localhost", user="root", passwd="root")
    cur = con.cursor()
    cur.execute('DROP DATABASE IF EXISTS bookstore')
    cur.execute('CREATE DATABASE bookstore')
    con.close()

def deleter():
    (con,cur) = con_cur()

    cur.execute('DROP TABLE sellers;')
    con.commit()

    cur.execute('DROP TABLE buyers;')
    con.commit()

    cur.execute('DROP TABLE users;')
    con.commit()

    cur.execute('DROP TABLE shop;')
    con.commit()

    con.close()

    (con,cur) = con_cur()


def table_maker():
    (con,cur) = con_cur()
    # make shop table
    cur.execute('CREATE TABLE IF NOT EXISTS shop(b_id INT PRIMARY KEY,b_name VARCHAR(60), b_price FLOAT,b_stock INT,genre VARCHAR(30))')
    con.commit()

    # make users table
    cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INT  PRIMARY KEY, user_name VARCHAR(40) NOT NULL, user_pass VARCHAR(30) NOT NULL, user_ph_no BIGINT NOT NULL, user_email_id VARCHAR(30) NOT NULL, user_fullname VARCHAR(40) NOT NULL, profit FLOAT DEFAULT 0);')
    con.commit()

    # make buyers table
    cur.execute('CREATE TABLE IF NOT EXISTS buyers(buyer_id INT PRIMARY KEY, buyer_name VARCHAR(40), buyer_phno BIGINT,buyer_quantity INT, b_id_child INT NOT NULL, user_id_child INT , FOREIGN KEY(user_id_child) REFERENCES users(user_id) ON DELETE CASCADE, FOREIGN KEY(b_id_child) REFERENCES shop(b_id) ON DELETE CASCADE);')
    con.commit()

    # make sellers table
    cur.execute('CREATE TABLE IF NOT EXISTS sellers(seller_id INT PRIMARY KEY, seller_name VARCHAR(30), seller_phno BIGINT, seller_quantity INT,b_id_child INT NOT NULL, user_id_child INT, FOREIGN KEY(user_id_child) REFERENCES users(user_id) ON DELETE CASCADE, FOREIGN KEY(b_id_child) REFERENCES shop(b_id) ON DELETE CASCADE);')
    con.commit()


def user_data():
    # user table
    data = open('data_users.txt', 'r').read()
    data_list = list(data.split('\n'))
    data_list.pop(0)

    for i in data_list:
        temp = i.split(',')
        con_cur_exec_commit(f"INSERT INTO users VALUES({int(temp[0])},'{temp[1]}','{temp[2]}',{int(temp[3])},'{temp[4]}','{temp[5]}',{randint(50,400)})")


def shop_data():

    data = open('data_shop.txt','r').read()
    data_list = data.split('\n')
    data_list.pop(0)

    for i in data_list:
        price = randint(100,300)
        stock = randint(10,30)

        temp = i.split(',')
        if temp[2] == 'A':
            genre = 'Academics'
        else:
            genre = 'Fiction'
        # print(f"INSERT INTO shop VALUES({int(temp[0])},'{temp[1]}',{int(price)},{int(stock)},'{genre}');")
        con_cur_exec_commit(f"INSERT INTO shop VALUES({int(temp[0])},'{temp[1]}',{int(price)},{int(stock)},'{genre}');")


# deleter()
print("Please wait for a few seconds...")
database()
table_maker()
user_data()
shop_data()
print('Done')
