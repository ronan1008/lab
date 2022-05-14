
import pymysql

connection = pymysql.connect(
    host = 'mysql',
    user = 'root',
    password = 'mysql',
    db = 'demo'
)
cursor = connection.cursor()

sql = "SELECT id, username from users"
cursor.execute(sql)
result = cursor.fetchall()
print(result)

connection.close()
