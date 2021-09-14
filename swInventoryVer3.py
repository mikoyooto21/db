from pprint import pprint
import sqlite3
import swInventoryFunctions as dbf

#Mac-address sw7 is same with Mac-address of switch sw3 in 'data' list
data2 = [('0055.AAAA.CCCC', 'sw5', 'Cisco 3750', 'London, Green Str'),
        ('0066.BBBB.CCCC', 'sw6', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw7', 'Cisco 2960', 'London, Green Str'),
        ('0088.AAAA.CCCC', 'sw8', 'Cisco 3750', 'London, Green Str')]

def writeRowsInDB(connection, query, data, verbose=True):
    '''
        Функция ожидает аргументы:
        * connection - соединение с БД
        * query - запрос, который нужно выполнить
        * data - данные, которые надо передать в виде списка кортежей

        Функция пытается записать поочереди кортежи из списка data.
        Если кортеж удалось записать успешно, изменения сохраняются в БД.
        Если в процессе записи кортежа возникла ошибка, транзакция откатывается.

        Флаг verbose контролирует то, будут ли выведены сообщения об удачной
        или неудачной записи кортежа.
    '''
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as e:
                if verbose:
                    print('An error occured while {} was writing in database'.format(', '.join(row)))
        else:
                if verbose:
                    print('Data {} has been writed'.format(', '.join(row)))

con = dbf.createConnection('swInventory3.db')

queryInsert = 'insert into switch values (?,?,?,?)'
queryGetAll = 'select * from switch'

print('\nChecking current content of database...')
pprint(dbf.getAllFromDB(con, queryGetAll))

print('-' * 60)
print('Trying to write data with same Mac-address:')
pprint(data2)
writeRowsInDB(con, queryInsert, data2)
print('\nChecking content of database')
pprint(dbf.getAllFromDB(con, queryGetAll))

con.close()