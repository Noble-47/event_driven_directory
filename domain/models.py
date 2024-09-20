from __future__ import annotations

from .exceptions import FolderAlreadyExists, FileAlreadyExists

from . import events


class File:

    def __init__(self, file_name, upload_url):
        self.file_name = file_name
        self.upload_url = upload_url

    def __repr__(self):
        return f"File(name={self.file_name}>"


class Folder:

    def __init__(
        self,
        folder_name: str,
        id: int | None = None,
        prefix: str | None = None,
        parent_id: int | None = None,
    ):
        self.id = id
        self.folder_name = folder_name
        self.prefix = prefix
        self.parent_id = parent_id
        self.files = []

    def __repr__(self):
        return f"Folder(folder_name={self.folder_name})"

    def add_prefix(self, prefix: str) -> None:
        self.prefix = prefix.strip()

    def can_add_file(self, file: File):
        # check for duplicate name of file
        return not any([f.file_name == file.file_name for f in self.files])

    def add_file(self, file):
        if any([f.file_name == file.file_name for f in self.files]):
            raise FileAlreadyExists(self.folder_name, file.file_name)
        self.files.append(file)

    def remove_file(self, file_name: str):
        [file] = [file for file in self.files if file.file_name == file_name]
        if file:
            self.files.pop(file)
            return file


class Directory:
    """Tree hierarchy of folders"""

    def __init__(self, folder, folders: list[Folder] = []):
        self.root = folder
        self.folders = folders
        self.events = []

    @property
    def root_id(self):
        return self.root.id

    def _get_folder(self, folder_name: str) -> Union[Folder, None]:
        [folder] = [
            folder for folder in self.folders if folder.folder_name == folder_name
        ]
        if folder:
            return folder

    def move_to(self, target_dir: Directory) -> None:
        """Move folder to another folder."""
        # target_dir.add_folder(self.root)
        self.root.parent_id = target_dir.parent_id
        self.events.append(
            events.MovedFolder(folder_id=self.root_id, to=target_folder.id)
        )

    def create_folder(self, folder_name: str) -> Folder:
        folder = Folder(folder_name)
        self.add_folder(folder)
        self.events.append(
            events.CreatedFolder(parent_id=self.root_id, new_folder_name=folder_name)
        )
        return folder

    def can_add_folder(self, folder: Folder):
        # check if a subfolder already has the folder_name of `folder`
        return not any(
            [subfolder.folder_name == folder.folder_name for subfolder in self.folders]
        )

    def add_folder(self, folder: Folder) -> None:
        """Add a folder to directory."""
        if self.can_add_folder(folder):
            self.folders.append(folder)
        else:
            folder.add_prefix(datetime.now().strftime(format="%Y_%m_%d_%H_%M_%S"))
            self.folders.append(folder)
            self.events.append(
                events.AddedPrefixToFolderName(
                    folder_id=folder.id, prefix=folder.prefix
                )
            )
        self.events.append(events.AddedFolder(folder_id=self.root_id, added=folder.id))

    def remove_folder(self, folder_name: str) -> None:
        """Delete a folder from directory."""
        folder = self._get_folder(folder_name)
        if folder:
            self.folders.pop(folder)
            self.events.append(
                events.DeletedFolder(
                    folder_id=folder.id, folder_name=folder.folder_name
                )
            )

    def add_file(self, file: File, folder_name: str | None = None) -> None:
        """
        Add file to a folder.

        If `folder_name` is None, add file to root
        """
        folder = self._get_folder(folder_name) if folder_name else self.root
        if folder.can_add_file(file):
            folder.add_file(file)
            self.events.append(
                events.AddedFile(file.file_name, file.file_url, folder.id)
            )
        else:
            self.events.append(
                events.FoundFile(file.file_name, file.file_url, folder.id)
            )

    def remove_file(self, file_name: str, folder_name: str | None = None) -> None:
        """
        Remove a file from a folder

        If `folder_name` is None, use root as folder
        """
        folder = self._get_folder(folder_name) if folder_name else self.root
        file = folder.remove_file(file_name)
        if file is not None:
            self.events.append(
                events.RemovedFile(file.file_name, file.file_url, folder.id)
            )
