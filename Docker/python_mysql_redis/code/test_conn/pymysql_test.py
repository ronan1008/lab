import pymysql

connection = pymysql.connect(
    host = 'mysql',
    user = 'root',
    password = 'mysql',
    db = 'demo'
)

cursor = connection.cursor()
sql = "CREATE TABLE users(id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(20), password VARCHAR(20))"
cursor.execute(sql)
connection.commit()


sql = "INSERT INTO users(username, password) VALUES (%s, %s)"
cursor.execute( sql, ('user1', 'password1'))
cursor.execute( sql, ('user2', 'password2'))
cursor.execute( sql, ('user3', 'password3'))
connection.commit()

sql = "SELECT id, username from users"
cursor.execute(sql)
result = cursor.fetchall()
print(result)

connection.close()
