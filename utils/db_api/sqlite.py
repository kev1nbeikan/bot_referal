import sqlite3
from dataclasses import dataclass
from typing import Union

# нэминг полей
TABLE_USERS_NAME = 'Users'
IDENTIFIER_LINE_NAME = 'id'
REFERRAL_LINE_NAME = 'referral'
INVITES_COUNT_LINE_NAME = 'invites_count'
TABLE_CAPTCHA_NAME = 'Captcha'
ANSWER_LINE_NAME = 'Answer'
SERVER_ID_LINE_NAME = 'id'
NUM_SQL_LINE_NAME = 'num'


@dataclass
class DB:

    def __init__(self, path_db='users.db'):
        self.path_db = path_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_db)

    def execute(self, command: str, params: tuple = (), fetch_one=False, fetch_all=False, commit=False) -> Union[
        tuple, list[tuple]]:

        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(command, params)

        data = None

        if commit:
            connection.commit()
        if fetch_one:
            data = cursor.fetchone()
        if fetch_all:
            data = cursor.fetchall()

        connection.close()

        return data

    def create_table_users(self):
        command = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_USERS_NAME}(
        {IDENTIFIER_LINE_NAME} int PRIMARY KEY,
        {REFERRAL_LINE_NAME} str NOT NULL,
        {INVITES_COUNT_LINE_NAME} int NOT NULL);
        '''

        self.execute(command, commit=True)

    def create_table_captcha(self):
        command = f'''
        CREATE TABLE IF NOT EXISTS {TABLE_CAPTCHA_NAME}(
        {NUM_SQL_LINE_NAME} int PRIMARY KEY,
        {SERVER_ID_LINE_NAME} str NOT NULL,
        {ANSWER_LINE_NAME} str NOT NULL)
        '''

        self.execute(command, commit=True)

    def add_captcha(self, identifier: str, answer: str):
        command = f'''
            INSERT INTO {TABLE_CAPTCHA_NAME} VALUES(?, ?, ?)
                        '''
        command1 = f'''
                SELECT *
                FROM {TABLE_CAPTCHA_NAME}
                ORDER BY {NUM_SQL_LINE_NAME} DESC LIMIT 1'''
        try:
            f = self.execute(command1, (), fetch_all=True)[0][0]
        except IndexError:
            f = -1
        self.execute(command, (f + 1, identifier, answer), commit=True)

    def get_captcha(self, num) -> str:
        command = f'''
        SELECT {SERVER_ID_LINE_NAME}, {ANSWER_LINE_NAME}  FROM {TABLE_CAPTCHA_NAME} WHERE {NUM_SQL_LINE_NAME} = ?
            '''
        f = self.execute(command, (num,), fetch_one=True)
        return f

    def add_user(self, identifier: int, referral: str, invites_count=0):
        command = f'''
        INSERT INTO {TABLE_USERS_NAME} VALUES(?, ?, ?)
        '''

        self.execute(command, (identifier, referral, invites_count), commit=True)

    def is_exist_user(self, identifier: int) -> bool:
        command = f'''
                SELECT {IDENTIFIER_LINE_NAME} FROM {TABLE_USERS_NAME} WHERE {IDENTIFIER_LINE_NAME} = ?
                        '''
        f = self.execute(command, (identifier,), fetch_one=True)

        return bool(f)

    def get_referral_user(self, identifier: int) -> str:
        command = f'''
        SELECT {REFERRAL_LINE_NAME} FROM {TABLE_USERS_NAME} WHERE {IDENTIFIER_LINE_NAME} = ?
        '''
        f = self.execute(command, (identifier,), fetch_one=True)
        return f[0]

    def get_referral_all(self) -> set:
        command = f'''
                SELECT {REFERRAL_LINE_NAME} FROM {TABLE_USERS_NAME}
                '''
        f = self.execute(command, fetch_all=True)

        return set(map(lambda x: x[0], f))

    def check_referral(self, ref: str) -> bool:
        command = f'''
                SELECT {REFERRAL_LINE_NAME} FROM {TABLE_USERS_NAME} WHERE {REFERRAL_LINE_NAME} = ? 
                '''
        f = self.execute(command, (ref,), fetch_all=True)
        return len(f) > 0

    def update_invites_count(self, ref: str):
        command = f'''
                UPDATE {TABLE_USERS_NAME} SET {INVITES_COUNT_LINE_NAME} = ? WHERE {REFERRAL_LINE_NAME} = ? 
                '''
        current = self.get_invites_count_by_ref(ref)
        self.execute(command, (current + 1, ref,), commit=True)

    def get_invites_count_by_ref(self, ref: str) -> int:
        command = f'''
                SELECT {INVITES_COUNT_LINE_NAME} FROM {TABLE_USERS_NAME} WHERE {REFERRAL_LINE_NAME} = ?
                '''
        return self.execute(command, (ref,), fetch_one=True)[0]

    def get_invites_count_by_id(self, identifier: int) -> int:
        command = f'''
                SELECT {INVITES_COUNT_LINE_NAME} FROM {TABLE_USERS_NAME} WHERE {IDENTIFIER_LINE_NAME} = ?
                '''

        return self.execute(command, (identifier,), fetch_one=True)[0]

    def get_top_invites_count(self) -> list[tuple]:
        command = f'''
                SELECT {IDENTIFIER_LINE_NAME}, {INVITES_COUNT_LINE_NAME}
                FROM {TABLE_USERS_NAME}
                ORDER BY {INVITES_COUNT_LINE_NAME} DESC LIMIT 5'''
        f = self.execute(command, fetch_all=True)

        return f

    def delete_users_table(self):
        command = f'''DROP TABLE {TABLE_USERS_NAME}'''
        self.execute(command, commit=True)
# tests
#
# db = DB()
# db.create_table_captcha()
# print(db.get_captcha(0))
# db.add_captcha('AgACAgIAAxkBAAIEuWK-oTzXOxNsqnc8qPiRodKgqu5rAAJRuzEbf3v4STta0olJ-1wOAQADAgADcwADKQQ', '1a1SZ')
