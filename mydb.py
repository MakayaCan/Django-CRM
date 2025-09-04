#Installed Mysql on this computer
#https://dev.mysql.com/downloads/installer/
#pip install mysql
#pip install mysql-connector
#pip install mysql-connector-python
#pip install PyMySQL

import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Root@1234",
    #database="webs"
    #auth_plugin="mysql_native_password"
)

cursorObject = conn.cursor()
cursorObject.execute("CREATE DATABASE IF NOT EXISTS webs")
print("All Done!")

cursorObject.close()
conn.close()
