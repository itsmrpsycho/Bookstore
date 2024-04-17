from prettytable import PrettyTable
import store_modules.mysql_connector as sq_con
from store_modules.emailer_2 import *


def buy_books(user_curdata):

    if user_curdata != 'ERROR_LOGIN':
        # getting data
        (con,cur)= sq_con.con_cur_exec('SELECT b_id, b_name, b_price, b_stock, genre FROM shop')
        data = cur.fetchall()
        con.close()

        # outputting data
        displayer = PrettyTable()
        displayer.field_names = ["Book ID", "Name", "Price","Stock","Genre"]
        for i in data:
            displayer.add_row([i[0],i[1],round(i[2] * 1.2),i[3],i[4]])
        print(displayer,'\n')

        # Fetching buy_id
        def buy_id_checker():
            buy_id_try = input('Enter the Book ID - ')
            if buy_id_try.isdigit():
                buy_id_try = int(buy_id_try)
                while buy_id_try not in range(1,len(data)+1):
                    print("Please enter a valid Book ID.")
                    buy_id_try = int(input('Enter the Book ID - '))
                return buy_id_try
            else:
                print('Enter a Valid Book ID')
                return buy_id_checker()
        buy_id = buy_id_checker()

        # storing book data for later use
        (con, cur) = sq_con.con_cur_exec(f'SELECT * FROM shop WHERE b_id = {buy_id}')
        book_data = cur.fetchall()
        con.close()

        # Fetching buy quantity
        def quan_checker():
            buy_quantity_try = input('Enter quantity - ')
            if buy_quantity_try.isdigit():
                buy_quantity_try = int(buy_quantity_try)
                if buy_quantity_try <= 0:
                    print('Please Enter a valid number')
                    return quan_checker()
                else:
                    return buy_quantity_try
            else:
                print('Please Enter a valid number')
                return quan_checker()
        buy_quantity = quan_checker()


        (con, cur) = sq_con.con_cur_exec(f'SELECT * FROM shop WHERE b_id = {buy_id}')
        buy_book_data = cur.fetchall()
        if buy_quantity > buy_book_data[0][3]:
            print("Not enough stock")
            return 'ERROR_BUYING'
        else:
            bookstore_charge = buy_quantity * book_data[0][2] * 0.2
            final_price = round(buy_quantity * book_data[0][2] * 1.12 + bookstore_charge)
            ord_confirm = input(f'Total Price (including GST) would be INR {final_price}\nIf you want to cancel this order enter n, if not, press return key to register transaction. ')
            if ord_confirm != 'n':
                # Entering into shop table
                (con, cur) = sq_con.con_cur_exec(f'UPDATE shop SET b_stock = b_stock - {buy_quantity} WHERE b_id = {buy_id}')
                con.commit()
                con.close()

                buyer_ph_no = user_curdata.uph

                # Getting buyer id
                (con2, cur2) = sq_con.con_cur_exec('SELECT * FROM buyers')
                data = cur2.fetchall()
                buyer_id = cur2.rowcount + 1
                con2.close()

                # Entering into buyers table
                (con, cur) = sq_con.con_cur_exec(f'INSERT INTO buyers VALUES({buyer_id},"{user_curdata.ufullname}",{buyer_ph_no},{buy_quantity},{buy_id},{user_curdata.uid})')
                con.commit()
                con.close()

                # Entering into users table
                (con, cur) = sq_con.con_cur_exec(f'UPDATE users SET profit = profit + {bookstore_charge} WHERE user_id = {user_curdata.uid}')
                con.commit()
                con.close()

                # Sending Email
                b_quan_name = f'{str(buy_quantity)} {book_data[0][1]}'
                print('\nPlease wait. This might take a few seconds.\n')
                buyer_mail(user_curdata.ufullname, user_curdata.umail, b_quan_name, final_price)
                print("Check your e-mail for confirmation of order.")
                con.close()
                return 'done'
            else:
                return 'ERROR_BUYING'
    else:
        print('Try again')
        return 'ERROR_BUYING'
