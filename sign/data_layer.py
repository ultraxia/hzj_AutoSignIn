import pymysql


def query(sql):
    mysql_conn = {
        'host': '',
        'port': 3306,
        'user': '',
        'password': '',
        'db': '',
        'charset': 'utf8'
    }
    db = pymysql.connect(**mysql_conn)
    cursor = db.cursor()
    cursor.execute(sql)
    tasks = cursor.fetchall()
    return tasks


