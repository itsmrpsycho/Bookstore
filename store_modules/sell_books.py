import store_modules.mysql_connector as sq_con
from store_modules.emailer_2 import *


def sell_books(user_curdata):
    if user_curdata != 'ERROR_LOGIN':
        # getting b_id
        (con, cur) = sq_con.con_cur_exec('SELECT * FROM shop')
        temp = cur.fetchall()
        b_id = cur.rowcount + 1
        con.close()

        # getting data
        print(f'book id is {b_id}')
        b_name = input('Book name - ')

        # Fetching Genre
        def genre_inputter():
            book_genre= input("Genre Fiction (f) / Academics (a) - ")
            if book_genre.lower() == "f":
                return "Fiction"
            elif book_genre.lower() == "a":
                return "Academics"
            else:
                print("Please enter a valid choice.")
                return genre_inputter()
        b_genre = genre_inputter()

        # Fetching right price
        def price_checker():
            b_price_try = input('Price (in INR) - ')
            if b_price_try.isdigit():
                b_price_try = int(b_price_try)
                while b_price_try <= 0:
                    print("Please enter a valid price.")
                    b_price_try = float(input('Price (in INR)- '))
                return b_price_try
            else:
                print("Please Enter A Valid Price.")
                return price_checker()

        b_price = price_checker()

        # Fetching Stock Quantity
        def stock_checker():
            b_stock_try = input('How many books are you going to sell - ')
            if b_stock_try.isdigit():
                if int(b_stock_try) > 0:
                    return b_stock_try
                else:
                    print('Enter a valid number')
                    return stock_checker()
            print('Enter a valid number')
            return stock_checker()
        b_stock = stock_checker()

        # entering into books table
        (con, cur) = sq_con.con_cur_exec(f"INSERT INTO shop VALUES({b_id},'{b_name}',{b_price},{b_stock},'{b_genre}')")
        con.commit()
        con.close()

        # getting seller id
        (con, cur) = sq_con.con_cur_exec('SELECT * FROM sellers')
        temp = cur.fetchall()
        seller_id = cur.rowcount + 1

        # entering into sellers table
        (con, cur) = sq_con.con_cur_exec(f"INSERT INTO sellers VALUES({seller_id},'{user_curdata.ufullname}',{user_curdata.uph},{b_stock},{b_id},{user_curdata.uid})")
        con.commit()
        con.close()

        # Sending E-Mail
        b_quan_name = f"{str(b_stock)} {b_name}"
        print("Please Wait. This might take a few seconds.")
        seller_mail(user_curdata.ufullname, user_curdata.umail, b_quan_name)
        print('Check your e-mail for confirmation.')

        return 'done'

    else:
        print('Try again')
        return 'ERROR_SELLING'
