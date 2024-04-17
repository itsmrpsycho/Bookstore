import store_modules.mysql_connector as sq_con
from prettytable import PrettyTable


def displayer():
    (con, cur) = sq_con.con_cur_exec("SELECT * FROM shop")
    data = cur.fetchall()
    con.close()

    def disp_key():
        table = PrettyTable()
        table.field_names=['id','name','price','stock','genre']
        for i in data:
            table.add_row([i[0],i[1],round(i[2] * 1.2),i[3],i[4]])
        print(table,'\n')
    disp_key()
