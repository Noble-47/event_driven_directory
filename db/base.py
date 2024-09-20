from abc import ABC, abstractmethod
from event_handler import EventHandler

from dataclasses import dataclass

@dataclass
class FolderSchema:
    folder_name: str
    id : int
    parent_id : int | None
    files : list


@dataclass
class FileSchema:
    file_name:str
    file_url:str
    id:int
    folder_id:int


class Database(ABC):

    listner = EventHandler()
    FileSchema = FileSchema
    FolderSchema = FolderSchema

    @abstractmethod
    def save_folder(self, folder_name:str, parent_id=None):
        pass

    @abstractmethod
    def get_folder_by_id(self, folder_id:int) -> dict:
        pass

    @abstractmethod
    def get_files_in_folder(self, folder_id:int) -> list:
        pass

    @abstractmethod
    def delete_folder(self, folder_id:int) -> None:
        pass

    @abstractmethod
    def delete_files_from_folder(self, folder_id:int, file_name:str) -> None:
        """Delete a specific file from a folder by its file name."""
        pass

    def dispatch(events):
        for event in events:
            self.listner.handle(event)
