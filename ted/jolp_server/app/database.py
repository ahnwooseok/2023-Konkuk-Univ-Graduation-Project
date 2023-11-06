import pymysql
import os
from dotenv import load_dotenv


class Database:
    def __init__(self):
        self.connector = None
        self.cursor = None

    def connect(self, debug=False):
        load_dotenv()
        if debug:
            self.connector = pymysql.connect()
            self.cursor = self.connector.cursor()
        else:
            self.connector = pymysql.connect(
                host=os.environ["host"],
                port=int(os.environ["port"]),
                user=os.environ["user"],
                password=os.environ["password"],
                database=os.environ["database"],
                charset="utf8mb4",
                ssl={"any_non_empty_dict": True},
            )
            self.cursor = self.connector.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    # 데이터 하나만 가져올 때
    def execute_one(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row

    # 데이터 하나만 가져오더라도 list로 가져와짐
    def execute_all(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.connector.commit()

    def close(self):
        self.connector.close()
