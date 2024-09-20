from db import JsonDatabase, SQLiteDatabase
from repository import DirectoryRepository

import abc


class AbstractUnitOfWork(abc.ABC):
    folders: FolderRepository

    def __enter__(self):
        self.folders = DirectoryRepository(db)
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def __commit__(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()


class JsonUnitOfWork(AbstractUnitOfWork):

    def __init__(self, file_path:str="folders_db.json"):
        self.file_path = file_path
        self.db = JsonDatabase(self.file_path)

    def rollback(self):
        pass


class SQLUnitOfWork(AbstractUnitOfWork):

    def __init__(self, db_path:str="file_management.db"):
        self.db_path = db_path
        self.db = SQLiteDatabase(db_path)

