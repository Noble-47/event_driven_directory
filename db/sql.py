from typing import Union
import sqlite3

from .base import Database

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


class SQLiteDatabase(Database):
    
    def __init__(self, db_path:str="file_management.db") -> None:
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = dict_factory 
        self.cursor = self.connection.cursor()
        self.create_tables()

    def close(self) -> None:
        self.connection.close()

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()
    
    def create_tables(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_name TEXT NOT NULL,
                prefix TEXT,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES folders(id) ON DELETE CASCADE
            )
        """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                file_url TEXT NOT NULL,
                folder_id INTEGER,
                FOREIGN KEY (folder_id) REFERENCES folders(id) ON DELETE CASCADE
            )
        """
        )
        self.connection.commit()


    def get_folder_by_id(self, folder_id:int) -> Union[tuple, None]:
        self.cursor.execute("SELECT * FROM folders WHERE id = ?", (folder_id,))
        row = self.cursor.fetchone()
        if row:
            return self.FolderSchema(**row)


    def get_files_in_folder(self, folder_id:int) -> list:
        self.cursor.execute("SELECT * FROM files WHERE folder_id = ?", (folder_id,))
        rows = self.cursor.fetchall()
        return [self.FileSchema(**row) for row in rows]


    @listner.add_handler("CreatedFolder")
    def save_folder(self, new_folder_name:str, parent_id=None) -> int:
        self.cursor.execute(
            "INSERT INTO folders (folder_name, parent_id) VALUES (?, ?)",
            (new_folder_name, parent_id),
        )
        return self.cursor.lastrowid


    @listner.add_handler("AddedPrefixToFolderName")
    def update_folder_prefix(self, folder_id:int, prefix:str) -> None:
        self.cursor.execute("""
            UPDATE folders
            SET prefix = ?
            WHERE id =?
        """, (prefix, folder_id)
        )

    
    @listner.add_handler("MovedFolder")
    def update_folder_parent(self, folder_id:int, to:int) -> None:
        self.cursor.execute("""
            UPDATE folders
            SET parent_id = ?
            WHERE id = ?
        """, (to, parent_id))



    @listner.add_handler("DeletedFolder")
    def delete_folder(self, folder_id:int, folder_name:str|None) -> None:
        self.cursor.execute("DELETE FROM folders WHERE id = ?", (folder_id,))


    @listner.add_handler("AddedFile")
    def save_file(self, file_name:str, file_url:str, folder_id:int) -> None:
        self.cursor.execute(
            "INSERT INTO files (file_name, file_url, folder_id) VALUES (?, ?, ?)",
            (file_name, file_url, folder_id),
        )

    
    @listner.add_handler("RemovedFile")
    def delete_file_from_folder(self, folder_id:int, file_url:str, file_name:str|None=None) -> None:
        # Deletes a specific file by its name from the given folder
        self.cursor.execute(
            "DELETE FROM files WHERE folder_id = ? AND file_url = ?", (folder_id, file_url)
        )
