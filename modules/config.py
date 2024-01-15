import pymysql as MySQLdb

db_hostname = input('input database hostname: ')
db_username = input('input database username: ')
db_password = input('input database password: ')
db_database = input('input database name: ')

def db_connect() -> callable:
    ''' Quickly connects to database from MySQL database credentials

        Designed to connect to database in a way which keeps the code readable
        whilst also condensing the code '''
    
    return MySQLdb.connect(
                host=db_hostname,
                user=db_username,
                passwd=db_password,
                db=db_database)
