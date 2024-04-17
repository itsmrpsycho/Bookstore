import store_modules.mysql_connector as sq_con
from validate_email import validate_email


class Data:
    uid = ''
    uname = ''
    password = ''
    uph = ''
    umail = ''
    ufullname = ''


def log_reg():
    key_l_r = input('\nDo you want to login or register or exit (l/r/e) - ')
    # login
    if key_l_r.lower() == 'l':
        user_name_input = input('Enter your username - ')
        user_pass_input = input('Enter your password - ')
        (con, cur) = sq_con.con_cur_exec('SELECT user_name, user_pass FROM users')
        table_data = cur.fetchall()
        con.close()

        if (user_name_input, user_pass_input) in table_data:
            (con, cur) = sq_con.con_cur_exec(f'SELECT * FROM users WHERE user_name = "{user_name_input}"')
            user_data_raw = cur.fetchall()
            con.close()
            Data.uid = user_data_raw[0][0]
            Data.uname = user_data_raw[0][1]
            Data.password = user_data_raw[0][2]
            Data.uph = user_data_raw[0][3]
            Data.umail = user_data_raw[0][4]
            Data.ufullname = user_data_raw[0][5]
            print(f'\nLogin Successful, logged in as {Data.uname}\n')
            return Data
        else:
            print('\nIncorrect entries / not registered')
            return log_reg()
    # register
    elif key_l_r.lower() == 'r':
        (con, cur) = sq_con.con_cur_exec('SELECT * FROM users')
        temp_file = cur.fetchall()
        user_id = cur.rowcount + 1
        con.close()

        # checking validity of user_name
        (con, cur) = sq_con.con_cur_exec("SELECT user_name FROM users;")
        data_check = cur.fetchall()
        con.close()

        def user_name_checker(data_check_try):
            user_name_try = input("username: ")
            a = True
            for i in data_check_try:
                if i[0] == user_name_try:
                    a = False
                    break
            if a:
                return user_name_try
            else:
                print('The username has already been used. Please try a different username')
                return user_name_checker(data_check_try)

        user_name = user_name_checker(data_check)

        user_pass = input("Pass: ")

        # ph number should be a 10 digit integer
        def ph_no_tryout():
            user_try_ph = input("Contact Number: ")
            ph_digit = True
            ph_10_digit = True
            if not len(user_try_ph) == 10:
                ph_10_digit = False
            for i in list(user_try_ph):
                if i.isdigit():
                    ph_digit = True
                else:
                    ph_digit = False
                    break
            if ph_digit and ph_10_digit:
                return user_try_ph
            elif ph_digit and not ph_10_digit:
                print("Your phone number must be of 10 digits")
                return ph_no_tryout()
            else:
                print("Please enter a valid contact number.")
                return ph_no_tryout()
        user_ph_no = ph_no_tryout()

        # checking validity of email id
        def email_checker():
            user_email_id_temp = input("Email Id: ")
            email_validity = validate_email(user_email_id_temp)
            if email_validity:
                return user_email_id_temp
            else:
                print('Please enter a valid email id.')
                return email_checker()
        user_email_id = email_checker()

        user_fullname = input('Enter your full name: ')
        (con, cur) = sq_con.con_cur_exec(f"INSERT INTO users VALUES({user_id},'{user_name}','{user_pass}',{user_ph_no},'{user_email_id}','{user_fullname}',{0})")
        con.commit()
        con.close()

        # returning data to function
        (con, cur) = sq_con.con_cur_exec(f'SELECT * FROM users WHERE user_name = "{user_name}"')
        user_data_raw = cur.fetchall()
        con.close()
        Data.uid = user_data_raw[0][0]
        Data.uname = user_data_raw[0][1]
        Data.password = user_data_raw[0][2]
        Data.uph = user_data_raw[0][3]
        Data.umail = user_data_raw[0][4]
        Data.ufullname = user_data_raw[0][5]
        print(f'\nLogin Successful, logged in as {Data.uname}\n')
        return Data
    elif key_l_r.lower() == 'e':
        return 'EXIT'
    else:
        print('Please enter a valid input')
        return log_reg()
