import time
import pymysql
import os
from dotenv import load_dotenv



def wait_for_mysql():
    while True:
        try:
            load_dotenv()
            conn = pymysql.connect(
                host=os.getenv("MYSQL_HOST"),
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DATABASE")
            )
            conn.close()
            break
        except pymysql.MySQLError:
            time.sleep(2)