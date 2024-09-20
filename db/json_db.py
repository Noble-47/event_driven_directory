from domain.events import Event
from .base import Database

from json.decoder import JSONDecodeError
from typing import Union
import json

"""
{
    folders : {
        folder_id : {
            "parent_id" : None,
            "folder_id" : 0,
            "files" : []
        },

    files : {
        file_id : {
            "folder_id" : 0,
            "file_name" : "some_name",
            "file_url" : "some_url"
        }
    },
}
"""

class JsonDatabase(Database):

    def __init__(self, file_path:str, events:list=[]) -> None:
        self.json_file = file_path

    @property
    def data(self) -> dict:
        if not self._data:
            self._data = self._load_data()
        return self._data

    def _load_data(self) -> dict:
        with open(self.json_file, "r") as f:
            try:
                data = json.load(f)
            except JSONDecodeError:
                data = {"folders" : {}, "files" : {}}
        return data

    def commit(self) -> None:
        with open(self.json_file, "w") as f:
            json.dump(self.data, f, indent=4)
        # self._data stores staged data
        # data that has been modified from
        # the recently read data in the json file
        # after commiting the changes
        # set staged data to None
        self._data = None
    
      def get_folder_by_id(self, folder_id: int) -> Union[tuple, None]:
        data = self.data['folders'].get(folder_id, None)
        if data:
            return data

    def get_files_in_folder(self, folder_id: int) -> list:
        folder = self.get_folder_by_id(folder_id)
        if folder:
            return [self.data["files"][file_id] for file_id in folder]
        return []

    
    @listner.add_handler("CreatedFolder")
    def create_folder(self, new_folder_name, parent_id=None) -> int:
        folder_id = len(self.data["folders"]) + 1
        self.data["folders"][folder_id] = {"folder_name": folder_name, "parent_id": parent_id, "files": []})
        return folder_id

    
    @listner.add_handler("DeletedFolder")
    def delete_folder(self, folder_id: int, folder_name:str|None=None) -> None:
        folder = self.get_folder_by_id(folder_id)
        if folder:
            self.data['folders'].pop(folder_id)
    

    @listner.add_handler("AddedPrefixToFolderName")
    def update_folder_prefix(folder_id:int, prefix:str) -> None:
        folder = self.get_folder_by_id(folder_id)
        folder['prefix'] = prefix


    @listner.add_handler("MovedFolder")
    def move_folder(self, folder_id:int, to:int) -> None:
        folder = self.get_folder_by_id(folder_id)
        folder['parent_id'] = to


    @listner.add_handler("AddedFile")
    def save_file(self, file_name:str, file_url:str, folder_id:int) -> None:
        file_id = len(self.data["files"]) + 1
        self.data["files"][file_id] = {
            "file_name": file_name,
            "file_url": file_url,
            "folder_id": folder_id,
        })
        self.data["folders"][folder_id]["files"].append(file_id)


    @listner.add_handler("RemovedFile")
    def delete_file(self, folder_id:int, file_url:str, file_name:str|None = None) -> None:
        folder = self.get_folder_by_id(folder_id)
        if folder is None:
            return

        [file_id] = [
            file_id
            for file_id, attr in self.data["files"].items()
            if attr["folder_id"] == folder_id and attr["file_url"] == file_url
        ]

        if file_id:
            self.data["folders"][folder_id]["files"].remove(file_id)
            del self.data["files"][file_id]


    def close(self) -> None:
        pass

