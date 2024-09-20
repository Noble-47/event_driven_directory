from __future__ import annotations

from .unit_of_work import AbstractUnitOfWork


class FolderService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    def create_folder(self, folder_name: str, parent_id: int) -> None:
        with self.uow as uow:
            directory = uow.directories.get(parent_id)
            folder = directory.create_folder(folder_name)
            self.uow.commit()
        return folder

    def move_folder(self, folder_id: int, target_folder_id: int) -> None:
        """Move a folder to another folder."""
        with self.uow as uow:
            directory = uow.directories.get(folder_id)
            target = uow.directories.get(target_id)
            directory.move_to(target)
            uow.commit()

    def delete_folder(self, folder_name: str, from_: int | None = None) -> None:
        """Delete a folder and all its files."""
        with self.uow as uow:
            directory = uow.directories.get(from_)
            directory.remove(folder_name)
            uow.commit()

    def add_file_to_folder(self, folder_id, file):
        with self.uow as uow:
            directory = uow.directory.get(folder_id)
            directory.add_file(file)
            uow.commit()

    def delete_file_from_folder(self, folder_id, file_name):
        """Delete a specific file from a folder."""
        with self.uow as uow:
            directory = uow.directory.get(folder_id)
            directory.remove_file(file_name)
            self.uow.commit()
