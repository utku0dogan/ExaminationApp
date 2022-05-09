import sqlite3
class DB():

    def __init__(self) -> None:
        self.connection = sqlite3.connect('examination.db')
        self.connection.cursor()

    def Query(self, query):
        result = self.connection.execute(query, tuple=[])
        values = result.fetchall()
        value = result.fetchone()
        self.connection.close()
