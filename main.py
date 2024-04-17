import store_modules.buy_books as buyer
import store_modules.login_mod as log
import store_modules.sell_books as seller
import store_modules.review_site_2 as reviewer
from store_modules.display_books import *


def search_database():
    b_name_input = input('Enter a keyword to search - ')
    (con, cur) = sq_con.con_cur()
    cur.execute('SELECT b_name FROM shop;')
    b_name_data = cur.fetchall()
    search_list = []
    n = 1
    for i in b_name_data:
        if b_name_input.lower() in i[0].lower():
            search_list.append(n)
        n += 1
    cur.execute('SELECT * FROM shop;')
    data = cur.fetchall()
    output_raw = []
    for i in data:
        if i[0] in search_list:
            output_raw.append(i)
    con.close()
    if output_raw != []:
        output = PrettyTable()
        output.field_names = ["Book ID", "Name", "Price", "Stock","Genre"]
        for i in output_raw:
            output.add_row([i[0], i[1],round(i[2] * 1.2), i[3],i[4]])
        print(output)
    else:
        print('No results')



def buyer_interface(user_curdata_temp):
    purchase = buyer.buy_books(user_curdata_temp)
    if purchase == 'done':
        key1 = input('Do you want to purchase anything else? (y/n) ')
        if key1.lower() == 'y':
            return buyer_interface(user_curdata_temp)
        elif key1.lower() == 'n':
            return 'interface_end'
        else:
            print("Sorry, we couldn't process your request.")
    else:
        return buyer_interface(user_curdata_temp)


def seller_interface(user_curdata_temp):
    sell = seller.sell_books(user_curdata_temp)
    if sell == 'done':
        def key_func():
            key2 = input('Do you want to sell anything else? (y/n) ')
            if key2.lower() == 'y':
                return seller_interface(user_curdata_temp)
            elif key2.lower() == 'n':
                return 'key_end'
            else:
                return 'key_error'
        a = key_func()
        if a == 'key_end':
            return 'interface_end'
        while a == 'key_error':
            print("Sorry, we couldn't process your request.")
            a = key_func()
    else:
        return seller_interface(user_curdata_temp)


def leaderb_disp():
    (con, cur) = sq_con.con_cur_exec('SELECT user_name, profit FROM users ORDER BY profit DESC')
    data = cur.fetchall()
    con.close()
    tab = PrettyTable()
    tab.field_names = ['Rank', 'Username', 'Score']
    for i in range(1, 4):
        tab.add_row([i, data[i-1][0], data[i-1][1]])
    print(f"\n{tab}\n")


# Menu Selection
def menu(user_curdata_temp):
    print('''\n--Menu--\nDisplay - 1
Buy - 2
Sell - 3
Search - 4
Write a review - 5''')
    rev_number = reviewer.review_number()
    if rev_number > 4:
        print("Read Reviews - 6")
    print("User leaderboard - U\nLogout - L\n")
    key = input('Please enter your choice - ')
    if key == '1':
        displayer()
        return menu(user_curdata_temp)
    elif key == '2':
        buyer_interface(user_curdata_temp)
        return menu(user_curdata_temp)
    elif key == '3':
        seller_interface(user_curdata_temp)
        return menu(user_curdata_temp)
    elif key == '4':
        search_database()
        return menu(user_curdata_temp)
    elif key == '5':
        reviewer.review_writer(user_curdata_temp)
        return menu(user_curdata_temp)
    elif key == '6':
        reviewer.review_reader(6, user_curdata_temp)
        return menu(user_curdata_temp)
    elif key.upper() == 'L':
        print('\nLogged out successfully.\n')
        return 'MAIN_LOGOUT'
    elif key.upper() == 'U':
        leaderb_disp()
        return menu(user_curdata_temp)
    else:
        return menu(user_curdata_temp)


def log_main():
    print("\nPlease Log-in")
    return log.log_reg()


def func(log_info_temp):
    if not log_info_temp == 'EXIT':

        rev_number = reviewer.review_number()
        if rev_number >= 2:
            # return reviewer.review_reader(2, log_info_temp)
            reviewer.review_reader(2, log_info_temp)

        if log_info_temp != 'ERROR_LOGIN':
            logout_key = menu(log_info_temp)
            if logout_key == 'MAIN_LOGOUT':
                # if pressed L in menu
                log_info2 = log_main()
                if log_info2 == 'EXIT':
                    print('\nThank you for visiting us')
                else:
                    return func(log_info2)


log_info = log_main()
func(log_info)
