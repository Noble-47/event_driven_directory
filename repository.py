from __future__ import annotations

from typing import Union

from models import Directory, Folder, File
from db import Database


class DirectoryRepositry:

    def __init__(self, db: Database):
        self.db = db
        self.seen = set()

    def _get_folder(id: int) -> Union[Folder, None]:
        folder = self.db.get_folder_by_id(id)
        if folder is None:
            return

        return Folder(folder.folder_name, id=folder.id, prefix=folder.prefix)

    def _get_subfolders(folder_id: int) -> list[Folder]:
        subfolders = self.db.get_subfolders(parent_id=folder_id)
        return [
            Folder(subfolder.folder_name, subfolder.id, subfolder.prefix)
            for subfolder in subfolders
        ]

    def _get_folder_files(folder_id: int) -> list[Files]:
        files = self.db.get_files(folder_id=folder_id)
        return [Files(file.file_name, file.file_url) for file in files]

    def get(self, dir_id: int) -> Directory:
        folder = self._get_folder(dir_id)
        if folder is None:
            return None

        directory = Directory(folder)

        subfolders = self._get_subfolders(dir_id)
        files = self._get_files(dir_id)

        directory.subfolders = subfolders
        directory.root.files = files

        self.seen.add(directory)

        return directory

    def save(self):
        events = [directory.events for directory in self.seen]
        self.db.dispatch(events)
