import sqlite3
from pprint import pprint


data = [('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str'),
        ('0000.BBBB.CCCC', 'sw2', 'Cisco 3780', 'London, Green Str'),
        ('0000.AAAA.DDDD', 'sw3', 'Cisco 2960', 'London, Green Str'),
        ('0011.AAAA.CCCC', 'sw4', 'Cisco 3750', 'London, Green Str')]

def createConnection(dbName):
    '''
    Создание соединения с БД и возвращение оного
    '''
    connection = sqlite3.connect(dbName)
    return connection

def writeDataToDB(connection, query, data):
    '''
    Функция ожидает аргументы:
    -connection -- соединение с БД
    -query -- запрос, который нужно выполнить
    -data -- данные которые надо обработать

    Функция пытается записть все данные из списка.
    Если данные удалось записать успешно, изменения сохраняются в БД и ф-ия возвращает True.
    Если в процессе записи возникла ошибка, транзакция откатывается и ф-ия возвращает False.
    '''
    try:
        with connection:
            connection.executemany(query,data)
    except sqlite3.IntegrityError as e:
        print('Error occurred: ', e)
        return False
    else:
        print('Data has been wroten to database')
        return True

def getAllFromDB(connection, query):
    '''
    Функция ожидает аргументы:
    -connection -- соединение с БД
    -query -- запрос, который нужно выполнить.

    Ф-ия возвращает данные полученные из БД.
    '''
    result = [row for row in connection.execute(query)]
    return result

if __name__ == '__main__':
    con = createConnection('swInventory3.db')

    print('Creating table...')
    schema = '''create table switch(mac text primary key, hostname text, model text, location text)'''
    con.execute(schema)

    queryInsert = 'insert into switch values(?,?,?,?)'
    queryGetAll = 'select * from switch'

    print('Writing data into db:')
    pprint(data)
    writeDataToDB(con, queryInsert, data)
    print('\nVerification of db containing')
    pprint(getAllFromDB(con, queryGetAll))

    con.close()